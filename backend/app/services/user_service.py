"""User service (CP4): list/get users, assign roles. Admin-guarded at the route layer."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.audit.logger import write_audit
from app.repositories.user_repository import UserRepository

VALID_ROLES = {
    "super_admin", "jpn_admin", "sector_admin", "ppd_admin",
    "kpi_pic", "finance_officer", "executive", "read_only", "internal_audit",
}


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def list_users(self, limit: int = 100, offset: int = 0):
        return self.repo.list_users(limit=limit, offset=offset)

    def get_user(self, user_id: str):
        return self.repo.get_by_id(user_id)

    def set_roles(self, *, user_id: str, role_names: list[str], actor_id: str | None):
        invalid = [r for r in role_names if r not in VALID_ROLES]
        if invalid:
            raise ValueError(f"Unknown role(s): {invalid}. Valid: {sorted(VALID_ROLES)}")
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        before = ",".join(user.role_names)
        applied = self.repo.set_roles(user, role_names)
        write_audit(self.db, entity_type="user", entity_id=user_id, action="set_roles",
                    actor_id=actor_id, before=before, after=",".join(applied))
        self.db.commit()
        return self.repo.get_by_id(user_id)
