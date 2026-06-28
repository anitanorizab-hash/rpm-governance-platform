// NotificationQueueStatus (CP20D): the email queue (GET /notifications/email-queue) with delivery state.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import NotificationStatusBadge from "./NotificationStatusBadge";

export default function NotificationQueueStatus({ queue, canView }) {
  if (!canView) return null;
  const rows = queue || [];
  return (
    <Card>
      <CardHeader><CardTitle>Email Queue ({rows.length})</CardTitle></CardHeader>
      <CardContent className="px-0 py-0">
        {rows.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">The email queue is empty.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-4 py-2 font-medium">Recipient</th>
                  <th className="px-4 py-2 font-medium">Subject</th>
                  <th className="px-4 py-2 font-medium">Delivery</th>
                  <th className="px-4 py-2 font-medium">Retries</th>
                  <th className="px-4 py-2 font-medium">Failure</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {rows.map((n) => (
                  <tr key={n.id} className="hover:bg-slate-50">
                    <td className="px-4 py-2 text-slate-700">{n.recipient || "—"}</td>
                    <td className="max-w-xs px-4 py-2 text-slate-700"><span className="line-clamp-1">{n.subject || "—"}</span></td>
                    <td className="px-4 py-2"><NotificationStatusBadge status={n.status} /></td>
                    <td className="px-4 py-2 text-slate-600">{n.retry_count ?? 0}</td>
                    <td className="px-4 py-2 text-slate-600">{n.failure_reason || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <p className="px-4 py-2 text-[11px] text-slate-400">
          Delivery is dry-run unless production SMTP is configured — no email is sent.
        </p>
      </CardContent>
    </Card>
  );
}
