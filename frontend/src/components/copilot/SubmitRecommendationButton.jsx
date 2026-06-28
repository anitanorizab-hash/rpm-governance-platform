// SubmitRecommendationButton (CP20E): routes a Copilot recommendation to CP9 approval (HITL).
// Never approves — only creates a pending approval request.
import { Button } from "../ui/button";

const SUBMITTED = ["pending_approval", "approved", "rejected"];

export default function SubmitRecommendationButton({ recommendation, submitting, onSubmit }) {
  if (!recommendation?.id) return null;
  if (SUBMITTED.includes(recommendation.status)) {
    return <span className="text-xs font-medium text-slate-600">Routed for approval (status: {recommendation.status}).</span>;
  }
  return (
    <Button onClick={() => onSubmit(recommendation.id)} disabled={submitting}>
      {submitting ? "Submitting…" : "Submit for Approval"}
    </Button>
  );
}
