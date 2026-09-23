"""A bounded local OCR worker. Use one API process with this prototype queue."""

import logging
import time

from sqlalchemy import select

from ..models import EvidenceImage, Inspection
from ..serializers import image_dict
from .evidence_storage import restore_evidence
from .extraction import extract_declarations
from .inspection_service import audit, evaluate_inspection, save_assessment, touch
from .ocr import OCRUnavailableError

logger = logging.getLogger(__name__)


def run_analysis(app, inspection_id: str, actor: str):
    try:
        # Avoid simultaneously loading/running several memory-hungry OCR models.
        with app.state.processing_lock:
            started = time.perf_counter()
            with app.state.database.session() as db:
                images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection_id)).all()
                results = [
                    (image.id, app.state.ocr.scan(restore_evidence(db, image, app.state.settings.data_dir)))
                    for image in images
                ]
            with app.state.write_lock, app.state.database.session() as db:
                inspection = db.get(Inspection, inspection_id)
                for image_id, result in results:
                    image = db.get(EvidenceImage, image_id)
                    image.lines = result["lines"]
                    image.ocr_text = result["ocr_text"]
                    image.quality = result["quality"]
                db.flush()
                images = db.scalars(select(EvidenceImage).where(EvidenceImage.inspection_id == inspection_id)).all()
                fields = extract_declarations([image_dict(image) for image in images])
                # Keep deliberate corrections on a retry; do not silently replace
                # an officer's judgement with a second OCR guess.
                for name, candidate in inspection.fields.items():
                    if candidate.get("source") == "manual":
                        fields[name] = candidate
                inspection.fields = fields
                inspection.processing_error = None
                inspection.processing_seconds = round(time.perf_counter() - started, 2)
                evaluate_inspection(db, inspection)
                touch(inspection)
                assessment = save_assessment(db, inspection, actor)
                audit(
                    db,
                    inspection,
                    actor,
                    "Analysis completed",
                    f"Created assessment {assessment.id[:8]} using real RapidOCR output.",
                )
                db.commit()
    except Exception as error:
        logger.exception("Analysis failed for inspection %s", inspection_id)
        message = (
            str(error)
            if isinstance(error, OCRUnavailableError)
            else "Analysis could not finish. Your photographs are saved. Retry, or check the API logs."
        )
        with app.state.write_lock, app.state.database.session() as db:
            inspection = db.get(Inspection, inspection_id)
            if inspection:
                inspection.status = "failed"
                inspection.processing_error = message
                touch(inspection)
                audit(db, inspection, actor, "Analysis failed", message)
                db.commit()
    finally:
        app.state.job_slots.release()
