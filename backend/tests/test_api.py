"""End-to-end API behaviors using a temporary database and real sessions."""

from io import BytesIO

import pytest
from app.config import Settings
from app.main import create_app
from app.users import create_user
from fastapi.testclient import TestClient
from PIL import Image


@pytest.fixture
def app(tmp_path):
    application = create_app(Settings(data_dir=tmp_path, database_url=f"sqlite:///{tmp_path / 'test.db'}"))
    with TestClient(application) as client:
        with application.state.database.session() as db:
            create_user(db, "inspector@example.com", "Inspector One", "inspector", "a-good-test-password")
            create_user(db, "second@example.com", "Inspector Two", "inspector", "a-good-test-password")
            create_user(db, "reviewer@example.com", "Reviewer", "reviewer", "a-good-test-password")
        yield application, client


def login(client, email="inspector@example.com"):
    response = client.post("/api/auth/login", json={"email": email, "password": "a-good-test-password"})
    assert response.status_code == 200
    client.headers["X-CSRF-Token"] = response.json()["csrf_token"]
    return response.json()


def create_inspection(client):
    response = client.post(
        "/api/inspections",
        json={
            "product_name": "Test Soap",
            "category": "household",
            "origin": "domestic",
            "scope_confirmed": True,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def image_file():
    image = Image.new("RGB", (900, 600), "white")
    stream = BytesIO()
    image.save(stream, "PNG")
    return stream.getvalue()


def test_records_require_authentication(app):
    _, client = app
    assert client.get("/api/inspections").status_code == 401


def test_health_accepts_uptime_monitor_head_requests(app):
    _, client = app
    assert client.head("/api/health").status_code == 200
    assert client.get("/api/health").json()["status"] == "ok"


def test_database_evidence_recovers_after_ephemeral_disk_loss(app):
    from app.models import EvidencePayload

    application, client = app
    application.state.settings.evidence_in_database = True
    login(client)
    inspection = create_inspection(client)
    source = image_file()
    result = client.post(
        f"/api/inspections/{inspection['id']}/images",
        data={"panel": "front"},
        files={"file": ("label.png", source, "image/png")},
    )
    assert result.status_code == 201, result.text
    image = result.json()["images"][0]
    with application.state.database.session() as db:
        payload = db.get(EvidencePayload, image["id"])
        assert payload.original == source
        normalized = payload.normalized
    directory = application.state.settings.data_dir / "images"
    for file in directory.iterdir():
        file.unlink()
    with TestClient(application) as anonymous:
        assert anonymous.get(image["url"]).status_code == 401
    assert list(directory.iterdir()) == []
    assert client.get(image["url"]).content == normalized
    assert (directory / f"{image['id']}.original").read_bytes() == source


def test_ocr_and_report_restore_evidence_after_disk_loss(app, monkeypatch):
    from pathlib import Path

    application, client = app
    application.state.settings.evidence_in_database = True
    login(client)
    inspection = create_inspection(client)
    result = client.post(
        f"/api/inspections/{inspection['id']}/images",
        files={"file": ("label.png", image_file(), "image/png")},
    )
    assert result.status_code == 201
    directory = application.state.settings.data_dir / "images"

    def scan_restored(path):
        assert Path(path).is_file()
        return {"lines": [], "ocr_text": "", "quality": {"warnings": []}}

    monkeypatch.setattr(application.state.ocr, "scan", scan_restored)
    for file in directory.iterdir():
        file.unlink()
    assert client.post(f"/api/inspections/{inspection['id']}/analyze").status_code == 200
    record = client.get(f"/api/inspections/{inspection['id']}").json()
    assert record["status"] == "ready"
    for file in directory.iterdir():
        file.unlink()
    report = client.get(f"/api/inspections/{inspection['id']}/reports/{record['current_assessment_id']}.pdf")
    assert report.status_code == 200
    assert report.content.startswith(b"%PDF")
    assert len(list(directory.iterdir())) == 2


def test_bootstrap_accounts_are_private_and_do_not_overwrite_users(app, monkeypatch):
    from app.security import hash_password
    from app.users import bootstrap_users

    application, client = app
    monkeypatch.setenv("BOOTSTRAP_INSPECTOR_EMAIL", "bootstrap@example.com")
    monkeypatch.setenv("BOOTSTRAP_INSPECTOR_PASSWORD_HASH", hash_password("a-unique-bootstrap-password"))
    with application.state.database.session() as db:
        bootstrap_users(db)
        monkeypatch.setenv("BOOTSTRAP_INSPECTOR_PASSWORD_HASH", hash_password("another-bootstrap-password"))
        bootstrap_users(db)
    response = client.post("/api/auth/login", json={
        "email": "bootstrap@example.com", "password": "a-unique-bootstrap-password",
    })
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "inspector"
    assert "password" not in response.text


def test_login_checks_password_and_logout_revokes_session(app):
    _, client = app
    assert (
        client.post("/api/auth/login", json={"email": "inspector@example.com", "password": "wrong"}).status_code == 401
    )
    login(client)
    assert client.get("/api/auth/me").json()["user"]["role"] == "inspector"
    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_mutation_without_csrf_token_is_rejected(app):
    _, client = app
    login(client)
    del client.headers["X-CSRF-Token"]
    assert client.post("/api/inspections", json={"product_name": "Soap"}).status_code == 403


def test_inspector_cannot_read_another_inspectors_record(app):
    application, client = app
    login(client)
    inspection = create_inspection(client)
    with TestClient(application) as second:
        login(second, "second@example.com")
        assert second.get(f"/api/inspections/{inspection['id']}").status_code == 404
        assert second.get("/api/inspections").json() == []


def test_invalid_upload_content_is_rejected(app):
    _, client = app
    login(client)
    inspection = create_inspection(client)
    result = client.post(
        f"/api/inspections/{inspection['id']}/images",
        data={"panel": "front"},
        files={"file": ("fake.png", b"this is not an image", "image/png")},
    )
    assert result.status_code == 400
    assert client.get(f"/api/inspections/{inspection['id']}").json()["images"] == []


def test_upload_is_private_and_preserves_evidence(app):
    application, client = app
    login(client)
    inspection = create_inspection(client)
    result = client.post(
        f"/api/inspections/{inspection['id']}/images",
        data={"panel": "front"},
        files={"file": ("label.png", image_file(), "image/png")},
    )
    assert result.status_code == 201, result.text
    evidence = result.json()["images"][0]
    assert evidence["width"] == 900
    assert client.get(evidence["url"]).status_code == 200
    with TestClient(application) as anonymous:
        assert anonymous.get(evidence["url"]).status_code == 401


def test_stale_edit_does_not_overwrite_newer_work(app):
    _, client = app
    login(client)
    inspection = create_inspection(client)
    url = f"/api/inspections/{inspection['id']}"
    assert client.patch(url, json={"version": inspection["version"], "notes": "first update"}).status_code == 200
    assert client.patch(url, json={"version": inspection["version"], "notes": "stale update"}).status_code == 409
    assert client.get(url).json()["notes"] == "first update"


def test_inspector_cannot_issue_reviewer_decision(app):
    _, client = app
    login(client)
    inspection = create_inspection(client)
    result = client.post(
        f"/api/inspections/{inspection['id']}/review",
        json={
            "version": inspection["version"],
            "decision": "accepted",
            "notes": "Checked evidence",
        },
    )
    assert result.status_code == 403


def test_search_and_dashboard_use_visible_real_records(app):
    _, client = app
    login(client)
    create_inspection(client)
    assert client.get("/api/dashboard").json()["total"] == 1
    assert len(client.get("/api/inspections?q=Soap").json()) == 1
    assert client.get("/api/inspections?q=missing").json() == []


def test_analysis_review_and_versioned_report_flow(app):
    application, client = app
    login(client)
    inspection = create_inspection(client)
    client.post(
        f"/api/inspections/{inspection['id']}/images",
        data={"panel": "back"},
        files={"file": ("label.png", image_file(), "image/png")},
    )

    class TestOCR:
        available = True

        def scan(self, _path):
            texts = [
                "Product: Test Soap",
                "Manufactured by: Example Labs Private Limited",
                "Address: 12 Market Road, Pune 411001",
                "Net Quantity: 100 g",
                "MRP Rs. 45.00 inclusive of all taxes",
                "MFD: 08/2026",
                "Consumer Care: 1800 111 222",
            ]
            return {
                "lines": [
                    {
                        "text": text,
                        "confidence": 0.97,
                        "box": [[0, row * 30], [600, row * 30], [600, row * 30 + 25], [0, row * 30 + 25]],
                    }
                    for row, text in enumerate(texts, start=1)
                ],
                "ocr_text": "\n".join(texts),
                "quality": {"warnings": [], "blur_score": 150.0},
            }

    application.state.ocr = TestOCR()
    started = client.post(f"/api/inspections/{inspection['id']}/analyze")
    assert started.status_code == 200, started.text
    analyzed = client.get(f"/api/inspections/{inspection['id']}").json()
    assert analyzed["status"] == "ready"
    assert analyzed["fields"]["net_quantity"]["value"] == "100 g"
    first_assessment = analyzed["current_assessment_id"]
    assert first_assessment
    assert client.get(f"/api/inspections/{inspection['id']}/reports/{first_assessment}.pdf").status_code == 200
    assert client.get(f"/api/inspections/{inspection['id']}/reports/{first_assessment}.docx").status_code == 200

    with TestClient(application) as reviewer:
        login(reviewer, "reviewer@example.com")
        latest = reviewer.get(f"/api/inspections/{inspection['id']}").json()
        reviewed = reviewer.post(
            f"/api/inspections/{inspection['id']}/review",
            json={
                "version": latest["version"],
                "decision": "follow_up",
                "notes": "Confirm the physical lettering size.",
            },
        )
        assert reviewed.status_code == 200, reviewed.text
        assert reviewed.json()["status"] == "reviewed"
        assert reviewed.json()["current_assessment_id"] != first_assessment

    assert client.get(f"/api/inspections/{inspection['id']}/reports/{first_assessment}.pdf").status_code == 200
