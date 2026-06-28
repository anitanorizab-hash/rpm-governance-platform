// KpiMappingTable (V1.2 restyle): premium table. Data binding and search behaviour unchanged.
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const RISK_BADGE = {
  high: "bg-red-50 text-danger", medium: "bg-amber-50 text-amber-600",
  low: "bg-green-50 text-success", unknown: "bg-slate-100 text-slate-600",
};
const prettify = (s) =>
  s == null ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function KpiMappingTable({ kpiMapping }) {
  const rows = kpiMapping || [];
  const [q, setQ] = useState("");
  const filtered = q
    ? rows.filter((r) =>
        [r.code, r.pic, r.sector, r.status, r.risk]
          .filter(Boolean)
          .some((v) => String(v).toLowerCase().includes(q.toLowerCase())))
    : rows;

  return (
    <Card>
      <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <CardTitle>KPI Mapping ({rows.length})</CardTitle>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Filter…"
          className="w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm focus:border-royal focus:outline-none focus:ring-2 focus:ring-royal/30 sm:w-56"
        />
      </CardHeader>
      <CardContent className="px-0 py-0">
        <div className="max-h-[28rem] overflow-auto">
          <table className="table-premium min-w-[760px]">
            <thead>
              <tr>
                <th>Code</th><th>Level</th><th>Organisation</th><th>Teras</th><th>PIC</th>
                <th>Sector</th><th>Status</th><th>Risk</th><th>Finance</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={9} className="px-4 py-6 text-center text-slate-500">No KPIs.</td></tr>
              ) : (
                filtered.map((r) => (
                  <tr key={r.kpi_id}>
                    <td className="font-semibold text-slate-700">{r.code}</td>
                    <td>
                      {r.organisation_type ? (
                        <span className={`badge ${r.organisation_type === "JPN" ? "bg-royal-50 text-royal-600" : "bg-violet-50 text-violet-700"}`}>{r.organisation_type}</span>
                      ) : "—"}
                    </td>
                    <td className="text-slate-600">{r.organisation_name || "—"}</td>
                    <td className="text-slate-600">{r.teras_number ?? "—"}</td>
                    <td className="text-slate-600">{r.pic || "—"}</td>
                    <td className="text-slate-600">{r.sector || "—"}</td>
                    <td className="text-slate-600">{prettify(r.status)}</td>
                    <td><span className={`badge ${RISK_BADGE[r.risk] || RISK_BADGE.unknown}`}>{prettify(r.risk)}</span></td>
                    <td className="text-slate-600">{prettify(r.finance_status)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
