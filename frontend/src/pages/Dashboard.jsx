// Dashboard page (CP20A): main landing page; deterministic Teras 1–7 summary.
// Aggregates the CP10 dashboard APIs. No AI provider is called from the client.
import { useCallback, useEffect, useState } from "react";
import { dashboardService } from "../services/dashboardService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Button } from "../components/ui/button";
import OverviewCards from "../components/dashboard/OverviewCards";
import TerasSummaryChart from "../components/dashboard/TerasSummaryChart";
import RiskSummaryChart from "../components/dashboard/RiskSummaryChart";
import BudgetSummaryChart from "../components/dashboard/BudgetSummaryChart";
import SubmissionSummary from "../components/dashboard/SubmissionSummary";
import HighRiskKpiList from "../components/dashboard/HighRiskKpiList";
import KpiMappingTable from "../components/dashboard/KpiMappingTable";
import ExecutiveSummaryCard from "../components/dashboard/ExecutiveSummaryCard";

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        overview, terasSummary, riskSummary, budgetSummary,
        submissionSummary, highRiskKpis, kpiMapping, executiveSummary,
      ] = await Promise.all([
        dashboardService.overview(),
        dashboardService.terasSummary(),
        dashboardService.riskSummary(),
        dashboardService.budgetSummary(),
        dashboardService.submissionSummary(),
        dashboardService.highRiskKpis(),
        dashboardService.kpiMapping(),
        dashboardService.executiveSummary(),
      ]);
      setData({
        overview, terasSummary, riskSummary, budgetSummary,
        submissionSummary, highRiskKpis, kpiMapping, executiveSummary,
      });
    } catch (err) {
      setError(err.message || "Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) return <Loading label="Loading dashboard…" />;

  if (error) {
    return (
      <div className="space-y-4">
        <ErrorMessage message={error} />
        <Button onClick={load}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Dashboard</h1>
          <p className="text-sm text-slate-500">
            RPM 2026–2035 KPI overview across Teras 1–7
            {user?.name ? ` · ${user.name}` : ""}
          </p>
        </div>
        <Button variant="outline" onClick={load}>Refresh</Button>
      </div>

      <OverviewCards overview={data.overview} />

      <ExecutiveSummaryCard executiveSummary={data.executiveSummary} />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <TerasSummaryChart terasSummary={data.terasSummary} />
        <RiskSummaryChart riskSummary={data.riskSummary} />
        <BudgetSummaryChart budgetSummary={data.budgetSummary} />
        <SubmissionSummary submissionSummary={data.submissionSummary} />
      </div>

      <HighRiskKpiList highRiskKpis={data.highRiskKpis} />

      <KpiMappingTable kpiMapping={data.kpiMapping} />
    </div>
  );
}
