"""Reusable audit helper (CP5): masking, request context, and the canonical write_audit().

All modules (import, KPI, approvals, reports, notifications, AI) MUST log via this helper so the
audit trail is consistent and append-only. Secrets/passwords are NEVER written.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.operational.governance import AuditLog

# Keys whose values must be masked if they ever appear in before/after payloads.
SENSITIVE_KEYS = {
    "password", "password_hash", "pwd", "secret", "token", "access_token",
    "refresh_token", "api_key", "jwt_secret_key", "authorization", "auth",
}
_MASK = "***"


def _is_sensitive(key: str) -> bool:
    k = key.lower()
    return any(s in k for s in SENSITIVE_KEYS)


def mask_payload(value):
    """Mask sensitive keys in dict/list payloads; pass through other scalars."""
    if isinstance(value, dict):
        return {k: (_MASK if _is_sensitive(k) else mask_payload(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_payload(v) for v in value]
    return value


def _to_text(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(mask_payload(value), default=str, ensure_ascii=False)
    return str(value)


@dataclass
class AuditContext:
    ip_address: str | None = None
    user_agent: str | None = None
    request_id: str | None = None


def get_audit_context(request: Request) -> AuditContext:
    """FastAPI dependency: capture request metadata for audit (no body, no secrets)."""
    client_ip = request.client.host if request.client else None
    return AuditContext(
        ip_address=client_ip,
        user_agent=request.headers.get("user-agent"),
        request_id=request.headers.get("x-request-id") or str(uuid.uuid4()),
    )


def write_audit(
    db: Session,
    *,
    entity_type: str,
    action: str,
    entity_id: str | None = None,
    actor_id: str | None = None,
    before=None,
    after=None,
    reason: str | None = None,
    context: AuditContext | None = None,
) -> AuditLog:
    """Append one audit entry (append-only). before/after are masked + serialised."""
    ctx = context or AuditContext()
    entry = AuditLog(
        id=str(uuid.uuid4()),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_id=actor_id,
        before=_to_text(before),
        after=_to_text(after),
        reason=reason,
        ip_address=ctx.ip_address,
        user_agent=(ctx.user_agent or "")[:512] or None,
        request_id=ctx.request_id,
    )
    db.add(entry)
    db.flush()
    return entry
