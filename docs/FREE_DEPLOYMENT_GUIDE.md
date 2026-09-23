# CompliSense: complete free deployment guide

This guide deploys the React interface and FastAPI/OCR backend together on **one free Render web service**, with **free Render PostgreSQL** and an **UptimeRobot free monitor**. No paid disk, paid web instance, or paid monitoring subscription is required.

**Current setup status:** the private GitHub repository and free PostgreSQL database have been created. Render, GitHub, and UptimeRobot connections are active. Public web-service creation is waiting for Render's GitHub integration to receive access to `Vineet6809/CompliSense1`; Render currently rejects the repository as unfetchable. The CompliSense uptime monitor will be created after the actual public health URL exists. The complete app has passed a local login → real OCR → PDF/DOCX smoke test at `http://127.0.0.1:8011`.

## 1. Understand the free limits

| Component | Configuration | Limit to plan around |
| --- | --- | --- |
| GitHub | Private source repository | Render needs permission to read it |
| Render web | Docker, Free, Singapore | Sleeps after 15 minutes without traffic; cold start takes about a minute; limited memory and 750 free instance hours per workspace/month |
| Render PostgreSQL | Free, PostgreSQL 16, Singapore | 1 GB; expires 30 days after creation; no managed backups |
| Evidence | `EVIDENCE_IN_DATABASE=true` | Original and normalized photos count toward the 1 GB database limit |
| UptimeRobot | Free HTTP monitor | Five-minute checks supported by the connected account; monitoring is not an uptime guarantee |

**The database created for this setup expires on 23 October 2026. Export or migrate before that date.** The free service may restart at any time. Monitoring does not prevent database expiry, memory failures, or platform maintenance. Keep a working local demo for the presentation.

Do not select a paid plan or enable billable add-ons. Render can charge usage overages on accounts with a payment method; review Billing and set available spending controls to zero. Without a payment method, exhausted free bandwidth/build allowances can suspend service/builds instead. Check your account's current limits in the dashboard.

## 2. Accounts and authorization

1. Sign into [GitHub](https://github.com), [Render](https://dashboard.render.com), and [UptimeRobot](https://dashboard.uptimerobot.com).
2. Authorize the connections supplied in this Codex task. API keys belong only in the secure connection forms.
3. In Render's Git provider connection, grant access to the private repository **Vineet6809/CompliSense1**. A Render API connection and permission to clone GitHub code are separate permissions.
4. Use the Free instance selection throughout. If a screen requires a paid upgrade, stop that flow.

## 3. Prepare the repository

The application source is at [Vineet6809/CompliSense1](https://github.com/Vineet6809/CompliSense1).

Required deployment files:

- `Dockerfile`: builds React and runs FastAPI as a non-root user.
- `render.yaml`: reproducible free web/database configuration.
- `backend/requirements.txt` and `frontend/package-lock.json`: dependencies.
- `.dockerignore` and `.gitignore`: exclude local credentials, data, environments, and generated output.

Never upload `.env`, `.env.local`, `.work/`, `backend/data/`, database backups, or deployment login credentials.

For a new local checkout:

```powershell
git clone https://github.com/Vineet6809/CompliSense1.git
cd CompliSense1
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-dev.txt
npm.cmd --prefix frontend ci
npm.cmd --prefix frontend run build
.\.venv\Scripts\python.exe -m pytest backend -q
```

## 4. Generate private sign-in accounts

The free Render service has no Shell tab/SSH access. Initial accounts are therefore created once at startup from secret password hashes.

```powershell
.\.venv\Scripts\python.exe deploy\create_bootstrap_credentials.py
```

This generates two local files:

- `.work/deployment/login-credentials.txt`: inspector and reviewer emails and random passwords, for your use.
- `.work/deployment/bootstrap-env.json`: four Render environment variables containing emails and salted password hashes.

Both are Git-ignored. Open them locally; do not paste their contents into a chat, commit, or screenshot. The helper refuses to overwrite existing credentials. Optional `--inspector-email` and `--reviewer-email` arguments select your own email identifiers; the app does not send email or require mailbox verification.

The bootstrap only creates missing users. It never resets an existing password on restart. After both accounts work, remove the four bootstrap variables from Render; the accounts remain in PostgreSQL. Retain the private login file securely.

## 5. Create the free database

If the task has already created `complisense-db`, reuse it. Do not create duplicates.

1. Render → **New → Postgres**.
2. Name: `complisense-db`.
3. Database and user: `complisense`.
4. Region: **Singapore**. PostgreSQL: **16**.
5. Instance: **Free**. Leave high availability and storage autoscaling disabled.
6. Restrict external network access; the application uses the internal database URL in the same region.
7. Wait for **Available**, then obtain the **Internal Database URL** from the database's connection settings.
8. Record the expiration date immediately. Never store that URL in Git or public documentation.

The current task's database is visible in the [Render database dashboard](https://dashboard.render.com/d/dpg-dapjg80473hc73bucua0-a).

## 6. Create the free web service

If `complisense` already exists from this task, update that service rather than creating another.

1. Render → **New → Web Service**.
2. Connect the private GitHub repository `Vineet6809/CompliSense1`.
3. Branch: `main`. Root directory: leave blank.
4. Runtime: **Docker**.
5. Dockerfile path: `./Dockerfile`. Docker context: `.`.
6. Region: **Singapore**. Instance: **Free**.
7. Add the environment variables below.
8. Health check path: `/api/health`.
9. Leave the Docker command empty: the Dockerfile already starts Uvicorn on `0.0.0.0` and Render's `PORT`.
10. Do not attach a disk or select a paid build instance. Deploy and watch the build log, then runtime log.

| Variable | Value |
| --- | --- |
| `DATA_DIR` | `/data` (temporary local cache) |
| `DATABASE_URL` | Internal Database URL from step 5 |
| `EVIDENCE_IN_DATABASE` | `true` |
| `COOKIE_SECURE` | `true` |
| `ALLOWED_ORIGINS` | The actual HTTPS Render application origin, without trailing slash |
| `BOOTSTRAP_INSPECTOR_EMAIL` | Generated value from `bootstrap-env.json` |
| `BOOTSTRAP_INSPECTOR_PASSWORD_HASH` | Generated secret hash |
| `BOOTSTRAP_REVIEWER_EMAIL` | Generated value from `bootstrap-env.json` |
| `BOOTSTRAP_REVIEWER_PASSWORD_HASH` | Generated secret hash |

Do not set `VITE_API_BASE_URL` for this deployment. The browser uses `/api` on the same Render domain. The Docker build includes the interface, so Vercel is optional.

Alternatively, use **New → Blueprint** with `render.yaml` for a fresh account. Review that both plans are `free` and no disk is listed, supply the prompted variables, and apply. Do not apply a fresh Blueprint over manually created resources unless you have checked how Render will handle their names and ownership.

## 7. Verify the running app

Use the URL Render actually assigns, not a guessed service-name URL. Replace `YOUR-SERVICE` below:

```powershell
$appOrigin = 'https://YOUR-SERVICE.onrender.com'
Invoke-RestMethod "$appOrigin/api/health"
```

Expected response:

```json
{"status":"ok","ocr_available":true,"ocr_engine":"RapidOCR ONNX (CPU)"}
```

Check all of the following:

1. `/` displays the sign-in interface and a refreshed `/inspections` route still loads.
2. Sign in using the private inspector credentials.
3. Create an inspection; upload a sample or a clear label photograph.
4. Run analysis and wait for OCR to finish. A healthy HTTP response alone does not prove OCR can run in the free service's memory limit.
5. Review extracted fields and download both PDF and DOCX reports.
6. Sign out and use the reviewer account to review the record.
7. After a service restart, sign in again and verify the inspection, photograph, OCR retry, and report are still available.

With database evidence enabled, original and normalized photographs are saved transactionally alongside their metadata. Missing local copies are restored on demand after access checks. Report snapshots remain in PostgreSQL; report files are regenerated when the temporary cache disappears.

## 8. Add the uptime monitor

1. UptimeRobot → **Add new monitor**.
2. Type: **HTTP(s)**. Name: **CompliSense API**.
3. URL: the real `https://YOUR-SERVICE.onrender.com/api/health`.
4. Interval: **5 minutes** on the free plan. Timeout: **30 seconds**.
5. Enable SSL verification. Use **GET**; the endpoint also supports **HEAD**.
6. Select your verified email contact for failure/recovery alerts. Avoid attaching unrelated existing contacts.
7. Save and wait for the first check to show **Up**.

An HTTP monitor proves that the health route responds. A separate keyword monitor can check `"status":"ok"` if desired, but a full OCR smoke test is still needed before a demo. The health route checks whether the OCR package is installed; it does not run OCR or continuously query PostgreSQL.

UptimeRobot's API represents monitor intervals in **seconds** (`300` means five minutes). Some connector descriptions mislabel this field; read the created monitor back and verify the displayed interval.

Do not point the monitor at the old Vercel `/api/health`: without an API proxy that URL can serve the React HTML fallback and produce a false positive.

## 9. What to do with Vercel

The fastest verified arrangement is to share the Render application URL. Both frontend and API then use the same origin, including photos, reports, CSRF protection, and session cookies.

The older `complisense-five.vercel.app` deployment is a separate frontend deployment. Merely setting `VITE_API_BASE_URL` to an unrelated `onrender.com` domain is insufficient for this app: its `SameSite=Lax` session cookie and relative evidence/report URLs expect same-origin requests.

To retain Vercel later, configure a same-origin `/api/:path*` reverse proxy to Render **before** the SPA fallback, leave `VITE_API_BASE_URL` empty, and validate cookie forwarding, private image downloads, reports, and long OCR requests. That optional proxy is not required for the single Render deployment described here.

## 10. Back up and migrate before expiry

Free Render PostgreSQL has no managed backups. Download important PDF/DOCX reports after each demo, keep original source photos locally, and make a full PostgreSQL backup before the expiration date. Reports alone are not a database backup.

For a complete backup, install PostgreSQL 16 client tools locally. Temporarily allow only your current public IP in the database's external access list, use the external hostname/user/database from Render, and let `pg_dump` prompt for the password (do not put passwords in command history):

```powershell
$env:PGSSLMODE = 'require'
pg_dump --host=YOUR_EXTERNAL_HOST --username=complisense --dbname=complisense --password --format=custom --file=complisense-backup.dump
```

Remove your temporary external access rule afterward. Store the backup privately outside the repository. It contains accounts, sessions, records, snapshots, and both photo copies in `evidence_payloads`.

To restore into a **new, empty** PostgreSQL database you control:

```powershell
pg_restore --host=NEW_HOST --username=NEW_USER --dbname=NEW_DATABASE --password --no-owner --no-acl complisense-backup.dump
```

Verify the restore, update Render's `DATABASE_URL`, redeploy, and rerun the full smoke test. Never restore over a populated database casually. For a longer-lived free option, choose a currently available free PostgreSQL provider such as Neon or Supabase, check its current storage/compute limits, and migrate before expiry. This requires a separate provider account; it is not configured automatically by this guide.

## 11. Troubleshooting

| Symptom | Check / fix |
| --- | --- |
| Repository not found | Grant Render's GitHub integration access to the private repository; authorizing the Render API alone does not grant clone access |
| Payment requested | Confirm Free compute, no disk, no paid add-ons; do not upgrade to continue |
| Build fails | Read the first Docker build error; root context must include both `frontend/` and `backend/` |
| Service cannot start | Check database availability, internal URL, same region, and the four bootstrap variables |
| Health returns HTML | Wrong origin or SPA fallback; use the Render API health URL and verify JSON content |
| Slow first page | Free service may be waking; wait roughly a minute and retry |
| Login works then immediately logs out | Use the single Render origin; check `COOKIE_SECURE=true` over HTTPS |
| Invalid credentials after changing env | Bootstrap does not overwrite existing accounts; use the original private login file |
| Missing photos after restart | Confirm `EVIDENCE_IN_DATABASE=true` was enabled when uploaded; old disk-only photos are not automatically imported |
| OCR process killed / exit 137 | Free memory limit exceeded; try one smaller, readable photo and inspect logs; do not silently upgrade |
| Monitor Down but page works later | Check cold-start timeout, expected URL, SSL, and actual monitor interval |
| Database stops after 30 days | Restore/migrate the backup; UptimeRobot cannot extend database lifetime |

## 12. Local presentation fallback

```powershell
cd D:\SIH\CompliSense1
npm.cmd --prefix frontend ci
npm.cmd --prefix frontend run build
cd backend
..\.venv\Scripts\python.exe -m app.cli seed-demo
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. The predictable demo accounts in the README are for this local fallback only. Public deployment uses the random credentials generated in step 4.

## Official references

- [Render free service and database limits](https://render.com/docs/free)
- [Render Docker deployment](https://render.com/docs/docker)
- [Render Blueprint specification](https://render.com/docs/blueprint-spec)
- [Render PostgreSQL](https://render.com/docs/postgresql)
- [UptimeRobot API](https://uptimerobot.com/api/)

Checked for this setup on 23 September 2026. Provider limits and interface labels can change; review the actual account screens before applying a plan.
