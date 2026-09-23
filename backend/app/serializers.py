"""Explicit JSON responses keep private file paths and password hashes off the wire."""

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Assessment, AuditEvent, EvidenceImage, Inspection, User
from .services.extraction import reconcile_fields


def summarize_findings(findings: list[dict]) -> dict:
    counts = Counter(finding["status"] for finding in findings)
    return {status: counts[status] for status in ("pass", "potential_violation", "needs_review", "not_applicable")}


def normalized_applicability(value: dict | None, scope_confirmed: bool = False) -> dict:
    current = value or {}
    return {
        "status": current.get("status") or ("applicable" if scope_confirmed else "unknown"),
        "exemption": current.get("exemption") or "none",
        "reason": current.get("reason") or "",
    }


def image_dict(image: EvidenceImage) -> dict:
    return {
        "id": image.id,
        "filename": image.filename,
        "panel": image.panel,
        "width": image.width,
        "height": image.height,
        "url": f"/api/inspections/{image.inspection_id}/images/{image.id}",
        "quality": image.quality,
        "ocr_text": image.ocr_text,
        "lines": image.lines,
    }


def inspection_summary(db: Session, inspection: Inspection) -> dict:
    owner = db.get(User, inspection.owner_id)
    images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection.id)).all()
    counts = summarize_findings(inspection.findings)
    return {
        "id": inspection.id,
        "product_name": inspection.product_name,
        "brand": inspection.brand,
        "barcode": inspection.barcode,
        "category": inspection.category,
        "origin": inspection.origin,
        "scope_confirmed": inspection.scope_confirmed,
        "applicability": normalized_applicability(inspection.applicability, inspection.scope_confirmed),
        "notes": inspection.notes,
        "status": inspection.status,
        "version": inspection.version,
        "created_at": inspection.created_at,
        "updated_at": inspection.updated_at,
        "owner_name": owner.name if owner else "Former user",
        "image_count": len(images),
        "potential_violations": counts["potential_violation"],
        "needs_review": counts["needs_review"],
        "review_decision": inspection.review_decision,
    }


def inspection_detail(db: Session, inspection: Inspection) -> dict:
    images = db.scalars(
        select(EvidenceImage).where(EvidenceImage.inspection_id == inspection.id).order_by(EvidenceImage.created_at)
    ).all()
    assessments = db.scalars(
        select(Assessment).where(Assessment.inspection_id == inspection.id).order_by(Assessment.created_at.desc())
    ).all()
    events = db.scalars(
        select(AuditEvent).where(AuditEvent.inspection_id == inspection.id).order_by(AuditEvent.id.desc())
    ).all()
    return {
        **inspection_summary(db, inspection),
        "coverage_confirmed": inspection.coverage_confirmed,
        "applicability": normalized_applicability(inspection.applicability, inspection.scope_confirmed),
        "reconciliation": reconcile_fields(inspection.fields),
        "images": [image_dict(image) for image in images],
        "fields": inspection.fields,
        "findings": inspection.findings,
        "manual_checks": inspection.manual_checks,
        "processing_error": inspection.processing_error,
        "processing_seconds": inspection.processing_seconds,
        "rule_version": inspection.rule_version,
        "current_assessment_id": inspection.current_assessment_id,
        "review_notes": inspection.review_notes,
        "assessments": [
            {
                "id": assessment.id,
                "created_at": assessment.created_at,
                "rule_version": assessment.rule_version,
                "summary": summarize_findings(assessment.snapshot["findings"]),
                "review_decision": assessment.snapshot.get("review_decision"),
                "assessment_version": assessment.snapshot.get("assessment_version", assessment.id[:8]),
                "evidence_count": len(assessment.snapshot.get("images", [])),
            }
            for assessment in assessments
        ],
        "audit": [
            {
                "id": event.id,
                "created_at": event.created_at,
                "actor": event.actor,
                "action": event.action,
                "detail": event.detail,
            }
            for event in events
        ],
    }
