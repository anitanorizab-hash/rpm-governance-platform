// Notifications page (CP20D): draft → submit → queue (dry-run) with HITL. No direct send.
import { useCallback, useEffect, useState } from "react";
import { notificationService, NOTIFICATION_TYPES } from "../services/notificationService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import { Button } from "../components/ui/button";
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

  const [notifications, setNotifications] = useState([]);
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    setLoading(true);
    setError(null);
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
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Notifications</h1>
        <p className="text-sm text-slate-500">Draft, review and queue KPI notifications.</p>
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

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <NotificationTable notifications={notifications} selectedId={selected?.id} onSelect={setSelected} />
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
