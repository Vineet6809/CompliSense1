"""Generate initial deployment credentials into a local, Git-ignored directory.

Run from the repository root. The JSON is for Render's secret environment values;
the text file is for the operator. Neither file is uploaded with source code.
"""

import argparse
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.security import hash_password  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspector-email", default="inspector@complisense.local")
    parser.add_argument("--reviewer-email", default="reviewer@complisense.local")
    args = parser.parse_args()
    directory = ROOT / ".work" / "deployment"
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "login-credentials.txt"
    environment = directory / "bootstrap-env.json"
    if target.exists() or environment.exists():
        raise SystemExit("Credentials already exist in .work/deployment; refusing to replace them.")
    values = []
    accounts = []
    for role, email in (("inspector", args.inspector_email), ("reviewer", args.reviewer_email)):
        password = secrets.token_urlsafe(24)
        values.extend([
            {"key": f"BOOTSTRAP_{role.upper()}_EMAIL", "value": email},
            {"key": f"BOOTSTRAP_{role.upper()}_PASSWORD_HASH", "value": hash_password(password)},
        ])
        accounts.append(f"{role.title()}\nEmail: {email}\nPassword: {password}\n")
    target.write_text("CompliSense deployment login credentials — keep private.\n\n" + "\n".join(accounts), encoding="utf-8")
    environment.write_text(json.dumps(values, indent=2), encoding="utf-8")
    print("Created .work/deployment/login-credentials.txt and bootstrap-env.json. Keep both private.")


if __name__ == "__main__":
    main()
