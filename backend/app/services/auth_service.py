"""Auth service (CP4): registration, authentication, token issue, MOE-domain enforcement.

BR-003: only @moe.gov.my / @moe-dl.edu.my may access the system. New users default to read_only
(least privilege); admins elevate roles via the User API.
"""
from __future__ import annotations

import jwt
from sqlalchemy.orm import Session

from app.audit.logger import write_audit
from app.core.security import (
    create_access_token, create_refresh_token, decode_token, hash_password, verify_password,
)
from app.repositories.user_repository import UserRepository

ALLOWED_DOMAINS = ("@moe.gov.my", "@moe-dl.edu.my")
DEFAULT_ROLE = "read_only"


class AuthError(Exception):
    """Raised for auth failures (invalid domain/credentials/token). Carries a safe message."""


def is_allowed_domain(email: str) -> bool:
    e = (email or "").strip().lower()
    return any(e.endswith(d) for d in ALLOWED_DOMAINS)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def register(self, *, email: str, name: str, password: str) -> object:
        email = (email or "").strip().lower()
        if not is_allowed_domain(email):
            raise AuthError("Registration is restricted to @moe.gov.my and @moe-dl.edu.my accounts.")
        if self.repo.get_by_email(email):
            raise AuthError("An account with this email already exists.")
        user = self.repo.create_user(email=email, name=name, password_hash=hash_password(password))
        role = self.repo.get_role_by_name(DEFAULT_ROLE)
        if role:
            self.repo.assign_role(user, role)
        write_audit(self.db, entity_type="user", entity_id=user.id, action="register", actor_id=user.id)
        self.db.commit()
        return self.repo.get_by_id(user.id)

    def authenticate(self, *, email: str, password: str) -> object:
        email = (email or "").strip().lower()
        user = self.repo.get_by_email(email)
        if not user or not user.active or not verify_password(password, user.password_hash):
            # Log the failed attempt (email is not sensitive; password is NEVER logged).
            write_audit(self.db, entity_type="user", entity_id=email, action="login_failed",
                        actor_id=(user.id if user else None), reason="invalid credentials")
            self.db.commit()
            raise AuthError("Invalid email or password.")
        write_audit(self.db, entity_type="user", entity_id=user.id, action="login", actor_id=user.id)
        self.db.commit()
        return user

    @staticmethod
    def issue_tokens(user) -> dict:
        roles = user.role_names
        return {
            "access_token": create_access_token(user.id, roles, user.scope),
            "refresh_token": create_refresh_token(user.id, roles, user.scope),
            "token_type": "bearer",
        }

    def refresh(self, refresh_token: str) -> dict:
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError:
            raise AuthError("Invalid or expired refresh token.")
        if payload.get("type") != "refresh":
            raise AuthError("Provided token is not a refresh token.")
        user = self.repo.get_by_id(payload.get("sub"))
        if not user or not user.active:
            raise AuthError("User no longer active.")
        write_audit(self.db, entity_type="user", entity_id=user.id, action="token_refresh", actor_id=user.id)
        self.db.commit()
        return self.issue_tokens(user)

    def logout(self, user_id: str | None) -> None:
        # Stateless JWT: logout is client-side (discard tokens). A server-side blocklist can be
        # added later. We record the event for audit.
        if user_id:
            write_audit(self.db, entity_type="user", entity_id=user_id, action="logout", actor_id=user_id)
            self.db.commit()
