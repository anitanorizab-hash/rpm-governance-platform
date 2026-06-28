// Dashboard page (V1.2 executive redesign). All data-loading logic is unchanged from CP20A/V1.1:
// same dashboard APIs, same organisation scoping, same comparison branch, same calculations.
// Only the presentation/layout is redesigned (hero + filter bar + executive KPI cards + grid).
// The Reporting Year is forwarded to the existing submission-summary `year` param (other metrics
// are current-state). No AI provider is called from the client.
import { useCallback, useEffect, useMemo, useState } from "react";
import { dashboardService } from "../services/dashboardService";
import { organisationService } from "../services/organisationService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import DashboardHero from "../components/dashboard/DashboardHero";
import DashboardFilterBar from "../components/dashboard/DashboardFilterBar";
import OverviewCards from "../components/dashboard/OverviewCards";
import TerasSummaryChart from "../components/dashboard/TerasSummaryChart";
import RiskSummaryChart from "../components/dashboard/RiskSummaryChart";
import BudgetSummaryChart from "../components/dashboard/BudgetSummaryChart";
import SubmissionSummary from "../components/dashboard/SubmissionSummary";
import HighRiskKpiList from "../components/dashboard/HighRiskKpiList";
import KpiMappingTable from "../components/dashboard/KpiMappingTable";
import ExecutiveSummaryCard from "../components/dashboard/ExecutiveSummaryCard";
import PpdComparisonPanel from "../components/dashboard/PpdComparisonPanel";
import QuickActions from "../components/dashboard/QuickActions";

const CURRENT_YEAR = 2026; // RPM cycle start; matches the current reporting year.

export default function Dashboard() {
  const { user } = useAuth();
  const [orgs, setOrgs] = useState([]);
  const [orgLevel, setOrgLevel] = useState("all"); // all | jpn | ppd
  const [ppdId, setPpdId] = useState("");
  const [year, setYear] = useState(CURRENT_YEAR);
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
          dashboardService.submissionSummary(oid, year),
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
  }, [showComparison, effectiveOrgId, jpnOrg, year]);

  useEffect(() => { load(); }, [load]);

  const scopeLabel =
    orgLevel === "all" ? "All organisations"
      : orgLevel === "jpn" ? (jpnOrg?.name || "JPN")
        : (ppdId ? (ppdOptions.find((p) => p.id === ppdId)?.name || "PPD") : "All PPD (comparison)");

  return (
    <div className="space-y-6">
      <DashboardHero year={year} scopeLabel={scopeLabel} />

      <DashboardFilterBar
        level={orgLevel}
        onLevelChange={(lvl) => { setOrgLevel(lvl); setPpdId(""); }}
        ppdId={ppdId}
        onPpdChange={setPpdId}
        ppdOptions={ppdOptions}
        year={year}
        onYearChange={setYear}
        onRefresh={load}
        onExport={() => window.print()}
      />

      {error && <ErrorMessage message={error} />}

      {loading ? (
        <Loading label="Loading dashboard…" />
      ) : showComparison ? (
        <PpdComparisonPanel comparison={comparison} />
      ) : data ? (
        <div className="space-y-6">
          {/* Executive KPI cards */}
          <OverviewCards overview={data.overview} />

          {/* Advisory executive / AI summary (deterministic; ASM-11) */}
          <ExecutiveSummaryCard executiveSummary={data.executiveSummary} />

          {/* Responsive executive grid — every panel is a real, existing data binding */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
            <RiskSummaryChart riskSummary={data.riskSummary} />
            <TerasSummaryChart terasSummary={data.terasSummary} />
            <BudgetSummaryChart budgetSummary={data.budgetSummary} />
            <SubmissionSummary submissionSummary={data.submissionSummary} />
            <HighRiskKpiList highRiskKpis={data.highRiskKpis} />
            <QuickActions />
          </div>

          {/* Full-width premium mapping table */}
          <KpiMappingTable kpiMapping={data.kpiMapping} />
        </div>
      ) : null}
    </div>
  );
}
