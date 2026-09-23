# SIH 2026 PPT Research and CompliSense Deck Review

Research basis: official SIH 2026 guidelines and SIH 2024 evaluation guidance already stored in this repository, the attached NotebookLM compilation, and visual/text inspection of `SIH2026_PS26034-final-ppt (2).pptx`.

## Evidence boundary

The official SIH 2026 guidelines say idea selection considers novelty, complexity, clarity and detail, feasibility, practicability, sustainability, scale of impact, user experience, and future progression. They also state that 4–5 teams per problem statement may be selected and that the problem-statement organization makes the final decision.

The SIH 2024 evaluator guide is useful historical preparation guidance, not a confirmed 2026 score sheet. It evaluates presentation/idea, innovation, solution approach, technical soundness/feasibility, and execution timeline in round 1; prototype progress, feedback improvement, integration, usability, and teamwork in round 2; and functionality/relevance, final demo, user experience, market readiness/impact, and implementation plan/future scope in round 3. Its published weighting is 20% / 30% / 50%.

The NotebookLM compilation contains useful patterns from prior decks and a strong technical critique, but its claims about specific winning decks, judge preferences, time limits, accuracy, and competitor capabilities are not independently established by the official SIH documents. Treat those as hypotheses or presentation advice, not official rules.

## What selection reviewers need to understand quickly

Within the first minute, the jury should be able to answer five questions:

1. What inspection problem does SIH26034 create for the user?
2. What exactly does CompliSense scan and check?
3. What makes the approach technically credible?
4. What can be demonstrated now?
5. Why is this useful to the problem-statement owner?

The strongest central sentence for this project is:

> AI perceives evidence. Deterministic rules evaluate it. An officer verifies the result.

This communicates the architecture and avoids the risky claim that an LLM makes a legal decision.

## Review of the current deck

### Slide 1: title and metadata

The slide contains the required identity information, but the problem title is long and visually dominant. Add the sponsoring organization if it is confirmed in the problem statement, and replace `Team ID - NA` before submission. Use a short solution descriptor below the title, such as `Evidence-backed package-label inspection for Legal Metrology officers`.

### Slide 2: challenges, solution, innovation

This is the most overloaded slide. It has several large text blocks, repeated ideas, and a visible text collision around the innovation section. The bottom content is too close to the footer and some text is clipped or hard to scan.

Reduce it to three regions:

- Problem: manual, inconsistent inspection; missing or unreadable declarations; weak evidence traceability.
- Solution flow: multi-view images -> OCR/evidence -> deterministic rules -> officer review -> report.
- Three differentiators: evidence-linked findings, cross-view contradiction checks, and an uncertainty review queue.

Remove repeated phrases such as “AI scanning”, “rule checking”, and “violation evidence” when they already appear in the solution flow.

### Slide 3: technical approach

This is conceptually strong and aligned with the NotebookLM research. It is too dense for a jury slide, however. Keep the architecture diagram, but make the data contract visible:

`images -> extracted fields + boxes + confidence -> applicability gate -> rule checks -> findings -> report`

Show one concrete contradiction example, such as a different net quantity on two package faces. State clearly that OCR/VLM extracts evidence and does not issue the compliance verdict. Move the long technology logo strip into a small footer or remove it; stack names do not prove feasibility.

### Slide 4: feasibility and viability

The rendered slide is visually attractive but currently reads like a generic infographic. It does not show enough project-specific feasibility evidence. Replace the generic four-way feasibility graphic with a risk-to-mitigation table:

| Risk | Prototype treatment |
| --- | --- |
| Glare, blur, curved labels | image-quality warning, confidence score, human review |
| Missing panel coverage | inspector confirms coverage before a missing-field finding |
| Different product applicability | applicability/context gate before rule checks |
| OCR extraction error | bounding-box evidence and manual correction with audit history |
| Rule changes | versioned rule catalogue and report snapshot |

Add the actual prototype status: what works today, what is assisted review, and what remains future scope. Never claim 100% accuracy.

### Slide 5: impact and benefits

This slide contains too many audiences, business-model claims, revenue streams, and future integrations. Several claims are not supported by the attached official sources and distract from SIH26034.

Keep four user outcomes:

- Field officers: faster, evidence-linked inspection records.
- Controllers and regulators: searchable history and consistent review.
- Manufacturers and sellers: earlier detection of label problems.
- Consumers: clearer declared information and stronger traceability.

Replace the business model with a rollout path: pilot with a small product set, validate with domain experts, expand the rule catalogue, then consider registry integrations. Use “potential benefit” language unless you have measured results.

### Slide 6: research and references

This is currently the strongest slide because it shows the product flow. Keep the three-screen sequence, but label the screens with the actual workflow: `Capture`, `Evidence review`, `Officer-assisted report`.

Correct or verify every legal date before submission. The current slide states both “effective 1 July 2027” and an amendment dated 2026; this must match the exact official notification and effective date. Include the source title, issuing body, URL, and access date in small readable text. Do not use a reference merely because it appeared in NotebookLM.

## Recommended six-slide structure

### 1. Problem and solution identity

Title: `CompliSense: Evidence-backed Legal Metrology inspection`

Include SIH26034, official problem title, team name, category, and confirmed sponsor. Add one sentence: “A field inspection assistant that scans package labels, links findings to image evidence, and supports rule-based review.”

### 2. Problem, users, and proposed solution

Use a simple before/after composition. Before: manual label checking, inconsistent evidence, repeated work. After: multi-view capture, structured extraction, applicable rule checks, reviewable report. Put `AI perceives. Rules evaluate. Officer verifies.` in the visual center.

### 3. Technical approach and architecture

Show the five-stage pipeline and one worked example. Include the fields you actually support: manufacturer/address, generic name, net quantity, MRP, date, consumer care, and origin where applicable. Describe readability and placement as assisted or relative checks unless calibrated evidence exists.

### 4. Feasibility and risk control

Use the risk-to-mitigation table above. Add the build boundary: real image upload, OCR extraction, deterministic checks, evidence boxes, history, and report export. Mark live registries, e-commerce crawling, millimetre calibration, advanced dewarping, and legal-notice automation as future scope unless already implemented and validated.

### 5. Impact, adoption, and future progression

Show the four user groups, the workflow benefit for each, and a three-stage progression: prototype validation, supervised pilot, broader rule/product coverage. Do not add unmeasured market size, revenue, or accuracy numbers.

### 6. Prototype evidence and references

Use the three UI screenshots plus a small evidence crop showing a field, its confidence, and its rule reference. End with official sources and a short limitations line: “The prototype assists inspection; final statutory action remains with the authorized officer.”

## Keywords that help because they are concrete

Use these when they describe implemented behavior:

`multi-view package scanning`, `structured declaration extraction`, `bounding-box evidence`, `confidence scoring`, `applicability checks`, `versioned rule catalogue`, `deterministic rule engine`, `cross-view contradiction`, `human-in-the-loop review`, `PASS / REVIEW REQUIRED / NOT APPLICABLE`, `audit trail`, `inspection history`, `searchable repository`, `evidence-backed report`, `role-based access`, `offline-tolerant workflow`, `relative readability assessment`, `officer-assisted decision support`.

Avoid unsupported or risky phrases:

`100% accurate`, `autonomous legal decision`, `legally binding`, `court-defensible`, `automatic prosecution`, `certified millimetre measurement from any photo`, `zero hallucination`, `real-time national compliance`, `guaranteed penalty prevention`, and `AI replaces inspectors`.

## What a convincing SIH deck tends to show

The NotebookLM examples consistently point toward a problem-first narrative, architecture that explains data movement, visible prototype screens, concrete edge-case handling, and explicit risk mitigation. Those are useful design patterns, but they are not official SIH guarantees. For this project, a convincing deck should show one normal scan, one uncertainty case, and one cross-view contradiction. Each result should show the source image, the extracted field, the rule reference, and the action expected from the officer.

## Jury questions to prepare

- How do you prevent an AI model from making a legal decision?  Explain the separation between extraction and deterministic rule evaluation.
- What happens when OCR is wrong?  Show confidence, evidence boxes, correction, and audit history.
- How do you know a missing declaration is actually missing?  Require relevant panel coverage and route uncertain cases to review.
- Can a photo prove physical net quantity or certified font size?  No; describe those as assisted or relative checks unless calibrated validation exists.
- How do exemptions and product context affect checks?  Run applicability checks before mandatory-field evaluation.
- What is genuinely new?  State the combination of evidence linkage, cross-view reconciliation, applicability handling, and officer workflow; do not claim that OCR alone is novel.
- What works in the prototype today?  Demonstrate the exact path from upload to finding to report.
- What data did you test on?  Disclose the sample size, product types, languages, and limitations. Never invent a benchmark.
- How are rules updated?  Use versioned rule packs and preserve the rule version in each report.
- Why would a regulator use this?  It reduces repetitive capture and makes evidence and review history easier to inspect; it does not replace statutory authority.

## Final recommendation

Proceed with modifications. The core idea is aligned with SIH26034 and technically defensible when framed as officer-assisted inspection. The strongest differentiator is the evidence chain from package image to extracted field to rule reference to reviewable report. The largest presentation risk is overclaiming legal coverage or adding business and platform features that are not demonstrated.

For the actual presentation, spend less time naming technologies and more time showing one complete inspection. A jury should remember the evidence chain and the phrase “AI perceives, rules evaluate, officer verifies.”
