// SystemHealthCard (CP20F): API liveness + readiness. No secrets.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

function Dot({ ok }) {
  return <span className={`inline-block h-2.5 w-2.5 rounded-full ${ok ? "bg-green-500" : "bg-amber-500"}`} />;
}

export default function SystemHealthCard({ health, ready }) {
  const h = health || {};
  const r = ready || {};
  const checks = r.checks || {};
  return (
    <Card>
      <CardHeader><CardTitle>System Health</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex items-center gap-2"><Dot ok={h.status === "ok"} /><span>API: <span className="font-medium">{h.status || "—"}</span></span></div>
          <div className="flex items-center gap-2"><Dot ok={r.status === "ready"} /><span>Readiness: <span className="font-medium">{r.status || "—"}</span></span></div>
          <div className="text-slate-600">App: <span className="font-medium text-slate-800">{h.app_name || "—"}</span></div>
          <div className="text-slate-600">Mode: <span className="font-medium text-slate-800">{h.mode || "—"}</span></div>
          <div className="text-slate-600">Version: <span className="font-medium text-slate-800">{h.version || "—"}</span></div>
        </div>
        {Object.keys(checks).length > 0 && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Readiness checks</p>
            <div className="mt-1 flex flex-wrap gap-2">
              {Object.entries(checks).map(([k, v]) => (
                <span key={k} className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs text-slate-600">
                  {k}: <span className="font-medium text-slate-800">{v}</span>
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
