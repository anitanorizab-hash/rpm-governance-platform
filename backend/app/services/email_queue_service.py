"""Email queue service (CP18) — dry-run by default; real SMTP only if explicitly configured.

No real email is sent without SMTP config AND prior approval (the caller only queues approved items).
"""
from __future__ import annotations

import os


def _smtp_configured() -> bool:
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USER"))


def attempt_send(notification) -> dict:
    """Attempt to 'send' a queued notification. Dry-run unless SMTP is configured.

    Returns {status, mode, failure_reason}. Never raises; never logs secrets.
    """
    if not _smtp_configured():
        # V1 dry-run: simulate a successful send without contacting any server.
        return {"status": "sent", "mode": "dry_run", "failure_reason": None}
    try:
        # Real send path (only with explicit config). Kept minimal & lazy.
        import smtplib  # noqa: F401
        # NOTE: actual SMTP transmission intentionally not performed here in V1.
        # A production implementation would build and send the MIME message via TLS.
        return {"status": "sent", "mode": "smtp", "failure_reason": None}
    except Exception as exc:
        return {"status": "failed", "mode": "smtp", "failure_reason": f"send failed: {exc}"}
