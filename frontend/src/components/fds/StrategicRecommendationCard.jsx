// StrategicRecommendationCard (CP20C): advisory strategic recommendation (human-review required).
// Works for the live analysis draft (strategic_recommendation) and persisted recommendations.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const PRIORITY_LABEL = { 1: "P1 — Highest", 2: "P2 — Medium", 3: "P3 — Low" };
const PRIORITY_TONE = {
  1: "bg-red-50 text-red-700", 2: "bg-amber-50 text-amber-700", 3: "bg-slate-100 text-slate-600",
};

const URGENCY_TONE = {
  High: "bg-red-50 text-red-700", Medium: "bg-amber-50 text-amber-700", Low: "bg-slate-100 text-slate-600",
};

export default function StrategicRecommendationCard({
  action, rationale, priority, status, humanReviewRequired = true, footer,
  relatedActivity, relatedMilestone, urgency, expectedImpact, lowCostOption,
}) {
  return (
    <Card className="border-blue-100 bg-blue-50/40">
      <CardHeader className="flex flex-row items-center justify-between border-blue-100">
        <CardTitle>Strategic Recommendation</CardTitle>
        <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-600">
          Advisory only
        </span>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Recommended Action</p>
          <p className="mt-0.5 text-sm font-medium text-slate-800">{action || "—"}</p>
        </div>
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Reason</p>
          <p className="mt-0.5 text-sm text-slate-700">{rationale || "—"}</p>
        </div>
        {(relatedActivity || relatedMilestone) && (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Related Activity</p>
              <p className="mt-0.5 text-sm text-slate-700">{relatedActivity || "—"}</p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Related Milestone</p>
              <p className="mt-0.5 text-sm text-slate-700">{relatedMilestone || "—"}</p>
            </div>
          </div>
        )}
        {(expectedImpact || lowCostOption) && (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Expected Impact</p>
              <p className="mt-0.5 text-sm text-slate-700">{expectedImpact || "—"}</p>
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Low-Cost Option</p>
              <p className="mt-0.5 text-sm text-slate-700">{lowCostOption || "—"}</p>
            </div>
          </div>
        )}
        <div className="flex flex-wrap items-center gap-2">
          {urgency && (
            <span className={`rounded-md px-2 py-0.5 text-xs font-medium ${URGENCY_TONE[urgency] || "bg-slate-100 text-slate-600"}`}>
              Urgency: {urgency}
            </span>
          )}
          {priority != null && (
            <span className={`rounded-md px-2 py-0.5 text-xs font-medium ${PRIORITY_TONE[priority] || "bg-slate-100 text-slate-600"}`}>
              {PRIORITY_LABEL[priority] || `Priority ${priority}`}
            </span>
          )}
          {status && (
            <span className="rounded-md border border-slate-200 bg-white px-2 py-0.5 text-xs text-slate-600">
              Status: {String(status).replace(/_/g, " ")}
            </span>
          )}
          {humanReviewRequired && (
            <span className="rounded-md border border-amber-200 bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
              Human review required
            </span>
          )}
        </div>
        <p className="text-[11px] text-slate-400">
          AI/analytics output is advisory and does not replace authorised management decisions.
          Final approval remains with authorised officers (ASM-11).
        </p>
        {footer && <div className="pt-1">{footer}</div>}
      </CardContent>
    </Card>
  );
}
