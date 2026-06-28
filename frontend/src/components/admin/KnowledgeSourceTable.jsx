// KnowledgeSourceTable (CP20F): RAG knowledge sources + process action.
import { Button } from "../ui/button";

const prettify = (s) => (s == null || s === "" ? "—" : String(s).replace(/_/g, " "));
const STATUS_TONE = {
  registered: "bg-slate-100 text-slate-600", pending_validation: "bg-amber-50 text-amber-700",
  processed: "bg-green-50 text-green-700", active: "bg-green-50 text-green-700",
  error: "bg-red-50 text-red-700",
};

export default function KnowledgeSourceTable({ sources, onProcess, processingId }) {
  const rows = sources || [];
  if (rows.length === 0) {
    return <div className="rounded-xl border border-slate-200 bg-white py-10 text-center text-sm text-slate-500">No knowledge sources registered.</div>;
  }
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="max-h-[28rem] overflow-auto">
        <table className="w-full min-w-[680px] text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Title</th>
              <th className="px-4 py-2 font-medium">Type</th>
              <th className="px-4 py-2 font-medium">Category</th>
              <th className="px-4 py-2 font-medium">Reliability</th>
              <th className="px-4 py-2 font-medium">Status</th>
              <th className="px-4 py-2 font-medium text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((s) => (
              <tr key={s.id} className="hover:bg-slate-50">
                <td className="px-4 py-2 font-medium text-slate-700">{s.title || "—"}</td>
                <td className="px-4 py-2 text-slate-600">{prettify(s.type)}</td>
                <td className="px-4 py-2 text-slate-600">{prettify(s.category)}</td>
                <td className="px-4 py-2 text-slate-600">{prettify(s.reliability)}</td>
                <td className="px-4 py-2">
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_TONE[s.status] || "bg-slate-100 text-slate-600"}`}>
                    {prettify(s.status)}
                  </span>
                </td>
                <td className="px-4 py-2 text-right">
                  <Button variant="outline" onClick={() => onProcess(s.id)} disabled={processingId === s.id}>
                    {processingId === s.id ? "Processing…" : "Process"}
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
