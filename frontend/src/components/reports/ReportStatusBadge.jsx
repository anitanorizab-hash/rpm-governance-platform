// ReportStatusBadge (CP20D): colour-coded report status.
const STYLES = {
  draft: "bg-slate-100 text-slate-600",
  pending_review: "bg-amber-50 text-amber-700",
  approved: "bg-green-50 text-green-700",
  rejected: "bg-red-50 text-red-700",
  archived: "bg-blue-50 text-blue-700",
};
const prettify = (s) =>
  s == null ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function ReportStatusBadge({ status }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${STYLES[status] || "bg-slate-100 text-slate-600"}`}>
      {prettify(status)}
    </span>
  );
}
