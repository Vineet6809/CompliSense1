# Government Officer UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recreate the working CompliSense frontend as a restrained government officer workstation with the alternate project's GoI identity and the current application's functioning evidence-led workflow.

**Architecture:** Keep React Router, existing API calls, data types, and feature components. Replace the shared visual shell and token layer first, then tune page composition and inspection surfaces to the approved design. Use local assets and CSS rather than adding a UI framework.

**Tech Stack:** React 18, TypeScript, Vite, React Router, CSS, Lucide icons, existing FastAPI API.

**Spec:** `.spec-workflow/specs/government-officer-ui-redesign/requirements.md` and `.spec-workflow/specs/government-officer-ui-redesign/design.md`

## Global Constraints

- Preserve existing API endpoints, route paths, authentication, OCR, assessment, reviewer, report, and audit behavior.
- Use the authentic local State Emblem asset and the existing aperture-C CompliSense mark.
- Keep tricolour treatment limited to the Government authority bar and CompliSense mark.
- Use English for operational labels and bilingual Hindi/English only in the GoI authority bar.
- Use blue for application actions; reserve green, amber, red, and grey for finding and review status.
- Do not add marketing heroes, architecture explainers, demo shortcut navigation, heavy charts, or unsupported government-adoption claims.
- Verify at 1440 x 900, 1366 x 768, 768 x 1024, and 375 x 812 with no document-level horizontal overflow.

---

### Task 1: Add approved institutional assets and document the design handoff

**Files:**
- Create: `frontend/public/emblem-of-india.svg`
- Modify: `frontend/index.html`
- Modify: `.gitignore` only if the public asset pattern requires it

**Interfaces:**
- Produces the local State Emblem URL `/emblem-of-india.svg` used by `GovernmentBar`.

- [ ] Copy the authentic State Emblem SVG from `D:\SIH\CompliSense\apps\web\public\emblem-of-india.svg` into `frontend/public/emblem-of-india.svg`.
- [ ] Update the document theme color and title description to match the government-service direction while keeping the product name CompliSense.
- [ ] Confirm the copied asset is included by Vite and does not depend on the alternate project at runtime.

### Task 2: Rebuild the shared government application shell

**Files:**
- Modify: `frontend/src/components/Layout.tsx`
- Modify: `frontend/src/auth.tsx` only if logout/account display needs a typed role label
- Modify: `frontend/src/styles.css`

**Interfaces:**
- `Layout` continues to render `Outlet` and existing navigation routes.
- `Brand` continues to accept `{ light?: boolean }` so `LoginPage` remains compatible.

- [ ] Replace the Command icon brand with the aperture-C mark and split wordmark using the approved three-stroke SVG geometry.
- [ ] Add a `GovernmentBar` component with the local emblem, Hindi/English authority text, Department of Consumer Affairs, rule-set chip, and tricolour bottom rule.
- [ ] Move the authenticated shell below the Government bar and keep the current route-aware breadcrumb and OCR service state.
- [ ] Keep only Overview, Inspections, Rule reference, and New inspection in the rail; remove persistent slogans and demo shortcuts.
- [ ] Keep the officer account and sign-out action at the rail bottom.
- [ ] Implement the mobile navigation drawer without changing route behavior.
- [ ] Add accessible labels, active navigation state, visible focus treatment, and a narrow utility header.

### Task 3: Replace global tokens and component styling

**Files:**
- Modify: `frontend/src/styles.css`
- Modify: `frontend/src/styles-inspection.css`

**Interfaces:**
- Existing class names used by all current pages and components remain valid unless the class is intentionally removed from a deleted demo-only section.

- [ ] Replace the warm editorial green palette with the approved authority navy, neutral page background, white surfaces, service blue, and reserved status tokens.
- [ ] Set the base typography, heading scale, field sizes, table density, radius, border, focus, button, status badge, notice, and responsive tokens.
- [ ] Restyle shared page headings, forms, notices, tables, empty states, filters, rule rows, and footer to the government-service hierarchy.
- [ ] Restyle inspection-specific evidence, declarations, findings, report rows, activity, workflow steps, and context sections without changing their DOM contracts.
- [ ] Remove decorative gradients, oversized serif hero treatment, persistent slogan blocks, and visually competing surfaces.

### Task 4: Recompose the sign-in screen

**Files:**
- Modify: `frontend/src/pages/LoginPage.tsx`
- Modify: `frontend/src/styles.css`

**Interfaces:**
- Continue using `useAuth().login`, `ErrorBanner`, and current form submission behavior.

- [ ] Use the Government bar and centered single-column sign-in surface.
- [ ] Show CompliSense mark, `Officer sign in`, concise scope language, email, password, sign-in action, access guidance, and prototype limitation.
- [ ] Preserve invalid, submitting, service-error, and local-demo credential states.
- [ ] Remove the split-screen marketing story, decorative scan illustration, and team badge from the login workflow.

### Task 5: Recompose dashboard and inspection register

**Files:**
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/pages/InspectionsPage.tsx`
- Modify: `frontend/src/components/Common.tsx`
- Modify: `frontend/src/styles.css`

**Interfaces:**
- Preserve `api.dashboard`, `api.inspections`, `InspectionTable`, `StatusBadge`, and current data types.

- [ ] Use administrative page titles and one primary New inspection action.
- [ ] Convert dashboard metrics into a compact bordered metric band and remove sample blocks and workflow marketing copy from the work queue.
- [ ] Sort or label dashboard records so attention states are easy to find while preserving API order where no attention priority exists.
- [ ] Make the inspection register toolbar, result count, table columns, active filters, loading state, no-result state, and empty state align to the approved register design.
- [ ] Make `InspectionTable` responsive without document-level overflow: desktop table, mobile stacked record rows.

### Task 6: Recompose New inspection as a formal guided form

**Files:**
- Modify: `frontend/src/pages/CreateInspectionPage.tsx`
- Modify: `frontend/src/components/UploadPicker.tsx` only for labels or layout hooks needed by the design
- Modify: `frontend/src/styles.css`

**Interfaces:**
- Preserve `api.create`, `api.upload`, `InspectionInput`, `PendingImage`, and current navigation/error handling.

- [ ] Add the compact five-stage workflow indicator.
- [ ] Group product details and packaging evidence into official-looking form sections with explicit required/optional labels.
- [ ] Turn the existing capture guide into a narrow checklist panel that collapses below the form on mobile.
- [ ] Keep panel assignment, file limits, validation, upload progress, scope acknowledgement, and duplicate-submit protection intact.

### Task 7: Tune the case-file and rule-reference surfaces

**Files:**
- Modify: `frontend/src/pages/InspectionPage.tsx` only where labels/order are needed
- Modify: `frontend/src/components/ContextEditor.tsx`
- Modify: `frontend/src/components/AssessmentPanel.tsx`
- Modify: `frontend/src/components/ReportHistory.tsx`
- Modify: `frontend/src/components/EvidenceViewer.tsx`
- Modify: `frontend/src/components/DeclarationsEditor.tsx`
- Modify: `frontend/src/pages/RulesPage.tsx`
- Modify: `frontend/src/styles-inspection.css`

**Interfaces:**
- Preserve all existing inspection API callbacks, evidence selection, declaration editing, assessment review, report downloads, and audit data.

- [ ] Align the case header, workflow stages, collapsed context row, tabs, evidence/declarations grid, and report/activity sections with the design document.
- [ ] Make evidence/declaration relationships more legible through section headers and stable alignment while retaining OCR boxes and source locate actions.
- [ ] Ensure finding status text, rule code, reason, evidence source, citation, and human action read in that order.
- [ ] Label manual checks as officer-recorded observations and keep the legal limitation visible.
- [ ] Restyle the rule reference scope/limits panel and rule register as an official reference list.

### Task 8: Verify and polish the redesign

**Files:**
- Modify: any frontend files required by verification findings
- Create: `output/playwright/government-ui-dashboard.png`
- Create: `output/playwright/government-ui-register-mobile.png`
- Create: `output/playwright/government-ui-casefile.png`

- [ ] Run `npm.cmd --prefix frontend run build`.
- [ ] Start or reuse the frontend/API service and authenticate with the existing demo account.
- [ ] Capture screenshots at 1440 x 900, 1366 x 768, and 375 x 812 for dashboard, register, new inspection, and case file.
- [ ] Check `document.documentElement.scrollWidth === document.documentElement.clientWidth` on desktop and mobile.
- [ ] Check keyboard focus on navigation, search, form fields, tabs, and primary actions.
- [ ] Check browser console for errors and confirm current backend flows still load.
- [ ] Run `.venv\Scripts\python.exe -m pytest backend -q` and `.venv\Scripts\python.exe -m ruff check backend` to confirm the frontend redesign did not regress the service.

