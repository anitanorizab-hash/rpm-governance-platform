// HumanReviewBanner (CP20E): standing advisory-only / human-review notice (ASM-11).
export default function HumanReviewBanner({ humanReviewRequired = true }) {
  return (
    <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
      <span className="font-medium">Advisory only.</span>{" "}
      Executive Copilot output supports decisions but does not make them.
      {humanReviewRequired && " Human review is required before any formal action — final approval remains with authorised officers (ASM-11)."}
    </div>
  );
}
