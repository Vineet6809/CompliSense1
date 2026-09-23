"""Beginner-friendly local administration commands.

Examples from backend/:
    python -m app.cli seed-demo
    python -m app.cli create-user --email officer@example.com --name "A. Officer" --role inspector
"""

import argparse
import getpass

from sqlalchemy import select

from .config import Settings
from .database import Database
from .models import User
from .users import create_user


def add_user(database: Database, email: str, name: str, role: str, password: str | None = None):
    password = password or getpass.getpass("Password (12+ characters): ")
    with database.session() as db:
        user = create_user(db, email, name, role, password)
        print(f"Created {user.role} account for {user.email}.")


def seed_demo(database: Database):
    # These predictable accounts are for local demonstration only. The command
    # is opt-in and the deployment guide tells operators to create real users.
    accounts = [
        ("inspector@demo.local", "Demo Inspector", "inspector", "InspectorDemo123!"),
        ("reviewer@demo.local", "Demo Reviewer", "reviewer", "ReviewerDemo123!"),
    ]
    with database.session() as db:
        for email, name, role, password in accounts:
            if db.scalar(select(User).where(User.email == email)):
                print(f"Account already exists: {email}")
            else:
                create_user(db, email, name, role, password)
                print(f"Created {role}: {email} / {password}")


def main():
    parser = argparse.ArgumentParser(description="Manage CompliSense users.")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create-user", help="Create an inspector or reviewer account.")
    create.add_argument("--email", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--role", required=True, choices=("inspector", "reviewer"))
    commands.add_parser("seed-demo", help="Create clearly marked local demo accounts.")
    args = parser.parse_args()
    database = Database(Settings().database_url)
    database.initialize()
    if args.command == "create-user":
        add_user(database, args.email, args.name, args.role)
    else:
        seed_demo(database)


if __name__ == "__main__":
    main()
