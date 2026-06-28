// KpiManagement page (CP20B): KPI list with search + server-side filters + completeness summary.
import { useCallback, useEffect, useMemo, useState } from "react";
import { kpiService } from "../services/kpiService";
import { useAuth } from "../context/AuthContext";
import { useOrgScope } from "../hooks/useOrgScope";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent } from "../components/ui/card";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import KpiFilters from "../components/kpi/KpiFilters";
import KpiTable from "../components/kpi/KpiTable";

const EMPTY = { search: "", teras: "", sector: "", pic: "", status: "", completeness: "" };
const ADMIN_ROLES = ["super_admin", "jpn_admin"];

export default function KpiManagement() {
  const { hasRole } = useAuth();
  const canRemove = hasRole(...ADMIN_ROLES);
  const { level, ppdId, setPpdId, onLevelChange, ppdOptions, organisationId, scopeLabel } = useOrgScope();

  const [filters, setFilters] = useState(EMPTY);
  const [applied, setApplied] = useState(EMPTY);
  const [showRemoved, setShowRemoved] = useState(false);
  const [kpis, setKpis] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async (f) => {
    setLoading(true);
    setError(null);
    try {
      const serverFilters = {
        teras: f.teras, sector: f.sector, pic: f.pic, status: f.status, completeness: f.completeness,
        organisation_id: organisationId || undefined,
        include_removed: (canRemove && showRemoved) ? true : undefined,
      };
      const [list, sum] = await Promise.all([
        kpiService.list(serverFilters),
        kpiService.completenessSummary(),
      ]);
      setKpis(list);
      setSummary(sum);
    } catch (err) {
      setError(err.message || "Failed to load KPIs.");
    } finally {
      setLoading(false);
    }
  }, [organisationId, showRemoved, canRemove]);

  useEffect(() => { load(applied); }, [load, applied]);

  // Build dropdown options from loaded data.
  const departments = useMemo(
    () => [...new Set(kpis.map((k) => k.sector).filter(Boolean))].sort(), [kpis]);
  const pics = useMemo(
    () => [...new Set(kpis.map((k) => k.pic_email).filter(Boolean))].sort(), [kpis]);

  // Client-side free-text search on the loaded rows.
  const visible = useMemo(() => {
    const q = (applied.search || "").toLowerCase();
    if (!q) return kpis;
    return kpis.filter((k) =>
      [k.code, k.statement].filter(Boolean).some((v) => String(v).toLowerCase().includes(q)));
  }, [kpis, applied.search]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="font-display text-2xl font-bold text-navy-700">KPI Management</h1>
          <p className="text-sm text-slate-500">
            View, search and filter RPM KPIs · {scopeLabel}. All updates are in-system (no Excel).
          </p>
        </div>
        <div className="flex items-end gap-3">
          <OrgLevelFilter level={level} onLevelChange={onLevelChange} ppdId={ppdId} onPpdChange={setPpdId} ppdOptions={ppdOptions} />
          {canRemove && (
            <label className="flex items-center gap-2 pb-2 text-sm text-slate-600">
              <input type="checkbox" checked={showRemoved} onChange={(e) => setShowRemoved(e.target.checked)} />
              Show removed
            </label>
          )}
        </div>
      </div>

      {summary && (
        <div className="grid grid-cols-3 gap-4">
          <Card><CardContent className="py-3"><p className="text-xs uppercase tracking-wide text-slate-400">Total KPIs</p><p className="text-xl font-semibold text-slate-800">{summary.total_kpis}</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs uppercase tracking-wide text-slate-400">Complete</p><p className="text-xl font-semibold text-green-700">{summary.complete}</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs uppercase tracking-wide text-slate-400">Incomplete</p><p className="text-xl font-semibold text-amber-700">{summary.incomplete}</p></CardContent></Card>
        </div>
      )}

      <KpiFilters
        filters={filters}
        onChange={setFilters}
        onApply={() => setApplied(filters)}
        onReset={() => { setFilters(EMPTY); setApplied(EMPTY); }}
        departments={departments}
        pics={pics}
      />

      {loading ? (
        <Loading label="Loading KPIs…" />
      ) : error ? (
        <ErrorMessage message={error} />
      ) : (
        <>
          <p className="text-sm text-slate-500">{visible.length} KPI{visible.length === 1 ? "" : "s"} shown.</p>
          <KpiTable kpis={visible} />
        </>
      )}
    </div>
  );
}
