// AutomationPanel (V1.1.1): administrator-triggered, HITL-safe draft generation.
// Generates report + notification DRAFTS; they appear in the approval queues — nothing is sent here.
import { useState } from "react";
import { automationService, AUTOMATION_TYPES } from "../../services/automationService";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";

export default function AutomationPanel() {
  const [selected, setSelected] = useState(AUTOMATION_TYPES.map((t) => t.value));
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const toggle = (v) =>
    setSelected((s) => (s.includes(v) ? s.filter((x) => x !== v) : [...s, v]));

  async function run() {
    setBusy(true); setError(null); setResult(null);
    try {
      setResult(await automationService.run({ types: selected, limit: 10 }));
    } catch (err) {
      setError(err.message || "Automation failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <CardHeader><CardTitle>Automated Draft Generation</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
          Generates <span className="font-medium">drafts only</span>. Drafts go to the approval queues —
          nothing is queued or emailed without human approval, a valid recipient and configured email (ASM-11).
        </div>
        <div className="flex flex-wrap gap-3">
          {AUTOMATION_TYPES.map((t) => (
            <label key={t.value} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" checked={selected.includes(t.value)} onChange={() => toggle(t.value)} />
              {t.label}
            </label>
          ))}
        </div>
        <Button onClick={run} disabled={busy || selected.length === 0}>
          {busy ? "Generating drafts…" : "Generate Drafts"}
        </Button>
        {error && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}
        {result && (
          <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-800">
            <p className="font-medium">Drafts generated (pending approval):</p>
            <ul className="mt-1 list-inside list-disc">
              {Object.entries(result.generated || {}).map(([k, v]) => <li key={k}>{k}: {v}</li>)}
            </ul>
            {result.skipped_no_valid_email && Object.values(result.skipped_no_valid_email).some((n) => n > 0) && (
              <p className="mt-1 text-xs text-slate-500">
                Skipped (no valid recipient email): {Object.entries(result.skipped_no_valid_email).map(([k, v]) => `${k}=${v}`).join(", ")}
              </p>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
