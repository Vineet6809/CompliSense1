# CompliSense

CompliSense is a working Smart India Hackathon prototype for inspecting packaged-product labels. An inspector uploads real label photographs, runs local OCR, verifies extracted declarations, reviews explainable rule findings, and exports a frozen PDF or editable DOCX report. A reviewer can then record an accepted or follow-up decision.

The prototype is deliberately conservative: unreadable or incomplete evidence becomes `needs_review`; it does not automatically become a legal violation. The active `demo-2026.09` rules cover a small set of declaration-presence checks for ordinary household packaged commodities and are not legal certification.

## What works

- Real local OCR with RapidOCR and ONNX Runtime
- Multi-panel JPEG, PNG, and WebP evidence uploads
- Evidence-linked extracted declarations and manual corrections
- Multi-view reconciliation for conflicting front/back quantity declarations
- Applicability and exemption recording before a missing declaration can become a potential violation
- Confidence-based review signals for blur, glare, low OCR confidence, and incomplete evidence
- Pass, potential violation, needs review, and not-applicable outcomes
- Inspector and reviewer roles with HttpOnly sessions and CSRF protection
- Searchable inspection history, audit trail, and immutable assessment versions
- PDF and editable DOCX reports generated from frozen snapshots, with assessment versions and finding-level evidence/rule references
- SQLite for the simplest local demo and PostgreSQL for deployment
- Synthetic sample labels for a repeatable demo

## Quick start on Windows

Prerequisites: Python 3.12, Node.js 20 or newer, and PowerShell.

```powershell
cd D:\SIH\CompliSense1

py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-dev.txt

npm.cmd --prefix frontend install
npm.cmd --prefix frontend run build

cd backend
..\.venv\Scripts\python.exe -m app.cli seed-demo
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>.

Local demonstration accounts:

| Role | Email | Password |
| --- | --- | --- |
| Inspector | `inspector@demo.local` | `InspectorDemo123!` |
| Reviewer | `reviewer@demo.local` | `ReviewerDemo123!` |

These predictable accounts are only for a local demonstration. Create real accounts with the CLI before any shared deployment.

```powershell
cd backend
..\.venv\Scripts\python.exe -m app.cli create-user --email officer@example.in --name "Inspection Officer" --role inspector
```

## Development mode

Run the API from `backend/`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, run Vite from the repository root:

```powershell
npm.cmd --prefix frontend run dev
```

Open <http://127.0.0.1:5173>. Vite proxies `/api` to FastAPI.

## Demonstration flow

1. Sign in as the inspector.
2. Select **New inspection** and enter a product name.
3. Confirm the supported scope and upload a label image, or download a synthetic sample from the form.
4. Open the inspection, confirm relevant panel coverage, and run analysis.
5. Compare OCR declarations with the highlighted evidence. Correct any field that needs it.
6. Review findings and record the assisted readability, placement, and type-size checks.
7. Download the PDF or DOCX from **Reports**.
8. Sign out, sign in as the reviewer, open the same inspection, and record a decision.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest backend -q
.\.venv\Scripts\python.exe -m ruff check backend
npm.cmd --prefix frontend run build
```

## Docker deployment

Copy `.env.production.example` to `.env`, replace every placeholder, then run:

```powershell
docker compose up --build -d
docker compose exec app python -m app.cli create-user --email officer@example.in --name "Inspection Officer" --role inspector
docker compose exec app python -m app.cli create-user --email reviewer@example.in --name "Review Officer" --role reviewer
```

The application is exposed on port `8000`. Put it behind HTTPS before setting `COOKIE_SECURE=true`; see [the deployment chapter](docs/RECREATE_FROM_SCRATCH.md#production-deployment).

## Free hosted deployment

Use the [complete free setup guide](docs/FREE_DEPLOYMENT_GUIDE.md) for GitHub, Render, initial accounts, health monitoring, backups, and troubleshooting.

The root `render.yaml` provisions a **free Docker web service** and **free PostgreSQL database** in Singapore. The Docker service serves React and `/api` together, so use its single HTTPS URL for sign-in, uploads, OCR, and reports. A separate Vercel deployment is optional; direct cross-site API configuration is not sufficient for the current cookie and private-file flows.

`EVIDENCE_IN_DATABASE=true` preserves original and normalized photos in PostgreSQL, allowing local files and reports to be recreated after a free service restarts. No paid disk is required. Bootstrap account hashes are supplied through secret environment variables because free Render services have no interactive shell.

**Free-tier limits:** the web service sleeps when idle, has limited memory, and is subject to monthly quotas. The free PostgreSQL database expires after 30 days and has 1 GB of storage. The database created for this setup expires on **23 October 2026**. Back up or migrate before that date. An uptime monitor does not guarantee uninterrupted operation or extend database lifetime.

## Project map

| Path | Purpose |
| --- | --- |
| `frontend/src/` | React screens, reusable components, API client, and responsive styling |
| `backend/app/routers/` | HTTP endpoints and role checks |
| `backend/app/services/` | OCR, extraction, rules, image handling, reports, and samples |
| `backend/tests/` | Security, API, extraction, rules, and report tests |
| `docs/PROJECT_PLAN.md` | 36-hour SIH plan aligned to official judging material |
| `docs/research/SIH_JUDGING_RESEARCH.md` | Judging-source research and judge-facing implications |
| `docs/RECREATE_FROM_SCRATCH.md` | Beginner-friendly build and six-member team guide |
| `docs/research/LEGAL_RULES_RESEARCH.md` | Rule-source map and legal verification boundary |

## Important limitations

- A `pass` only means the supplied evidence supports the implemented check.
- OCR confidence is not a probability of legal correctness.
- Font size, physical placement, legibility, exemptions, and factual truth still require calibrated measurement or expert review.
- The demo database schema is created automatically. A pilot or production system should add versioned database migrations, backups, monitoring, and a formally approved rule catalogue.
