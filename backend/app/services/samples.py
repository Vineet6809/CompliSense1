"""Create fictional labels that exercise the real OCR pipeline without legal claims."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SAMPLES = [
    (
        "complete-label.png",
        "Complete fictional label",
        "Contains candidates for the supported declaration-presence checks.",
    ),
    (
        "missing-price-label.png",
        "Fictional label without price",
        "Useful for testing a potential missing-price finding after coverage confirmation.",
    ),
    (
        "low-contrast-label.png",
        "Difficult fictional label",
        "Low contrast demonstrates why uncertain evidence should be reviewed.",
    ),
]


def _font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _draw_label(path: Path, lines: list[str], foreground=(22, 43, 42), background=(249, 247, 240)):
    image = Image.new("RGB", (1600, 1200), background)
    draw = ImageDraw.Draw(image)
    draw.rectangle((55, 55, 1545, 1145), outline=(35, 102, 98), width=8)
    draw.text((105, 95), "COMPLISENSE SYNTHETIC TEST LABEL", fill=(35, 102, 98), font=_font(44, True))
    draw.text((105, 160), "Fictional product - not for sale", fill=(145, 70, 50), font=_font(28, True))
    y = 245
    for index, line in enumerate(lines):
        draw.text((115, y), line, fill=foreground, font=_font(34, index == 0))
        y += 76
    draw.text(
        (105, 1085),
        "Created only for software testing. Verify all rules with official sources.",
        fill=(80, 92, 90),
        font=_font(24),
    )
    image.save(path, "PNG")


def ensure_samples(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    complete = [
        "Product: Household Cleaning Soap",
        "Manufactured by: Example Labs Private Limited",
        "Address: 12 Market Road, Pune, Maharashtra 411001",
        "Net Quantity: 100 g",
        "MRP Rs. 45.00 (inclusive of all taxes)",
        "MFD: 08/2026",
        "Consumer Care: 1800 111 222",
        "Email: care@example.test",
    ]
    missing_price = [line for line in complete if not line.startswith("MRP")]
    _draw_label(directory / SAMPLES[0][0], complete)
    _draw_label(directory / SAMPLES[1][0], missing_price)
    _draw_label(directory / SAMPLES[2][0], complete, foreground=(174, 177, 170), background=(218, 218, 211))


def public_samples() -> list[dict]:
    return [
        {"name": name, "description": description, "url": f"/api/samples/{filename}"}
        for filename, name, description in SAMPLES
    ]
