"""Validate uploaded content before writing it to private evidence storage."""

import hashlib
import warnings
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 20_000_000


def store_image(data: bytes, image_id: str, directory: Path) -> dict:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as source:
                if source.format not in ("JPEG", "PNG", "WEBP"):
                    raise ValueError("Upload a JPEG, PNG, or WebP photograph.")
                source.verify()
            with Image.open(BytesIO(data)) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")
                if min(image.size) < 64 or max(image.size) > 10000:
                    raise ValueError("Images must be at least 64 pixels per side and at most 10,000 pixels per side.")
                normalized_name = f"{image_id}.jpg"
                original_name = f"{image_id}.original"
                # The immutable original preserves evidence. The display copy has
                # orientation fixed and EXIF removed so coordinate overlays agree.
                (directory / original_name).write_bytes(data)
                image.save(directory / normalized_name, format="JPEG", quality=95)
                return {
                    "stored_name": normalized_name,
                    "original_name": original_name,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "width": image.width,
                    "height": image.height,
                }
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        raise ValueError("This file is not a safe, readable image. Use a smaller JPEG, PNG, or WebP.") from error
