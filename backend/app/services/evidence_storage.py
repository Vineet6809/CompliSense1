"""Keep durable evidence in the database; local files are a rebuildable cache."""

import os
import tempfile
from pathlib import Path

from sqlalchemy.orm import Session

from ..models import EvidenceImage, EvidencePayload


def persist_evidence(db: Session, image: EvidenceImage, data_dir: Path) -> None:
    directory = data_dir / "images"
    db.add(EvidencePayload(
        image_id=image.id,
        original=(directory / image.original_name).read_bytes(),
        normalized=(directory / image.stored_name).read_bytes(),
    ))


def restore_evidence(db: Session, image: EvidenceImage, data_dir: Path) -> Path:
    """Call only after authorizing access to the owning inspection."""
    directory = data_dir / "images"
    path = directory / image.stored_name
    if path.is_file() and (directory / image.original_name).is_file():
        return path
    payload = db.get(EvidencePayload, image.id)
    if payload is None:
        return path  # Existing installations can still use a persistent disk.
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in ((image.stored_name, payload.normalized), (image.original_name, payload.original)):
        target = directory / name
        if target.is_file():
            continue
        # Atomic replacement prevents concurrent report/image reads seeing a partial file.
        with tempfile.NamedTemporaryFile(dir=directory, delete=False) as temporary:
            temporary.write(content)
            temporary_path = Path(temporary.name)
        try:
            os.replace(temporary_path, target)
        finally:
            temporary_path.unlink(missing_ok=True)
    return path
