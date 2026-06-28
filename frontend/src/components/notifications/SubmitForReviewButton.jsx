// SubmitForReviewButton (CP20D, notifications): routes a draft notification to CP9 approval (HITL).
import { Button } from "../ui/button";

export default function SubmitForReviewButton({ status, canDraft, busy, onSubmit }) {
  if (!canDraft) return null;
  if (status !== "draft") return null;
  return (
    <Button onClick={onSubmit} disabled={busy}>{busy ? "Submitting…" : "Submit for Review"}</Button>
  );
}
