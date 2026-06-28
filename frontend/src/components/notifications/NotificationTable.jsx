// NotificationTable (CP20D): notification list from GET /notifications.
import NotificationStatusBadge from "./NotificationStatusBadge";

const prettify = (s) =>
  s == null || s === "" ? "—" : String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function NotificationTable({ notifications, selectedId, onSelect }) {
  const rows = notifications || [];
  if (rows.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white py-12 text-center text-sm text-slate-500">
        No notifications yet. Draft one to get started.
      </div>
    );
  }
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="max-h-[34rem] overflow-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Recipient</th>
              <th className="px-4 py-2 font-medium">Subject</th>
              <th className="px-4 py-2 font-medium">Type</th>
              <th className="px-4 py-2 font-medium">Status</th>
              <th className="px-4 py-2 font-medium">Retries</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((n) => (
              <tr key={n.id} onClick={() => onSelect?.(n)}
                  className={`cursor-pointer hover:bg-slate-50 ${selectedId === n.id ? "bg-blue-50/50" : ""}`}>
                <td className="px-4 py-2 text-slate-700">{n.recipient || "—"}</td>
                <td className="max-w-xs px-4 py-2 text-slate-700"><span className="line-clamp-1">{n.subject || "—"}</span></td>
                <td className="px-4 py-2 text-slate-600">{prettify(n.type)}</td>
                <td className="px-4 py-2"><NotificationStatusBadge status={n.status} /></td>
                <td className="px-4 py-2 text-slate-600">{n.retry_count ?? 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
