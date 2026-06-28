// HighRiskKpiList (CP20A): quick list from GET /dashboard/high-risk-kpis.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function HighRiskKpiList({ highRiskKpis }) {
  const items = highRiskKpis || [];
  return (
    <Card>
      <CardHeader><CardTitle>High-Risk KPIs ({items.length})</CardTitle></CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <p className="py-6 text-center text-sm text-slate-500">No high-risk KPIs.</p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {items.map((k) => (
              <li key={k.kpi_id} className="py-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-slate-800">
                      <span className="text-slate-400">{k.code}</span> · {k.statement || "—"}
                    </p>
                    <p className="mt-0.5 text-xs text-slate-500">
                      {k.teras_number ? `Teras ${k.teras_number}` : "Teras —"}
                      {k.pic_email ? ` · ${k.pic_email}` : ""}
                    </p>
                  </div>
                  <span className="shrink-0 rounded-full bg-red-50 px-2.5 py-0.5 text-xs font-medium text-red-700">
                    High
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
