# Legal rule source map and verification boundary

Research note updated 17 September 2026.

## Purpose

This document records what the CompliSense demo implements and what must be verified before a pilot. It is an engineering source map, not legal advice or a statement that the prototype covers every applicable requirement.

The active code points users to the Department of Consumer Affairs Legal Metrology page:

- Department of Consumer Affairs, Legal Metrology Act and rules: https://consumeraffairs.gov.in/pages/legal-metrology-act
- Problem statement reference supplied for CompliSense: Legal Metrology (Packaged Commodities) Rules, 2011, including applicable amendments

Official consolidated text, commencement dates, amendment notifications, exemptions, commodity-specific rules, and state enforcement practice must be checked by a qualified Legal Metrology specialist before operational use. A link on an official page is useful provenance, but it does not by itself prove that a provision is current for every product and date.

## Implemented demo catalogue

The application labels its catalogue `demo-2026.09`. The rules are narrow presence checks derived from declarations commonly associated with Rule 6. They do not validate the factual truth of a declaration, exact formatting, measurement tolerances, penalties, or every exception.

| Application rule ID | Displayed provision | Software behavior | Required expert verification |
| --- | --- | --- | --- |
| `LMPC-6-1-A` | Rule 6(1)(a) | Looks for a manufacturer, packer, or importer candidate | Current wording, entity alternatives, exemptions, and product applicability |
| `LMPC-6-1-A-ADDRESS` | Rule 6(1)(a) | Looks for an address candidate | Address requirements and permitted formats |
| `LMPC-6-1-B` | Rule 6(1)(b) | Looks for a common or generic product-name candidate | Naming rules for the inspected commodity |
| `LMPC-6-1-C` | Rule 6(1)(c) | Looks for a net-quantity candidate | Units, tolerances, quantity expression, and product exceptions |
| `LMPC-6-1-D` | Rule 6(1)(d) | Looks for a manufacture, packing, or import-date candidate | Which date is required and all exceptions |
| `LMPC-6-1-E` | Rule 6(1)(e) | Looks for an MRP or retail-sale-price candidate | Current price wording, tax treatment, and exceptions |
| `LMPC-6-1-F` | Rule 6(1)(f) | Looks for consumer-care details | Required contact channels and current wording |
| `LMPC-6-1-AA` | Rule 6(1)(aa) | Applies only when the inspector records the product as imported | Current country-of-origin requirement and applicability |

Three additional items are always assisted human checks:

- readability and legibility;
- physical placement; and
- lettering or font size.

The software records the inspector's observation but does not claim to measure or certify these physical properties from an uncalibrated photograph.

## Why missing OCR text is not automatically a violation

OCR can miss text because a panel was not photographed, the image is blurred, glare hides the declaration, the layout is unusual, or the extractor failed. CompliSense only produces a `potential_violation` for a missing candidate when the inspector confirms relevant panel coverage and the uploaded images have no recorded quality warning. Even then, the result explicitly requires human review.

Other uncertain cases remain `needs_review`:

- scope is not confirmed;
- product origin is unknown for the country-of-origin check;
- OCR confidence is below the demo threshold;
- image quality is uncertain; or
- relevant panel coverage is not confirmed.

## Pilot verification checklist

Before changing the rule version from `demo-*` to an operational catalogue:

1. Obtain the official base rules and every applicable amendment notification.
2. Have a domain expert create a provision matrix with effective dates, applicability conditions, exceptions, and examples.
3. Link each executable rule to the exact official document, page, clause, and effective date.
4. Test every rule with positive, negative, exception, unreadable, and incomplete-panel examples.
5. Record who approved each rule and when. Treat rule changes like code releases.
6. Preserve the rule version inside every frozen assessment and report.
7. Add calibrated measurement only after validating the camera geometry, reference scale, and error bounds.

The current implementation already preserves a rule version and immutable report snapshot so that later catalogue changes do not silently rewrite old inspection reports.

