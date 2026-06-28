// ObbAnalysisCard (CP20C): Outcome-Based Budgeting value-for-money from analysis.obb_analysis.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import BudgetStatusBadge from "./BudgetStatusBadge";

function Row({ label, children }) {
  return (
    <div className="flex items-start justify-between gap-3 py-1.5">
      <span className="text-xs font-medium uppercase tracking-wide text-slate-400">{label}</span>
      <span className="text-right text-sm text-slate-700">{children}</span>
    </div>
  );
}

export default function ObbAnalysisCard({ obb }) {
  if (!obb) return null;
  return (
    <Card>
      <CardHeader><CardTitle>OBB Analysis (Outcome-Based Budgeting)</CardTitle></CardHeader>
      <CardContent className="divide-y divide-slate-100">
        <Row label="Expected Outcome">{obb.expected_outcome || "—"}</Row>
        <Row label="Resource Use">{obb.resource_use || "—"}</Row>
        <Row label="Achievement Ratio">{obb.achievement_ratio != null ? obb.achievement_ratio : "—"}</Row>
        <Row label="Value for Money"><BudgetStatusBadge value={obb.value_for_money} kind="risk" /></Row>
        <Row label="Outcome Risk"><BudgetStatusBadge value={obb.outcome_risk} kind="risk" /></Row>
        <Row label="Optimisation Opportunity">{obb.optimisation_opportunity ? "Yes" : "No"}</Row>
      </CardContent>
    </Card>
  );
}
