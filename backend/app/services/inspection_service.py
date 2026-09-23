"""Shared inspection operations used by HTTP routes and the OCR worker."""

from copy import deepcopy

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Assessment, AuditEvent, EvidenceImage, Inspection, User, timestamp
from ..serializers import image_dict, inspection_summary, normalized_applicability
from .extraction import reconcile_fields
from .rules import RULE_VERSION, evaluate_rules


def find_inspection(db: Session, inspection_id: str, user: User) -> Inspection:
    inspection = db.get(Inspection, inspection_id)
    if inspection is None or (user.role != "reviewer" and inspection.owner_id != user.id):
        # A 404 avoids revealing whether another inspector's record exists.
        raise HTTPException(404, "Inspection not found.")
    return inspection


def assert_editable(inspection: Inspection, version: int | None = None):
    if inspection.status == "processing":
        raise HTTPException(409, "Analysis is running. Wait for it to finish before changing evidence.")
    if version is not None and inspection.version != version:
        raise HTTPException(409, "This inspection changed in another tab. Reload before saving.")


def touch(inspection: Inspection):
    inspection.version += 1
    inspection.updated_at = timestamp()


def audit(db: Session, inspection: Inspection, actor: str, action: str, detail: str):
    db.add(AuditEvent(inspection_id=inspection.id, actor=actor, action=action, detail=detail))


def evaluate_inspection(db: Session, inspection: Inspection):
    images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection.id)).all()
    context = {
        "category": inspection.category,
        "origin": inspection.origin,
        "scope_confirmed": inspection.scope_confirmed,
        "coverage_confirmed": inspection.coverage_confirmed,
        "manual_checks": inspection.manual_checks,
        "applicability": normalized_applicability(inspection.applicability, inspection.scope_confirmed),
        "reconciliation": reconcile_fields(inspection.fields),
    }
    inspection.findings = evaluate_rules(inspection.fields, context, [image_dict(image) for image in images])
    inspection.rule_version = RULE_VERSION
    inspection.review_decision = None
    inspection.review_notes = None
    inspection.status = "ready"


def save_assessment(db: Session, inspection: Inspection, actor: str) -> Assessment:
    """Freeze a deep copy: future edits never mutate an already exported report."""
    images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection.id)).all()
    evidence_index = {
        image.id: {"image_id": image.id, "filename": image.filename, "panel": image.panel, "sha256": image.sha256}
        for image in images
    }
    findings = []
    for finding in deepcopy(inspection.findings):
        evidence = evidence_index.get(finding.get("evidence_image_id"))
        finding["evidence"] = evidence
        finding["rule_reference"] = {
            "rule_id": finding.get("rule_id"),
            "provision": finding.get("provision"),
            "source_url": finding.get("source_url"),
            "rule_version": inspection.rule_version or RULE_VERSION,
        }
        findings.append(finding)
    snapshot = {
        **inspection_summary(db, inspection),
        "fields": deepcopy(inspection.fields),
        "findings": findings,
        "manual_checks": deepcopy(inspection.manual_checks),
        "coverage_confirmed": inspection.coverage_confirmed,
        "applicability": deepcopy(normalized_applicability(inspection.applicability, inspection.scope_confirmed)),
        "reconciliation": reconcile_fields(inspection.fields),
        "processing_seconds": inspection.processing_seconds,
        "rule_version": inspection.rule_version,
        "review_notes": inspection.review_notes,
        "prepared_by": actor,
        "images": [{**image_dict(image), "stored_name": image.stored_name, "sha256": image.sha256} for image in images],
    }
    assessment = Assessment(
        inspection_id=inspection.id, rule_version=inspection.rule_version or RULE_VERSION, snapshot=snapshot
    )
    db.add(assessment)
    db.flush()
    snapshot["assessment_id"] = assessment.id
    snapshot["assessment_version"] = assessment.id[:8]
    snapshot["report_created_at"] = assessment.created_at
    assessment.snapshot = snapshot
    inspection.current_assessment_id = assessment.id
    return assessment
