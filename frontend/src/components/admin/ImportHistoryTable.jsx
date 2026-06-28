// ImportHistoryTable (CP20F): Excel import batches (read-only). Import-once status visible.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const fmt = (s) => { if (!s) return "—"; const d = new Date(s); return isNaN(d) ? s : d.toLocaleString(); };
const STATUS_TONE = {
  completed: "bg-green-50 text-green-700", blocked: "bg-amber-50 text-amber-700",
  failed: "bg-red-50 text-red-700",
};

export default function ImportHistoryTable({ batches }) {
  const rows = batches || [];
  return (
    <Card>
      <CardHeader><CardTitle>Import History ({rows.length})</CardTitle></CardHeader>
      <CardContent className="space-y-2 px-0 py-0">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[680px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">File</th>
                <th className="px-4 py-2 font-medium">Plan</th>
                <th className="px-4 py-2 font-medium">Rows</th>
                <th className="px-4 py-2 font-medium">Imported</th>
                <th className="px-4 py-2 font-medium">Warnings</th>
                <th className="px-4 py-2 font-medium">Status</th>
                <th className="px-4 py-2 font-medium">When</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.length === 0 ? (
                <tr><td colSpan={7} className="px-4 py-6 text-center text-slate-500">No import batches.</td></tr>
              ) : rows.map((b) => (
                <tr key={b.id} className="hover:bg-slate-50">
                  <td className="px-4 py-2 font-medium text-slate-700">{b.filename || "—"}</td>
                  <td className="px-4 py-2 text-slate-600">{b.plan_type || "—"}</td>
                  <td className="px-4 py-2 text-slate-600">{b.rows_total}</td>
                  <td className="px-4 py-2 text-slate-600">{b.rows_imported}</td>
                  <td className="px-4 py-2 text-slate-600">{b.warnings_count}</td>
                  <td className="px-4 py-2">
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_TONE[b.status] || "bg-slate-100 text-slate-600"}`}>{b.status}</span>
                  </td>
                  <td className="px-4 py-2 text-slate-600">{fmt(b.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="px-4 py-2 text-[11px] text-slate-400">
          Excel is initial input only (import-once). Re-import requires an explicit admin override and is not available here.
        </p>
      </CardContent>
    </Card>
  );
}
