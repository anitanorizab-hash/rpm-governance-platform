// PpdComparisonPanel (V1.1): cross-PPD comparison view from GET /dashboard/ppd-comparison.
// Highlights top/lowest/highest-risk PPDs, charts achievement & high-risk by PPD, and lists detail.
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const shortName = (n) => (n || "").replace(/^PPD\s+/i, "");

export default function PpdComparisonPanel({ comparison }) {
  const ppds = comparison?.ppds || [];

  if (ppds.length === 0) {
    return (
      <Card>
        <CardHeader><CardTitle>PPD Comparison</CardTitle></CardHeader>
        <CardContent>
          <p className="py-8 text-center text-sm text-slate-500">No PPDs available to compare.</p>
        </CardContent>
      </Card>
    );
  }

  const achData = ppds.map((p) => ({ name: shortName(p.name), rate: Math.round((p.achievement_rate || 0) * 100) }));
  const riskData = ppds.map((p) => ({ name: shortName(p.name), high_risk: p.high_risk || 0 }));

  const highlights = [
    { label: "Top Performing PPD", value: comparison?.top_performer, tone: "text-green-700" },
    { label: "Lowest Performing PPD", value: comparison?.lowest_performer, tone: "text-amber-700" },
    { label: "Highest-Risk PPD", value: comparison?.highest_risk, tone: "text-red-700" },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {highlights.map((h) => (
          <Card key={h.label}>
            <CardContent className="py-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">{h.label}</p>
              <p className={`mt-1 text-lg font-semibold ${h.tone}`}>{h.value || "—"}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Achievement Rate by PPD (%)</CardTitle></CardHeader>
          <CardContent>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={achData} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#64748b" }} />
                  <YAxis allowDecimals={false} domain={[0, 100]} tick={{ fontSize: 12, fill: "#64748b" }} />
                  <Tooltip />
                  <Bar dataKey="rate" name="Achievement %" fill="#059669" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>High-Risk KPIs by PPD</CardTitle></CardHeader>
          <CardContent>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={riskData} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#64748b" }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: "#64748b" }} />
                  <Tooltip />
                  <Bar dataKey="high_risk" name="High-risk KPIs" fill="#dc2626" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>PPD Comparison ({ppds.length})</CardTitle></CardHeader>
        <CardContent className="px-0 py-0">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[720px] text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-4 py-2 font-medium">Rank</th>
                  <th className="px-4 py-2 font-medium">PPD</th>
                  <th className="px-4 py-2 font-medium">KPIs</th>
                  <th className="px-4 py-2 font-medium">Achieved</th>
                  <th className="px-4 py-2 font-medium">Achievement %</th>
                  <th className="px-4 py-2 font-medium">High Risk</th>
                  <th className="px-4 py-2 font-medium">Missing Info</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {ppds.map((p) => (
                  <tr key={p.organisation_id} className="hover:bg-slate-50">
                    <td className="px-4 py-2 text-slate-600">{p.rank}</td>
                    <td className="px-4 py-2 font-medium text-slate-700">{p.name}</td>
                    <td className="px-4 py-2 text-slate-600">{p.total_kpis}</td>
                    <td className="px-4 py-2 text-slate-600">{p.achieved}</td>
                    <td className="px-4 py-2 text-slate-600">{Math.round((p.achievement_rate || 0) * 100)}%</td>
                    <td className="px-4 py-2 text-slate-600">{p.high_risk}</td>
                    <td className="px-4 py-2 text-slate-600">{p.missing_information}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
