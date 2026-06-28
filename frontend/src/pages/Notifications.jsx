// Notifications page (CP20D; V1.1 organisation-aware filtering): draft → submit → queue (dry-run) HITL.
// Filters: Status (client-side) + Organisation. Notifications are not organisation-scoped in the data
// model, so org filtering is best-effort — it resolves a notification's referenced KPI to its
// organisation (via the org-tagged KPI list). Notifications with no resolvable KPI appear under "All".
import { useCallback, useEffect, useMemo, useState } from "react";
import { notificationService, NOTIFICATION_TYPES } from "../services/notificationService";
import { kpiService } from "../services/kpiService";
import { useAuth } from "../context/AuthContext";
import { useOrgScope } from "../hooks/useOrgScope";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import { Button } from "../components/ui/button";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import NotificationTable from "../components/notifications/NotificationTable";
import NotificationPreview from "../components/notifications/NotificationPreview";
import NotificationQueueStatus from "../components/notifications/NotificationQueueStatus";

const DRAFT_ROLES = ["super_admin", "jpn_admin", "sector_admin"];
const QUEUE_ROLES = ["super_admin", "jpn_admin"];
const VIEW_QUEUE_ROLES = ["super_admin", "jpn_admin", "executive"];
const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function Notifications() {
  const { hasRole } = useAuth();
  const canDraft = hasRole(...DRAFT_ROLES);
  const canQueue = hasRole(...QUEUE_ROLES);
  const canViewQueue = hasRole(...VIEW_QUEUE_ROLES);
  const { level, ppdId, setPpdId, onLevelChange, ppdOptions, organisationId, scopeLabel } = useOrgScope();

  const [notifications, setNotifications] = useState([]);
  const [queue, setQueue] = useState([]);
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [statusFilter, setStatusFilter] = useState("");

  const [selected, setSelected] = useState(null);
  const [busy, setBusy] = useState(false);
  const [actionMsg, setActionMsg] = useState(null);
  const [actionError, setActionError] = useState(null);

  const [form, setForm] = useState({ type: "reminder", recipient: "", subject: "", kpi: "", detail: "" });
  const [drafting, setDrafting] = useState(false);
  const [draftMsg, setDraftMsg] = useState(null);
  const [draftError, setDraftError] = useState(null);
  const setF = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const list = await notificationService.list();
      setNotifications(list);
      if (canViewQueue) {
        try { setQueue(await notificationService.emailQueue()); } catch { setQueue([]); }
      }
    } catch (err) {
      setError(err.message || "Failed to load notifications.");
    } finally {
      setLoading(false);
    }
  }, [canViewQueue]);

  useEffect(() => { load(); }, [load]);
  // KPI → organisation map (for best-effort org filtering of notifications).
  useEffect(() => { kpiService.list({ limit: 500 }).then(setKpis).catch(() => setKpis([])); }, []);

  const kpiOrgMap = useMemo(() => {
    const m = {};
    kpis.forEach((k) => { m[k.id] = k.organisation_id; if (k.code) m[k.code] = k.organisation_id; });
    return m;
  }, [kpis]);

  const statusOptions = useMemo(
    () => Array.from(new Set(notifications.map((n) => n.status).filter(Boolean))).sort(),
    [notifications]
  );

  const resolveOrg = useCallback(
    (n) => kpiOrgMap[n.kpi] ?? kpiOrgMap[n.kpi_code] ?? kpiOrgMap[n.related_entity_id] ?? null,
    [kpiOrgMap]
  );

  const filteredNotifications = useMemo(() => {
    return notifications.filter((n) => {
      if (statusFilter && n.status !== statusFilter) return false;
      if (organisationId && resolveOrg(n) !== organisationId) return false;
      return true;
    });
  }, [notifications, statusFilter, organisationId, resolveOrg]);

  const refreshSelected = useCallback(async (id) => {
    const list = await notificationService.list();
    setNotifications(list);
    if (canViewQueue) { try { setQueue(await notificationService.emailQueue()); } catch { /* ignore */ } }
    const found = list.find((n) => n.id === id);
    if (found) setSelected(found);
  }, [canViewQueue]);

  async function onDraft(e) {
    e.preventDefault();
    setDrafting(true); setDraftError(null); setDraftMsg(null);
    try {
      const n = await notificationService.draft(form);
      setDraftMsg(`Draft created for ${n.recipient}.`);
      setForm({ type: "reminder", recipient: "", subject: "", kpi: "", detail: "" });
      await load();
      setSelected(n);
    } catch (err) {
      setDraftError(err.message || "Draft failed.");
    } finally {
      setDrafting(false);
    }
  }

  function runAction(fn, okMsg) {
    return async () => {
      if (!selected) return;
      setBusy(true); setActionError(null); setActionMsg(null);
      try {
        const res = await fn(selected.id);
        setActionMsg(typeof okMsg === "function" ? okMsg(res) : okMsg);
        await refreshSelected(selected.id);
      } catch (err) {
        setActionError(err.message || "Action failed.");
      } finally {
        setBusy(false);
      }
    };
  }

  const onSubmit = runAction(notificationService.submitForReview,
    (r) => `Submitted for review (approval state: ${r.approval_state}).`);
  const onQueue = runAction(notificationService.queue,
    (r) => `Queued — delivery status: ${r.status} (${r.mode}).`);
  const onRetry = runAction(notificationService.retry,
    (r) => `Retried — status: ${r.status} (attempt ${r.retry_count}).`);
  const onCancel = runAction(notificationService.cancel, "Notification cancelled.");

  if (loading) return <Loading label="Loading notifications…" />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Notifications</h1>
          <p className="text-sm text-slate-500">Draft, review and queue KPI notifications · {scopeLabel}.</p>
        </div>
        <OrgLevelFilter level={level} onLevelChange={onLevelChange} ppdId={ppdId} onPpdChange={setPpdId} ppdOptions={ppdOptions} />
      </div>

      <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
        Notifications require approval before queueing. Email delivery is <span className="font-medium">dry-run</span> unless
        production SMTP is configured — nothing is sent automatically (ASM-11 / BR-015).
      </div>

      {canDraft && (
        <Card>
          <CardHeader><CardTitle>Draft Notification</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={onDraft} className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div>
                <Label>Type</Label>
                <select className={selectCls} value={form.type} onChange={(e) => setF("type", e.target.value)}>
                  {NOTIFICATION_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
              </div>
              <div>
                <Label>Recipient (email)</Label>
                <Input value={form.recipient} onChange={(e) => setF("recipient", e.target.value)} placeholder="name@moe.gov.my" required />
              </div>
              <div>
                <Label>Subject (optional)</Label>
                <Input value={form.subject} onChange={(e) => setF("subject", e.target.value)} />
              </div>
              <div>
                <Label>KPI reference (optional)</Label>
                <Input value={form.kpi} onChange={(e) => setF("kpi", e.target.value)} />
              </div>
              <div className="sm:col-span-2">
                <Label>Detail (optional)</Label>
                <textarea className={selectCls} rows={2} value={form.detail} onChange={(e) => setF("detail", e.target.value)} />
              </div>
              <div className="sm:col-span-2">
                <Button type="submit" disabled={drafting}>{drafting ? "Drafting…" : "Draft Notification"}</Button>
              </div>
            </form>
            {draftError && <div className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{draftError}</div>}
            {draftMsg && <div className="mt-3 rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{draftMsg}</div>}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader><CardTitle>Filter Notifications</CardTitle></CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-end gap-3">
            <div>
              <Label>Status</Label>
              <select className={`${selectCls} w-48`} value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                <option value="">All statuses</option>
                {statusOptions.map((s) => <option key={s} value={s}>{s.replace(/_/g, " ")}</option>)}
              </select>
            </div>
            <span className="text-xs text-slate-400">
              Showing {filteredNotifications.length} of {notifications.length}
              {organisationId ? " · organisation scope applied via referenced KPI" : ""}.
            </span>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <NotificationTable notifications={filteredNotifications} selectedId={selected?.id} onSelect={setSelected} />
        <NotificationPreview
          notification={selected}
          canDraft={canDraft}
          canQueue={canQueue}
          busy={busy}
          actionMsg={actionMsg}
          actionError={actionError}
          onSubmit={onSubmit}
          onQueue={onQueue}
          onRetry={onRetry}
          onCancel={onCancel}
        />
      </div>

      <NotificationQueueStatus queue={queue} canView={canViewQueue} />
    </div>
  );
}
