# CompliSense — 36-hour SIH project plan

Problem statement: 26034, Department of Consumer Affairs.
Revised: 16 September 2026, following research into official SIH judging guidance.
Status: Planning only. No application code has been created.

## 1. Objective and evidence basis

Deliver a working inspection assistant that accepts real package photographs, extracts declarations, checks a bounded set of applicable rules, supports officer review, and produces traceable reports.

The user confirmed real label scanning and a 36-hour build budget. This plan assumes a prepared development laptop, access to sample products, and at least two contributors able to develop the application. Allocate the work across the six SIH team roles where available; actual team skills remain unconfirmed. This is an ambitious prototype schedule, not a production-readiness or winning guarantee.

Official 2026 idea-selection criteria include novelty, complexity, clarity, feasibility, practicability, sustainability, scale of impact, user experience, and future progression. The official 2024 evaluator guide adds useful historical detail: round 1 covers the idea, technical approach and timeline; round 2 covers progress, feedback-driven improvement, integration, usability and teamwork; round 3 covers functionality, demo performance, UX, readiness/impact and implementation plans.

The historical weights are 20%, 30%, and 50%. These are NOT confirmed 2026 weights. Internal college evaluation may differ. Use the actual event rubric when supplied.

Sources and exact page references: [SIH judging research](research/SIH_JUDGING_RESEARCH.md). The [original broader roadmap](PROJECT_ROADMAP.md) is retained for later development; this document controls the 36-hour milestone.

## 2. Product proposition

CompliSense helps inspectors identify potential packaged-label violations, with each finding linked to image evidence, an applicable legal rule, and a recorded human decision.

The differentiation to demonstrate is the combination of:

1. Evidence-linked declaration extraction: inspect the exact words and their image regions.
2. Applicability-aware rules: check the product context and rule version before making a finding.
3. Explicit uncertainty: incomplete panels, poor images and uncertain extraction produce needs-review outcomes.
4. A complete inspection record: corrections, review decisions, photographs and report history.

These are proposed product strengths, not verified claims of industry-first novelty. Build a small comparison of a manual checklist, raw OCR, and CompliSense using the same held-out labels. Do not claim that a third-party OCR engine is our own invention.

## 3. What judges can inspect

| Evaluation ground | Deliverable | Evidence to present |
| --- | --- | --- |
| Novelty and technical approach | Extraction + evidence + applicability + review workflow | One side-by-side example showing what raw OCR fails to provide |
| Feasibility and execution timeline | Small category scope, runnable local system, time gates | Architecture and completed milestones, with honest remaining gaps |
| Prototype development and integration | Full inspection flow | A real image reaches a saved finding and report through working components |
| Improvement from feedback | Timestamped feedback log | Actual evaluator/mentor request, resulting change, and verification |
| Usability and UX | Guided capture and image-side correction | An unfamiliar user can complete a supported inspection without developer intervention |
| Teamwork | Named owners and contribution record | Each member explains their actual artifact, decision or test |
| Functionality and problem relevance | Requirement coverage matrix below | Working outputs plus visibly assisted or deferred capabilities |
| Performance and impact | Held-out evaluation and timed comparison | Counts, errors, abstentions, latency and review time on named hardware |
| Sustainability and readiness | Cost and maintenance note | Hardware requirements, rule update process, pilot deployment and operating-cost assumptions |
| Future progression | Specific next pilot | More categories, validated measurement, language evaluation and field testing |

These mappings are our planning interpretation. They do not assign invented marks to features.

## 4. Final scope and requirement coverage

Scope one package category and one legal context. Select the category at hour 0–2 based on available labels and verified legal applicability. Prefer English-readable labels initially. Display the supported scope throughout the assessment and report.

| Problem-statement requirement | 36-hour implementation | Boundary |
| --- | --- | --- |
| Product scanning and image upload | Responsive capture/upload; multiple panels; panel tags | Upload fallback if browser camera capture is unreliable |
| Mandatory declaration extraction | OCR plus normalized candidates for identity, responsible business/address, net quantity, price, dates and consumer care | Only fields and rules verified as applicable to the selected scope |
| Correctness and completeness | A small source-backed rule set, field formatting checks, missing-field evidence checks | Usually validates declaration form/completeness, not the real-world truth of claims |
| Missing/non-standard/misleading declarations | Explainable potential violations and inconsistencies | No unsupported claim that the system establishes fraud |
| Readability | Basic image-quality check, extraction uncertainty, recapture guidance | Image quality is not itself a statutory lettering measurement |
| Font size | Record known dimensions/reference scale, reviewer measurement and unassessed status | Automatic calibrated flat-panel measurement is a stretch task |
| Placement | Capture panel type and offer a source-backed reviewer checklist | General automatic geometry/curved-package placement is deferred |
| Digital reports with evidence | PDF and basic editable DOCX from the same saved report data | Plain, correct documents take priority over elaborate formatting |
| Repository/search/history | Persistent inspections, search by product/date/status, reviewed snapshots | No bulk catalog ingestion |
| Dashboard | Three counts and a filterable inspection table | No decorative analytics or maps |
| Secure role-based access | Seeded inspector and reviewer accounts; server-side permission checks | Defer signup, password-reset service and user-administration UI |
| Documentation/deployment | Setup guide, architecture, rule catalogue, benchmark notes and pilot plan | One reproducible local deployment; cloud hosting only if already familiar |

Guided font/placement review is only partial coverage of automation requirements. Explicitly disclose this in demonstrations. If a judge asks for automatic sizing, show the calibrated prototype only when it has been validated.

## 5. Legal and extraction behavior

Research legal checks from the official rules and relevant amendments:
https://consumeraffairs.gov.in/pages/legal-metrology-act

This turn verified SIH judging documents, not the current Legal Metrology rules. Exact provisions, thresholds and exemptions still require verification before implementation.

Each implemented rule must have an ID, official source/provision, effective version, applicability condition, required evidence, and reviewed examples. Unverified checks are excluded from automatic conclusions and identified as unassessed coverage.

Use four per-rule states:

- Pass: evidence supports the implemented check.
- Potential violation: sufficient evidence supports a specific rule failure, subject to review.
- Needs review: evidence, extraction, applicability or measurement is uncertain.
- Not applicable: a recorded condition excludes the rule.

An empty OCR field is not proof of a missing declaration. Require readable coverage of relevant panels and reviewer confirmation before treating absence as a supported finding. Unknown applicability does not become not applicable.

Keep original images, extracted text, bounding boxes, corrected values and reviewer actions. Re-evaluation creates a new assessment version. Previously issued report snapshots do not silently change.

Use proposed confidence thresholds only after checking development samples; raw OCR confidence is not a calibrated probability of legal correctness.

## 6. Architecture for the time budget

Use a React/TypeScript responsive interface, a Python FastAPI backend, an off-the-shelf OCR engine, OpenCV for image preprocessing, SQLAlchemy persistence, and private local image/report storage.

Benchmark the already-working OCR candidate on actual labels before adding another dependency. Prefer PaddleOCR if setup and label results are good; use Tesseract if it provides the more reliable working baseline within the early time limit.

Use PostgreSQL if immediately available and familiar. At the hour-2 setup cutoff, use SQLite through the same persistence layer for a single-laptop demonstration if database setup is consuming the budget. Document that SQLite does not demonstrate multi-officer scaling.

Keep one API application. For the demo, process one inspection at a time in a bounded worker execution path with visible processing/failure state and manual retry. Preserve uploaded input before processing; mark interrupted work for retry after restart. Redis, distributed jobs and production-scale retries belong to the later pilot.

Run PDF and DOCX exports from the same frozen report payload. Use a familiar rendering library and simple templates. Keep model files installed locally so OCR can run without an external inference service; pre-download dependencies.

Minimum screens:

1. Sign-in.
2. Dashboard and saved inspections.
3. Capture/upload with panel coverage.
4. Evidence review and rule findings.
5. Report and review decision.

Minimum records: users/roles, inspections/context, images/panels, extraction runs/corrections, versioned rules, assessment findings, review decisions and report snapshots.

## 7. The 36-hour schedule

These are internal delivery checkpoints, not claims about official round timing. Adapt demonstrations to the organizer's actual schedule.

| Hours | Work | Exit condition |
| --- | --- | --- |
| 0–2 | Select category/context, source initial rules, collect labels, define shared data format, check OCR/setup | One actual label can be read; rule/source matrix started; task owners assigned |
| 2–6 | Capture UI, persistent inspection, OCR baseline, extraction schema, seeded authentication | Uploaded panels produce saved text and source coordinates |
| 6–10 | First rule checks, applicability, evidence highlights, basic corrections | First integrated upload-to-finding demonstration; no hardcoded product results |
| 10–16 | Improve declaration extraction, uncertain-evidence handling, correction history, reviewer actions | Supported good/bad/incomplete examples run through the same pipeline |
| 16–22 | PDF + DOCX, saved snapshots, search and minimal dashboard | An inspection can be reviewed, exported and reopened with its evidence |
| 22–24 | Integration fixes, role checks, font/placement assisted workflow, capture usability | Core product freeze; every promised core flow works locally |
| 24–28 | Held-out evaluation, timed manual comparison, actual feedback improvements | Measured results and failures recorded; fixes checked against regression examples |
| 28–30 | Calibrated font measurement ONLY if core is stable; otherwise reliability work | Validated flat-panel estimate or clearly declared assisted-only limitation |
| 30–33 | Prepare demo narrative, requirement coverage, cost/maintenance/pilot note, setup verification | Claims match the running build and evidence |
| 33–36 | Rehearse on clean and difficult labels, verify restart/retry, fix critical issues, prepare disclosed backup recording | Repeatable final demonstration; no new feature work |

Rule research, test annotation and demo documentation continue alongside development where people are available. Do not assume all dependencies are independent: a rule cannot be implemented before its source/applicability are understood.

### Cut rules

- If upload-to-finding is not integrated by hour 10, stop adding fields and improve the existing supported checks.
- If the complete inspection-to-report flow is not stable by hour 24, cancel automatic font measurement.
- Preserve genuine OCR, uncertainty handling, evidence links and report consistency.
- Reduce visual styling, animation, number of rules and dashboard breadth before cutting essential functionality.
- If basic DOCX or server-side roles cannot be finished, record the requirement gap; never present a cosmetic export or login as complete.
- After hour 30, new requirements go into the pilot roadmap unless they fix a critical demonstration failure.

## 8. Team ownership and feedback

For a six-member team, suggested ownership is:

| Owner | Main responsibility | Demonstrable contribution |
| --- | --- | --- |
| 1 | Integration, API and persistence | Full flow, error recovery, shared schema |
| 2 | Capture and review UI | Mobile workflow, evidence overlays, correction UX |
| 3 | OCR and extraction | Baseline comparison, field extraction, failure handling |
| 4 | Legal rule research and engine | Source matrix, applicability, rule fixtures |
| 5 | Reports, access control and deployment | Exports, permissions, reproducible startup |
| 6 | Test data, evaluation and presentation | Held-out results, feedback record, requirements coverage |

Adjust to actual skills; combine responsibilities if fewer people are building. Non-coding contributions still need specific outputs and technical understanding.

Maintain a feedback log with time, source, exact suggestion, action/decision, owner and verification. Record actual mentor/evaluator feedback; do not manufacture feedback to match a judging criterion. Feedback that would break the time budget receives a documented pilot plan rather than an unsupported claim of implementation.

At each evaluation, briefly state what changed since the last demonstration and show it.

## 9. Evaluation and proof of impact

Aim for an initial 20 distinct product examples with multiple panels: approximately 12 for development and 8 held out by product identity. This is a planning target, not data already collected. If fewer are available, disclose the actual count. The later 50–100-example target is outside this build budget.

Include clean photographs, glare/blur, incomplete panels and varied quantity/price formatting. Add clearly labeled synthetic rule violations for coverage, reported separately from natural examples. Do not infer population-level reliability from this small sample.

Record:

- Correctly extracted values over labeled values, per declaration.
- True and false potential violations, missed reviewed violations, and sample counts.
- Needs-review/abstention rate and number of manual corrections.
- Median and slow-case processing time on named hardware.
- Time to complete a manual checklist/report versus assisted review/report, including capture and correction time.

Use the same checklist and matched cases for the timing comparison. Counterbalance the order where possible to reduce practice effects. Team members acting as inspectors are proxy users, not validated officer field testing.

Do not announce a target such as “95% accuracy” or “10× faster” as a result. Present observed counts and measurements, including failures.

Essential checks: incomplete images never imply absence; wrong-context rules are excluded or unresolved; corrections trigger a new assessment; both exports agree; unauthorized actions are rejected; failed OCR preserves evidence and can be retried.

## 10. Presentation and demonstration

Prepare a six-minute core story that can be shortened or expanded to the allotted slot:

- 0:00–0:40 — Who inspects packages, what the problem statement asks for, and the current supported scope.
- 0:40–2:30 — Photograph/upload a package, extract declarations, click a finding to show its evidence and rule.
- 2:30–3:20 — Correct an OCR error and demonstrate a missing-panel/blur case that requests review.
- 3:20–4:00 — Review, export a PDF and editable report, and reopen the saved inspection.
- 4:00–4:45 — Show held-out results, timing, known errors and the comparison with raw OCR/manual work.
- 4:45–5:20 — Show an actual feedback improvement and summarize team contributions.
- 5:20–6:00 — Explain costs, rule maintenance, deployment and the next pilot milestone.

Keep one unfamiliar package for live testing if it falls within supported scope. Unexpected or unsupported input must receive an honest result. A backup recording is explicitly labeled as a recording and does not replace claims about a live test.

Calibrated measurement, if validated, can replace a portion of the demo. Do not try to fit every screen into the presentation.

## 11. Readiness and sustainability

Prepare a one-page pilot note covering:

- Intended first deployment: a supervised inspection setting, with a small authorized officer group.
- Baseline hardware, model download size, storage per inspection and measured throughput.
- Cost per inspection as an estimate derived from compute time, storage and any paid service; include human review and maintenance rather than claiming self-hosting is free.
- Rule update responsibility: a maintainer adds a sourced version and a domain reviewer verifies applicability before activation.
- Pilot acceptance: field accuracy, review time, officer usability, secure access and report reproducibility.
- Next engineering priorities: validated physical measurement/placement, broader categories, multilingual evaluation, durable job infrastructure and secure shared deployment.

Do not claim government adoption, independent legal approval or production scale without evidence.

## 12. Definition of a successful 36-hour build

- A real supported package completes capture → OCR → extraction → rule checks → review → saved PDF/DOCX.
- Findings open their supporting image evidence and source-backed rule explanation.
- Incomplete evidence remains unresolved; automatic measurement is not invented.
- A reviewer correction is reflected in a new assessment and traceable report.
- Saved inspections can be searched and authorization checks work.
- The team presents measured results, actual feedback improvements and a practical pilot path.
- The presentation clearly identifies assisted, implemented and deferred requirements.

The first implementation step remains legal/category selection and a real-label OCR baseline, followed immediately by an integrated upload-to-finding flow.
