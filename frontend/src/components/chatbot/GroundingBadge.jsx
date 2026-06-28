// GroundingBadge (CP20E): shows whether an answer is grounded in sources + a derived confidence.
// There is no numeric confidence from the backend; confidence is derived from grounding/fallback.
export default function GroundingBadge({ grounded, fallback }) {
  if (fallback) {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">
        ○ No grounding
      </span>
    );
  }
  if (grounded) {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-0.5 text-[11px] font-medium text-green-700">
        ● Grounded answer · high confidence
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-medium text-amber-700">
      ◐ Ungrounded · low confidence
    </span>
  );
}
