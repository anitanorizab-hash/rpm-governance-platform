// AdminPics (V1.1.1): PIC Directory — admin CRUD, search/filter, KPI assignment, Excel import/export.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { picService } from "../services/picService";
import { organisationService } from "../services/organisationService";
import { kpiService } from "../services/kpiService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import { Button } from "../components/ui/button";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";
const EMPTY = { name: "", email: "", organisation_id: "", department: "", active: true };

export default function AdminPics() {
  const [pics, setPics] = useState([]);
  const [orgs, setOrgs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [msg, setMsg] = useState(null);

  const [filters, setFilters] = useState({ search: "", organisation_id: "", status: "" });
  const [applied, setApplied] = useState({ search: "", organisation_id: "", status: "" });

  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const [busy, setBusy] = useState(false);

  const [assignFor, setAssignFor] = useState(null);   // pic being assigned
  const [orgKpis, setOrgKpis] = useState([]);
  const [checked, setChecked] = useState({});
  const fileRef = useRef(null);

  const orgName = useMemo(() => Object.fromEntries(orgs.map((o) => [o.id, o.name])), [orgs]);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      setPics(await picService.list(applied));
    } catch (err) { setError(err.message || "Failed to load PICs."); }
    finally { setLoading(false); }
  }, [applied]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => { organisationService.list().then(setOrgs).catch(() => setOrgs([])); }, []);

  const setF = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  async function save(e) {
    e.preventDefault();
    setBusy(true); setError(null); setMsg(null);
    try {
      if (editingId) await picService.update(editingId, form);
      else await picService.create(form);
      setForm(EMPTY); setEditingId(null);
      setMsg("Saved.");
      await load();
    } catch (err) { setError(err.message || "Save failed."); }
    finally { setBusy(false); }
  }

  function edit(p) {
    setEditingId(p.id);
    setForm({ name: p.name, email: p.email || "", organisation_id: p.organisation_id || "",
              department: p.department || "", active: p.active });
  }

  async function remove(p) {
    if (!window.confirm(`Soft-delete PIC "${p.name}"?`)) return;
    await picService.remove(p.id); await load();
  }

  async function openAssign(p) {
    setAssignFor(p); setChecked({});
    const all = await kpiService.list({ limit: 500 });
    const scoped = p.organisation_id ? all.filter((k) => k.organisation_id === p.organisation_id) : all;
    setOrgKpis(scoped);
    const pre = {};
    (await picService.get(p.id)).assigned_kpi_codes?.forEach(() => {});  // codes are display-only
    setChecked(pre);
  }

  async function saveAssign() {
    setBusy(true);
    try {
      const ids = Object.entries(checked).filter(([, v]) => v).map(([k]) => k);
      await picService.assignKpis(assignFor.id, ids);
      setAssignFor(null); setMsg(`Assigned ${ids.length} KPI(s).`);
      await load();
    } catch (err) { setError(err.message || "Assign failed."); }
    finally { setBusy(false); }
  }

  async function onImport(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true); setError(null);
    try {
      const r = await picService.importFile(file);
      setMsg(`Imported: ${r.created} created, ${r.updated} updated.`);
      await load();
    } catch (err) { setError(err.message || "Import failed."); }
    finally { setBusy(false); if (fileRef.current) fileRef.current.value = ""; }
  }

  return (
    <div className="space-y-5">
      <Link to="/app/admin" className="text-sm text-blue-700 hover:underline">← Back to administration</Link>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-800">PIC Directory</h1>
        <div className="flex gap-2">
          <input ref={fileRef} type="file" accept=".xlsx" className="hidden" onChange={onImport} />
          <Button variant="outline" onClick={() => fileRef.current?.click()} disabled={busy}>Import Excel</Button>
          <Button variant="outline" onClick={() => picService.exportFile().catch((e) => setError(e.message))}>Export Excel</Button>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}
      {msg && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{msg}</div>}

      {/* Add / Edit */}
      <Card>
        <CardHeader><CardTitle>{editingId ? "Edit PIC" : "Add PIC"}</CardTitle></CardHeader>
        <CardContent>
          <form onSubmit={save} className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <div><Label>PIC Name</Label><Input value={form.name} onChange={(e) => setF("name", e.target.value)} required /></div>
            <div><Label>PIC Email</Label><Input value={form.email} onChange={(e) => setF("email", e.target.value)} placeholder="name@moe.gov.my" /></div>
            <div>
              <Label>Organisation</Label>
              <select className={selectCls} value={form.organisation_id} onChange={(e) => setF("organisation_id", e.target.value)}>
                <option value="">—</option>
                {orgs.map((o) => <option key={o.id} value={o.id}>{o.name} ({o.type})</option>)}
              </select>
            </div>
            <div><Label>Department</Label><Input value={form.department} onChange={(e) => setF("department", e.target.value)} /></div>
            <div>
              <Label>Status</Label>
              <select className={selectCls} value={form.active ? "active" : "inactive"} onChange={(e) => setF("active", e.target.value === "active")}>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div className="flex items-end gap-2">
              <Button type="submit" disabled={busy}>{editingId ? "Update PIC" : "Add PIC"}</Button>
              {editingId && <Button type="button" variant="outline" onClick={() => { setEditingId(null); setForm(EMPTY); }}>Cancel</Button>}
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Filters */}
      <div className="flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <div><Label>Search (name / email)</Label><Input value={filters.search} onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))} placeholder="Type a name or email…" /></div>
        <div>
          <Label>Organisation</Label>
          <select className={selectCls} value={filters.organisation_id} onChange={(e) => setFilters((f) => ({ ...f, organisation_id: e.target.value }))}>
            <option value="">All</option>
            {orgs.map((o) => <option key={o.id} value={o.id}>{o.name}</option>)}
          </select>
        </div>
        <div>
          <Label>Status</Label>
          <select className={selectCls} value={filters.status} onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}>
            <option value="">All</option><option value="active">Active</option><option value="inactive">Inactive</option>
          </select>
        </div>
        <Button onClick={() => setApplied({ ...filters })}>Apply</Button>
        <Button variant="outline" onClick={() => { setFilters({ search: "", organisation_id: "", status: "" }); setApplied({ search: "", organisation_id: "", status: "" }); }}>Reset</Button>
      </div>

      {loading ? <Loading label="Loading PIC directory…" /> : (
        <Card>
          <CardHeader><CardTitle>PICs ({pics.length})</CardTitle></CardHeader>
          <CardContent className="px-0 py-0">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[820px] text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-4 py-2 font-medium">Name</th>
                    <th className="px-4 py-2 font-medium">Email</th>
                    <th className="px-4 py-2 font-medium">Organisation</th>
                    <th className="px-4 py-2 font-medium">Department</th>
                    <th className="px-4 py-2 font-medium">KPIs</th>
                    <th className="px-4 py-2 font-medium">Status</th>
                    <th className="px-4 py-2 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {pics.length === 0 ? (
                    <tr><td colSpan={7} className="px-4 py-6 text-center text-slate-500">No PICs.</td></tr>
                  ) : pics.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50">
                      <td className="px-4 py-2 font-medium text-slate-700">{p.name}</td>
                      <td className="px-4 py-2 text-slate-600">{p.email || <span className="text-amber-600">no email</span>}</td>
                      <td className="px-4 py-2 text-slate-600">{p.organisation_name || orgName[p.organisation_id] || "—"}</td>
                      <td className="px-4 py-2 text-slate-600">{p.department || "—"}</td>
                      <td className="px-4 py-2 text-slate-600">{p.assigned_kpi_count}</td>
                      <td className="px-4 py-2">
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${p.active ? "bg-green-50 text-green-700" : "bg-slate-100 text-slate-500"}`}>
                          {p.active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <div className="flex gap-2 text-xs">
                          <button className="text-blue-700 hover:underline" onClick={() => edit(p)}>Edit</button>
                          <button className="text-blue-700 hover:underline" onClick={() => openAssign(p)}>Assign KPIs</button>
                          <button className="text-red-600 hover:underline" onClick={() => remove(p)}>Delete</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Assign KPIs modal */}
      {assignFor && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4">
          <div className="max-h-[80vh] w-full max-w-2xl overflow-auto rounded-xl bg-white p-5 shadow-lg">
            <h3 className="text-base font-semibold text-slate-800">Assign / Reassign KPIs → {assignFor.name}</h3>
            <p className="mt-1 text-xs text-slate-500">
              {assignFor.organisation_name ? `Showing KPIs for ${assignFor.organisation_name}.` : "Showing KPIs."}
              {" "}Checking a KPI reassigns it to this PIC.
            </p>
            <div className="mt-3 max-h-[50vh] divide-y divide-slate-100 overflow-auto rounded-md border border-slate-200">
              {orgKpis.length === 0 ? <p className="p-4 text-sm text-slate-500">No KPIs found.</p> :
                orgKpis.map((k) => (
                  <label key={k.id} className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-slate-50">
                    <input type="checkbox" checked={!!checked[k.id]}
                           onChange={(e) => setChecked((c) => ({ ...c, [k.id]: e.target.checked }))} />
                    <span className="text-slate-400">{k.code}</span>
                    <span className="truncate text-slate-700">{k.statement || "—"}</span>
                  </label>
                ))}
            </div>
            <div className="mt-4 flex justify-end gap-2">
              <Button variant="outline" onClick={() => setAssignFor(null)} disabled={busy}>Cancel</Button>
              <Button onClick={saveAssign} disabled={busy}>{busy ? "Assigning…" : "Assign selected"}</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
