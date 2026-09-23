"""FastAPI dependencies: open a database session, then authorize the request."""

import hmac
import time

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .models import LoginSession, User
from .security import token_hash

COOKIE_NAME = "complisense_session"


def get_db(request: Request):
    with request.app.state.database.session() as db:
        yield db


def get_login_session(request: Request, db: Session = Depends(get_db)) -> LoginSession:
    cookie = request.cookies.get(COOKIE_NAME, "")
    session = db.get(LoginSession, token_hash(cookie)) if cookie else None
    if session is None or session.expires_at <= time.time():
        raise HTTPException(401, "Sign in to continue.")
    return session


def get_current_user(session: LoginSession = Depends(get_login_session), db: Session = Depends(get_db)) -> User:
    user = db.get(User, session.user_id)
    if user is None:
        raise HTTPException(401, "This account is no longer available.")
    return user


def require_csrf(request: Request, session: LoginSession = Depends(get_login_session)):
    submitted = request.headers.get("X-CSRF-Token", "")
    if not submitted or not hmac.compare_digest(submitted, session.csrf_token):
        raise HTTPException(403, "Security token missing or expired. Refresh the page and try again.")


def require_reviewer(user: User = Depends(get_current_user)) -> User:
    if user.role != "reviewer":
        raise HTTPException(403, "Only a reviewer can record a review decision.")
    return user


def user_dict(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
