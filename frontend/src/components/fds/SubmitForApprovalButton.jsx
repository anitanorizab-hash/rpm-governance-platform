// SubmitForApprovalButton (CP20C): routes a recommendation to the CP9 approval engine (HITL).
// This NEVER approves — it only creates a pending approval request (BR-015/ASM-11).
import { Button } from "../ui/button";

const SUBMITTED_STATES = ["pending_approval", "approved", "rejected"];

export default function SubmitForApprovalButton({ recommendation, canManage, submitting, onSubmit }) {
  if (!recommendation?.id) return null;
  const alreadySubmitted = SUBMITTED_STATES.includes(recommendation.status);

  if (!canManage) {
    return <span className="text-xs text-slate-500">Submission requires an authorised administrator.</span>;
  }
  if (alreadySubmitted) {
    return (
      <span className="text-xs font-medium text-slate-600">
        Already routed for approval (status: {recommendation.status}).
      </span>
    );
  }
  return (
    <Button onClick={() => onSubmit(recommendation.id)} disabled={submitting}>
      {submitting ? "Submitting…" : "Submit for Approval"}
    </Button>
  );
}
