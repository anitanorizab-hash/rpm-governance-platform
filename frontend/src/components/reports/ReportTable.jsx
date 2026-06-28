// ReportTable (CP20D): report list from GET /reports.
import { useNavigate } from "react-router-dom";
import ReportStatusBadge from "./ReportStatusBadge";

export default function ReportTable({ reports }) {
  const navigate = useNavigate();
  const rows = reports || [];

  if (rows.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white py-12 text-center text-sm text-slate-500">
        No reports yet. Generate a draft to get started.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="max-h-[34rem] overflow-auto">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Title</th>
              <th className="px-4 py-2 font-medium">Period</th>
              <th className="px-4 py-2 font-medium">Type</th>
              <th className="px-4 py-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((r) => (
              <tr key={r.id} onClick={() => navigate(`/app/reports/${r.id}`)} className="cursor-pointer hover:bg-slate-50">
                <td className="px-4 py-2 font-medium text-blue-700">{r.title || "(untitled)"}</td>
                <td className="px-4 py-2 text-slate-600">{r.period || "—"}</td>
                <td className="px-4 py-2 text-slate-600">{r.type || "—"}</td>
                <td className="px-4 py-2"><ReportStatusBadge status={r.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
