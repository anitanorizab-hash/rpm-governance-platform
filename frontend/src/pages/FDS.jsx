// FDS page (CP20C): Financial Decision Support — Budget Intelligence, OBB, Low Cost High Impact,
// Strategic Recommendations + HITL approval submission. All outputs are advisory (BR-015/ASM-11).
import { useCallback, useEffect, useMemo, useState } from "react";
import { fdsService } from "../services/fdsService";
import { kpiService } from "../services/kpiService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Label } from "../components/ui/input";
import FdsSummaryCards from "../components/fds/FdsSummaryCards";
import KpiFinancialAnalysis from "../components/fds/KpiFinancialAnalysis";
import RecommendationList from "../components/fds/RecommendationList";

const MANAGE_ROLES = ["super_admin", "jpn_admin", "sector_admin", "finance_officer"];
const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function FDS() {
  const { hasRole } = useAuth();
  const canManage = hasRole(...MANAGE_ROLES);

  const [summary, setSummary] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedKpiId, setSelectedKpiId] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  const [generatedRec, setGeneratedRec] = useState(null);

  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState(null);

  const refreshLists = useCallback(async () => {
    const [sum, recs] = await Promise.all([fdsService.summary(), fdsService.listRecommendations()]);
    setSummary(sum);
    setRecommendations(recs);
    return recs;
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [sum, recs, list] = await Promise.all([
        fdsService.summary(),
        fdsService.listRecommendations(),
        kpiService.list({ limit: 500 }),
      ]);
      setSummary(sum);
      setRecommendations(recs);
      setKpis(list);
    } catch (err) {
      setError(err.message || "Failed to load FDS data.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  // Latest persisted recommendation for a KPI (used to drive the submit button).
  const findRecForKpi = useCallback((kpiId, recs = recommendations) => {
    const matches = recs.filter((r) => r.kpi_id === kpiId);
    if (!matches.length) return null;
    return matches.slice().sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];
  }, [recommendations]);

  const loadAnalysis = useCallback(async (kpiId, recs) => {
    if (!kpiId) { setAnalysis(null); setGeneratedRec(null); return; }
    setAnalysisLoading(true);
    setAnalysisError(null);
    setSubmitMessage(null);
    setGenerateError(null);
    try {
      const a = await fdsService.analysis(kpiId);
      setAnalysis(a);
      setGeneratedRec(findRecForKpi(kpiId, recs || recommendations));
    } catch (err) {
      setAnalysisError(err.message || "Failed to load analysis.");
      setAnalysis(null);
    } finally {
      setAnalysisLoading(false);
    }
  }, [findRecForKpi, recommendations]);

  function onSelectKpi(kpiId) {
    setSelectedKpiId(kpiId);
    loadAnalysis(kpiId);
  }

  async function onGenerate() {
    if (!selectedKpiId) return;
    setGenerating(true);
    setGenerateError(null);
    try {
      const res = await fdsService.generate(selectedKpiId);
      setAnalysis(res);
      const recs = await refreshLists();
      setGeneratedRec(res.recommendation_id
        ? { id: res.recommendation_id, status: "draft", kpi_id: selectedKpiId }
        : findRecForKpi(selectedKpiId, recs));
    } catch (err) {
      setGenerateError(err.message || "Generation failed.");
    } finally {
      setGenerating(false);
    }
  }

  async function onSubmit(recId) {
    setSubmitting(true);
    setSubmitMessage(null);
    try {
      const res = await fdsService.submitForApproval(recId);
      setSubmitMessage(`Routed for approval (approval state: ${res.approval_state}). Awaiting an authorised officer.`);
      setGeneratedRec((g) => (g ? { ...g, status: res.recommendation_status } : g));
      await refreshLists();
    } catch (err) {
      setSubmitMessage(null);
      setGenerateError(err.message || "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  }

  function onSelectRecommendation(rec) {
    setSelectedKpiId(rec.kpi_id);
    loadAnalysis(rec.kpi_id);
  }

  const selectedKpi = useMemo(() => kpis.find((k) => k.id === selectedKpiId), [kpis, selectedKpiId]);

  if (loading) return <Loading label="Loading Financial Decision Support…" />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Financial Decision Support</h1>
        <p className="text-sm text-slate-500">
          Budget intelligence, OBB, Low Cost High Impact analysis and advisory recommendations.
          All outputs are advisory — final approval remains with authorised officers (ASM-11).
        </p>
      </div>

      <FdsSummaryCards summary={summary} />

      <Card>
        <CardHeader><CardTitle>KPI Financial Analysis</CardTitle></CardHeader>
        <CardContent className="space-y-2">
          <Label>Select KPI</Label>
          <select className={selectCls} value={selectedKpiId} onChange={(e) => onSelectKpi(e.target.value)}>
            <option value="">— Choose a KPI —</option>
            {kpis.map((k) => (
              <option key={k.id} value={k.id}>{k.code} — {k.statement || "(no statement)"}</option>
            ))}
          </select>
          {selectedKpi && (
            <p className="text-xs text-slate-500">
              Teras {selectedKpi.teras_number ?? "—"} · {selectedKpi.sector || "—"}
            </p>
          )}
        </CardContent>
      </Card>

      {analysisLoading ? (
        <Loading label="Analysing KPI finances…" />
      ) : analysisError ? (
        <ErrorMessage message={analysisError} />
      ) : (
        <KpiFinancialAnalysis
          analysis={analysis}
          canManage={canManage}
          generatedRec={generatedRec}
          onGenerate={onGenerate}
          generating={generating}
          generateError={generateError}
          onSubmit={onSubmit}
          submitting={submitting}
          submitMessage={submitMessage}
        />
      )}

      <RecommendationList
        recommendations={recommendations}
        selectedId={generatedRec?.id}
        onSelect={onSelectRecommendation}
      />
    </div>
  );
}
