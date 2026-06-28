// TerasSummaryChart (CP20A): KPI count by Teras 1–7 from GET /dashboard/teras-summary.
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const TERAS_COLORS = ["#1d4ed8", "#0891b2", "#059669", "#65a30d", "#d97706", "#dc2626", "#7c3aed"];

export default function TerasSummaryChart({ terasSummary }) {
  const data = (terasSummary || []).map((t) => ({
    name: `Teras ${t.teras_number}`,
    teras: t.teras_number,
    count: t.kpi_count || 0,
  }));

  return (
    <Card>
      <CardHeader><CardTitle>KPI Count by Teras (1–7)</CardTitle></CardHeader>
      <CardContent>
        {data.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">No KPI data available.</p>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#64748b" }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: "#64748b" }} />
                <Tooltip />
                <Bar dataKey="count" name="KPIs" radius={[4, 4, 0, 0]}>
                  {data.map((d, i) => (
                    <Cell key={d.name} fill={TERAS_COLORS[(d.teras - 1) % TERAS_COLORS.length] || "#1d4ed8"} />
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
