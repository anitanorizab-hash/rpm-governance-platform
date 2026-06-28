"""Backward-compatible audit entrypoint. Canonical implementation lives in app.core.audit (CP5)."""
from app.core.audit import AuditContext, get_audit_context, mask_payload, write_audit  # noqa: F401

__all__ = ["write_audit", "mask_payload", "AuditContext", "get_audit_context"]
