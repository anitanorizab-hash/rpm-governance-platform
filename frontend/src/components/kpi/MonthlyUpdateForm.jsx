// MonthlyUpdateForm (CP20B): submit an in-system monthly KPI update (POST /monthly-updates).
// Achievement Status is DERIVED server-side (achievement value vs target) — it is not an input,
// so it is shown read-only here and returned after submission.
import { useState } from "react";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";
import { FINANCE_STATUSES } from "../../services/monthlyUpdateService";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

const now = new Date();

export default function MonthlyUpdateForm({ kpiId, onSubmit, submitting, error, success, derivedStatus }) {
  const [form, setForm] = useState({
    reporting_year: now.getFullYear(),
    reporting_month: now.getMonth() + 1,
    achievement_value: "",
    finance_status: "",
    evidence_ref: "",
    remarks: "",
    issue_description: "",
    proposed_action: "",
  });
  const [override, setOverride] = useState(false);
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  function submit(e) {
    e.preventDefault();
    const body = {
      kpi_id: kpiId,
      reporting_year: Number(form.reporting_year),
      reporting_month: Number(form.reporting_month),
      achievement_value: form.achievement_value || null,
      finance_status: form.finance_status || null,
      evidence_ref: form.evidence_ref || null,
      remarks: form.remarks || null,
      issue_description: form.issue_description || null,
      proposed_action: form.proposed_action || null,
    };
    onSubmit(body, override);
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label>Reporting Year</Label>
          <Input type="number" min={2020} max={2100} value={form.reporting_year}
                 onChange={(e) => set("reporting_year", e.target.value)} required />
        </div>
        <div>
          <Label>Reporting Month</Label>
          <select className={selectCls} value={form.reporting_month}
                  onChange={(e) => set("reporting_month", e.target.value)} required>
            {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <Label>Achievement Value</Label>
        <Input value={form.achievement_value} onChange={(e) => set("achievement_value", e.target.value)}
               placeholder="e.g. 85 or 85%" />
      </div>

      <div>
        <Label>Achievement Status (auto-derived)</Label>
        <Input value={derivedStatus || "Computed from achievement value vs target after submission"} disabled />
        <p className="mt-1 text-xs text-slate-500">
          Status is calculated by the system from the achievement value against the KPI target.
        </p>
      </div>

      <div>
        <Label>Finance Status</Label>
        <select className={selectCls} value={form.finance_status} onChange={(e) => set("finance_status", e.target.value)}>
          <option value="">— Select —</option>
          {FINANCE_STATUSES.map((f) => (
            <option key={f.value} value={f.value}>{f.label}</option>
          ))}
        </select>
      </div>

      <div>
        <Label>Evidence Reference</Label>
        <Input value={form.evidence_ref} onChange={(e) => set("evidence_ref", e.target.value)}
               placeholder="Document / link reference" />
      </div>

      <div>
        <Label>Remarks</Label>
        <textarea className={selectCls} rows={2} value={form.remarks} onChange={(e) => set("remarks", e.target.value)} />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <Label>Issue Description</Label>
          <textarea className={selectCls} rows={3} value={form.issue_description}
                    onChange={(e) => set("issue_description", e.target.value)} />
        </div>
        <div>
          <Label>Proposed Action</Label>
          <textarea className={selectCls} rows={3} value={form.proposed_action}
                    onChange={(e) => set("proposed_action", e.target.value)} />
        </div>
      </div>

      <label className="flex items-center gap-2 text-xs font-medium text-slate-600">
        <input type="checkbox" checked={override} onChange={(e) => setOverride(e.target.checked)} />
        Override existing update for this period (admin) — replaces the prior submission.
      </label>

      {error && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}
      {success && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{success}</div>}

      <Button type="submit" disabled={submitting}>{submitting ? "Submitting…" : "Submit Monthly Update"}</Button>
    </form>
  );
}
