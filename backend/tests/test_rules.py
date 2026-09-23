"""Rule checks must distinguish missing declarations from missing evidence."""

from app.services.rules import evaluate_rules


def field(value="", confidence=0.0, image_id=None):
    return {"value": value, "confidence": confidence, "image_id": image_id, "box": None, "source": "ocr", "note": ""}


def base_fields():
    return {
        name: field()
        for name in (
            "product_name",
            "manufacturer",
            "address",
            "net_quantity",
            "mrp",
            "date",
            "consumer_care",
            "country_of_origin",
        )
    }


def context(**overrides):
    value = {
        "category": "household",
        "origin": "domestic",
        "scope_confirmed": True,
        "coverage_confirmed": True,
        "manual_checks": {},
    }
    value.update(overrides)
    return value


def by_id(findings, rule_id):
    return next(finding for finding in findings if finding["rule_id"] == rule_id)


def test_missing_field_is_not_violation_without_confirmed_panel_coverage():
    findings = evaluate_rules(base_fields(), context(coverage_confirmed=False), [])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "needs_review"


def test_missing_field_can_be_potential_violation_after_coverage_confirmation():
    findings = evaluate_rules(base_fields(), context(), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "potential_violation"


def test_low_confidence_candidate_needs_review_instead_of_passing():
    fields = base_fields()
    fields["mrp"] = field("MRP Rs 45", 0.42, "image-1")
    findings = evaluate_rules(fields, context(), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-E")["status"] == "needs_review"


def test_imported_product_requires_country_of_origin_candidate():
    findings = evaluate_rules(base_fields(), context(origin="imported"), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-AA")["status"] == "potential_violation"
    domestic = evaluate_rules(base_fields(), context(origin="domestic"), [{"quality": {"warnings": []}}])
    assert by_id(domestic, "LMPC-6-1-AA")["status"] == "not_applicable"


def test_officer_confirmed_physical_checks_resolve_to_pass():
    findings = evaluate_rules(base_fields(), context(manual_checks={"font_size": "acceptable"}), [])
    assert by_id(findings, "LMPC-ASSISTED-FONT")["status"] == "pass"


def test_unknown_applicability_blocks_potential_violation():
    findings = evaluate_rules(base_fields(), context(applicability={"status": "unknown", "exemption": "none", "reason": ""}), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "needs_review"


def test_confirmed_exemption_is_not_applicable():
    findings = evaluate_rules(base_fields(), context(applicability={"status": "applicable", "exemption": "confirmed", "reason": "Verified category exemption."}), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "not_applicable"


def test_uncertain_image_quality_requires_review_even_with_a_value():
    fields = base_fields()
    fields["net_quantity"] = field("100 g", 0.96, "image-1")
    findings = evaluate_rules(fields, context(), [{"quality": {"warnings": ["glare"], "review_required": True}}])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "needs_review"


def test_conflicting_net_quantities_require_review():
    fields = base_fields()
    fields["net_quantity"] = {
        **field("100 g", 0.96, "front"),
        "candidates": [
            {"value": "100 g", "confidence": 0.96, "image_id": "front", "panel": "front", "box": None},
            {"value": "250 g", "confidence": 0.96, "image_id": "back", "panel": "back", "box": None},
        ],
    }
    findings = evaluate_rules(fields, context(), [{"quality": {"warnings": []}}])
    assert by_id(findings, "LMPC-6-1-C")["status"] == "needs_review"
