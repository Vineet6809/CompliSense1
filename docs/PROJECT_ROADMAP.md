# CompliSense — Project Plan

Problem statement: SIH 26034, Department of Consumer Affairs.
Prepared: 16 September 2026.
Status: Archived initial proposal, retained as a broader future roadmap. The revised PROJECT_PLAN.md controls the 36-hour SIH milestone. Features and data targets here are not all commitments for that milestone.

## 1. Goal and planning assumptions

Build a mobile-friendly inspection application that turns photographs of packaged commodity labels into evidence-linked assessments under the applicable Legal Metrology (Packaged Commodities) Rules, 2011 and amendments.

The user confirmed the initial milestone: a working SIH demonstration with real label scanning. Team size, deadline, hosting budget, and availability of representative product photographs are not yet specified. The sequence below is deliverable-based rather than a delivery-time promise.

The product supports inspection and human review. It must distinguish an automated finding from an officer's reviewed decision. An assessment covers only the selected rules and supplied evidence, not every aspect of a product's legal compliance.

## 2. Approach options

| Approach | Strength | Trade-off |
| --- | --- | --- |
| OCR + deterministic rules + human review — recommended | Explainable findings, repeatable checks, measurable extraction quality | Requires a carefully researched rule catalogue and handling uncertain evidence |
| Vision-language model as the main checker | Quick initial prototype and flexible label interpretation | Can invent values or legal reasoning; harder to reproduce and audit |
| Native mobile app with on-device analysis | Strong offline capture potential | More device testing, model packaging, and engineering before the inspection flow works |

Start with the first approach as a responsive web app. If a vision-language model is added later, use it only to suggest extracted fields with supporting image evidence; deterministic rules and reviewers still control findings.

## 3. First complete user journey

1. An inspector signs in and creates an inspection.
2. The inspector records product category, domestic/imported status, inspection date, and available package measurements. Unknown information remains explicitly unknown.
3. The inspector uploads or photographs the front, back, and other declaration-bearing panels. The app records which panels are available.
4. Image checks identify blur, glare, rotation, and insufficient resolution and request recapture where needed.
5. OCR extracts words and coordinates. Field extraction proposes declaration values without overwriting the original text.
6. The inspector compares extracted values with highlighted image regions and corrects mistakes. Every correction is recorded.
7. The engine evaluates the applicable, versioned rules and displays evidence, explanations, and source references.
8. A reviewer resolves uncertain findings and records a decision with reasons.
9. The application saves a report snapshot and exports PDF and editable DOCX. The inspection becomes searchable in the repository and dashboard.

## 4. Scope

### First working demonstration

- Authentication and server-enforced inspector, reviewer, and administrator roles.
- Multiple photographs per inspection, with camera capture where the browser supports it and an upload fallback.
- Image quality feedback, OCR, declaration extraction, and manual correction.
- A researched subset of rules for a clearly documented package category and inspection context.
- Checks for candidate declarations such as manufacturer/packer/importer details, product identity, net quantity, retail price, date declarations, and consumer-care details, subject to verified applicability.
- Evidence highlights and per-rule results with legal source references.
- A review queue, reviewed report snapshots, PDF/DOCX exports, and supporting photographs.
- Product/inspection history, search, filters, and dashboard summaries.
- Readability assessment and a controlled font-measurement demonstration using known dimensions or a reference scale.

### Expansion after the core flow works

- Broader categories and exceptions, imported-product scenarios, and additional declaration types after legal validation.
- English/Hindi support as an explicit evaluation track; enable each language only after representative OCR testing. Expand to further scripts based on results.
- Product-listing text and screenshot analysis using a separate e-commerce applicability profile. Do not assume physical-package obligations and online-display obligations are identical.
- More robust measurements for perspective, curved surfaces, panel identification, and placement checks.
- Batch inspection and additional analytics.

### Deferred beyond the first demonstration

- Native Android/iOS apps, offline synchronization, and large-scale marketplace crawling.
- Automatic penalties, notices, or other enforcement actions.
- Custom OCR model training before a baseline benchmark demonstrates a need.

## 5. Rules and evidence model

Before implementing legal checks, research the official rules, amendments, effective dates, and relevant exemptions. The source link supplied with the problem statement is a legal-reference starting point, not an annotated image dataset:

https://consumeraffairs.gov.in/pages/legal-metrology-act

No current legal thresholds, amendment completeness, or exact rule citations have been verified during this planning step. Avoid hardcoding remembered requirements.

Maintain a rule matrix with:

- Stable rule ID and human-readable name.
- Official document, provision, page, source URL, and retained source snapshot/hash.
- Effective dates and rule-set version.
- Product/context applicability and exceptions.
- Required evidence, validation method, and whether automatic evaluation is supported.
- Explanation templates and reviewed passing, failing, and uncertain examples.

Every rule returns one of four results:

| Result | Meaning |
| --- | --- |
| Pass | Supplied evidence supports the selected check |
| Potential violation | Sufficient evidence supports a specific rule failure; still subject to review |
| Needs review | Evidence, extraction, measurement, or applicability is uncertain |
| Not applicable | A recorded applicability condition excludes the check |

Do not treat an empty OCR result as proof of a missing declaration. Missing-declaration findings require sufficient readable panel coverage. Unsupported rules and uncertain applicability remain visible as needs-review results, not silent passes.

Keep field confidence, rule outcome, inspection workflow state, and reviewer decision separate. Dashboard percentages must expose their denominator and unresolved checks; avoid an unexplained overall compliance score.

## 6. Readability, font size, and placement

Readability checks can flag blur, glare, low contrast, small pixel height, and poor OCR agreement. These are image-quality observations, not direct proof of a physical lettering-size violation.

Physical font measurement requires a known scale, adequate image resolution, and suitable geometry. The first demonstration should use a flat panel photographed with a reference scale or known panel dimensions. Estimate physical character dimensions after perspective correction, record measurement uncertainty, and compare only against a verified applicable requirement. A borderline or uncalibrated measurement returns needs review.

Placement evaluation needs identified package panels, dimensions where required, and the appropriate rule context. Start with guided panel tagging and reviewer assistance. Do not claim robust automatic placement verification for arbitrary curved packaging in the first release.

The software can flag inconsistent or suspicious declaration text. Verifying whether a printed address, quantity, or claim is factually true may require external evidence or physical inspection.

## 7. Proposed architecture

```text
React web application
        |
        v
FastAPI application -------- PostgreSQL
        |                   inspections, rules, reviews, audit trail
        |
        +------------------ Private image/report storage
        |
        v
Redis job queue --> Python worker
                   quality checks --> OCR --> field extraction
                                             --> rule evaluation
                                             --> report generation
```

| Component | Proposed technology and reason |
| --- | --- |
| Web interface | React, TypeScript, Vite, Tailwind CSS; suitable for a responsive authenticated application |
| API | Python FastAPI and Pydantic; shared language with OCR and image-processing code |
| OCR and geometry | Benchmark PaddleOCR and Tesseract; use OpenCV for preprocessing and measurement |
| Persistence | PostgreSQL with SQLAlchemy and Alembic migrations |
| Background work | Redis and RQ; keep OCR and document generation outside web requests |
| File storage | Private local storage for development; S3-compatible private object storage for hosting |
| Reports | HTML-to-PDF renderer and python-docx, generated from the same frozen report data |
| Authentication | Established authentication library with secure sessions, password hashing, and server-side role checks |
| Deployment | Docker Compose for a reproducible local demo; container hosting with HTTPS for a pilot |

Keep this as one backend application plus a worker, with modules for inspections, extraction, rules, review, reports, and identity. Avoid microservices for the first release.

Processing jobs have queued, running, succeeded, and failed states, bounded retries, and idempotency keys. Failures preserve uploaded evidence and permit retry without duplicating findings. Record OCR, extraction, and rule-set versions for reproducibility.

## 8. Main screens and records

Screens: sign-in, dashboard, new inspection/capture, processing status, extraction review with image highlights, findings/reviewer decision, inspection history, report details, and rule/user administration.

Core records:

- User and role assignment.
- Product and its inspection history; barcodes are optional identifiers, not proof of compliance.
- Inspection with context, captured panel coverage, workflow state, and timestamps.
- Evidence image with original file hash, panel label, dimensions, and derived-image references.
- OCR run, text spans, coordinates, language, and extraction version.
- Declaration candidate and correction history linked to source text/image regions.
- Rule-set version, rule definition, and applicability conditions.
- Assessment run and findings tied to the exact evidence and rule version used.
- Review decision with reviewer identity and rationale.
- Frozen report snapshot, generated files, and append-only audit events.

Reassessment creates a new version. Changing a rule or correcting a field must not silently change an already issued report. Edited DOCX exports are external copies and do not modify the recorded assessment.

## 9. Build sequence and acceptance gates

| Phase | Deliverable | Exit condition |
| --- | --- | --- |
| 1. Evidence and legal groundwork | Scope one product category; assemble rule matrix and annotated photo set; compare OCR candidates | Every planned automatic rule has an official source and applicability description; baseline OCR results are recorded |
| 2. Capture and persistence | Application shell, authentication, roles, inspection creation, private uploads, job status | An inspector can capture multiple panels, reopen an inspection, and cannot access unauthorized evidence |
| 3. Extraction and review | OCR worker, declaration schema, evidence highlights, quality feedback, corrections | Real labels produce editable candidates with image coordinates; uncertain/unreadable values are visibly unresolved |
| 4. Compliance engine | Versioned rule evaluation, applicability checks, evidence-linked findings | Reviewed fixtures cover pass, potential violation, needs review, and not applicable; insufficient images never imply a missing declaration |
| 5. Review and reporting | Reviewer decisions, immutable assessment snapshots, PDF/DOCX | Both exports match the same snapshot and include evidence, sources, unresolved checks, scope, and reviewer status |
| 6. Repository and dashboard | Search, filters, product history, aggregate views | Dashboard counts match stored inspection states and exclude unauthorized records |
| 7. Measurement and demonstration | Calibrated flat-panel measurement, representative end-to-end scenarios, deployment guide | Uncalibrated input produces needs review; clean, violating, and insufficient-evidence scenarios work end to end |

Build the first complete upload-to-report flow before widening categories or adding advanced automation. Prepare detailed implementation tasks for each phase once scope and stack are agreed.

## 10. Evaluation and demonstration data

Collect an initial target of 50–100 product examples with multiple panels and permission to use the photographs. This is a starting evaluation set, not enough to establish production reliability. Annotate declaration values, source boxes, category/context, panel coverage, and reviewed findings. Include glare, blur, curved packs, missing panels, varied price/quantity formatting, and language variation.

Split evaluation by product/package identity rather than photograph so images of the same package do not leak across development and held-out sets. Clearly label synthetic violations and evaluate them separately from naturally occurring examples.

Measure field extraction accuracy per declaration and language, potential-violation precision/recall against reviewed examples, abstention/needs-review rate, correction effort, and end-to-end latency on named hardware. Choose model confidence thresholds using the development set; publish held-out results and sample counts rather than claiming an arbitrary accuracy percentage.

Required automated checks include rule boundary cases, applicability/exemptions, uncertain evidence, unit normalization, immutable report versions, object-level authorization, job retry behavior, and export consistency. Include a browser-level capture-to-review-to-report test.

The final demo should show: a package passing the implemented checks, a package with a supported potential violation, and an incomplete or unreadable package that correctly requests review. Demonstrate a reviewer correction and its audit history.

## 11. Security and operational essentials

Enforce role and record permissions at the API and download layers. Validate file content, file size, image dimensions, and file type. Use private storage and authenticated downloads or short-lived signed links. Isolate OCR/document processing, restrict report-renderer access to arbitrary URLs, and avoid running uploaded content.

Keep secrets outside source control. Record administrative rule changes and review actions. Provide backup/restore instructions, configurable retention, and useful job-error logs without exposing label contents unnecessarily. Confirm hosting requirements, data residency, and retention policy before an enforcement pilot.

## 12. Decisions that refine the next plan

The milestone is confirmed as a working SIH demonstration with real label scanning. The remaining open inputs are team size/deadline, available compute/hosting budget, and sample-label availability. Recommended defaults are local reproducible deployment, baseline OCR without paid-model dependency, and one well-evaluated category before expansion.

The next concrete deliverable is the first category's requirements and rule matrix, followed by implementation tasks for the upload/extraction/review flow.
