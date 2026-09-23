"""Public health, sample-data and signed-in legal-reference endpoints."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from ..dependencies import get_current_user
from ..services.rules import public_rule_data
from ..services.samples import SAMPLES, public_samples

router = APIRouter(tags=["Reference"])


@router.get("/health")
@router.head("/health", include_in_schema=False)
def health(request: Request):
    return {"status": "ok", "ocr_available": request.app.state.ocr.available, "ocr_engine": "RapidOCR ONNX (CPU)"}


@router.get("/rules", dependencies=[Depends(get_current_user)])
def rules():
    return public_rule_data()


@router.get("/samples", dependencies=[Depends(get_current_user)])
def samples():
    return public_samples()


@router.get("/samples/{filename}")
def sample_file(filename: str, request: Request):
    allowed = {item[0] for item in SAMPLES}
    if filename not in allowed or Path(filename).name != filename:
        raise HTTPException(404, "Sample not found.")
    path = request.app.state.settings.data_dir / "samples" / filename
    if not path.is_file():
        raise HTTPException(404, "Sample not found.")
    return FileResponse(path, media_type="image/png", filename=filename)
