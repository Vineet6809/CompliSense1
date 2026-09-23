"""Small, explicit configuration object; tests can pass their own settings."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")


def database_url_from_environment() -> str:
    """Use the installed Psycopg 3 driver for Render and local Postgres URLs."""
    value = os.getenv("DATABASE_URL", "").strip()
    if value.startswith("postgres://"):
        value = "postgresql://" + value.removeprefix("postgres://")
    if value.startswith("postgresql://"):
        value = "postgresql+psycopg://" + value.removeprefix("postgresql://")
    return value


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: Path(os.getenv("DATA_DIR", str(BACKEND_DIR / "data"))))
    database_url: str = field(default_factory=database_url_from_environment)
    cookie_secure: bool = field(default_factory=lambda: os.getenv("COOKIE_SECURE", "false").lower() == "true")
    allowed_origins: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            value.strip()
            for value in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
            if value.strip()
        )
    )
    session_hours: int = 12
    evidence_in_database: bool = field(
        default_factory=lambda: os.getenv("EVIDENCE_IN_DATABASE", "false").lower() == "true"
    )
    max_upload_bytes: int = 10 * 1024 * 1024
    max_images: int = 8

    def __post_init__(self):
        self.data_dir = self.data_dir.resolve()
        if not self.database_url:
            self.database_url = f"sqlite:///{self.data_dir / 'complisense.db'}"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "images").mkdir(exist_ok=True)
