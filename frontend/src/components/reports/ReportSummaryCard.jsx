// ReportSummaryCard (CP20D): KPI / Risk / Financial / Recommendation summaries from report.content.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const prettify = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function Dist({ data }) {
  const entries = Object.entries(data || {}).filter(([, v]) => v != null);
  if (!entries.length) return <p className="text-sm text-slate-500">—</p>;
  return (
    <div className="flex flex-wrap gap-2">
      {entries.map(([k, v]) => (
        <span key={k} className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs text-slate-600">
          {prettify(k)}: <span className="font-medium text-slate-800">{v}</span>
        </span>
      ))}
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div>
      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-slate-400">{title}</p>
      {children}
    </div>
  );
}

export default function ReportSummaryCard({ content }) {
  const c = content || {};
  const fds = c.budget_fds_summary || {};
  return (
    <Card>
      <CardHeader><CardTitle>Report Summary</CardTitle></CardHeader>
      <CardContent className="space-y-4">
        <Section title="KPI Achievement Overview"><Dist data={c.kpi_achievement_overview} /></Section>
        <Section title="By Teras"><Dist data={c.by_teras} /></Section>
        <Section title="Risk Summary"><Dist data={c.risk_summary} /></Section>
        <Section title="Financial Summary (FDS)">
          <div className="space-y-2">
            <p className="text-sm text-slate-600">
              Recommendations: <span className="font-medium text-slate-800">{fds.total_recommendations ?? 0}</span>
            </p>
            <Dist data={fds.financial_risk_distribution} />
          </div>
        </Section>
        <Section title="Missing Information">
          <p className="text-sm text-slate-700">{c.missing_information_summary ?? 0} KPI(s)</p>
        </Section>
        <Section title="Recommendation Summary">
          <p className="text-sm text-slate-700">
            {typeof c.recommendations === "string" ? c.recommendations : (c.summary || c.narrative || "—")}
          </p>
        </Section>
      </CardContent>
    </Card>
  );
}
