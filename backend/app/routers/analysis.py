"""Queue analysis and record reviewer decisions, with concurrency checks."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db, require_csrf, require_reviewer
from ..models import EvidenceImage, User
from ..schemas import ReviewRequest
from ..serializers import inspection_detail
from ..services.inspection_service import assert_editable, audit, find_inspection, save_assessment, touch
from ..services.processing import run_analysis

router = APIRouter(tags=["Analysis and review"])


@router.post("/inspections/{inspection_id}/analyze", dependencies=[Depends(require_csrf)])
def analyze(
    inspection_id: str,
    request: Request,
    tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    with request.app.state.write_lock:
        inspection = find_inspection(db, inspection_id, user)
        assert_editable(inspection)
        if not db.scalar(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection_id)):
            raise HTTPException(400, "Upload at least one label photograph before analyzing.")
        if not request.app.state.ocr.available:
            raise HTTPException(503, "OCR is not installed. Install backend/requirements.txt and restart.")
        if not request.app.state.job_slots.acquire(blocking=False):
            raise HTTPException(503, "The local processing queue is full. Please try again shortly.")
        try:
            inspection.status = "processing"
            inspection.processing_error = None
            # Findings from a previous run are historical until the new run ends.
            inspection.findings = []
            inspection.current_assessment_id = None
            inspection.review_decision = None
            inspection.review_notes = None
            touch(inspection)
            audit(
                db,
                inspection,
                user.name,
                "Analysis started",
                "Queued supplied photographs for OCR and rule evaluation.",
            )
            db.commit()
            result = inspection_detail(db, inspection)
        except Exception:
            request.app.state.job_slots.release()
            raise
        tasks.add_task(run_analysis, request.app, inspection_id, user.name)
        return result


@router.post("/inspections/{inspection_id}/review", dependencies=[Depends(require_csrf)])
def review(
    inspection_id: str,
    payload: ReviewRequest,
    request: Request,
    user: User = Depends(require_reviewer),
    db: Session = Depends(get_db),
):
    with request.app.state.write_lock:
        inspection = find_inspection(db, inspection_id, user)
        assert_editable(inspection, payload.version)
        if inspection.current_assessment_id is None:
            raise HTTPException(400, "Analyze this inspection before recording a review.")
        inspection.review_decision = payload.decision
        inspection.review_notes = payload.notes
        inspection.status = "reviewed"
        touch(inspection)
        save_assessment(db, inspection, user.name)
        audit(db, inspection, user.name, "Review recorded", f"{payload.decision}: {payload.notes}")
        db.commit()
        return inspection_detail(db, inspection)
