// KpiTable (CP20B): KPI list rendered from GET /kpis (KPIListItem).
// Note: /kpis returns code/statement/teras/sector/status/pic/completeness.
// Risk and finance status are not in this payload — they are shown on the KPI detail page.
import { useNavigate } from "react-router-dom";

const prettify = (s) =>
  s == null || s === "" ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function KpiTable({ kpis }) {
  const navigate = useNavigate();
  const rows = kpis || [];

  if (rows.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white py-12 text-center text-sm text-slate-500">
        No KPIs match the current filters.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="max-h-[34rem] overflow-auto">
        <table className="w-full min-w-[980px] text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Code</th>
              <th className="px-4 py-2 font-medium">KPI Statement</th>
              <th className="px-4 py-2 font-medium">Level</th>
              <th className="px-4 py-2 font-medium">Organisation</th>
              <th className="px-4 py-2 font-medium">Teras</th>
              <th className="px-4 py-2 font-medium">Department</th>
              <th className="px-4 py-2 font-medium">PIC</th>
              <th className="px-4 py-2 font-medium">Status</th>
              <th className="px-4 py-2 font-medium">Completeness</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((k) => (
              <tr
                key={k.id}
                onClick={() => navigate(`/app/kpis/${k.id}`)}
                className="cursor-pointer hover:bg-slate-50"
              >
                <td className="px-4 py-2 font-medium text-blue-700">{k.code}</td>
                <td className="max-w-md px-4 py-2 text-slate-700">
                  <span className="line-clamp-2">{k.statement || "—"}</span>
                </td>
                <td className="px-4 py-2">
                  {k.organisation_type ? (
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${k.organisation_type === "JPN" ? "bg-blue-50 text-blue-700" : "bg-violet-50 text-violet-700"}`}>
                      {k.organisation_type}
                    </span>
                  ) : "—"}
                </td>
                <td className="px-4 py-2 text-slate-600">{k.organisation_name || "—"}</td>
                <td className="px-4 py-2 text-slate-600">{k.teras_number ?? "—"}</td>
                <td className="px-4 py-2 text-slate-600">{k.sector || "—"}</td>
                <td className="px-4 py-2 text-slate-600">{k.pic_email || "—"}</td>
                <td className="px-4 py-2 text-slate-600">{prettify(k.status)}</td>
                <td className="px-4 py-2">
                  {k.is_complete ? (
                    <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">Complete</span>
                  ) : (
                    <span className="rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">Incomplete</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
