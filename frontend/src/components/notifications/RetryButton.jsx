// RetryButton (CP20D): retry a failed/queued email-queue item (dry-run). Manage roles only.
import { Button } from "../ui/button";

export default function RetryButton({ status, canQueue, busy, retryCount, onRetry }) {
  if (!canQueue) return null;
  if (!["failed", "queued"].includes(status)) return null;
  return (
    <Button variant="outline" onClick={onRetry} disabled={busy}>
      {busy ? "Retrying…" : `Retry${retryCount ? ` (${retryCount})` : ""}`}
    </Button>
  );
}
