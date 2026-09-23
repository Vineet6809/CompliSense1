"""Database tables. JSON columns hold small OCR documents, not executable code."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, Float, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def new_id() -> str:
    return uuid4().hex


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20))
    password_hash: Mapped[str] = mapped_column(String(255))


class LoginSession(Base):
    __tablename__ = "login_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    csrf_token: Mapped[str] = mapped_column(String(100))
    expires_at: Mapped[float] = mapped_column(Float)


class Inspection(Base):
    __tablename__ = "inspections"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_name: Mapped[str] = mapped_column(String(200))
    brand: Mapped[str] = mapped_column(String(150), default="")
    barcode: Mapped[str] = mapped_column(String(100), default="")
    category: Mapped[str] = mapped_column(String(30), default="household")
    origin: Mapped[str] = mapped_column(String(20), default="unknown")
    scope_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    applicability: Mapped[dict] = mapped_column(JSON, default=dict)
    coverage_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[str] = mapped_column(String(40), default=timestamp)
    updated_at: Mapped[str] = mapped_column(String(40), default=timestamp)
    fields: Mapped[dict] = mapped_column(JSON, default=dict)
    findings: Mapped[list] = mapped_column(JSON, default=list)
    manual_checks: Mapped[dict] = mapped_column(JSON, default=dict)
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_assessment_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    rule_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    review_decision: Mapped[str | None] = mapped_column(String(30), nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class EvidenceImage(Base):
    __tablename__ = "evidence_images"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    inspection_id: Mapped[str] = mapped_column(ForeignKey("inspections.id"), index=True)
    filename: Mapped[str] = mapped_column(String(200))
    stored_name: Mapped[str] = mapped_column(String(100))
    original_name: Mapped[str] = mapped_column(String(100))
    sha256: Mapped[str] = mapped_column(String(64))
    panel: Mapped[str] = mapped_column(String(20))
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    quality: Mapped[dict] = mapped_column(JSON, default=dict)
    lines: Mapped[list] = mapped_column(JSON, default=list)
    ocr_text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(String(40), default=timestamp)


class EvidencePayload(Base):
    """Durable evidence for a small demo hosted without a persistent disk."""

    __tablename__ = "evidence_payloads"
    image_id: Mapped[str] = mapped_column(ForeignKey("evidence_images.id"), primary_key=True)
    original: Mapped[bytes] = mapped_column(LargeBinary)
    normalized: Mapped[bytes] = mapped_column(LargeBinary)


class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    inspection_id: Mapped[str] = mapped_column(ForeignKey("inspections.id"), index=True)
    created_at: Mapped[str] = mapped_column(String(40), default=timestamp)
    rule_version: Mapped[str] = mapped_column(String(100))
    snapshot: Mapped[dict] = mapped_column(JSON)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    inspection_id: Mapped[str] = mapped_column(ForeignKey("inspections.id"), index=True)
    actor: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(100))
    detail: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(40), default=timestamp)
