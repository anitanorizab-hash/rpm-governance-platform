"""User schemas (CP4)."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    scope: str | None = None
    active: bool
    roles: list[str] = []

    @classmethod
    def from_model(cls, user) -> "UserOut":
        return cls(
            id=user.id, email=user.email, name=user.name,
            scope=user.scope, active=user.active, roles=user.role_names,
        )


class RoleAssignIn(BaseModel):
    roles: list[str] = Field(min_length=1)
