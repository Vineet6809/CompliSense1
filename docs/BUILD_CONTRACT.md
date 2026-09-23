# Implementation contract

This is the shared integration contract for the current build. The public learning guide will explain it step by step.

## Structure and choices

- `frontend/`: React, TypeScript, Vite, plain CSS, lucide-react, react-router-dom. Responsive government-service inspection workspace using a local Noto Sans-compatible system font stack. No paid services or external font dependency.
- `backend/app/`: FastAPI, SQLAlchemy, SQLite default (Postgres via DATABASE_URL), cookie sessions, private files.
- `backend/app/services/`: OCR, extraction, rules, reports. Prefer portable CPU RapidOCR/ONNX so Windows users do not need a separate Tesseract installer. Real OCR, never fake responses.
- `backend/tests/`: pytest and API integration tests. `frontend/`: browser checks and production build.
- Two roles: `inspector`, `reviewer`; admin CLI creates users. No public signup. Local demo accounts are explicitly opt-in via seed command.
- PDFs with reportlab; DOCX with python-docx. Full reports include images, source references, scope, uncertain checks and reviewer notes.
- Sample labels are clearly synthetic and generated as PNGs for honest testing of real OCR.
- Keep comments useful and functions explicit. Avoid clever abstractions, state libraries and giant files.

## API

All paths below start `/api`. Auth uses HttpOnly cookie, `credentials: include`. Every mutation except login requires `X-CSRF-Token` returned by login/me. JSON errors have `detail` string or FastAPI validation array. Vite proxies `/api` to `http://127.0.0.1:8000`.

Auth:
- `POST /auth/login` JSON `{email,password}` → `{user,csrf_token}`.
- `GET /auth/me` → `{user,csrf_token}`; 401 means sign-in required.
- `POST /auth/logout` → `{message}`.
- User: `{id:number,name:string,email:string,role:'inspector'|'reviewer'}`.

Inspection:
- `GET /inspections?q=&status=` → `InspectionSummary[]`, visible records only.
- `GET /dashboard` → `{total,needs_review,reviewed,potential_violations,recent:InspectionSummary[]}`.
- `POST /inspections` JSON `{product_name,brand?,barcode?,category:'household'|'other',origin:'domestic'|'imported'|'unknown',scope_confirmed:boolean,notes?}` → full inspection.
- `GET /inspections/{id}` → full inspection.
- `PATCH /inspections/{id}` JSON `{version:number,product_name?,brand?,barcode?,origin?,scope_confirmed?,applicability?:{status:'unknown'|'applicable'|'not_applicable',exemption:'none'|'claimed'|'confirmed',reason:string},notes?,coverage_confirmed?,fields?:Record<string,string>,field_notes?:Record<string,string>,manual_checks?:{readability?:string,placement?:string,font_size?:string,notes?:string}}` → full inspection; optimistic-lock 409 on stale version. Corrections after processing recompute a new assessment. Manual check values `unassessed`, `acceptable`, `concern`. Empty field is explicit correction. Field notes store evidence/provenance; corrected fields are marked manual. Applicability and exemptions are evaluated before a missing declaration can become a potential violation.
- `POST /inspections/{id}/images` multipart `file`, `panel` ('front'|'back'|'side'|'other') → full inspection. Max 8 images, 10MB/image, JPEG/PNG/WebP, original private storage. Invalid content is rejected. Adding image invalidates current findings/review, but preserves history.
- `GET /inspections/{id}/images/{image_id}` → image bytes, authenticated.
- `POST /inspections/{id}/analyze` → full inspection (status processing). UI polls GET while processing. Retry allowed after failure. Server processes CPU OCR in background, bounded one-at-a-time. A process restart marks interrupted jobs failed for safe manual retry.
- `POST /inspections/{id}/review` JSON `{version:number,decision:'accepted'|'follow_up',notes:string}` → full inspection. Reviewer only, must have current assessment. Follow-up decision leaves unresolved findings explicit; accepted is acknowledgement of assessment, not legal certification.
- `GET /inspections/{id}/reports/{assessment_id}.pdf` and `.docx` → attachment. Versioned frozen snapshot, previous versions preserved.
- `GET /rules` → `{version,scope,limitations:string[],rules:Rule[]}`.
- `GET /health` → `{status,ocr_available,ocr_engine}`.
- `GET /samples` → `[{name,description,url}]`; `GET /samples/{filename}` public synthetic PNG downloads.

## Response shapes

InspectionSummary = `{id:string,product_name,brand,barcode,category,origin,scope_confirmed,notes,status:'draft'|'processing'|'ready'|'reviewed'|'failed',created_at,updated_at,owner_name,version:number,image_count:number,potential_violations:number,needs_review:number,review_decision:string|null}`.

Full inspection extends summary:
`{coverage_confirmed:boolean,applicability:Applicability,reconciliation:{net_quantity:{status,candidates,normalized?}},images:EvidenceImage[],fields:Record<string,Declaration>,findings:Finding[],assessments:AssessmentSummary[],audit:AuditEvent[],manual_checks:Record<string,string>,processing_error:string|null,processing_seconds:number|null,rule_version:string|null,current_assessment_id:string|null,review_notes:string|null}`.

EvidenceImage = `{id:string,filename:string,panel:string,width:number,height:number,url:string,quality:{warnings:string[],blur_score?:number,reflection_score?:number,ocr_confidence?:number,review_required?:boolean},ocr_text:string,lines:OcrLine[]}`.
OcrLine = `{text:string,confidence:number,box:number[][]}` (pixel quadrilateral in original image).
Declaration = `{value:string,confidence:number,image_id:string|null,box:number[][]|null,source:'ocr'|'manual',note:string,candidates?:DeclarationCandidate[]}`. Cross-view candidate values preserve the front/back/side source instead of collapsing evidence.
Fields: `product_name`, `manufacturer`, `address`, `net_quantity`, `mrp`, `date`, `consumer_care`, `country_of_origin`.
Finding = `{rule_id:string,title:string,status:'pass'|'potential_violation'|'needs_review'|'not_applicable',explanation:string,field:string|null,evidence_image_id:string|null,evidence_box:number[][]|null,evidence?:{image_id,filename,panel,sha256},source_url,provision}`. Each frozen assessment copies the evidence and rule reference next to the finding.
AssessmentSummary = `{id:string,created_at,rule_version,summary:{pass:number,potential_violation:number,needs_review:number,not_applicable:number},review_decision:string|null}`.
AuditEvent = `{id:number,created_at,actor:string,action:string,detail:string}`.
Rule = `{id,title,field,provision,source_url,description}`.

## Core acceptance

Real uploads and OCR work; no hardcoded product findings. Missing/unreadable declarations and unknown applicability never become automatic violations. Low confidence is clearly reviewable. Evidence fields and corrections remain auditable. Inspector sees own records; reviewer sees all and can review. Exports use frozen assessment/review snapshots. UI shows honest empty/loading/failure states, not seeded fake inspection activity.

## Build ownership

Root owns API/models/security/reports/deployment integration and final verification. Frontend agent owns only `frontend/`. Legal research agent owns only `docs/research/LEGAL_RULES_RESEARCH.md` and legal reference files. Later OCR and guide work will use this same contract. No agent should change another agent's files or start subagents.
