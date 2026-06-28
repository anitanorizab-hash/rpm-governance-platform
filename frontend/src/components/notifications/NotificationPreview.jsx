// NotificationPreview (CP20D): selected notification detail + HITL actions.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import NotificationStatusBadge from "./NotificationStatusBadge";
import SubmitForReviewButton from "./SubmitForReviewButton";
import QueueButton from "./QueueButton";
import RetryButton from "./RetryButton";
import { Button } from "../ui/button";

const prettify = (s) =>
  s == null || s === "" ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function NotificationPreview({
  notification, canDraft, canQueue, busy, actionMsg, actionError,
  onSubmit, onQueue, onRetry, onCancel,
}) {
  if (!notification) {
    return (
      <Card><CardContent className="py-12 text-center text-sm text-slate-500">
        Select a notification to view its detail and actions.
      </CardContent></Card>
    );
  }
  const n = notification;
  const cancellable = canDraft && !["sent", "cancelled"].includes(n.status);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Notification Detail</CardTitle>
        <NotificationStatusBadge status={n.status} />
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div><p className="text-xs uppercase tracking-wide text-slate-400">Recipient</p><p className="text-slate-700">{n.recipient || "—"}</p></div>
          <div><p className="text-xs uppercase tracking-wide text-slate-400">Type</p><p className="text-slate-700">{prettify(n.type)}</p></div>
          <div className="col-span-2"><p className="text-xs uppercase tracking-wide text-slate-400">Subject</p><p className="text-slate-700">{n.subject || "—"}</p></div>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-400">Body</p>
          <p className="mt-0.5 whitespace-pre-line rounded-md bg-slate-50 px-3 py-2 text-sm text-slate-700">{n.body || "—"}</p>
        </div>
        {n.failure_reason && (
          <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            Failure reason: {n.failure_reason}
          </div>
        )}

        <div className="flex flex-wrap items-center gap-3 pt-1">
          <SubmitForReviewButton status={n.status} canDraft={canDraft} busy={busy} onSubmit={onSubmit} />
          <QueueButton status={n.status} canQueue={canQueue} busy={busy} onQueue={onQueue} />
          <RetryButton status={n.status} canQueue={canQueue} busy={busy} retryCount={n.retry_count} onRetry={onRetry} />
          {cancellable && <Button variant="outline" onClick={onCancel} disabled={busy}>Cancel</Button>}
        </div>
        {actionMsg && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{actionMsg}</div>}
        {actionError && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{actionError}</div>}
        <p className="text-[11px] text-slate-400">
          Notifications require approval before queueing. Sending is dry-run unless production SMTP is configured.
        </p>
      </CardContent>
    </Card>
  );
}
