"""Download a selected frozen assessment, including older versions."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import Assessment, EvidenceImage, User
from ..services.evidence_storage import restore_evidence
from ..services.inspection_service import find_inspection
from ..services.reports import build_docx, build_pdf

router = APIRouter(tags=["Reports"])


@router.get("/inspections/{inspection_id}/reports/{assessment_id}.{extension}")
def download_report(
    inspection_id: str,
    assessment_id: str,
    extension: str,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    inspection = find_inspection(db, inspection_id, user)
    assessment = db.get(Assessment, assessment_id)
    if assessment is None or assessment.inspection_id != inspection.id:
        raise HTTPException(404, "Assessment report not found.")
    if extension not in ("pdf", "docx"):
        raise HTTPException(404, "Report format not found.")
    reports_dir = request.app.state.settings.data_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    output = reports_dir / f"{assessment.id}.{extension}"
    if not output.is_file():
        for item in assessment.snapshot.get("images", []):
            image = db.get(EvidenceImage, item["id"])
            if image is not None and image.inspection_id == inspection.id:
                restore_evidence(db, image, request.app.state.settings.data_dir)
        if extension == "pdf":
            build_pdf(assessment.snapshot, output, request.app.state.settings.data_dir)
        else:
            build_docx(assessment.snapshot, output, request.app.state.settings.data_dir)
    media = (
        "application/pdf"
        if extension == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    safe_product = (
        "".join(character if character.isalnum() else "-" for character in inspection.product_name).strip("-")[:50]
        or "inspection"
    )
    return FileResponse(
        output,
        media_type=media,
        filename=f"complisense-{safe_product}-{assessment.id[:8]}.{extension}",
        headers={"Cache-Control": "private, no-store"},
    )
