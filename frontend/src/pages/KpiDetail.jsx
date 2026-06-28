// KpiDetail page (CP20B): KPI detail + completeness + submission history + monthly update form.
import { useCallback, useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { kpiService } from "../services/kpiService";
import { monthlyUpdateService } from "../services/monthlyUpdateService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import KpiDetailCard from "../components/kpi/KpiDetailCard";
import CompletenessCard from "../components/kpi/CompletenessCard";
import SubmissionHistory from "../components/kpi/SubmissionHistory";
import MonthlyUpdateForm from "../components/kpi/MonthlyUpdateForm";

const MANAGE_ROLES = ["super_admin", "jpn_admin", "sector_admin"];
const UPDATE_ROLES = ["super_admin", "jpn_admin", "sector_admin", "kpi_pic"];
const REMOVE_ROLES = ["super_admin", "jpn_admin"];

export default function KpiDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { hasRole } = useAuth();
  const canManage = hasRole(...MANAGE_ROLES);
  const canUpdate = hasRole(...UPDATE_ROLES);
  const canRemove = hasRole(...REMOVE_ROLES);
  const isSuperAdmin = hasRole("super_admin");

  const [removeOpen, setRemoveOpen] = useState(false);
  const [removeReason, setRemoveReason] = useState("");
  const [removeBusy, setRemoveBusy] = useState(false);
  const [removeError, setRemoveError] = useState(null);

  async function handleRemove() {
    if (!removeReason.trim()) { setRemoveError("A removal reason is required."); return; }
    setRemoveBusy(true); setRemoveError(null);
    try {
      await kpiService.remove(id, removeReason.trim());
      navigate("/app/kpis");
    } catch (err) {
      setRemoveError(err.message || "Removal failed.");
    } finally {
      setRemoveBusy(false);
    }
  }

  const [kpi, setKpi] = useState(null);
  const [completeness, setCompleteness] = useState(null);
  const [updates, setUpdates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(null);
  const [derivedStatus, setDerivedStatus] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [detail, comp, hist] = await Promise.all([
        kpiService.get(id),
        kpiService.completeness(id),
        monthlyUpdateService.listForKpi(id),
      ]);
      setKpi(detail);
      setCompleteness(comp);
      setUpdates(hist);
    } catch (err) {
      setError(err.message || "Failed to load KPI.");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  async function handleSave(patch, override) {
    if (Object.keys(patch).length === 0) { setSaveError("No changes to save."); return false; }
    setSaving(true);
    setSaveError(null);
    try {
      const updated = await kpiService.patch(id, patch, override);
      setKpi(updated);
      const comp = await kpiService.completeness(id);
      setCompleteness(comp);
      return true;
    } catch (err) {
      setSaveError(err.message || "Update failed.");
      return false;
    } finally {
      setSaving(false);
    }
  }

  async function handleAssignPic({ name, email, sector }) {
    try {
      const updated = await kpiService.assignPic(id, { name, email, sector });
      setKpi(updated);
      return true;
    } catch { return false; }
  }

  async function handleUpdateActivity(activityId, fields) {
    try {
      const updated = await kpiService.updateActivity(id, activityId, fields);
      setKpi(updated);
      return true;
    } catch { return false; }
  }

  async function handleSubmitUpdate(body, override) {
    setSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(null);
    try {
      const res = await monthlyUpdateService.create(body, override);
      setDerivedStatus(res.achievement_status || null);
      setSubmitSuccess(
        `Monthly update saved for ${res.reporting_year}-${String(res.reporting_month).padStart(2, "0")}.` +
        (res.achievement_status ? ` Derived status: ${res.achievement_status}.` : "")
      );
      const [hist, detail, comp] = await Promise.all([
        monthlyUpdateService.listForKpi(id),
        kpiService.get(id),
        kpiService.completeness(id),
      ]);
      setUpdates(hist);
      setKpi(detail);
      setCompleteness(comp);
    } catch (err) {
      setSubmitError(
        err.status === 409
          ? `${err.message} Tick the override box to replace it.`
          : (err.message || "Submission failed.")
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <Loading label="Loading KPI…" />;
  if (error) return (
    <div className="space-y-3">
      <ErrorMessage message={error} />
      <Link to="/app/kpis" className="text-sm text-blue-700 hover:underline">← Back to KPI list</Link>
    </div>
  );

  return (
    <div className="space-y-6">
      <Link to="/app/kpis" className="text-sm text-blue-700 hover:underline">← Back to KPI list</Link>

      <KpiDetailCard
        kpi={kpi}
        canManage={canManage}
        canUpdateActivity={canUpdate}
        canRemove={canRemove}
        isSuperAdmin={isSuperAdmin}
        onSave={handleSave}
        saving={saving}
        saveError={saveError}
        onAssignPic={handleAssignPic}
        onUpdateActivity={handleUpdateActivity}
        onRequestRemove={() => { setRemoveReason(""); setRemoveError(null); setRemoveOpen(true); }}
      />

      {removeOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4">
          <div className="w-full max-w-lg rounded-xl bg-white p-5 shadow-lg">
            <h3 className="text-base font-semibold text-slate-800">Remove KPI {kpi.code}</h3>
            <div className="mt-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
              This KPI will be removed from active monitoring but retained in audit history.
            </div>
            <p className="mt-3 text-xs text-slate-500">
              {kpi.organisation_type ? `${kpi.organisation_type} · ${kpi.organisation_name || ""} · ` : ""}{kpi.statement || ""}
            </p>
            <label className="mt-3 block text-sm font-medium text-slate-700">Reason for removal (required)</label>
            <textarea className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      rows={3} value={removeReason} onChange={(e) => setRemoveReason(e.target.value)}
                      placeholder="e.g. Officially agreed for removal at the Aug review (ref …)" />
            {removeError && <div className="mt-2 text-xs text-red-600">{removeError}</div>}
            <div className="mt-4 flex justify-end gap-2">
              <Button variant="outline" onClick={() => setRemoveOpen(false)} disabled={removeBusy}>Cancel</Button>
              <Button className="bg-red-600 hover:bg-red-700" onClick={handleRemove} disabled={removeBusy}>
                {removeBusy ? "Removing…" : "Confirm removal"}
              </Button>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1"><CompletenessCard completeness={completeness} /></div>
        <div className="lg:col-span-2"><SubmissionHistory updates={updates} /></div>
      </div>

      <Card>
        <CardHeader><CardTitle>Submit Monthly Update</CardTitle></CardHeader>
        <CardContent>
          {canUpdate ? (
            <MonthlyUpdateForm
              kpiId={id}
              onSubmit={handleSubmitUpdate}
              submitting={submitting}
              error={submitError}
              success={submitSuccess}
              derivedStatus={derivedStatus}
            />
          ) : (
            <p className="rounded-md bg-slate-50 px-3 py-2 text-sm text-slate-500">
              Your role has read-only access. Monthly updates are submitted by the assigned PIC or an administrator.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
