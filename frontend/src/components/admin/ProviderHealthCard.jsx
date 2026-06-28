// ProviderHealthCard (CP20F): active LLM + embedding provider health. No API keys/secrets shown.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

function ProviderRow({ label, p }) {
  if (!p) return (
    <div className="flex items-center justify-between py-2">
      <span className="text-sm text-slate-600">{label}</span>
      <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-500">unavailable</span>
    </div>
  );
  const ok = p.configured;
  return (
    <div className="flex items-center justify-between py-2">
      <span className="text-sm text-slate-700">{label}: <span className="font-medium">{p.provider}</span></span>
      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${ok ? "bg-green-50 text-green-700" : "bg-amber-50 text-amber-700"}`}>
        {p.status || (ok ? "configured" : "not_configured")}
      </span>
    </div>
  );
}

export default function ProviderHealthCard({ providers }) {
  const p = providers || {};
  return (
    <Card>
      <CardHeader><CardTitle>Provider Health</CardTitle></CardHeader>
      <CardContent className="divide-y divide-slate-100">
        <div className="flex items-center justify-between py-2">
          <span className="text-sm text-slate-600">Mode</span>
          <span className="font-medium text-slate-800">{p.mode || "—"}</span>
        </div>
        <ProviderRow label="LLM provider" p={p.llm} />
        <ProviderRow label="Embedding provider" p={p.embedding} />
        {Array.isArray(p.errors) && p.errors.length > 0 && (
          <div className="py-2">
            <p className="text-xs font-medium text-amber-700">Configuration notes</p>
            <ul className="mt-1 list-inside list-disc text-xs text-slate-600">
              {p.errors.map((e, i) => <li key={i}>{e}</li>)}
            </ul>
          </div>
        )}
        <p className="pt-2 text-[11px] text-slate-400">Provider keys are never displayed. Configuration is via config.md + .env.</p>
      </CardContent>
    </Card>
  );
}
