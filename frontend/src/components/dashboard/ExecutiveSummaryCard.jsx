// ExecutiveSummaryCard (CP20A): deterministic summary from GET /dashboard/executive-summary.
// Per ASM-11, this text is advisory and deterministic — no AI provider is called here.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function ExecutiveSummaryCard({ executiveSummary }) {
  if (!executiveSummary) return null;
  const h = executiveSummary.highlights || {};
  const chips = [
    { label: "Total KPIs", value: h.total_kpis },
    { label: "High Risk", value: h.high_risk },
    { label: "Missing Info", value: h.missing_information },
    { label: "Incomplete / Not Updated", value: h.incomplete_or_not_updated },
    { label: "Top Teras", value: h.top_teras ? `Teras ${h.top_teras}` : "—" },
  ];

  return (
    <Card className="border-blue-100 bg-blue-50/40">
      <CardHeader className="border-blue-100">
        <CardTitle className="flex items-center gap-2">
          Executive Summary
          <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-600">
            {executiveSummary.generated_by || "deterministic"}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-sm leading-relaxed text-slate-700">{executiveSummary.text}</p>
        <div className="flex flex-wrap gap-2">
          {chips.map((c) => (
            <span key={c.label} className="rounded-md border border-blue-100 bg-white px-2.5 py-1 text-xs text-slate-600">
              <span className="font-medium text-slate-800">{c.value ?? 0}</span> {c.label}
            </span>
          ))}
        </div>
        <p className="text-[11px] text-slate-400">
          Advisory summary — final decisions remain with authorised officers (ASM-11).
        </p>
      </CardContent>
    </Card>
  );
}
