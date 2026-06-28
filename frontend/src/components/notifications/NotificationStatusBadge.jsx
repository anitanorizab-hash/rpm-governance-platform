// NotificationStatusBadge (CP20D): colour-coded notification status.
const STYLES = {
  draft: "bg-slate-100 text-slate-600",
  pending_review: "bg-amber-50 text-amber-700",
  approved: "bg-green-50 text-green-700",
  queued: "bg-blue-50 text-blue-700",
  sent: "bg-green-100 text-green-800",
  failed: "bg-red-50 text-red-700",
  cancelled: "bg-slate-200 text-slate-600",
};
const LABELS = { sent: "Sent (Dry Run)" };
const prettify = (s) =>
  s == null ? "—" : (LABELS[s] || String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()));

export default function NotificationStatusBadge({ status }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${STYLES[status] || "bg-slate-100 text-slate-600"}`}>
      {prettify(status)}
    </span>
  );
}
