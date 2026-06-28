// SubmissionHistory (CP20B): monthly-update history from GET /kpis/{id}/monthly-updates.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const prettify = (s) =>
  s == null || s === "" ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

const fmtDate = (s) => {
  if (!s) return "—";
  const d = new Date(s);
  return isNaN(d) ? s : d.toLocaleDateString();
};

export default function SubmissionHistory({ updates }) {
  const rows = (updates || [])
    .slice()
    .sort((a, b) => (b.reporting_year - a.reporting_year) || (b.reporting_month - a.reporting_month));

  return (
    <Card>
      <CardHeader><CardTitle>Submission History ({rows.length})</CardTitle></CardHeader>
      <CardContent className="px-0 py-0">
        {rows.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">No monthly updates submitted yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-4 py-2 font-medium">Period</th>
                  <th className="px-4 py-2 font-medium">Achievement</th>
                  <th className="px-4 py-2 font-medium">Status</th>
                  <th className="px-4 py-2 font-medium">Finance</th>
                  <th className="px-4 py-2 font-medium">Evidence</th>
                  <th className="px-4 py-2 font-medium">Submitted</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {rows.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50">
                    <td className="px-4 py-2 font-medium text-slate-700">
                      {u.reporting_year}-{String(u.reporting_month).padStart(2, "0")}
                    </td>
                    <td className="px-4 py-2 text-slate-600">{u.achievement_value || "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{prettify(u.achievement_status)}</td>
                    <td className="px-4 py-2 text-slate-600">{prettify(u.finance_status)}</td>
                    <td className="px-4 py-2 text-slate-600">{u.evidence_ref || "—"}</td>
                    <td className="px-4 py-2 text-slate-600">{fmtDate(u.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
