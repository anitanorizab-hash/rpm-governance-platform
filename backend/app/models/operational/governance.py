"""Governance & HITL models (CP3) — OPERATIONAL plane.

AmendmentWindow, KPIAmendment, Approval, Report, Notification, AuditLog (append-only).
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, CreatedAtMixin, TimestampMixin, fk_uuid, uuid_pk


class AmendmentWindow(Base, TimestampMixin):
    """KPI definitional edits allowed only in July & October (BR-008)."""
    __tablename__ = "amendment_window"
    id = uuid_pk()
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)     # 7 (July) or 10 (October)
    is_open = Column(Boolean, default=False)


class KPIAmendment(Base, TimestampMixin):
    __tablename__ = "kpi_amendment"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    field = Column(String(64))                  # statement | indicator | target
    old_value = Column(Text)
    new_value = Column(Text)
    window_id = fk_uuid("amendment_window.id")
    actor_id = fk_uuid("user.id")
    reason = Column(Text)


class Approval(Base, TimestampMixin):
    """Human-in-the-loop approval (polymorphic target) with a state machine (CP9)."""
    __tablename__ = "approval"
    id = uuid_pk()
    item_type = Column(String(32), nullable=False)  # report | notification | recommendation | copilot_recommendation
    item_id = Column(String(36), nullable=False)
    state = Column(String(20), default="draft", nullable=False)  # draft|pending_review|approved|rejected|cancelled
    requested_by = fk_uuid("user.id")               # creator (cannot approve own unless super-admin override)
    decision = Column(String(16))                   # approve | reject (set on final decision)
    actor_id = fk_uuid("user.id")                   # decision maker (human only)
    comment = Column(Text)


class Report(Base, TimestampMixin):
    __tablename__ = "report"
    id = uuid_pk()
    title = Column(String(512))                     # CP17
    period = Column(String(7))
    type = Column(String(32))
    status = Column(String(16), default="draft")    # draft|pending_review|approved|rejected|archived
    content = Column(Text)                          # CP17 JSON sections
    summary = Column(Text)                          # CP17
    reject_reason = Column(Text)                    # CP17
    approval_id = fk_uuid("approval.id")            # CP17 link to CP9 approval
    generated_by = fk_uuid("user.id")
    approved_by = fk_uuid("user.id")
    archive_ref = Column(String(512))


class Notification(Base, TimestampMixin):
    __tablename__ = "notification"
    id = uuid_pk()
    type = Column(String(48))                       # reminder | missing_info | approval | report | escalation | fds_review
    recipient = Column(String(255))
    subject = Column(String(512))                   # CP18
    body = Column(Text)                             # CP18
    content_ref = Column(Text)
    related_entity_type = Column(String(48))        # CP18
    related_entity_id = Column(String(36))          # CP18
    status = Column(String(16), default="draft")    # draft|pending_review|approved|queued|sent|failed|cancelled
    approval_id = fk_uuid("approval.id")            # CP18 link to CP9
    failure_reason = Column(Text)                   # CP18
    created_by = fk_uuid("user.id")                 # CP18
    approved_by = fk_uuid("user.id")
    retry_count = Column(Integer, default=0)


class AuditLog(Base, CreatedAtMixin):
    """APPEND-ONLY audit trail (BR-009/029). No updated_at; never updated/deleted (enforced in service layer)."""
    __tablename__ = "audit_log"
    id = uuid_pk()
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(36))
    action = Column(String(64), nullable=False)
    actor_id = fk_uuid("user.id")
    before = Column(Text)               # old_value (masked, JSON/text)
    after = Column(Text)                # new_value (masked, JSON/text)
    reason = Column(Text)
    # request context (CP5)
    ip_address = Column(String(64))
    user_agent = Column(String(512))
    request_id = Column(String(64))
