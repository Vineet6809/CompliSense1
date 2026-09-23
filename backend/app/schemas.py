"""Request validation is separate from database tables and business rules."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Applicability(RequestModel):
    status: Literal["unknown", "applicable", "not_applicable"] = "unknown"
    exemption: Literal["none", "claimed", "confirmed"] = "none"
    reason: str = Field(default="", max_length=2000)


class LoginRequest(RequestModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


class InspectionCreate(RequestModel):
    product_name: str = Field(min_length=1, max_length=200)
    brand: str = Field(default="", max_length=150)
    barcode: str = Field(default="", max_length=100)
    category: Literal["household", "other"] = "household"
    origin: Literal["domestic", "imported", "unknown"] = "unknown"
    scope_confirmed: bool = False
    applicability: Applicability = Field(default_factory=Applicability)
    notes: str = Field(default="", max_length=5000)


class ManualChecks(RequestModel):
    readability: Literal["unassessed", "acceptable", "concern"] = "unassessed"
    placement: Literal["unassessed", "acceptable", "concern"] = "unassessed"
    font_size: Literal["unassessed", "acceptable", "concern"] = "unassessed"
    notes: str = Field(default="", max_length=3000)


class InspectionUpdate(RequestModel):
    version: int = Field(ge=1)
    product_name: str | None = Field(default=None, min_length=1, max_length=200)
    brand: str | None = Field(default=None, max_length=150)
    barcode: str | None = Field(default=None, max_length=100)
    origin: Literal["domestic", "imported", "unknown"] | None = None
    scope_confirmed: bool | None = None
    applicability: Applicability | None = None
    coverage_confirmed: bool | None = None
    notes: str | None = Field(default=None, max_length=5000)
    fields: dict[str, str] | None = None
    field_notes: dict[str, str] | None = None
    manual_checks: ManualChecks | None = None


class ReviewRequest(RequestModel):
    version: int = Field(ge=1)
    decision: Literal["accepted", "follow_up"]
    notes: str = Field(min_length=5, max_length=3000)
