"""Create, retrieve and edit inspections. Business checks live in services."""

from copy import deepcopy
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db, require_csrf
from ..models import EvidenceImage, Inspection, User, new_id
from ..schemas import InspectionCreate, InspectionUpdate
from ..serializers import inspection_detail, inspection_summary
from ..services.evidence_storage import persist_evidence, restore_evidence
from ..services.extraction import FIELD_NAMES, empty_declaration
from ..services.images import store_image
from ..services.inspection_service import (
    assert_editable,
    audit,
    evaluate_inspection,
    find_inspection,
    save_assessment,
    touch,
)

router = APIRouter(tags=["Inspections"])


def visible_inspections(db: Session, user: User, query: str = "", status: str = "") -> list[Inspection]:
    statement = select(Inspection)
    if user.role != "reviewer":
        statement = statement.where(Inspection.owner_id == user.id)
    if query.strip():
        # SQLAlchemy binds the search value as data, never SQL source code.
        search = f"%{query.strip()[:200]}%"
        statement = statement.where(
            or_(Inspection.product_name.ilike(search), Inspection.brand.ilike(search), Inspection.barcode.ilike(search))
        )
    if status:
        statement = statement.where(Inspection.status == status)
    return list(db.scalars(statement.order_by(Inspection.updated_at.desc())).all())


@router.get("/inspections")
def list_inspections(
    q: str = "", status: str = "", user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return [inspection_summary(db, item) for item in visible_inspections(db, user, q, status)]


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    summaries = [inspection_summary(db, item) for item in visible_inspections(db, user)]
    return {
        "total": len(summaries),
        "needs_review": sum(item["status"] == "ready" for item in summaries),
        "reviewed": sum(item["status"] == "reviewed" for item in summaries),
        "potential_violations": sum(item["potential_violations"] for item in summaries),
        "recent": summaries[:6],
    }


@router.post("/inspections", status_code=201, dependencies=[Depends(require_csrf)])
def create_inspection(
    payload: InspectionCreate, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    with request.app.state.write_lock:
        inspection = Inspection(owner_id=user.id, **payload.model_dump())
        db.add(inspection)
        db.flush()
        audit(db, inspection, user.name, "Inspection created", "Created a new inspection record.")
        db.commit()
        return inspection_detail(db, inspection)


@router.get("/inspections/{inspection_id}")
def get_inspection(inspection_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return inspection_detail(db, find_inspection(db, inspection_id, user))


@router.patch("/inspections/{inspection_id}", dependencies=[Depends(require_csrf)])
def update_inspection(
    inspection_id: str,
    payload: InspectionUpdate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    with request.app.state.write_lock:
        inspection = find_inspection(db, inspection_id, user)
        assert_editable(inspection, payload.version)
        changes = payload.model_dump(exclude_unset=True, exclude_none=True)
        corrections = changes.pop("fields", {})
        field_notes = changes.pop("field_notes", {})
        changes.pop("version")
        if set(corrections) - set(FIELD_NAMES) or set(field_notes) - set(FIELD_NAMES):
            raise HTTPException(422, "An unknown declaration field was supplied.")
        if any(len(value) > 2000 for value in corrections.values()) or any(
            len(value) > 3000 for value in field_notes.values()
        ):
            raise HTTPException(422, "Declaration values must be under 2,000 characters and notes under 3,000.")
        fields = deepcopy(inspection.fields)
        correction_log = []
        for field, value in corrections.items():
            previous = fields.get(field, empty_declaration())
            fields[field] = {
                **previous,
                "value": value.strip(),
                "confidence": 1.0,
                "source": "manual",
                "note": field_notes.get(field, "Officer-entered correction; verify against the photograph."),
            }
            correction_log.append(f"{field}: {previous['value']!r} → {value.strip()!r}")
        for field, note in field_notes.items():
            if field in fields:
                fields[field] = {**fields[field], "note": note}
        inspection.fields = fields
        for name, value in changes.items():
            setattr(inspection, name, value)
        touch(inspection)
        if inspection.current_assessment_id:
            evaluate_inspection(db, inspection)
            save_assessment(db, inspection, user.name)
        detail = "; ".join(correction_log) if correction_log else "Updated inspection context, applicability, or assisted checks."
        audit(db, inspection, user.name, "Inspection updated", detail)
        db.commit()
        return inspection_detail(db, inspection)


@router.post("/inspections/{inspection_id}/images", status_code=201, dependencies=[Depends(require_csrf)])
async def upload_image(
    inspection_id: str,
    request: Request,
    file: UploadFile = File(...),
    panel: str = Form("other"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if panel not in ("front", "back", "side", "other"):
        raise HTTPException(422, "Panel must be front, back, side, or other.")
    settings = request.app.state.settings
    data = await file.read(settings.max_upload_bytes + 1)
    await file.close()
    if not data or len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "Upload a non-empty image up to 10 MB.")
    with request.app.state.write_lock:
        inspection = find_inspection(db, inspection_id, user)
        assert_editable(inspection)
        images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection_id)).all()
        if len(images) >= settings.max_images:
            raise HTTPException(400, "Each inspection can contain up to eight photographs.")
        image_id = new_id()
        try:
            saved = store_image(data, image_id, settings.data_dir / "images")
        except ValueError as error:
            raise HTTPException(400, str(error)) from error
        image = EvidenceImage(
            id=image_id,
            inspection_id=inspection_id,
            panel=panel,
            filename=Path(file.filename or "label.jpg").name[:200],
            **saved,
        )
        db.add(image)
        if settings.evidence_in_database:
            db.flush()
            persist_evidence(db, image, settings.data_dir)
        inspection.status = "draft"
        inspection.findings = []
        inspection.current_assessment_id = None
        inspection.review_decision = None
        inspection.review_notes = None
        inspection.coverage_confirmed = False
        inspection.processing_error = None
        touch(inspection)
        audit(
            db,
            inspection,
            user.name,
            "Evidence uploaded",
            f"Added {panel} photograph ({image.width} × {image.height}).",
        )
        db.commit()
        return inspection_detail(db, inspection)


@router.get("/inspections/{inspection_id}/images/{image_id}")
def view_image(
    inspection_id: str,
    image_id: str,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    find_inspection(db, inspection_id, user)
    image = db.get(EvidenceImage, image_id)
    if image is None or image.inspection_id != inspection_id:
        raise HTTPException(404, "Evidence image not found.")
    path = restore_evidence(db, image, request.app.state.settings.data_dir)
    if not path.is_file():
        raise HTTPException(404, "The evidence file is unavailable. Restore it from backup.")
    return FileResponse(path, media_type="image/jpeg", headers={"Cache-Control": "private, no-store"})
