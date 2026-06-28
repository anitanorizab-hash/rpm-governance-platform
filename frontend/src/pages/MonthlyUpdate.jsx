// MonthlyUpdate page (CP20B): submission summary + pick a KPI and submit an in-system update.
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { kpiService } from "../services/kpiService";
import { monthlyUpdateService } from "../services/monthlyUpdateService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Label } from "../components/ui/input";
import MonthlyUpdateForm from "../components/kpi/MonthlyUpdateForm";

const UPDATE_ROLES = ["super_admin", "jpn_admin", "sector_admin", "kpi_pic"];
const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";
const prettify = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function MonthlyUpdate() {
  const { hasRole } = useAuth();
  const canUpdate = hasRole(...UPDATE_ROLES);

  const [summary, setSummary] = useState(null);
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedId, setSelectedId] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(null);
  const [derivedStatus, setDerivedStatus] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [sum, list] = await Promise.all([
        monthlyUpdateService.summary(),
        kpiService.list({ limit: 500 }),
      ]);
      setSummary(sum);
      setKpis(list);
    } catch (err) {
      setError(err.message || "Failed to load monthly update data.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const selectedKpi = useMemo(() => kpis.find((k) => k.id === selectedId), [kpis, selectedId]);

  async function handleSubmit(body, override) {
    setSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(null);
    try {
      const res = await monthlyUpdateService.create(body, override);
      setDerivedStatus(res.achievement_status || null);
      setSubmitSuccess(
        `Saved for ${res.reporting_year}-${String(res.reporting_month).padStart(2, "0")}.` +
        (res.achievement_status ? ` Derived status: ${res.achievement_status}.` : "")
      );
      setSummary(await monthlyUpdateService.summary());
    } catch (err) {
      setSubmitError(
        err.status === 409 ? `${err.message} Tick the override box to replace it.` : (err.message || "Submission failed.")
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <Loading label="Loading monthly updates…" />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Monthly Updates</h1>
        <p className="text-sm text-slate-500">Submit and track in-system monthly KPI updates.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card><CardContent className="py-3"><p className="text-xs uppercase tracking-wide text-slate-400">Total Updates</p><p className="text-xl font-semibold text-slate-800">{summary?.total_updates ?? 0}</p></CardContent></Card>
        <Card>
          <CardHeader className="py-3"><CardTitle className="text-sm">By Status</CardTitle></CardHeader>
          <CardContent className="py-2 text-sm text-slate-600">
            {summary && Object.keys(summary.by_status || {}).length
              ? Object.entries(summary.by_status).map(([k, v]) => <div key={k}>{prettify(k)}: <b>{v}</b></div>)
              : "—"}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="py-3"><CardTitle className="text-sm">By Risk</CardTitle></CardHeader>
          <CardContent className="py-2 text-sm text-slate-600">
            {summary && Object.keys(summary.by_risk || {}).length
              ? Object.entries(summary.by_risk).map(([k, v]) => <div key={k}>{prettify(k)}: <b>{v}</b></div>)
              : "—"}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>Submit an Update</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          {!canUpdate ? (
            <p className="rounded-md bg-slate-50 px-3 py-2 text-sm text-slate-500">
              Your role has read-only access. Monthly updates are submitted by the assigned PIC or an administrator.
            </p>
          ) : (
            <>
              <div>
                <Label>Select KPI</Label>
                <select className={selectCls} value={selectedId} onChange={(e) => { setSelectedId(e.target.value); setSubmitSuccess(null); setSubmitError(null); }}>
                  <option value="">— Choose a KPI —</option>
                  {kpis.map((k) => (
                    <option key={k.id} value={k.id}>{k.code} — {k.statement || "(no statement)"}</option>
                  ))}
                </select>
                {selectedKpi && (
                  <p className="mt-1 text-xs text-slate-500">
                    Teras {selectedKpi.teras_number ?? "—"} · {selectedKpi.sector || "—"} ·{" "}
                    <Link to={`/app/kpis/${selectedKpi.id}`} className="text-blue-700 hover:underline">open full detail</Link>
                  </p>
                )}
              </div>

              {selectedId ? (
                <MonthlyUpdateForm
                  key={selectedId}
                  kpiId={selectedId}
                  onSubmit={handleSubmit}
                  submitting={submitting}
                  error={submitError}
                  success={submitSuccess}
                  derivedStatus={derivedStatus}
                />
              ) : (
                <p className="text-sm text-slate-500">Choose a KPI above to enter its monthly update.</p>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
