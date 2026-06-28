// Dashboard page (CP20A; V1.1 organisation-aware): main landing page.
// Organisation-level filter (All / JPN / PPD); a specific PPD scopes every view, while
// "All PPD" shows the cross-PPD comparison. No AI provider is called from the client.
import { useCallback, useEffect, useMemo, useState } from "react";
import { dashboardService } from "../services/dashboardService";
import { organisationService } from "../services/organisationService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Button } from "../components/ui/button";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import OverviewCards from "../components/dashboard/OverviewCards";
import TerasSummaryChart from "../components/dashboard/TerasSummaryChart";
import RiskSummaryChart from "../components/dashboard/RiskSummaryChart";
import BudgetSummaryChart from "../components/dashboard/BudgetSummaryChart";
import SubmissionSummary from "../components/dashboard/SubmissionSummary";
import HighRiskKpiList from "../components/dashboard/HighRiskKpiList";
import KpiMappingTable from "../components/dashboard/KpiMappingTable";
import ExecutiveSummaryCard from "../components/dashboard/ExecutiveSummaryCard";
import PpdComparisonPanel from "../components/dashboard/PpdComparisonPanel";

export default function Dashboard() {
  const { user } = useAuth();
  const [orgs, setOrgs] = useState([]);
  const [orgLevel, setOrgLevel] = useState("all"); // all | jpn | ppd
  const [ppdId, setPpdId] = useState("");
  const [data, setData] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const jpnOrg = useMemo(() => orgs.find((o) => o.type === "JPN") || null, [orgs]);
  const ppdOptions = useMemo(
    () => orgs.filter((o) => o.type === "PPD").map((o) => ({ id: o.id, name: o.name })),
    [orgs]
  );
  const showComparison = orgLevel === "ppd" && !ppdId;
  const effectiveOrgId = useMemo(() => {
    if (orgLevel === "jpn") return jpnOrg?.id || null;
    if (orgLevel === "ppd") return ppdId || null;
    return null;
  }, [orgLevel, ppdId, jpnOrg]);

  // Load the organisation hierarchy once (populates the filter).
  useEffect(() => {
    organisationService.list().then(setOrgs).catch(() => setOrgs([]));
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (showComparison) {
        const cmp = await dashboardService.ppdComparison(jpnOrg?.id || undefined);
        setComparison(cmp);
        setData(null);
      } else {
        const oid = effectiveOrgId || undefined;
        const [
          overview, terasSummary, riskSummary, budgetSummary,
          submissionSummary, highRiskKpis, kpiMapping, executiveSummary,
        ] = await Promise.all([
          dashboardService.overview(oid),
          dashboardService.terasSummary(oid),
          dashboardService.riskSummary(oid),
          dashboardService.budgetSummary(oid),
          dashboardService.submissionSummary(oid),
          dashboardService.highRiskKpis(oid),
          dashboardService.kpiMapping(oid),
          dashboardService.executiveSummary(oid),
        ]);
        setData({
          overview, terasSummary, riskSummary, budgetSummary,
          submissionSummary, highRiskKpis, kpiMapping, executiveSummary,
        });
        setComparison(null);
      }
    } catch (err) {
      setError(err.message || "Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  }, [showComparison, effectiveOrgId, jpnOrg]);

  useEffect(() => { load(); }, [load]);

  const scopeLabel =
    orgLevel === "all" ? "All organisations"
      : orgLevel === "jpn" ? (jpnOrg?.name || "JPN")
        : (ppdId ? (ppdOptions.find((p) => p.id === ppdId)?.name || "PPD") : "All PPD (comparison)");

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Dashboard</h1>
          <p className="text-sm text-slate-500">
            RPM 2026–2035 KPI overview · {scopeLabel}
            {user?.name ? ` · ${user.name}` : ""}
          </p>
        </div>
        <div className="flex items-end gap-3">
          <OrgLevelFilter
            level={orgLevel}
            onLevelChange={(lvl) => { setOrgLevel(lvl); setPpdId(""); }}
            ppdId={ppdId}
            onPpdChange={setPpdId}
            ppdOptions={ppdOptions}
          />
          <Button variant="outline" onClick={load}>Refresh</Button>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {loading ? (
        <Loading label="Loading dashboard…" />
      ) : showComparison ? (
        <PpdComparisonPanel comparison={comparison} />
      ) : data ? (
        <>
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
        </>
      ) : null}
    </div>
  );
}
