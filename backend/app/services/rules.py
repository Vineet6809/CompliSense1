"""Explainable declaration checks for the deliberately narrow demo scope.

These checks establish whether the supplied evidence supports a small set of
declaration-presence checks. They do not determine penalties, factual truth, or
complete legal compliance. The Rules page and every export repeat that limit.
"""

from typing import Any

from .extraction import reconcile_fields

RULE_VERSION = "demo-2026.09"
SOURCE_URL = "https://consumeraffairs.gov.in/pages/legal-metrology-act"

RULES = [
    {
        "id": "LMPC-6-1-A",
        "title": "Responsible business declaration",
        "field": "manufacturer",
        "provision": "Rule 6(1)(a)",
        "description": "Checks for a candidate manufacturer, packer, or importer declaration.",
    },
    {
        "id": "LMPC-6-1-A-ADDRESS",
        "title": "Responsible business address",
        "field": "address",
        "provision": "Rule 6(1)(a)",
        "description": "Checks for a candidate address linked to the responsible business.",
    },
    {
        "id": "LMPC-6-1-B",
        "title": "Common or generic product name",
        "field": "product_name",
        "provision": "Rule 6(1)(b)",
        "description": "Checks for a candidate product identity declaration.",
    },
    {
        "id": "LMPC-6-1-C",
        "title": "Net quantity declaration",
        "field": "net_quantity",
        "provision": "Rule 6(1)(c)",
        "description": "Checks for a candidate net quantity declaration.",
    },
    {
        "id": "LMPC-6-1-D",
        "title": "Manufacture, packing, or import date",
        "field": "date",
        "provision": "Rule 6(1)(d)",
        "description": "Checks for a candidate date declaration; applicability and exceptions require review.",
    },
    {
        "id": "LMPC-6-1-E",
        "title": "Retail sale price declaration",
        "field": "mrp",
        "provision": "Rule 6(1)(e)",
        "description": "Checks for a candidate retail sale price or MRP declaration.",
    },
    {
        "id": "LMPC-6-1-F",
        "title": "Consumer care declaration",
        "field": "consumer_care",
        "provision": "Rule 6(1)(f)",
        "description": "Checks for candidate consumer complaint or customer care details.",
    },
    {
        "id": "LMPC-6-1-AA",
        "title": "Country of origin for imported products",
        "field": "country_of_origin",
        "provision": "Rule 6(1)(aa)",
        "description": "Checks for a country-of-origin candidate only when the product is recorded as imported.",
    },
]

LIMITATIONS = [
    "The active rule set is an educational prototype for ordinary household packaged commodities. A domain expert must verify current amendments, exemptions, and product-specific applicability before operational use.",
    "A pass means the supplied evidence supports this implemented declaration check. It is not a certificate of legal compliance.",
    "OCR confidence is not legal certainty. Low-confidence, blurred, incomplete, or conflicting evidence is sent for review.",
    "Font size, physical placement, readability, and factual truth require measurements or human inspection in this build.",
]


def public_rule_data() -> dict[str, Any]:
    return {
        "version": RULE_VERSION,
        "scope": "Prototype checks for ordinary household packaged commodities",
        "limitations": LIMITATIONS,
        "rules": [{**rule, "source_url": SOURCE_URL} for rule in RULES],
    }


def _evidence_quality_is_uncertain(images: list[dict]) -> bool:
    if not images:
        return True
    return any(
        image.get("quality", {}).get("warnings") or image.get("quality", {}).get("review_required")
        for image in images
    )


def _finding(rule: dict, status: str, explanation: str, candidate: dict | None = None) -> dict:
    candidate = candidate or {}
    return {
        "rule_id": rule["id"],
        "title": rule["title"],
        "status": status,
        "explanation": explanation,
        "field": rule.get("field"),
        "evidence_image_id": candidate.get("image_id"),
        "evidence_box": candidate.get("box"),
        "source_url": SOURCE_URL,
        "provision": rule["provision"],
    }


def _presence_check(rule: dict, fields: dict, context: dict, images: list[dict]) -> dict:
    candidate = fields.get(rule["field"], {})
    value = str(candidate.get("value", "")).strip()
    applicability = context.get("applicability") or {}
    applicability_status = applicability.get("status")
    exemption = applicability.get("exemption", "none")
    if applicability_status == "not_applicable" or exemption == "confirmed":
        reason = applicability.get("reason") or "The recorded product context excludes this check."
        return _finding(rule, "not_applicable", f"Applicability recorded as not applicable. {reason}", candidate)
    if applicability_status == "unknown" or exemption == "claimed" or not context.get("scope_confirmed"):
        return _finding(
            rule,
            "needs_review",
            "Confirm applicability and any exemption before treating this declaration check as a violation.",
            candidate,
        )
    if rule["field"] == "net_quantity":
        reconciliation = (context.get("reconciliation") or {}).get("net_quantity", {})
        if reconciliation.get("status") == "conflict":
            return _finding(
                rule,
                "needs_review",
                "The front, back, or other supplied views contain different net quantities. Reconcile the package views before deciding whether the declaration is compliant.",
                candidate,
            )
    if value:
        confidence = float(candidate.get("confidence", 0))
        if _evidence_quality_is_uncertain(images) and candidate.get("source") != "manual":
            return _finding(
                rule,
                "needs_review",
                "The supporting image quality is uncertain because it may be blurred, reflective, low-resolution, or incomplete. Verify the highlighted photograph before relying on this value.",
                candidate,
            )
        if candidate.get("source") != "manual" and confidence < 0.70:
            return _finding(
                rule,
                "needs_review",
                "A possible declaration was extracted, but OCR confidence is low. Compare it with the highlighted photograph.",
                candidate,
            )
        return _finding(
            rule,
            "pass",
            "The supplied evidence contains a candidate declaration for this implemented presence check. Verify its accuracy and legal applicability.",
            candidate,
        )
    if context.get("coverage_confirmed") and not _evidence_quality_is_uncertain(images):
        return _finding(
            rule,
            "potential_violation",
            "The inspector confirmed relevant panel coverage, the supplied images were readable, and no candidate declaration was found. Human review is still required.",
        )
    return _finding(
        rule,
        "needs_review",
        "No reliable candidate was extracted, but panel coverage or image readability is insufficient to treat that as a missing declaration.",
    )


def evaluate_rules(fields: dict, context: dict, images: list[dict]) -> list[dict]:
    applicability = context.get("applicability")
    if applicability is None:
        # Preserve the original API contract for callers that only supplied the
        # scope checkbox; new records send an explicit applicability decision.
        applicability = {"status": "applicable" if context.get("scope_confirmed") else "unknown", "exemption": "none"}
    reconciliation = context.get("reconciliation") or reconcile_fields(fields)
    context = {**context, "applicability": applicability, "reconciliation": reconciliation}
    findings = []
    for rule in RULES:
        if rule["id"] == "LMPC-6-1-AA":
            if applicability.get("status") != "applicable" or applicability.get("exemption", "none") != "none":
                findings.append(_presence_check(rule, fields, context, images))
                continue
            origin = context.get("origin", "unknown")
            if origin == "domestic":
                findings.append(
                    _finding(
                        rule,
                        "not_applicable",
                        "The inspection records this product as domestic. Change the origin if that context is incorrect.",
                    )
                )
                continue
            if origin == "unknown":
                findings.append(
                    _finding(
                        rule,
                        "needs_review",
                        "Record whether the product is domestic or imported before applying this check.",
                    )
                )
                continue
        findings.append(_presence_check(rule, fields, context, images))

    manual = context.get("manual_checks") or {}
    assisted = [
        ("LMPC-ASSISTED-READABILITY", "Readability review", "Readability / legibility", "readability"),
        ("LMPC-ASSISTED-PLACEMENT", "Placement review", "Physical placement requirements", "placement"),
        ("LMPC-ASSISTED-FONT", "Type-size review", "Physical lettering-size requirements", "font_size"),
    ]
    for rule_id, title, provision, key in assisted:
        recorded = manual.get(key, "unassessed")
        explanation = {
            "acceptable": "An inspector recorded this assisted check as acceptable. The software has not independently measured or certified the physical requirement.",
            "concern": "An inspector recorded a concern. Capture measurements and supporting evidence for domain review.",
            "unassessed": "This physical requirement has not been assessed. Photographs without calibration are not enough for an automatic conclusion.",
        }.get(recorded, "This physical requirement requires human review.")
        status = "pass" if recorded == "acceptable" else "needs_review"
        findings.append(
            {
                "rule_id": rule_id,
                "title": title,
                "status": status,
                "explanation": explanation,
                "field": None,
                "evidence_image_id": None,
                "evidence_box": None,
                "source_url": SOURCE_URL,
                "provision": provision,
            }
        )
    return findings
