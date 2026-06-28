// RiskSummaryChart (CP20A): overall risk distribution from GET /dashboard/risk-summary.
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const RISK_COLORS = {
  high: "#dc2626", medium: "#d97706", low: "#059669", unknown: "#94a3b8",
};
const LABELS = { high: "High", medium: "Medium", low: "Low", unknown: "Unknown" };

export default function RiskSummaryChart({ riskSummary }) {
  const overall = riskSummary?.overall || {};
  const data = Object.entries(overall)
    .map(([k, v]) => ({ name: LABELS[k] || k, key: k, value: v }))
    .filter((d) => d.value > 0);
  const total = data.reduce((s, d) => s + d.value, 0);

  return (
    <Card>
      <CardHeader><CardTitle>Risk Summary</CardTitle></CardHeader>
      <CardContent>
        {total === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">No risk data available.</p>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%"
                     innerRadius={50} outerRadius={90} paddingAngle={2}>
                  {data.map((d) => (
                    <Cell key={d.key} fill={RISK_COLORS[d.key] || "#94a3b8"} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
