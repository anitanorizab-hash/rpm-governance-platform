// KpiFinancialAnalysis (CP20C): renders one KPI's FDS analysis (advisory, deterministic).
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import BudgetStatusBadge from "./BudgetStatusBadge";
import LowCostHighImpactMatrix from "./LowCostHighImpactMatrix";
import ObbAnalysisCard from "./ObbAnalysisCard";
import StrategicRecommendationCard from "./StrategicRecommendationCard";
import SubmitForApprovalButton from "./SubmitForApprovalButton";

export default function KpiFinancialAnalysis({
  analysis, canManage, generatedRec,
  onGenerate, generating, generateError,
  onSubmit, submitting, submitMessage,
}) {
  if (!analysis) {
    return (
      <Card>
        <CardContent className="py-12 text-center text-sm text-slate-500">
          Select a KPI above to view its financial analysis.
        </CardContent>
      </Card>
    );
  }

  const bi = analysis.budget_intelligence || {};
  const lchi = analysis.low_cost_high_impact || {};
  const rec = analysis.strategic_recommendation || {};

  // Footer for the recommendation card: generate (if not persisted) or submit-for-approval.
  const footer = generatedRec?.id ? (
    <div className="space-y-2">
      <SubmitForApprovalButton
        recommendation={generatedRec}
        canManage={canManage}
        submitting={submitting}
        onSubmit={onSubmit}
      />
      {submitMessage && (
        <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{submitMessage}</div>
      )}
    </div>
  ) : canManage ? (
    <div className="space-y-2">
      <Button onClick={onGenerate} disabled={generating}>
        {generating ? "Generating…" : "Generate Recommendation"}
      </Button>
      <p className="text-xs text-slate-500">
        Generating persists this advisory recommendation as a draft (audited). It is not approved or sent.
      </p>
      {generateError && (
        <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{generateError}</div>
      )}
    </div>
  ) : (
    <p className="text-xs text-slate-500">This is a draft advisory analysis. Generation requires an authorised administrator.</p>
  );

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>{analysis.code} — Financial Analysis</CardTitle>
          <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-600">
            Advisory only
          </span>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Finance Status</p>
              <div className="mt-1"><BudgetStatusBadge value={bi.finance_status} kind="finance" /></div>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Financial Risk</p>
              <div className="mt-1"><BudgetStatusBadge value={bi.financial_risk} kind="risk" /></div>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Funding Gap</p>
              <div className="mt-1 text-sm text-slate-700">{bi.funding_gap ? "Yes" : "No"}</div>
            </div>
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Budget Intelligence</p>
            <p className="mt-0.5 text-sm text-slate-700">{bi.summary || "—"}</p>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <LowCostHighImpactMatrix lchi={lchi} />
        <ObbAnalysisCard obb={analysis.obb_analysis} />
      </div>

      <Card>
        <CardHeader><CardTitle>Low-Cost Alternatives & Resource Optimisation</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Suggested Low-Cost Alternatives</p>
            {Array.isArray(lchi.low_cost_alternatives) && lchi.low_cost_alternatives.length ? (
              <ul className="mt-1 list-inside list-disc text-sm text-slate-700">
                {lchi.low_cost_alternatives.map((a, i) => <li key={i}>{a}</li>)}
              </ul>
            ) : <p className="text-sm text-slate-500">—</p>}
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Resource Optimisation Notes</p>
            <p className="mt-0.5 text-sm text-slate-700">{lchi.resource_optimisation_notes || "—"}</p>
          </div>
        </CardContent>
      </Card>

      <StrategicRecommendationCard
        action={rec.recommended_action}
        rationale={rec.rationale}
        priority={rec.priority}
        status={generatedRec?.status}
        humanReviewRequired={rec.human_review_required !== false}
        footer={footer}
      />
    </div>
  );
}
