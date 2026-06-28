// AuditLogTable (CP20F): read-only audit trail with filters + expandable detail. No edit/delete.
import { Fragment, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";

const fmt = (s) => { if (!s) return "—"; const d = new Date(s); return isNaN(d) ? s : d.toLocaleString(); };

export default function AuditLogTable({ logs, filters, onChange, onApply, onReset }) {
  const rows = logs || [];
  const [openId, setOpenId] = useState(null);
  const set = (k, v) => onChange({ ...filters, [k]: v });

  return (
    <Card>
      <CardHeader><CardTitle>Audit Logs ({rows.length})</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <div className="flex flex-wrap items-end gap-3">
          <div><Label>Entity Type</Label><Input value={filters.entity_type || ""} onChange={(e) => set("entity_type", e.target.value)} placeholder="kpi, report…" className="w-44" /></div>
          <div><Label>Action</Label><Input value={filters.action || ""} onChange={(e) => set("action", e.target.value)} placeholder="kpi_update…" className="w-44" /></div>
          <Button onClick={onApply}>Apply</Button>
          <Button variant="outline" onClick={onReset}>Reset</Button>
        </div>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full min-w-[680px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">When</th>
                <th className="px-4 py-2 font-medium">Entity</th>
                <th className="px-4 py-2 font-medium">Action</th>
                <th className="px-4 py-2 font-medium">Actor</th>
                <th className="px-4 py-2 font-medium"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.length === 0 ? (
                <tr><td colSpan={5} className="px-4 py-6 text-center text-slate-500">No audit entries.</td></tr>
              ) : rows.map((l) => (
                <Fragment key={l.id}>
                  <tr className="hover:bg-slate-50">
                    <td className="px-4 py-2 text-slate-600">{fmt(l.created_at)}</td>
                    <td className="px-4 py-2 text-slate-600">{l.entity_type}{l.entity_id ? ` · ${String(l.entity_id).slice(0, 8)}` : ""}</td>
                    <td className="px-4 py-2 font-medium text-slate-700">{l.action}</td>
                    <td className="px-4 py-2 text-slate-600">{l.actor_id ? String(l.actor_id).slice(0, 8) : "—"}</td>
                    <td className="px-4 py-2 text-right">
                      <button className="text-xs text-blue-700 hover:underline" onClick={() => setOpenId(openId === l.id ? null : l.id)}>
                        {openId === l.id ? "Hide" : "Detail"}
                      </button>
                    </td>
                  </tr>
                  {openId === l.id && (
                    <tr className="bg-slate-50">
                      <td colSpan={5} className="px-4 py-3 text-xs text-slate-600">
                        <div className="grid grid-cols-1 gap-1 sm:grid-cols-2">
                          <div><span className="font-medium">Before:</span> {l.before || "—"}</div>
                          <div><span className="font-medium">After:</span> {l.after || "—"}</div>
                          <div><span className="font-medium">Reason:</span> {l.reason || "—"}</div>
                          <div><span className="font-medium">Request:</span> {l.request_id || "—"}</div>
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[11px] text-slate-400">Audit logs are append-only — they cannot be edited or deleted.</p>
      </CardContent>
    </Card>
  );
}
