// BudgetInsightsPanel (CP20E): FDS budget insights from briefing.budget_fds_insights.
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

export default function BudgetInsightsPanel({ fds }) {
  const f = fds || {};
  return (
    <Card>
      <CardHeader><CardTitle>Financial Decision Support Insights</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <p className="text-sm text-slate-600">
          Strategic recommendations: <span className="font-medium text-slate-800">{f.total_recommendations ?? 0}</span>
        </p>
        <div>
          <p className="mb-1 text-xs font-medium uppercase tracking-wide text-slate-400">Financial Risk Distribution</p>
          <Dist data={f.financial_risk_distribution} />
        </div>
      </CardContent>
    </Card>
  );
}
