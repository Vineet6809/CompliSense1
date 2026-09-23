"""Application entry point: `uvicorn app.main:app --reload` from backend/."""

import logging
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from .config import Settings
from .database import Database
from .models import AuditEvent, Inspection, timestamp
from .routers import analysis, auth, inspections, reference, reports
from .services.ocr import OCRService
from .services.samples import ensure_samples
from .users import bootstrap_users

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        application.state.database.initialize()
        with application.state.database.session() as db:
            bootstrap_users(db)
        ensure_samples(settings.data_dir / "samples")
        # Background work cannot safely survive a local process restart. Mark it
        # failed so the inspector sees a retry action instead of an endless spinner.
        with application.state.write_lock, application.state.database.session() as db:
            interrupted = db.scalars(select(Inspection).where(Inspection.status == "processing")).all()
            for inspection in interrupted:
                inspection.status = "failed"
                inspection.processing_error = (
                    "The server restarted during analysis. Your evidence is saved; run analysis again."
                )
                inspection.version += 1
                inspection.updated_at = timestamp()
                db.add(
                    AuditEvent(
                        inspection_id=inspection.id,
                        actor="System",
                        action="Analysis interrupted",
                        detail="Server restart detected. Evidence was preserved for retry.",
                    )
                )
            db.commit()
        yield

    application = FastAPI(
        title="CompliSense API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
    )
    application.state.settings = settings
    application.state.database = Database(settings.database_url)
    application.state.ocr = OCRService()
    application.state.write_lock = threading.RLock()
    application.state.processing_lock = threading.Lock()
    application.state.job_slots = threading.BoundedSemaphore(2)
    application.state.login_attempts = {}
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type", "X-CSRF-Token"],
    )

    @application.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "camera=(self), microphone=(), geolocation=()"
        return response

    for router in (auth.router, inspections.router, analysis.router, reports.router, reference.router):
        application.include_router(router, prefix="/api")

    frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if not frontend_dist.is_dir():
        frontend_dist = Path(__file__).resolve().parents[3] / "frontend" / "dist"
    if (frontend_dist / "assets").is_dir():
        application.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="frontend-assets")

        @application.get("/{path:path}", include_in_schema=False)
        def frontend(path: str):
            if path == "api" or path.startswith("api/"):
                raise HTTPException(404, "API endpoint not found.")
            requested = frontend_dist / path
            if path and requested.is_file() and requested.resolve().is_relative_to(frontend_dist.resolve()):
                return FileResponse(requested)
            return FileResponse(frontend_dist / "index.html")
    else:

        @application.get("/", include_in_schema=False)
        def api_root():
            return {"message": "CompliSense API is running. Build frontend/ to serve the web interface here."}

    return application


app = create_app()
