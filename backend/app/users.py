"""User creation is a local administration action, not a public signup endpoint."""

import os
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .security import hash_password


def bootstrap_users(db: Session) -> None:
    """Create initial accounts from secret hashes on hosts without shell access.

    Existing users are never overwritten. No credentials are logged.
    """
    for role in ("inspector", "reviewer"):
        prefix = f"BOOTSTRAP_{role.upper()}"
        email = os.getenv(f"{prefix}_EMAIL", "").strip().lower()
        encoded = os.getenv(f"{prefix}_PASSWORD_HASH", "")
        if not email and not encoded:
            continue
        if "@" not in email or len(email) > 254 or not re.fullmatch(r"scrypt\$[0-9a-f]{32}\$[0-9a-f]{128}", encoded):
            raise ValueError(f"Configure a valid {prefix}_EMAIL and {prefix}_PASSWORD_HASH.")
        if db.scalar(select(User).where(User.email == email)):
            continue
        db.add(User(email=email, name=f"CompliSense {role.title()}", role=role, password_hash=encoded))
    db.commit()


def create_user(db: Session, email: str, name: str, role: str, password: str) -> User:
    email = email.strip().lower()
    if role not in ("inspector", "reviewer"):
        raise ValueError("Role must be inspector or reviewer.")
    if len(password) < 12 or len(password) > 256:
        raise ValueError("Use a password between 12 and 256 characters.")
    if "@" not in email or len(email) > 254 or not name.strip():
        raise ValueError("Provide a valid email and a non-empty name.")
    if db.scalar(select(User).where(User.email == email)):
        raise ValueError("A user with that email already exists.")
    user = User(email=email, name=name.strip()[:100], role=role, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
