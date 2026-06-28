// BudgetSummaryChart (CP20A): finance-status distribution from GET /dashboard/budget-summary.
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

// Finance status values are advisory/deterministic labels from the backend.
const FINANCE_COLORS = {
  on_budget: "#059669", under_budget: "#0891b2", over_budget: "#dc2626",
  at_risk: "#d97706", not_reported: "#94a3b8",
};
const prettify = (s) =>
  String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function BudgetSummaryChart({ budgetSummary }) {
  const overall = budgetSummary?.overall || {};
  const data = Object.entries(overall)
    .map(([k, v]) => ({ name: prettify(k), key: k, value: v }))
    .filter((d) => d.value > 0);
  const total = data.reduce((s, d) => s + d.value, 0);

  return (
    <Card>
      <CardHeader><CardTitle>Budget Summary</CardTitle></CardHeader>
      <CardContent>
        {total === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">No budget data reported.</p>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: "#64748b" }} interval={0} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: "#64748b" }} />
                <Tooltip />
                <Bar dataKey="value" name="KPIs" radius={[4, 4, 0, 0]}>
                  {data.map((d) => (
                    <Cell key={d.key} fill={FINANCE_COLORS[d.key] || "#1d4ed8"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
