// KpiManagement page (CP20B): KPI list with search + server-side filters + completeness summary.
import { useCallback, useEffect, useMemo, useState } from "react";
import { kpiService } from "../services/kpiService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent } from "../components/ui/card";
import KpiFilters from "../components/kpi/KpiFilters";
import KpiTable from "../components/kpi/KpiTable";

const EMPTY = { search: "", teras: "", sector: "", pic: "", status: "", completeness: "" };

export default function KpiManagement() {
  const [filters, setFilters] = useState(EMPTY);
  const [applied, setApplied] = useState(EMPTY);
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
  }, []);

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
      <div>
        <h1 className="text-xl font-semibold text-slate-800">KPI Management</h1>
        <p className="text-sm text-slate-500">View, search and filter RPM KPIs. All updates are in-system (no Excel).</p>
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
