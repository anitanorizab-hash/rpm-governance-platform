"""User & Role API (A6 G2) — CP4. Admin-guarded for list/role assignment."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import ADMIN_ROLES, get_current_user, require_roles
from app.db.session import get_db
from app.schemas.user import RoleAssignIn, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def my_profile(current_user=Depends(get_current_user)):
    return UserOut.from_model(current_user)


@router.get("", response_model=list[UserOut])
def list_users(
    _admin=Depends(require_roles(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    return [UserOut.from_model(u) for u in UserService(db).list_users()]


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: str,
    _admin=Depends(require_roles(*ADMIN_ROLES)),
    db: Session = Depends(get_db),
):
    user = UserService(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.from_model(user)


@router.patch("/{user_id}/roles", response_model=UserOut)
def assign_roles(
    user_id: str,
    body: RoleAssignIn,
    admin=Depends(require_roles("super_admin")),
    db: Session = Depends(get_db),
):
    try:
        user = UserService(db).set_roles(user_id=user_id, role_names=body.roles, actor_id=admin.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.from_model(user)
