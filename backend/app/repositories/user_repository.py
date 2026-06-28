"""User/Role repository (CP4) — DB access for auth & RBAC. No business logic."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.operational.access import Role, User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- queries ---
    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(
            select(User).options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.email == email)
        )

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.scalar(
            select(User).options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id == user_id)
        )

    def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        return list(self.db.scalars(
            select(User).options(selectinload(User.roles).selectinload(UserRole.role))
            .limit(limit).offset(offset)
        ))

    def get_role_by_name(self, name: str) -> Role | None:
        return self.db.scalar(select(Role).where(Role.name == name))

    # --- mutations ---
    def create_user(self, *, email: str, name: str, password_hash: str, scope: str | None = None) -> User:
        user = User(id=str(uuid.uuid4()), email=email, name=name,
                    password_hash=password_hash, scope=scope, active=True)
        self.db.add(user)
        self.db.flush()
        return user

    def assign_role(self, user: User, role: Role) -> None:
        exists = self.db.scalar(
            select(UserRole).where(UserRole.user_id == user.id, UserRole.role_id == role.id)
        )
        if not exists:
            self.db.add(UserRole(id=str(uuid.uuid4()), user_id=user.id, role_id=role.id))
            self.db.flush()

    def set_roles(self, user: User, role_names: list[str]) -> list[str]:
        """Replace the user's roles with the given set (by name). Returns applied names."""
        # clear existing
        for ur in list(user.roles):
            self.db.delete(ur)
        self.db.flush()
        applied: list[str] = []
        for name in role_names:
            role = self.get_role_by_name(name)
            if role:
                self.assign_role(user, role)
                applied.append(name)
        return applied
