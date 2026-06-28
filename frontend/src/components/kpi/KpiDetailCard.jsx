// KpiDetailCard (CP20B): shows KPI detail (GET /kpis/{id}) and, for authorised users,
// an inline editor that PATCHes the KPI. Amendable fields (statement/indicator/target)
// are gated by the amendment window (BR-008) with a Super Admin override.
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";
import AmendmentWarning, { isAmendmentWindowOpen } from "./AmendmentWarning";

function Field({ label, children }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{label}</p>
      <div className="mt-0.5 text-sm text-slate-700">{children}</div>
    </div>
  );
}

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function KpiDetailCard({ kpi, canManage, isSuperAdmin, onSave, saving, saveError }) {
  const [editing, setEditing] = useState(false);
  const [override, setOverride] = useState(false);
  const [form, setForm] = useState({
    statement: kpi.statement || "",
    indicator: kpi.indicators?.[0] || "",
    target: kpi.targets?.[0] || "",
    status: kpi.status || "",
    department: kpi.sector || "",
  });

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const windowOpen = isAmendmentWindowOpen();

  function submit(e) {
    e.preventDefault();
    // Only send changed fields; amendable fields require window or override.
    const patch = {};
    if (form.statement !== (kpi.statement || "")) patch.statement = form.statement;
    if (form.indicator !== (kpi.indicators?.[0] || "")) patch.indicator = form.indicator;
    if (form.target !== (kpi.targets?.[0] || "")) patch.target = form.target;
    if (form.status !== (kpi.status || "")) patch.status = form.status;
    if (form.department !== (kpi.sector || "")) patch.department = form.department;
    onSave(patch, override).then((ok) => { if (ok) setEditing(false); });
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{kpi.code} — KPI Detail</CardTitle>
        {canManage && !editing && (
          <Button variant="outline" onClick={() => setEditing(true)}>Edit</Button>
        )}
      </CardHeader>
      <CardContent className="space-y-4">
        {!editing ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="KPI Statement"><span className="font-medium">{kpi.statement || "—"}</span></Field>
            <Field label="Teras">{kpi.teras_number ?? "—"}</Field>
            <Field label="Indicator">{kpi.indicators?.length ? kpi.indicators.join("; ") : "—"}</Field>
            <Field label="Target">{kpi.targets?.length ? kpi.targets.join("; ") : "—"}</Field>
            <Field label="Activities">
              {kpi.activities?.length ? (
                <ul className="list-inside list-disc">{kpi.activities.map((a, i) => <li key={i}>{a}</li>)}</ul>
              ) : "—"}
            </Field>
            <Field label="Department / Sector">{kpi.sector || "—"}</Field>
            <Field label="Assigned PIC">{kpi.pic_name || kpi.pic_email || "—"}{kpi.pic_email && kpi.pic_name ? ` (${kpi.pic_email})` : ""}</Field>
            <Field label="Achievement Status">{kpi.status || "—"}</Field>
            <Field label="Financial Allocation (total)">
              {kpi.financial_allocation_total != null ? kpi.financial_allocation_total.toLocaleString() : "—"}
            </Field>
          </div>
        ) : (
          <form onSubmit={submit} className="space-y-4">
            <AmendmentWarning isSuperAdmin={isSuperAdmin} override={override} onToggleOverride={setOverride} />
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <Label>KPI Statement {(!windowOpen && !override) && <span className="text-amber-600">(amendment window closed)</span>}</Label>
                <Input value={form.statement} onChange={(e) => set("statement", e.target.value)}
                       disabled={!windowOpen && !override} />
              </div>
              <div>
                <Label>Indicator {(!windowOpen && !override) && <span className="text-amber-600">(window closed)</span>}</Label>
                <Input value={form.indicator} onChange={(e) => set("indicator", e.target.value)}
                       disabled={!windowOpen && !override} />
              </div>
              <div>
                <Label>Target {(!windowOpen && !override) && <span className="text-amber-600">(window closed)</span>}</Label>
                <Input value={form.target} onChange={(e) => set("target", e.target.value)}
                       disabled={!windowOpen && !override} />
              </div>
              <div>
                <Label>Achievement Status (editable anytime)</Label>
                <Input value={form.status} onChange={(e) => set("status", e.target.value)} />
              </div>
              <div>
                <Label>Department / Sector (editable anytime)</Label>
                <Input value={form.department} onChange={(e) => set("department", e.target.value)} />
              </div>
            </div>
            {saveError && (
              <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{saveError}</div>
            )}
            <div className="flex gap-2">
              <Button type="submit" disabled={saving}>{saving ? "Saving…" : "Save changes"}</Button>
              <Button type="button" variant="outline" onClick={() => setEditing(false)} disabled={saving}>Cancel</Button>
            </div>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
