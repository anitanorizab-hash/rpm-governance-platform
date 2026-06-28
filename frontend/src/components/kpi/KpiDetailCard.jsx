// KpiDetailCard (CP20B; V1.1.1): KPI detail with structured activities (Aktiviti Utama / Sokongan,
// Milestone, Status), PIC name/email, and inline editors. Amendable fields (statement/indicator/
// target) stay amendment-window gated (BR-008). PIC + activity-progress are operational edits.
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

const inputCls =
  "w-full rounded-md border border-slate-300 bg-white px-2 py-1 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

function ActivityRow({ activity, canEdit, onSave }) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({ status: activity.status || "", remarks: activity.remarks || "" });
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  async function save() {
    setBusy(true);
    const ok = await onSave(activity.id, { status: form.status, remarks: form.remarks });
    setBusy(false);
    if (ok) setEditing(false);
  }

  return (
    <li className="py-2">
      <p className="text-sm text-slate-700">{activity.description || "—"}</p>
      {activity.milestone && <p className="mt-0.5 text-xs text-slate-500">Milestone: {activity.milestone}</p>}
      {!editing ? (
        <div className="mt-1 flex flex-wrap items-center gap-2">
          {activity.status && (
            <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">
              {activity.status}
            </span>
          )}
          {activity.remarks && <span className="text-xs text-slate-400">{activity.remarks}</span>}
          {canEdit && (
            <button className="text-xs text-blue-700 hover:underline" onClick={() => setEditing(true)}>
              Update progress
            </button>
          )}
        </div>
      ) : (
        <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
          <div>
            <Label>Status</Label>
            <input className={inputCls} value={form.status} onChange={(e) => set("status", e.target.value)}
                   placeholder="e.g. In progress / Completed" />
          </div>
          <div>
            <Label>Remarks</Label>
            <input className={inputCls} value={form.remarks} onChange={(e) => set("remarks", e.target.value)} />
          </div>
          <div className="flex gap-2 sm:col-span-2">
            <Button onClick={save} disabled={busy}>{busy ? "Saving…" : "Save progress"}</Button>
            <Button variant="outline" onClick={() => setEditing(false)} disabled={busy}>Cancel</Button>
          </div>
        </div>
      )}
    </li>
  );
}

function ActivityList({ title, items, canEdit, onSaveActivity }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{title}</p>
      {items.length === 0 ? (
        <p className="mt-0.5 text-sm text-slate-400">—</p>
      ) : (
        <ul className="divide-y divide-slate-100">
          {items.map((a) => (
            <ActivityRow key={a.id} activity={a} canEdit={canEdit} onSave={onSaveActivity} />
          ))}
        </ul>
      )}
    </div>
  );
}

export default function KpiDetailCard({
  kpi, canManage, canUpdateActivity, isSuperAdmin, onSave, saving, saveError,
  onAssignPic, onUpdateActivity,
}) {
  const [editing, setEditing] = useState(false);
  const [override, setOverride] = useState(false);
  const [form, setForm] = useState({
    statement: kpi.statement || "",
    indicator: kpi.indicators?.[0] || "",
    target: kpi.targets?.[0] || "",
    status: kpi.status || "",
    department: kpi.sector || "",
  });
  const [picEditing, setPicEditing] = useState(false);
  const [picForm, setPicForm] = useState({ name: kpi.pic_name || "", email: kpi.pic_email || "" });
  const [picBusy, setPicBusy] = useState(false);
  const [picError, setPicError] = useState(null);

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const setPic = (k, v) => setPicForm((f) => ({ ...f, [k]: v }));
  const windowOpen = isAmendmentWindowOpen();

  const utama = (kpi.activities || []).filter((a) => a.type === "utama");
  const sokongan = (kpi.activities || []).filter((a) => a.type === "sokongan");

  function submit(e) {
    e.preventDefault();
    const patch = {};
    if (form.statement !== (kpi.statement || "")) patch.statement = form.statement;
    if (form.indicator !== (kpi.indicators?.[0] || "")) patch.indicator = form.indicator;
    if (form.target !== (kpi.targets?.[0] || "")) patch.target = form.target;
    if (form.status !== (kpi.status || "")) patch.status = form.status;
    if (form.department !== (kpi.sector || "")) patch.department = form.department;
    onSave(patch, override).then((ok) => { if (ok) setEditing(false); });
  }

  async function savePic() {
    setPicBusy(true); setPicError(null);
    const ok = await onAssignPic({ name: picForm.name, email: picForm.email, sector: kpi.sector });
    setPicBusy(false);
    if (ok) setPicEditing(false); else setPicError("Could not update PIC.");
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{kpi.code} — KPI Detail</CardTitle>
        {canManage && !editing && <Button variant="outline" onClick={() => setEditing(true)}>Edit KPI</Button>}
      </CardHeader>
      <CardContent className="space-y-5">
        {!editing ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="KPI Statement"><span className="font-medium">{kpi.statement || "—"}</span></Field>
            <Field label="Teras">{kpi.teras_number ?? "—"}</Field>
            <Field label="Indicator">{kpi.indicators?.length ? kpi.indicators.join("; ") : "—"}</Field>
            <Field label="Target">{kpi.targets?.length ? kpi.targets.join("; ") : "—"}</Field>
            <Field label="Department / Sector">{kpi.sector || "—"}</Field>
            <Field label="Achievement Status">{kpi.status || "—"}</Field>
          </div>
        ) : (
          <form onSubmit={submit} className="space-y-4">
            <AmendmentWarning isSuperAdmin={isSuperAdmin} override={override} onToggleOverride={setOverride} />
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <Label>KPI Statement {(!windowOpen && !override) && <span className="text-amber-600">(amendment window closed)</span>}</Label>
                <Input value={form.statement} onChange={(e) => set("statement", e.target.value)} disabled={!windowOpen && !override} />
              </div>
              <div>
                <Label>Indicator {(!windowOpen && !override) && <span className="text-amber-600">(window closed)</span>}</Label>
                <Input value={form.indicator} onChange={(e) => set("indicator", e.target.value)} disabled={!windowOpen && !override} />
              </div>
              <div>
                <Label>Target {(!windowOpen && !override) && <span className="text-amber-600">(window closed)</span>}</Label>
                <Input value={form.target} onChange={(e) => set("target", e.target.value)} disabled={!windowOpen && !override} />
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
            {saveError && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{saveError}</div>}
            <div className="flex gap-2">
              <Button type="submit" disabled={saving}>{saving ? "Saving…" : "Save changes"}</Button>
              <Button type="button" variant="outline" onClick={() => setEditing(false)} disabled={saving}>Cancel</Button>
            </div>
          </form>
        )}

        {/* PIC (name + email) */}
        <div className="rounded-md border border-slate-100 bg-slate-50/50 px-3 py-3">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Person In Charge (PIC)</p>
            {canManage && !picEditing && (
              <button className="text-xs text-blue-700 hover:underline" onClick={() => setPicEditing(true)}>Edit PIC</button>
            )}
          </div>
          {!picEditing ? (
            <p className="mt-1 text-sm text-slate-700">
              {kpi.pic_name || "—"}{kpi.pic_email ? ` · ${kpi.pic_email}` : " · (no email)"}
            </p>
          ) : (
            <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
              <div><Label>PIC Name</Label><input className={inputCls} value={picForm.name} onChange={(e) => setPic("name", e.target.value)} /></div>
              <div><Label>PIC Email</Label><input className={inputCls} value={picForm.email} onChange={(e) => setPic("email", e.target.value)} placeholder="name@moe.gov.my" /></div>
              {picError && <div className="text-xs text-red-600 sm:col-span-2">{picError}</div>}
              <div className="flex gap-2 sm:col-span-2">
                <Button onClick={savePic} disabled={picBusy}>{picBusy ? "Saving…" : "Save PIC"}</Button>
                <Button variant="outline" onClick={() => setPicEditing(false)} disabled={picBusy}>Cancel</Button>
              </div>
            </div>
          )}
        </div>

        {/* Activities */}
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
          <ActivityList title="Aktiviti Utama" items={utama} canEdit={canUpdateActivity} onSaveActivity={onUpdateActivity} />
          <ActivityList title="Aktiviti Sokongan" items={sokongan} canEdit={canUpdateActivity} onSaveActivity={onUpdateActivity} />
        </div>
      </CardContent>
    </Card>
  );
}
