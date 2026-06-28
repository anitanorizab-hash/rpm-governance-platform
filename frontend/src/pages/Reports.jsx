// Reports page (CP20D): report list + generate-draft. HITL — no approve/reject here.
import { useCallback, useEffect, useState } from "react";
import { reportService } from "../services/reportService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import { Button } from "../components/ui/button";
import ReportTable from "../components/reports/ReportTable";

const MANAGE_ROLES = ["super_admin", "jpn_admin", "executive"];
const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";
const thisPeriod = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, "0")}`;

export default function Reports() {
  const { hasRole } = useAuth();
  const canManage = hasRole(...MANAGE_ROLES);

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [period, setPeriod] = useState(thisPeriod);
  const [type, setType] = useState("monthly");
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState(null);
  const [genSuccess, setGenSuccess] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
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
    setGenerating(true);
    setGenError(null);
    setGenSuccess(null);
    try {
      const r = await reportService.generate(period, type);
      setGenSuccess(`Draft report generated for ${r.period}.`);
      await load();
    } catch (err) {
      setGenError(err.message || "Generation failed.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Reports</h1>
        <p className="text-sm text-slate-500">Generate, review and archive KPI reports.</p>
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
            </form>
            {genError && <div className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{genError}</div>}
            {genSuccess && <div className="mt-3 rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{genSuccess}</div>}
          </CardContent>
        </Card>
      )}

      {loading ? <Loading label="Loading reports…" />
        : error ? <ErrorMessage message={error} />
        : <ReportTable reports={reports} />}
    </div>
  );
}
