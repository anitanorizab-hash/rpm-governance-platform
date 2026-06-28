// QueueButton (CP20D): queue an APPROVED notification → dry-run send. Approved-only.
import { Button } from "../ui/button";

export default function QueueButton({ status, canQueue, busy, onQueue }) {
  if (!canQueue) return null;
  if (status !== "approved") {
    if (status === "pending_review") {
      return <span className="text-xs text-slate-500">Awaiting approval before it can be queued.</span>;
    }
    return null;
  }
  return (
    <Button onClick={onQueue} disabled={busy}>{busy ? "Queueing…" : "Queue (Dry-Run Send)"}</Button>
  );
}
