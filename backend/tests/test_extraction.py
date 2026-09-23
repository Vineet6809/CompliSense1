"""Test extraction with hand-labelled OCR lines, independently of OCR accuracy."""

from app.services.extraction import extract_declarations, reconcile_fields


def evidence(lines):
    return [
        {
            "id": "image-1",
            "lines": [
                {
                    "text": text,
                    "confidence": 0.96,
                    "box": [[10, i * 30], [700, i * 30], [700, i * 30 + 20], [10, i * 30 + 20]],
                }
                for i, text in enumerate(lines)
            ],
        }
    ]


def test_extracts_quantity_price_and_business_without_using_metadata():
    fields = extract_declarations(
        evidence(
            [
                "Product: Household cleaning soap",
                "Manufactured by: Example Labs Pvt Ltd",
                "Address: 12 Market Road, Pune 411001",
                "Net Quantity: 100 g",
                "MRP Rs. 45.00 (inclusive of all taxes)",
                "MFD: 08/2026",
                "Consumer Care: 1800-111-222; care@example.com",
            ]
        )
    )
    assert fields["net_quantity"]["value"] == "100 g"
    assert "45.00" in fields["mrp"]["value"]
    assert "Example Labs" in fields["manufacturer"]["value"]
    assert fields["net_quantity"]["image_id"] == "image-1"
    assert fields["net_quantity"]["box"] is not None


def test_handles_compact_ocr_price_and_ignores_synthetic_disclaimer():
    fields = extract_declarations(
        evidence(
            [
                "Fictionalproduct-notforsale",
                "Product: Household Cleaning Soap",
                "Manufacturedby:ExampleLabsPrivateLimited",
                "MRPRs.45.00(inclusiveofall taxes)",
                "MFD:08/2026",
            ]
        )
    )

    assert fields["product_name"]["value"] == "Household Cleaning Soap"
    assert fields["manufacturer"]["value"] == "ExampleLabsPrivateLimited"
    assert fields["manufacturer"]["confidence"] == 0.96
    assert fields["mrp"]["value"] == "MRPRs.45.00(inclusiveofall taxes)"
    assert fields["date"]["value"] == "08/2026"


def test_absent_declarations_remain_empty():
    fields = extract_declarations(evidence(["Some unrelated advertising text"]))
    assert fields["mrp"]["value"] == ""
    assert fields["manufacturer"]["value"] == ""


def test_best_before_is_not_a_manufacture_date():
    fields = extract_declarations(evidence(["Best before 12/2027", "Expiry: 12/2027"]))
    assert fields["date"]["value"] == ""


def test_customer_contact_can_span_multiple_lines():
    fields = extract_declarations(evidence(["Consumer care:", "Phone: 1800 123 4567", "Email: help@example.com"]))
    assert "help@example.com" in fields["consumer_care"]["value"]


def test_conflicting_values_do_not_get_high_confidence():
    fields = extract_declarations(evidence(["Net Quantity: 100 g", "Net Quantity: 250 g"]))
    assert fields["net_quantity"]["confidence"] < 0.8
    assert "conflict" in fields["net_quantity"]["note"].lower()


def test_reconciliation_flags_different_quantities_across_panels():
    fields = extract_declarations([
        {"id": "front", "panel": "front", "lines": [{"text": "Net Quantity: 100 g", "confidence": 0.96, "box": [[0, 0], [1, 0], [1, 1], [0, 1]]}]},
        {"id": "back", "panel": "back", "lines": [{"text": "Net Quantity: 250 g", "confidence": 0.96, "box": [[0, 0], [1, 0], [1, 1], [0, 1]]}]},
    ])
    reconciliation = reconcile_fields(fields)
    assert reconciliation["net_quantity"]["status"] == "conflict"
    assert {candidate["panel"] for candidate in reconciliation["net_quantity"]["candidates"]} == {"front", "back"}
