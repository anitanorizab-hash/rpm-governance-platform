// BudgetStatusBadge (CP20C): colour-coded badge for finance status or financial risk level.
const RISK_STYLES = {
  high: "bg-red-50 text-red-700 border-red-200",
  medium: "bg-amber-50 text-amber-700 border-amber-200",
  low: "bg-green-50 text-green-700 border-green-200",
};
const FINANCE_STYLES = {
  received: "bg-green-50 text-green-700 border-green-200",
  not_required: "bg-slate-100 text-slate-600 border-slate-200",
  will_be_received: "bg-amber-50 text-amber-700 border-amber-200",
  pending: "bg-amber-50 text-amber-700 border-amber-200",
  insufficient: "bg-red-50 text-red-700 border-red-200",
  not_received: "bg-red-50 text-red-700 border-red-200",
  not_reported: "bg-slate-100 text-slate-500 border-slate-200",
};
const prettify = (s) =>
  s == null || s === "" ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function BudgetStatusBadge({ value, kind = "finance" }) {
  const styles = kind === "risk" ? RISK_STYLES : FINANCE_STYLES;
  const cls = styles[value] || "bg-slate-100 text-slate-600 border-slate-200";
  return (
    <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-medium ${cls}`}>
      {prettify(value)}
    </span>
  );
}
