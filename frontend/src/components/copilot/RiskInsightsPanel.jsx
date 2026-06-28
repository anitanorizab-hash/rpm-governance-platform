// RiskInsightsPanel (CP20E): high-risk KPI insights from briefing.key_risks.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const prettify = (s) => (s == null ? "—" : String(s).replace(/_/g, " "));

export default function RiskInsightsPanel({ keyRisks }) {
  const rows = keyRisks || [];
  return (
    <Card>
      <CardHeader><CardTitle>Risk Insights</CardTitle></CardHeader>
      <CardContent>
        {rows.length === 0 ? (
          <p className="py-4 text-center text-sm text-slate-500">No high-risk KPIs.</p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {rows.map((r, i) => (
              <li key={i} className="flex items-center justify-between py-2">
                <span className="text-sm text-slate-700">
                  <span className="font-medium">{r.code}</span>
                  <span className="text-slate-400"> · Teras {r.teras ?? "—"}</span>
                </span>
                <span className="rounded-full bg-red-50 px-2 py-0.5 text-xs font-medium text-red-700">
                  {prettify(r.risk)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
