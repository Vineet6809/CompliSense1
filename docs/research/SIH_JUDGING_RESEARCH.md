# SIH judging research and implications for CompliSense

Research date: 16 September 2026.

## Source quality and scope

Two primary sources were downloaded from government domains, their text extracted, and the relevant pages visually checked. General blogs, Scribd rubrics, and institution-specific judging sheets were not used as national SIH scoring rules.

1. **SIH 2026 Guidelines**, official SIH website: https://sih.gov.in/letters/2026/SIH%202026%20Guidelines.pdf
   - PDF page 20, printed page 13: "IDEA SELECTION CRITERIA".
   - PDF page 18, printed page 12: "SHORTLISTED IDEAS ANNOUNCEMENT".
   - Local original: `sources/sih-2026-guidelines.pdf`; extracted text: `sources/sih-2026-guidelines.txt`.
2. **Evaluation Guideline for Smart India Hackathon**, Ministry of Education Innovation Cell evaluator portal: https://siceval.mic.gov.in/assets/img/Evaluation_Guidelines_for_sih2024.pdf
   - The filename and page branding identify SIH 2024.
   - PDF page 1: rounds 1 and 2; PDF page 2: round 3 and final-score calculation.
   - Local original: `sources/sih-2024-evaluation.pdf`; extracted text: `sources/sih-2024-evaluation.txt`.

The 2026 general guidelines provide idea-selection criteria but no round-by-round weights. Searches for a public 2025/2026 national finale scoring rubric did not locate a newer detailed official guide. This does not prove that none exists. The 2024 guide is historical preparation guidance, not a confirmed 2026 scoring scheme. Current organizer instructions and problem-owner feedback take precedence. Internal college hackathons may use their own rubric.

The user's 36-hour constraint is the planning budget; it is not inferred from the 2026 general guidelines.

## Confirmed 2026 idea-selection criteria

The guidelines state:

> Evaluation criteria will include novelty of the idea, complexity, clarity and details in the prescribed format, feasibility, practicability, sustainability, scale of impact, user experience and potential for future work progression.

The same guidelines say 4–5 teams per problem statement may be selected for the finale, while the final decision rests with the problem-statement organization, which is not obligated to declare a winner unless proposals meet its expectations.

Implication: meeting DoCA's stated workflow and requirements is central. Novel features do not substitute for missing required outputs. No official percentage weights for these 2026 selection criteria were found in this source.

## Historical 2024 finale rubric

Each round has five parameters scored from 1–20, for 100 maximum raw marks. Scores are averaged across evaluators and weighted by round.

| Round | Parameters in the official guide | Weight in the 2024 guide |
| --- | --- | --- |
| 1 | Presentation of the solution/idea; innovation; solution approach; technical soundness/feasibility; execution timeline for the hackathon | 20% |
| 2 | Prototype development; improvement based on evaluator/mentor feedback; integration; usability; teamwork, including individual contribution | 30% |
| 3 | Functionality/relevance to the problem statement; performance/final demo; user experience/aesthetics/design/ergonomics; market readiness/impact; implementation plan/future scope | 50% |

The guide's final calculation is `0.20 × round-1 average + 0.30 × round-2 average + 0.50 × round-3 average`.

The round-3 performance/demo parameter explicitly includes effectiveness in real-world scenarios and the clarity, coherence, and persuasiveness of the presentation. "Improvement" in round 2 explicitly concerns feedback from evaluators or mentors. A good final presentation alone therefore does not cover the complete historical rubric.

## Planning interpretations, not official scoring rules

| Research finding | Change to CompliSense planning |
| --- | --- |
| Novelty is evaluated | Demonstrate how linking declaration evidence, applicable rules, uncertainty, and review history improves a basic OCR workflow; do not claim a novel OCR model or industry-first product without evidence |
| Technical soundness and complexity are evaluated | Make panel coverage, extraction errors, unit normalization, and rule applicability visible; unnecessary services do not demonstrate useful technical depth |
| Execution timeline is evaluated | Use explicit integration deadlines and feature cutoffs within the 36-hour budget |
| Prototype progress and integration are evaluated | Achieve upload-to-finding by hour 10 and review-to-export by hour 24 |
| Feedback improvement is evaluated | Keep timestamped feedback, the action taken, and before/after evidence; record actual feedback only |
| Teamwork is evaluated | Assign accountable owners and track actual contributions; do not imply that every student must code |
| Functionality/relevance is evaluated | Preserve minimal secure roles, inspection history, PDF plus editable export, and a clear treatment of font size and placement |
| Performance and impact are evaluated | Report measured extraction quality, false flags, abstentions, review time, and hardware; avoid unsupported accuracy and speed claims |
| UX is evaluated | Prioritize capture guidance, image highlights, correction controls, and readable findings over decorative dashboards |
| Sustainability and future progression are evaluated | Explain rule maintenance, model replacement, deployment cost, legal review, and the next pilot milestone |

Font-size and placement checks remain only partially automated in the proposed 36-hour build. Guided review is a useful workflow, but it must not be described as satisfying full automatic measurement. This remains a competitive gap unless a calibrated demonstration is completed and validated.

## Corrections to earlier advice

- The previous advice was an informed assessment, not verified SIH judging guidance. This research now supplies the source basis.
- Dropping all editable exports and access control would weaken coverage of the actual problem statement. Keep basic DOCX and seeded inspector/reviewer accounts; defer sophisticated administration.
- Font size and placement cannot simply disappear from the demo. Show explicit reviewed/unassessed status, with calibrated automatic measurement as a tightly bounded stretch task.
- A 50–100-product evaluation corpus is a sensible later target, but collecting and annotating it from scratch is not a reasonable default inside this 36-hour build. Use a smaller disclosed pilot set and label the statistical limits.
- No evidence supports a promise that the judges will like this project, a winning probability, or a projected SIH score.

## ATS question and keyword strategy

### Is SIH using an ATS?

No public SIH 2026 source reviewed here describes an Applicant Tracking System (ATS), automated resume-style keyword ranking, or an ATS rejection stage for idea presentations. The official guideline describes a portal submission containing the problem statement, idea title, idea description, and idea presentation PDF. It then says that ideas are evaluated by experts against novelty, complexity, clarity and detail, feasibility, practicability, sustainability, scale of impact, user experience, and future progression. The problem-statement creating organization makes the final selection decision and may select 4–5 teams per problem statement.

This does not prove that the portal performs no technical validation or that a problem owner never uses internal software. It means teams should not optimize around a supposed hidden ATS as though it were an official SIH rule. The PDF should still contain selectable text, exact problem terminology, clear headings, and an unambiguous evidence trail so that both portal extraction and human review work well.

### How to make the submission machine-readable and judge-friendly

Use the exact problem statement ID and title in the metadata and on the first slide. Repeat the core terms naturally in the title, solution sentence, architecture labels, and prototype outcome. Keep important claims as editable text rather than text embedded only in screenshots. Use one term consistently; do not fill the PDF with repeated keywords or invisible text.

Recommended submission title:

> CompliSense: Evidence-backed Legal Metrology inspection for packaged commodities

Recommended opening description:

> CompliSense is an officer-assisted software system for checking compliance of packaged commodities under the Legal Metrology Rules, 2011. It scans multi-view product images and labels, extracts mandatory declarations with confidence and image evidence, applies applicability-aware deterministic rules, reconciles contradictions across package views, and routes uncertain findings to an authorized officer for review and an evidence-backed report.

Use keywords only when the prototype supports them:

`packaged commodities`, `Legal Metrology Rules, 2011`, `mandatory declarations`, `product label inspection`, `multi-view image scanning`, `OCR`, `structured extraction`, `confidence score`, `bounding-box evidence`, `applicability check`, `exemption handling`, `unit normalization`, `deterministic rule engine`, `missing declaration`, `incorrect declaration`, `cross-view contradiction`, `human-in-the-loop review`, `officer-assisted inspection`, `PASS`, `REVIEW REQUIRED`, `NOT APPLICABLE`, `versioned rule catalogue`, `audit trail`, `inspection history`, `evidence-backed report`, `role-based access`, `PDF/DOCX export`, `multilingual labels`, `glare and blur handling`, `readability assessment`, `future rule updates`.

Avoid ATS-style keyword stuffing and avoid claims that a reviewer can disprove: `100% accurate`, `fully autonomous legal decision`, `legally binding`, `automatic prosecution`, `certified measurement from any photograph`, `zero hallucination`, and `AI replaces inspectors`.

### What this means for CompliSense

The idea has a credible shortlist angle, but the novelty is the combination and workflow rather than OCR alone. OCR, image preprocessing, and a rule engine are individually familiar. The stronger differentiator is the chain from package image to extracted field to rule reference to officer review, combined with multi-view contradiction detection, applicability and exemption handling, confidence-based abstention, versioned rules, and an audit trail.

The current deck communicates the core idea but is not yet as shortlist-ready as it can be. Slide 2 is overloaded, Slide 4 lacks project-specific feasibility evidence, and Slide 5 is effectively empty in the extracted text. Before submission, show one complete normal inspection, one uncertain or low-confidence case, and one cross-view contradiction. For each, show the source image, extracted value, confidence, applicable rule, result, and officer action. This evidence is more valuable than adding more platform or business-model keywords.
