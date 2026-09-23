"""Sign in/out using an HttpOnly cookie and a separate CSRF token."""

import secrets
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..dependencies import COOKIE_NAME, get_current_user, get_db, get_login_session, require_csrf, user_dict
from ..models import LoginSession, User
from ..schemas import LoginRequest
from ..security import hash_password, token_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
DUMMY_HASH = hash_password("unused-random-password-for-timing")


@router.post("/login")
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    # A small local limiter. A shared deployment should also limit at its proxy.
    address = request.client.host if request.client else "unknown"
    now = time.time()
    attempts = request.app.state.login_attempts
    for key in list(attempts):
        attempts[key] = [attempt for attempt in attempts[key] if now - attempt < 600]
        if not attempts[key]:
            del attempts[key]
    if len(attempts.get(address, [])) >= 10:
        raise HTTPException(429, "Too many failed sign-in attempts. Try again in ten minutes.")
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    valid = verify_password(payload.password, user.password_hash if user else DUMMY_HASH)
    if not user or not valid:
        attempts.setdefault(address, []).append(now)
        raise HTTPException(401, "Email or password is incorrect.")
    attempts.pop(address, None)
    db.execute(delete(LoginSession).where(LoginSession.expires_at <= now))
    old_cookie = request.cookies.get(COOKIE_NAME)
    if old_cookie:
        db.execute(delete(LoginSession).where(LoginSession.token_hash == token_hash(old_cookie)))
    token = secrets.token_urlsafe(48)
    csrf = secrets.token_urlsafe(32)
    duration = request.app.state.settings.session_hours * 3600
    db.add(LoginSession(token_hash=token_hash(token), user_id=user.id, csrf_token=csrf, expires_at=now + duration))
    db.commit()
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=duration,
        httponly=True,
        secure=request.app.state.settings.cookie_secure,
        samesite="lax",
        path="/",
    )
    return {"user": user_dict(user), "csrf_token": csrf}


@router.get("/me")
def me(user: User = Depends(get_current_user), session: LoginSession = Depends(get_login_session)):
    return {"user": user_dict(user), "csrf_token": session.csrf_token}


@router.post("/logout", dependencies=[Depends(require_csrf)])
def logout(response: Response, session: LoginSession = Depends(get_login_session), db: Session = Depends(get_db)):
    db.delete(session)
    db.commit()
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"message": "Signed out."}
