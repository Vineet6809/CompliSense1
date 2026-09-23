# CompliSense SIH26034 PPT: ATS-Style Score and Improvement Report

Date: 21 September 2026  
Project: CompliSense  
Team: CypherX  
Problem statement: SIH26034

## Executive assessment

The revised deck is substantially stronger for both machine-readable screening and expert review. It preserves the core CompliSense workflow while making the important content editable text:

> AI extracts evidence. Deterministic rules evaluate it. An officer verifies the result.

SIH has not published an ATS system or an ATS scoring formula for the 2026 idea-submission process. The official SIH 2026 guideline describes portal submission of an idea title, idea description, and presentation PDF, followed by expert evaluation. The published criteria are novelty, complexity, clarity and detail, feasibility, practicability, sustainability, scale of impact, user experience, and future progression. The problem-statement creating organization makes the final selection decision.

Therefore, the scores in this report are a transparent simulation, not an official SIH prediction. They measure how well the PDF exposes relevant terms, problem alignment, technical credibility, feasibility, impact, and evidence to a hypothetical text-ranking system and to a human reviewer.

## Score estimate

### Original deck

Estimated ATS-style score: **70/100**, with a practical range of **65–75**.

The original deck had strong problem and technical keywords, but the machine-readable score was reduced by three weaknesses:

1. Slide 4 was mainly a generic feasibility graphic rather than project-specific risk evidence.
2. Slide 5 contained a large infographic whose important text was not available as editable slide text. XML extraction returned almost only the title.
3. The deck did not clearly separate implemented features, assisted review, and future scope.

### Revised deck

Estimated ATS-style score: **86/100**, with a practical range of **82–90**.

This estimate assumes a hypothetical screen that rewards exact problem alignment, relevant terminology, visible technical detail, feasibility controls, user impact, and future progression. It does not assume that SIH actually uses such a system.

| Criterion | Weight | Original | Revised | Reason for revised score |
| --- | ---: | ---: | ---: | --- |
| Exact problem-statement match | 20 | 18 | 20 | SIH26034 and the official problem wording are prominent on Slide 1 and repeated in the footer. |
| Domain relevance | 20 | 18 | 19 | The revised deck uses packaged commodities, Legal Metrology Rules, mandatory declarations, label inspection, and officer workflow consistently. |
| Technical solution specificity | 20 | 15 | 18 | The revised architecture exposes extraction, confidence, evidence boxes, applicability, versioned rules, contradiction checks, and report output. |
| Feasibility and risk control | 15 | 7 | 13 | Slide 4 now uses a risk-to-prototype-treatment table and clearly states the implementation boundary. |
| Impact and user value | 10 | 2 | 8 | Slide 5 now contains editable outcomes for officers, regulators, manufacturers, sellers, and consumers. |
| Sustainability and future progression | 5 | 3 | 5 | Versioned rules, supervised pilot, broader coverage, and replaceable models are explicit. |
| PDF structure and text accessibility | 10 | 5 | 9 | Critical content is native slide text; only the supplied prototype screenshot remains an image. |
| **Total** | **100** | **68–70** | **86** | The final number is an estimate, not an SIH score. |

## What changed in the revised deck

### Slide 1: Problem identity and solution position

The revised first slide keeps the exact problem ID `SIH26034` and the official problem title. It adds a concise solution description that contains the key searchable concepts: officer-assisted inspection, package labels, image evidence, and rule-based review.

The slide also makes the decision boundary memorable:

`AI extracts evidence` → `Rules evaluate` → `Officer verifies` → `Report preserves the trail`

Required submission action: replace any placeholder team metadata with the actual SIH team ID before uploading. The revised deck intentionally does not invent a team ID.

### Slide 2: Problem, users, and proposed solution

The original slide repeated the same ideas in several sections and had visible crowding. The revised slide has three purposes:

- It states the inspection problem in plain language.
- It shows a five-stage flow: capture, extract, apply, review, and report.
- It explains the distinctiveness through evidence-linked findings, cross-view contradiction checks, and human review for uncertainty.

This is the best location for terms such as `multi-view package scanning`, `structured declaration extraction`, `confidence`, `evidence boxes`, `applicability`, `exemptions`, `contradiction`, and `human-in-the-loop review`.

### Slide 3: Technical architecture and decision boundary

The revised architecture is deliberately expressed as a data path:

`Images + product context` → `OCR/VLM fields + confidence + boxes` → `applicability and exemptions` → `versioned deterministic checks` → `PASS / REVIEW REQUIRED / NOT APPLICABLE`

The slide includes a worked contradiction example:

- Front label: net quantity 1 kg
- Back label: net quantity 900 g
- Result: `REVIEW REQUIRED`
- Evidence: two image boxes and confidence for each value

This example is stronger than listing more technology names because it demonstrates technical complexity, user value, and safe handling of uncertainty in one scenario.

The build boundary is explicit. Image upload, extraction, evidence highlighting, applicability-aware checks, inspection history, and report export are presented as the working path. Physical font-size measurement, calibrated millimetre measurement, live registry integrations, and automatic statutory action are marked assisted or future scope.

### Slide 4: Feasibility, risk control, and implementation

The original generic feasibility graphic was replaced with a project-specific table:

| Risk | Prototype treatment |
| --- | --- |
| Glare, blur, curved labels | Image-quality warning, confidence score, recapture request |
| OCR extraction error | Evidence box, confidence display, officer correction, audit history |
| Missing package panel | Coverage confirmation before a missing-field finding |
| Different products and exemptions | Applicability gate before mandatory-field evaluation |
| Conflicting package views | Cross-view contradiction flag and review queue |
| Changing regulations | Versioned rule catalogue and rule version in every report |

The right-hand status panel tells the reviewer what the prototype can demonstrate now and what is assisted or future scope. This directly supports feasibility, practicability, sustainability, and future progression.

### Slide 5: Impact, adoption, and future progression

The original slide had useful visual content, but most of its important claims were inside an image and it gave too much emphasis to hypothetical revenue streams. The revised slide converts the content into editable text and focuses on outcomes relevant to the problem owner:

- Field officers: faster evidence capture, a clear review queue, and reports linked to source images and rule versions.
- Controllers and regulators: searchable history, consistent rule application, and visibility into repeated issues.
- Manufacturers and sellers: earlier label checks before printing or distribution.
- Consumers: clearer declared information and stronger traceability.

The business-model section is replaced by a defensible adoption path:

1. Prototype validation with disclosed product categories, languages, sample size, errors, and unresolved cases.
2. Supervised field pilot with domain experts and recorded feedback improvements.
3. Broader rule, product, language, and integration coverage.

This is more relevant to SIH selection than unsupported market-size, revenue, or national-deployment claims.

### Slide 6: Prototype evidence and official references

The supplied prototype image is retained because it shows the intended product sequence. It is labelled as:

`Capture` → `Evidence review` → `Officer-assisted report`

The editable text beside it exposes the evidence visible in the prototype: multi-view capture, extracted declaration fields, source image evidence, deterministic results, human review status, and report download.

The slide keeps official source references and includes the limitation:

> Prototype assists inspection; final statutory action remains with the authorized officer.

Every amendment number, date, and URL should be verified against the current official notification before submission. The deck should not rely on a NotebookLM citation unless the underlying official source has been checked.

## Keyword coverage

The revised deck uses the following terms because they describe the proposed workflow:

`SIH26034`, `packaged commodities`, `Legal Metrology Rules, 2011`, `mandatory declarations`, `product label inspection`, `multi-view image scanning`, `OCR`, `VLM`, `structured declaration extraction`, `confidence score`, `bounding-box evidence`, `applicability check`, `exemption handling`, `unit normalization`, `deterministic rule engine`, `missing declaration`, `incorrect declaration`, `cross-view contradiction`, `human-in-the-loop review`, `officer-assisted inspection`, `PASS`, `REVIEW REQUIRED`, `NOT APPLICABLE`, `versioned rule catalogue`, `audit trail`, `inspection history`, `evidence-backed report`, `role-based access`, `PDF/DOCX report export`, `multilingual labels`, `glare and blur handling`, `readability assessment`, `supervised field pilot`, and `future rule updates`.

These terms are distributed through meaningful headings and explanations. They are not inserted as invisible text or repeated keyword blocks.

## Claims deliberately avoided

The revised deck avoids claims that are difficult to defend or may create legal and technical concerns:

- `100% accurate`
- `fully autonomous legal decision`
- `legally binding`
- `automatic prosecution`
- `certified measurement from any photograph`
- `zero hallucination`
- `AI replaces inspectors`
- unsupported market size, revenue, or nationwide deployment figures

The deck presents CompliSense as officer-assisted decision support. That framing is more credible for Legal Metrology and better aligned with the evidence available in the project.

## Validation performed

The revised file was exported as a new PowerPoint presentation so the original deck remains unchanged.

- Six slides were generated.
- The presentation package integrity check passed with zero findings.
- The layout validation check passed with zero findings and zero warnings.
- The deck was imported again with the presentation runtime successfully.
- All six slides were rendered to PNG and visually inspected.
- The final rendered slides have no detected clipping or overlap in the repaired areas.
- Critical content on Slides 1–5 is editable slide text; the supplied UI prototype remains an image used as product evidence.

The validation receipt is stored at:

`D:\SIH\CompliSense1\.codex-ppt-build\CompliSense_SIH26034_Improved_v2.validation.json`

## Remaining limitations before SIH submission

The revised deck is optimized for selection, but it cannot manufacture evidence that the project does not yet have. Before submission, add measured results if available:

- Number of products tested
- Product categories
- Languages and scripts
- Image conditions
- Field extraction accuracy
- False-positive and false-negative observations
- Abstention or review rate
- Average officer review time
- Hardware and deployment assumptions

Do not invent these values. A small disclosed pilot is stronger than an unsupported benchmark.

The current screenshots also show sample or synthetic product data. Label demonstrations clearly as sample data unless the team has permission and evidence to present them as real field results.

## Final recommendation

Use the revised deck as the shortlist submission base. Before upload, complete the actual team ID, confirm the problem-statement organization, verify every legal amendment date and URL, and replace any sample claim with a measured result or a clearly labelled prototype limitation.

The strongest spoken explanation is:

> CompliSense does not ask an AI model to make a legal decision. It extracts declarations from package images, links each field to evidence, applies the applicable versioned rules, and sends uncertainty to the authorized officer for review.

That sentence makes the problem alignment, technical boundary, safety of the workflow, and practical value clear in one explanation.
