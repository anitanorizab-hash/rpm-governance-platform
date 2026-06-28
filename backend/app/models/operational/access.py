"""Access & reference models (CP3) — OPERATIONAL plane.

User, Role, UserRole, Department, PIC, Teras, StrategyEnabler, Prakarsa, BudgetStatus.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class Role(Base, TimestampMixin):
    __tablename__ = "role"
    id = uuid_pk()
    name = Column(String(64), unique=True, nullable=False)   # e.g. super_admin, kpi_pic
    description = Column(String(255))
    users = relationship("UserRole", back_populates="role")


class User(Base, TimestampMixin):
    __tablename__ = "user"
    id = uuid_pk()
    email = Column(String(255), unique=True, nullable=False)  # MOE domains (enforced in CP4)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)        # PBKDF2 (CP4)
    scope = Column(String(64))            # state/district/sector/own (set with RBAC in CP4)
    active = Column(Boolean, default=True, nullable=False)
    roles = relationship("UserRole", back_populates="user")

    @property
    def role_names(self) -> list[str]:
        return [ur.role.name for ur in self.roles if ur.role]


class UserRole(Base, TimestampMixin):
    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)
    id = uuid_pk()
    user_id = fk_uuid("user.id", nullable=False)
    role_id = fk_uuid("role.id", nullable=False)
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Department(Base, TimestampMixin):
    """Bahagian / implementing division (e.g. BPSH, BPK, IPGM)."""
    __tablename__ = "department"
    id = uuid_pk()
    code = Column(String(32), unique=True)
    name = Column(String(255), nullable=False)


class PIC(Base, TimestampMixin):
    __tablename__ = "pic"
    id = uuid_pk()
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)   # V1.1.1: imported PICs have no email until captured
    sector = Column(String(128))
    department_id = fk_uuid("department.id")


class Teras(Base, TimestampMixin):
    """RPM strategic pillar (1–7) — reference/master."""
    __tablename__ = "teras"
    id = uuid_pk()
    number = Column(Integer, unique=True, nullable=False)   # 1..7
    name = Column(String(255), nullable=False)
    strategies = relationship("StrategyEnabler", back_populates="teras")


class StrategyEnabler(Base, TimestampMixin):
    __tablename__ = "strategy_enabler"
    id = uuid_pk()
    teras_id = fk_uuid("teras.id", nullable=False)
    code = Column(String(32))
    type = Column(String(32))     # strategy | enabler
    name = Column(String(512))
    teras = relationship("Teras", back_populates="strategies")
    prakarsa = relationship("Prakarsa", back_populates="strategy")


class Prakarsa(Base, TimestampMixin):
    __tablename__ = "prakarsa"
    id = uuid_pk()
    strategy_id = fk_uuid("strategy_enabler.id", nullable=False)
    code = Column(String(32))
    name = Column(String(512))
    strategy = relationship("StrategyEnabler", back_populates="prakarsa")


class BudgetStatus(Base, TimestampMixin):
    """Six-value allocation-status vocabulary (reference)."""
    __tablename__ = "budget_status"
    id = uuid_pk()
    code = Column(String(32), unique=True, nullable=False)   # received, will_be_received, …
    label = Column(String(64), nullable=False)
