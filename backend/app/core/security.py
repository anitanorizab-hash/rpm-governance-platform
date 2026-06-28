"""Security utilities (CP4): password hashing (PBKDF2, stdlib) + JWT access/refresh tokens.

JWT_SECRET_KEY is read from .env only. In production a missing secret is a hard error; in
development/testing a clearly-marked ephemeral fallback is used so the app can run locally.
No secrets are hard-coded for production.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings
from app.core.env import get_secret

# ---------- Password hashing (PBKDF2-HMAC-SHA256, stdlib — no native deps) ----------
_PBKDF2_ITERATIONS = 200_000
_ALGO = "pbkdf2_sha256"


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), _PBKDF2_ITERATIONS)
    return f"{_ALGO}${_PBKDF2_ITERATIONS}${salt}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iters, salt, hexhash = stored.split("$")
        if algo != _ALGO:
            return False
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iters))
        return hmac.compare_digest(dk.hex(), hexhash)
    except Exception:
        return False


# ---------- JWT ----------
_ALGORITHM = "HS256"
_DEV_FALLBACK_SECRET = "dev-only-insecure-secret-change-me"


def _jwt_secret() -> str:
    secret = get_secret("JWT_SECRET_KEY")
    if secret:
        return secret
    if get_settings().get("mode") == "production":
        raise RuntimeError("JWT_SECRET_KEY is required in production (.env).")
    # development/testing fallback (not for production)
    return _DEV_FALLBACK_SECRET


def _expiry(kind: str) -> datetime:
    now = datetime.now(timezone.utc)
    if kind == "access":
        minutes = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "15"))
        return now + timedelta(minutes=minutes)
    days = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))
    return now + timedelta(days=days)


def create_token(*, subject: str, roles: list[str], scope: str | None, kind: str) -> str:
    payload = {
        "sub": subject,
        "roles": roles,
        "scope": scope,
        "type": kind,
        "exp": _expiry(kind),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm=_ALGORITHM)


def create_access_token(subject: str, roles: list[str], scope: str | None = None) -> str:
    return create_token(subject=subject, roles=roles, scope=scope, kind="access")


def create_refresh_token(subject: str, roles: list[str], scope: str | None = None) -> str:
    return create_token(subject=subject, roles=roles, scope=scope, kind="refresh")


def decode_token(token: str) -> dict:
    """Decode/verify a JWT. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, _jwt_secret(), algorithms=[_ALGORITHM])
