// SubmitForReviewButton (CP20D): routes a draft report to the CP9 approval engine (HITL).
// Never approves — only creates a pending review request.
import { Button } from "../ui/button";

export default function SubmitForReviewButton({ status, canManage, submitting, onSubmit }) {
  if (!canManage) return null;
  if (status !== "draft") {
    return <span className="text-xs text-slate-500">Submit available only for drafts (current: {status}).</span>;
  }
  return (
    <Button onClick={onSubmit} disabled={submitting}>
      {submitting ? "Submitting…" : "Submit for Review"}
    </Button>
  );
}
