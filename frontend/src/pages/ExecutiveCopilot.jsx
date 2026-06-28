// Executive Copilot page (CP20E; V1.1 organisation-aware): advisory leadership decision support
// (HITL; no direct approval). Org filter switches between Overall JPN / individual PPD / cross-PPD.
import { useCallback, useEffect, useMemo, useState } from "react";
import { copilotService } from "../services/copilotService";
import { dashboardService } from "../services/dashboardService";
import { kpiService } from "../services/kpiService";
import { useAuth } from "../context/AuthContext";
import { useOrgScope } from "../hooks/useOrgScope";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import PpdComparisonPanel from "../components/dashboard/PpdComparisonPanel";
import HumanReviewBanner from "../components/copilot/HumanReviewBanner";
import ExecutiveBriefingCard from "../components/copilot/ExecutiveBriefingCard";
import RiskInsightsPanel from "../components/copilot/RiskInsightsPanel";
import BudgetInsightsPanel from "../components/copilot/BudgetInsightsPanel";
import RecommendationPanel from "../components/copilot/RecommendationPanel";
import CitationViewer from "../components/copilot/CitationViewer";
import GroundingBadge from "../components/chatbot/GroundingBadge";

const COPILOT_ROLES = ["super_admin", "jpn_admin", "executive"];

export default function ExecutiveCopilot() {
  const { hasRole } = useAuth();
  const canUse = hasRole(...COPILOT_ROLES);
  const { level, ppdId, setPpdId, onLevelChange, ppdOptions, showComparison, organisationId, scopeLabel, jpnOrg } = useOrgScope();

  const [history, setHistory] = useState([]);
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [briefing, setBriefing] = useState(null);
  const [briefingBusy, setBriefingBusy] = useState(false);
  const [comparison, setComparison] = useState(null);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [asking, setAsking] = useState(false);

  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState(null);
  const [createdRec, setCreatedRec] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitMsg, setSubmitMsg] = useState(null);

  const scopedKpis = useMemo(
    () => (organisationId ? kpis.filter((k) => k.organisation_id === organisationId) : kpis),
    [kpis, organisationId]
  );

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const [hist, list] = await Promise.all([copilotService.history(), kpiService.list({ limit: 500 })]);
      setHistory(hist); setKpis(list);
    } catch (err) {
      setError(err.message || "Failed to load Executive Copilot.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { if (canUse) load(); else setLoading(false); }, [canUse, load]);

  // Cross-PPD comparison loads on demand when "All PPD" is selected.
  useEffect(() => {
    if (!canUse) return;
    if (showComparison) {
      dashboardService.ppdComparison(jpnOrg?.id || undefined).then(setComparison).catch(() => setComparison(null));
    } else {
      setComparison(null);
    }
  }, [canUse, showComparison, jpnOrg]);

  // Briefing/answer are scope-specific; clear them when the scope changes.
  useEffect(() => { setBriefing(null); setAnswer(null); }, [organisationId, showComparison]);

  async function onGenerateBriefing() {
    setBriefingBusy(true); setError(null);
    try {
      setBriefing(await copilotService.briefing(organisationId || undefined));
      setHistory(await copilotService.history());
    } catch (err) { setError(err.message || "Briefing failed."); }
    finally { setBriefingBusy(false); }
  }

  async function onAsk(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setAsking(true); setError(null);
    try {
      setAnswer(await copilotService.ask(question.trim(), organisationId || undefined));
      setHistory(await copilotService.history());
    } catch (err) { setError(err.message || "Question failed."); }
    finally { setAsking(false); }
  }

  async function onCreateRec(data) {
    setCreating(true); setCreateError(null); setSubmitMsg(null);
    try { setCreatedRec(await copilotService.createRecommendation(data)); }
    catch (err) { setCreateError(err.message || "Draft failed."); }
    finally { setCreating(false); }
  }

  async function onSubmitRec(recId) {
    setSubmitting(true); setSubmitMsg(null);
    try {
      const res = await copilotService.submitForApproval(recId);
      setSubmitMsg(`Routed for approval (state: ${res.approval_state}). Awaiting an authorised officer.`);
      setCreatedRec((r) => (r ? { ...r, status: res.recommendation_status } : r));
    } catch (err) { setCreateError(err.message || "Submission failed."); }
    finally { setSubmitting(false); }
  }

  if (loading) return <Loading label="Loading Executive Copilot…" />;

  if (!canUse) {
    return (
      <div className="space-y-4">
        <h1 className="text-xl font-semibold text-slate-800">Executive Copilot</h1>
        <Card><CardContent className="py-10 text-center text-sm text-slate-500">
          Executive Copilot is available to Executive Management, JPN Administrator and Super Admin only.
        </CardContent></Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Executive Copilot</h1>
          <p className="text-sm text-slate-500">Advisory leadership decision support · {scopeLabel}.</p>
        </div>
        <OrgLevelFilter level={level} onLevelChange={onLevelChange} ppdId={ppdId} onPpdChange={setPpdId} ppdOptions={ppdOptions} />
      </div>

      <HumanReviewBanner humanReviewRequired />
      {error && <ErrorMessage message={error} />}

      {showComparison ? (
        <>
          <p className="text-sm font-medium text-slate-600">Cross-PPD performance &amp; risk comparison</p>
          <PpdComparisonPanel comparison={comparison} />
        </>
      ) : (
        <>
          <div className="flex items-center gap-3">
            <Button onClick={onGenerateBriefing} disabled={briefingBusy}>
              {briefingBusy ? "Generating…" : briefing ? "Regenerate Briefing" : "Generate Briefing"}
            </Button>
            {briefing && <span className="text-xs text-slate-400">Briefing is advisory; human review required.</span>}
          </div>

          {briefing && (
            <>
              <ExecutiveBriefingCard briefing={briefing} />
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <RiskInsightsPanel keyRisks={briefing.key_risks} />
                <BudgetInsightsPanel fds={briefing.budget_fds_insights} />
              </div>
            </>
          )}

          <Card>
            <CardHeader><CardTitle>Ask a Strategic Question</CardTitle></CardHeader>
            <CardContent className="space-y-3">
              <form onSubmit={onAsk} className="flex items-end gap-2">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  rows={2}
                  placeholder="e.g. Where should we focus budget to reduce high-risk KPIs?"
                  className="flex-1 resize-none rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <Button type="submit" disabled={asking || !question.trim()}>{asking ? "Asking…" : "Ask"}</Button>
              </form>
              {answer && (
                <div className="space-y-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-3">
                  <p className="whitespace-pre-line text-sm text-slate-800">{answer.answer}</p>
                  <div className="flex flex-wrap items-center gap-2">
                    <GroundingBadge grounded={answer.grounded} fallback={answer.fallback_used} />
                    <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-500">Advisory only</span>
                  </div>
                  <CitationViewer citations={answer.citations} evidenceNote={answer.evidence_note} />
                </div>
              )}
            </CardContent>
          </Card>

          <RecommendationPanel
            kpis={scopedKpis}
            onCreate={onCreateRec}
            creating={creating}
            createError={createError}
            createdRec={createdRec}
            onSubmit={onSubmitRec}
            submitting={submitting}
            submitMsg={submitMsg}
          />
        </>
      )}

      <Card>
        <CardHeader><CardTitle>Copilot History ({history.length})</CardTitle></CardHeader>
        <CardContent className="px-0 py-0">
          {history.length === 0 ? (
            <p className="py-8 text-center text-sm text-slate-500">No interactions yet.</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {history.map((h) => (
                <li key={h.id} className="px-5 py-3">
                  <p className="text-sm font-medium text-slate-800">{h.question || "(briefing)"}</p>
                  {h.answer && <p className="mt-0.5 line-clamp-2 text-xs text-slate-500">{h.answer}</p>}
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
