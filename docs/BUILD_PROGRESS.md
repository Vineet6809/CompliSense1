# Build ledger - plan: `docs/PROJECT_PLAN.md`

## Scope and decisions

- The user authorized a working SIH demonstration with real label scanning and a comprehensive six-member recreation and deployment guide.
- The implementation uses readable React and TypeScript for the browser application, FastAPI and SQLAlchemy for the API, private file storage, SQLite for the local demo, and PostgreSQL as the documented deployment option.
- RapidOCR with ONNX Runtime provides portable local OCR without requiring a separate Tesseract installation on Windows.
- `docs/BUILD_CONTRACT.md` defines the API and UI integration contract. Rule checks consume verified declarations and product context; reports consume immutable assessment snapshots.
- The rule catalogue is intentionally narrow and conservative. The prototype does not claim automatic certification of physical font size, placement, legibility, exemptions, or legal compliance.

## Implemented result

- Session authentication, inspector and reviewer roles, HttpOnly cookies, CSRF checks, login throttling, and audit events.
- Inspection creation, searchable history, multi-image private uploads, real OCR, evidence bounding boxes, editable declaration provenance, panel coverage, and assisted physical checks.
- Explainable pass, potential-violation, needs-review, and not-applicable findings tied to source references.
- Reviewer decisions, immutable assessment history, and frozen PDF and editable DOCX exports.
- Responsive inspector workflow, rule reference, dashboard, report history, synthetic sample labels, and mobile layouts.
- Government-service interface redesign completed: neutral service bar that clearly labels the unofficial prototype, compact officer navigation rail, structured page hierarchy, case-file workflow stages, and responsive mobile navigation.
- Visual verification completed for login, overview, inspection case file, and mobile case-file views; the redesigned shell keeps evidence and declarations readable without document-level overflow.
- MVP review controls completed: cross-view net-quantity reconciliation, explicit applicability and exemption decisions, blur/glare/OCR confidence review signals, and finding-level frozen evidence and rule references in versioned reports.
- Multi-stage production `Dockerfile`, PostgreSQL `compose.yaml`, environment template, and reverse-proxy example.
- SIH judging research, legal-source boundary notes, project plan, and a beginner-friendly recreation guide divided across six team roles.

## Final verification - 21 September 2026

- `python -m pytest backend -q`: **31 passed**, with two upstream deprecation warnings from Starlette/TestClient dependencies.
- `python -m ruff check backend`: **all checks passed**.
- `npm --prefix frontend run build`: TypeScript and Vite production build completed successfully; 1,604 modules transformed, including bundled Noto Sans and Noto Sans Devanagari fonts.
- Live end-to-end browser flow completed on `http://127.0.0.1:8001`: inspector login, image upload, real OCR, corrections, panel confirmation, manual physical checks, PDF/DOCX exports, reviewer login, and accepted decision.
- Browser verification found no console errors and no document-level horizontal overflow at desktop or 375 px mobile width.
- The one-time inspection creation notice is removed from browser history state and does not return after refresh.
- Current accepted assessment `82849c21204d4750aa7696b8a00efbe4` produced a three-page PDF and DOCX. All PDF pages were visually inspected: the declaration table wraps correctly, reviewer notes render, no replacement glyphs appear, and the evidence image is fully framed.
- The DOCX opens through `python-docx`, contains the accepted decision and reviewer notes, and includes one evidence image.
- Docker configuration was reviewed but not executed because Docker is not installed on this workstation.
- The live redesigned UI was smoke-checked on `http://127.0.0.1:8001`; the health endpoint returned HTTP 200, and an existing inspection returned normalized applicability and reconciliation data without a database migration failure.
- Curated visual evidence is available in `output/playwright/government-ui-dashboard.png`, `output/playwright/government-ui-casefile.png`, and `output/playwright/government-ui-casefile-mobile.png`.
- Vercel frontend production deployment is ready at `https://complisense-five.vercel.app`; connect a persistent FastAPI deployment with `VITE_API_BASE_URL` before using sign-in, OCR uploads, or report generation from that URL.
- The final Vercel deployment is `dpl_Ht5KiV3EfwWyCiGSaBU2rJWg3uB7` and is marked `READY`; `/` and `/rules` both return HTTP 200.
- Render deployment is prepared in `render.yaml`; it still needs a Render account with repository access before a real service URL and health response can be verified.

## Demo state

- Live URL: `http://127.0.0.1:8001`
- Inspector: `inspector@demo.local` / `InspectorDemo123!`
- Reviewer: `reviewer@demo.local` / `ReviewerDemo123!`
- Verified inspection: `7b188b6724c04123930f397b973069b1`
- Final browser and report evidence is stored in `output/playwright/`.
