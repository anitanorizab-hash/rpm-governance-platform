// ExecutiveSummary (CP20E): the deterministic/AI-composed executive summary text.
export default function ExecutiveSummary({ text }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Executive Summary</p>
      <p className="mt-1 text-sm leading-relaxed text-slate-700">{text || "—"}</p>
    </div>
  );
}
