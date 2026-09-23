"""Turn OCR text into editable candidates, never into a legal decision."""

import re

FIELD_NAMES = (
    "product_name",
    "manufacturer",
    "address",
    "net_quantity",
    "mrp",
    "date",
    "consumer_care",
    "country_of_origin",
)

# Keep the expressions here, rather than hidden in a model prompt, so a student
# can inspect and improve each one against labelled package photographs.
PATTERNS = {
    "product_name": r"(?:product(?:\s+name)?|common\s+name|commodity)\s*[:\-]\s*(.*)",
    "manufacturer": r"(?:manufactured|packed|imported|manufacturer|packer|importer)\s*(?:&\s*packed\s*)?(?:by)?\s*[:\-]\s*(.*)",
    "address": r"(?:registered\s+office|address|factory\s+address)\s*[:\-]\s*(.*)",
    "net_quantity": r"(?:net\s*(?:quantity|qty\.?|weight|wt\.?|volume)|quantity)\s*[:\-]?\s*(.*)",
    "mrp": r"((?:m\.?\s*r\.?\s*p\.?(?=\s|rs|inr|₹|[:\-]|\d)|maximum\s+retail\s+price\b|retail\s+sale\s+price\b).*)",
    "date": r"(?:mfd\.?|mfg\.?\s*date|pkd\.?|packed\s+on|date\s+of\s+(?:manufacture|packing|import)|manufactured\s+(?:on|in))\s*[:\-]?\s*(.*)",
    "consumer_care": r"((?:consumer\s*(?:care|complaint)|customer\s*(?:care|service)|for\s+(?:queries|complaints))\b.*)",
    "country_of_origin": r"(?:country\s+of\s+origin|made\s+in)\s*[:\-]?\s*(.*)",
}
COMPILED = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in PATTERNS.items()}
QUANTITY_PATTERN = re.compile(r"(?P<number>\d+(?:\.\d+)?)\s*(?P<unit>kg|g|mg|l|ml|litre|litres|liter|liters|pcs?|pieces?)\b", re.IGNORECASE)


def empty_declaration() -> dict:
    return {
        "value": "",
        "confidence": 0.0,
        "image_id": None,
        "box": None,
        "source": "ocr",
        "note": "No reliable candidate extracted.",
    }


def merged_box(lines: list[dict]) -> list[list[float]] | None:
    points = [point for line in lines for point in line.get("box", [])]
    if not points:
        return None
    left = min(point[0] for point in points)
    top = min(point[1] for point in points)
    right = max(point[0] for point in points)
    bottom = max(point[1] for point in points)
    return [[left, top], [right, top], [right, bottom], [left, bottom]]


def is_another_field(text: str, current: str) -> bool:
    return any(pattern.search(text) for name, pattern in COMPILED.items() if name != current)


def looks_like_footer(text: str) -> bool:
    compact = re.sub(r"\s+", "", text).lower()
    return any(marker in compact for marker in ("fictional", "synthetic", "softwaretesting", "verifyallrules"))


def extract_declarations(images: list[dict]) -> dict:
    candidates: dict[str, list[dict]] = {name: [] for name in FIELD_NAMES}
    for image in images:
        lines = image.get("lines", [])
        for index, line in enumerate(lines):
            # Synthetic samples identify themselves clearly. Those disclaimer
            # lines can contain words such as "product", but they are not
            # declarations and must not compete with the actual label fields.
            if looks_like_footer(line["text"]):
                continue
            for name, pattern in COMPILED.items():
                match = pattern.search(line["text"])
                if not match:
                    continue
                value = match.group(1).strip(" :-")
                supporting = [line]
                # Addresses and contact information often wrap onto nearby lines.
                # Stop at a different declaration to avoid swallowing the label.
                if name in ("address", "consumer_care") or not value:
                    for following in lines[index + 1 : index + 4]:
                        if is_another_field(following["text"], name) or looks_like_footer(following["text"]):
                            break
                        if name not in ("address", "consumer_care") and value:
                            break
                        value = f"{value} {following['text']}".strip()
                        supporting.append(following)
                if not value:
                    continue
                candidates[name].append(
                    {
                        "value": value[:2000],
                        "confidence": round(min(item["confidence"] for item in supporting), 3),
                        "image_id": image["id"],
                        "panel": image.get("panel", "other"),
                        "box": merged_box(supporting),
                        "source": "ocr",
                        "note": "",
                    }
                )
    fields = {}
    for name, choices in candidates.items():
        if not choices:
            fields[name] = {**empty_declaration(), "candidates": []}
            continue
        best = dict(max(choices, key=lambda candidate: candidate["confidence"]))
        distinct = {
            normalized_quantity(item["value"]) if name == "net_quantity" else re.sub(r"\s+", "", item["value"]).lower()
            for item in choices
        }
        if len(distinct) > 1:
            best["confidence"] = min(best["confidence"], 0.5)
            best["note"] = (
                "Conflicting candidates were found across the supplied label images. Confirm the correct declaration."
            )
        best["candidates"] = choices
        fields[name] = best
    return fields


def normalized_quantity(value: str) -> tuple[float, str] | None:
    """Normalize common quantity units so 1000 g and 1 kg reconcile."""
    match = QUANTITY_PATTERN.search(value or "")
    if not match:
        return None
    amount = float(match.group("number"))
    unit = match.group("unit").lower()
    if unit == "kg":
        return round(amount * 1000, 3), "g"
    if unit == "mg":
        return round(amount / 1000, 3), "g"
    if unit in {"l", "litre", "litres", "liter", "liters"}:
        return round(amount * 1000, 3), "ml"
    if unit == "pcs" or unit == "pc" or unit.startswith("piece"):
        return round(amount, 3), "pcs"
    return round(amount, 3), unit


def reconcile_fields(fields: dict) -> dict:
    """Return a small, serializable view of cross-image declaration agreement."""
    declaration = fields.get("net_quantity", {})
    candidates = declaration.get("candidates", [])
    if len(candidates) < 2:
        return {"net_quantity": {"status": "insufficient", "candidates": candidates}}
    normalized = [normalized_quantity(candidate.get("value", "")) for candidate in candidates]
    comparable = [item for item in normalized if item is not None]
    status = "conflict" if len(comparable) >= 2 and len(set(comparable)) > 1 else "consistent"
    return {
        "net_quantity": {
            "status": status,
            "candidates": candidates,
            "normalized": [f"{item[0]:g} {item[1]}" if item is not None else None for item in normalized],
        }
    }
