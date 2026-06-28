// RecommendationPanel (CP20E): draft an advisory recommendation + submit for approval (HITL).
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";
import SubmitRecommendationButton from "./SubmitRecommendationButton";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function RecommendationPanel({
  kpis, onCreate, creating, createError, createdRec, onSubmit, submitting, submitMsg,
}) {
  const [form, setForm] = useState({ kpi_id: "", content: "", rationale: "", priority: 2 });
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  function submit(e) {
    e.preventDefault();
    if (!form.kpi_id || !form.content.trim()) return;
    onCreate({ ...form, priority: Number(form.priority) });
  }

  return (
    <Card>
      <CardHeader><CardTitle>Strategic Recommendation (Draft)</CardTitle></CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={submit} className="space-y-3">
          <div>
            <Label>KPI</Label>
            <select className={selectCls} value={form.kpi_id} onChange={(e) => set("kpi_id", e.target.value)} required>
              <option value="">— Choose a KPI —</option>
              {(kpis || []).map((k) => (
                <option key={k.id} value={k.id}>{k.code} — {k.statement || "(no statement)"}</option>
              ))}
            </select>
          </div>
          <div>
            <Label>Recommended Action</Label>
            <textarea className={selectCls} rows={2} value={form.content} onChange={(e) => set("content", e.target.value)} required />
          </div>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
              <Label>Rationale (optional)</Label>
              <Input value={form.rationale} onChange={(e) => set("rationale", e.target.value)} />
            </div>
            <div>
              <Label>Priority</Label>
              <select className={selectCls} value={form.priority} onChange={(e) => set("priority", e.target.value)}>
                <option value={1}>P1 — Highest</option>
                <option value={2}>P2 — Medium</option>
                <option value={3}>P3 — Low</option>
              </select>
            </div>
          </div>
          <Button type="submit" disabled={creating}>{creating ? "Drafting…" : "Generate Recommendation Draft"}</Button>
          {createError && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{createError}</div>}
        </form>

        {createdRec && (
          <div className="space-y-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-3">
            <p className="text-sm font-medium text-slate-800">{createdRec.content}</p>
            {createdRec.rationale && <p className="text-xs text-slate-600">{createdRec.rationale}</p>}
            <p className="text-xs text-slate-500">Priority P{createdRec.priority} · Status: {createdRec.status}</p>
            <SubmitRecommendationButton recommendation={createdRec} submitting={submitting} onSubmit={onSubmit} />
            {submitMsg && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{submitMsg}</div>}
          </div>
        )}
        <p className="text-[11px] text-slate-400">
          Drafting persists an advisory recommendation (audited). It is not approved or sent — submission routes to an authorised officer (ASM-11).
        </p>
      </CardContent>
    </Card>
  );
}
