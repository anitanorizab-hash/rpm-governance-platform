// Reports page (CP20D; V1.1 organisation-aware): report list + generate-draft. HITL — no approve here.
// One organisation scope drives both generation (organisation_id) and the client-side list filters
// (organisation + date range). Teras-segmented reports are not supported by V1.1 (portfolio-wide).
import { useCallback, useEffect, useMemo, useState } from "react";
import { reportService } from "../services/reportService";
import { useAuth } from "../context/AuthContext";
import { useOrgScope } from "../hooks/useOrgScope";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import { Button } from "../components/ui/button";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import ReportTable from "../components/reports/ReportTable";

const MANAGE_ROLES = ["super_admin", "jpn_admin", "executive"];
const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";
const thisPeriod = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, "0")}`;

export default function Reports() {
  const { hasRole } = useAuth();
  const canManage = hasRole(...MANAGE_ROLES);
  const { level, ppdId, setPpdId, onLevelChange, ppdOptions, organisationId, scopeLabel } = useOrgScope();

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [period, setPeriod] = useState(thisPeriod);
  const [type, setType] = useState("monthly");
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState(null);
  const [genSuccess, setGenSuccess] = useState(null);

  // List filters
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      setReports(await reportService.list());
    } catch (err) {
      setError(err.message || "Failed to load reports.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function onGenerate(e) {
    e.preventDefault();
    setGenerating(true); setGenError(null); setGenSuccess(null);
    try {
      const r = await reportService.generate(period, type, organisationId || undefined);
      setGenSuccess(`Draft report generated for ${r.period}${organisationId ? ` (${scopeLabel})` : ""}.`);
      await load();
    } catch (err) {
      setGenError(err.message || "Generation failed.");
    } finally {
      setGenerating(false);
    }
  }

  // Client-side list filters: organisation (content.organisation_id) + reporting-period range.
  const filteredReports = useMemo(() => {
    return reports.filter((r) => {
      if (organisationId && r.content?.organisation_id !== organisationId) return false;
      if (dateFrom && (r.period || "") < dateFrom) return false;
      if (dateTo && (r.period || "") > dateTo) return false;
      return true;
    });
  }, [reports, organisationId, dateFrom, dateTo]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Reports</h1>
          <p className="text-sm text-slate-500">Generate, review and archive KPI reports · {scopeLabel}.</p>
        </div>
        <OrgLevelFilter level={level} onLevelChange={onLevelChange} ppdId={ppdId} onPpdChange={setPpdId} ppdOptions={ppdOptions} />
      </div>

      <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
        Reports require approval before official use. Generation produces an advisory draft only — approval is
        performed by an authorised officer in the approvals workflow (ASM-11).
      </div>

      {canManage && (
        <Card>
          <CardHeader><CardTitle>Generate Draft Report</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={onGenerate} className="flex flex-wrap items-end gap-3">
              <div>
                <Label>Reporting Period</Label>
                <Input value={period} onChange={(e) => setPeriod(e.target.value)} placeholder="2026-06" required className="w-40" />
              </div>
              <div>
                <Label>Type</Label>
                <select className={`${selectCls} w-40`} value={type} onChange={(e) => setType(e.target.value)}>
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="annual">Annual</option>
                </select>
              </div>
              <Button type="submit" disabled={generating}>{generating ? "Generating…" : "Generate Draft"}</Button>
              <span className="text-xs text-slate-400">Organisation scope: {scopeLabel}</span>
            </form>
            {genError && <div className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{genError}</div>}
            {genSuccess && <div className="mt-3 rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{genSuccess}</div>}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader><CardTitle>Filter Reports</CardTitle></CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-end gap-3">
            <div>
              <Label>Date From</Label>
              <Input value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} placeholder="2026-01" className="w-36" />
            </div>
            <div>
              <Label>Date To</Label>
              <Input value={dateTo} onChange={(e) => setDateTo(e.target.value)} placeholder="2026-12" className="w-36" />
            </div>
            <div>
              <Label>Teras</Label>
              <select className={`${selectCls} w-44`} disabled title="V1.1 reports are portfolio-wide (cover all Teras).">
                <option>All Teras (portfolio)</option>
              </select>
            </div>
            <span className="text-xs text-slate-400">Organisation &amp; date filters apply to the list below.</span>
          </div>
        </CardContent>
      </Card>

      {loading ? <Loading label="Loading reports…" />
        : error ? <ErrorMessage message={error} />
        : <ReportTable reports={filteredReports} />}
    </div>
  );
}
