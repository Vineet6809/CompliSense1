# CompliSense evaluation disclosure

This note is intentionally small and reproducible. It records what was
observed on the available label photographs; it is not a claim of production
accuracy or legal compliance.

## Evaluation boundary

- **Build:** CompliSense rule set `demo-2026.09`
- **OCR engine:** RapidOCR ONNX Runtime on CPU
- **Extraction method:** editable, regex-based declaration candidates over OCR lines
- **Sample set:** the three synthetic labels in `backend/data/samples/`, plus the locally available external label photograph when it is manually reviewed
- **Limit:** no held-out, independently labelled benchmark set is included in this prototype

## What to record before the SIH demo

Run the same images on the presentation machine and fill the table from the
actual result. Keep the raw inspection IDs and report versions so a judge can
reproduce the numbers.

| Image | Condition | Fields checked | Correct candidates | Missed/incorrect | Abstained or needs review | Processing time | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `complete-label.png` | Synthetic, high contrast | 8 | _run and record_ | _run and record_ | _run and record_ | _run and record_ | Baseline workflow sample |
| `missing-price-label.png` | Synthetic, intentional missing field | 8 | _run and record_ | _run and record_ | _run and record_ | _run and record_ | Demonstrates potential violation gating |
| `low-contrast-label.png` | Synthetic, degraded contrast | 8 | _run and record_ | _run and record_ | _run and record_ | _run and record_ | Demonstrates conservative review routing |
| External label photograph | Real-looking, manually reviewed | _record visible fields_ | _run and record_ | _run and record_ | _run and record_ | _run and record_ | Do not generalize from one image |

## Reporting language

Use wording such as “On this four-image rehearsal set, the pipeline routed
uncertain evidence to review and extracted the following candidates.” Avoid
phrases such as “98% accurate” unless a larger labelled set and a defined
protocol support that number. The product claim is traceability and safe
abstention, not a new OCR model.
