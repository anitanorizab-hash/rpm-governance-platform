// KpiMappingTable (CP20A): KPI → Teras/PIC/sector/status mapping from GET /dashboard/kpi-mapping.
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const RISK_BADGE = {
  high: "bg-red-50 text-red-700", medium: "bg-amber-50 text-amber-700",
  low: "bg-green-50 text-green-700", unknown: "bg-slate-100 text-slate-600",
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
          className="w-full rounded-md border border-slate-200 px-3 py-1.5 text-sm sm:w-56"
        />
      </CardHeader>
      <CardContent className="px-0 py-0">
        <div className="max-h-[28rem] overflow-auto">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">Code</th>
                <th className="px-4 py-2 font-medium">Level</th>
                <th className="px-4 py-2 font-medium">Organisation</th>
                <th className="px-4 py-2 font-medium">Teras</th>
                <th className="px-4 py-2 font-medium">PIC</th>
                <th className="px-4 py-2 font-medium">Sector</th>
                <th className="px-4 py-2 font-medium">Status</th>
                <th className="px-4 py-2 font-medium">Risk</th>
                <th className="px-4 py-2 font-medium">Finance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.length === 0 ? (
                <tr><td colSpan={9} className="px-4 py-6 text-center text-slate-500">No KPIs.</td></tr>
              ) : (
                filtered.map((r) => (
                  <tr key={r.kpi_id} className="hover:bg-slate-50">
                    <td className="px-4 py-2 font-medium text-slate-700">{r.code}</td>
                    <td className="px-4 py-2">
                      {r.organisation_type ? (
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${r.organisation_type === "JPN" ? "bg-blue-50 text-blue-700" : "bg-violet-50 text-violet-700"}`}>
                          {r.organisation_type}
                        </span>
                      ) : "—"}
                    </td>
                    <td className="px-4 py-2 text-slate-600">{r.organisation_name || "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{r.teras_number ?? "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{r.pic || "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{r.sector || "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{prettify(r.status)}</td>
                    <td className="px-4 py-2">
                      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${RISK_BADGE[r.risk] || RISK_BADGE.unknown}`}>
                        {prettify(r.risk)}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-slate-600">{prettify(r.finance_status)}</td>
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
