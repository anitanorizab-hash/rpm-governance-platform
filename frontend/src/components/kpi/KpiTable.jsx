// KpiTable (V1.2 restyle): premium table. Columns, navigation and data binding unchanged.
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
      <div className="rounded-2xl border border-slate-200 bg-white py-12 text-center text-sm text-slate-500 shadow-card">
        No KPIs match the current filters.
      </div>
    );
  }

  return (
    <div className="table-wrap">
      <div className="max-h-[34rem] overflow-auto">
        <table className="table-premium min-w-[980px]">
          <thead>
            <tr>
              <th>Code</th><th>KPI Statement</th><th>Level</th><th>Organisation</th>
              <th>Teras</th><th>Department</th><th>PIC</th><th>Status</th><th>Completeness</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((k) => (
              <tr key={k.id} onClick={() => navigate(`/app/kpis/${k.id}`)} className="cursor-pointer">
                <td className="font-semibold text-royal-600">{k.code}</td>
                <td className="max-w-md text-slate-700"><span className="line-clamp-2">{k.statement || "—"}</span></td>
                <td>
                  {k.organisation_type ? (
                    <span className={`badge ${k.organisation_type === "JPN" ? "bg-royal-50 text-royal-600" : "bg-violet-50 text-violet-700"}`}>{k.organisation_type}</span>
                  ) : "—"}
                </td>
                <td className="text-slate-600">{k.organisation_name || "—"}</td>
                <td className="text-slate-600">{k.teras_number ?? "—"}</td>
                <td className="text-slate-600">{k.sector || "—"}</td>
                <td className="text-slate-600">{k.pic_email || "—"}</td>
                <td className="text-slate-600">{prettify(k.status)}</td>
                <td>
                  {k.is_complete ? (
                    <span className="badge bg-green-50 text-success">Complete</span>
                  ) : (
                    <span className="badge bg-amber-50 text-amber-600">Incomplete</span>
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
