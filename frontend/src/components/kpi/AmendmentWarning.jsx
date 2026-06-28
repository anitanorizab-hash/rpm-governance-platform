// AmendmentWarning (CP20B): mirrors BR-008 — statement/indicator/target are amendable
// only during July and October, unless a Super Admin override is applied.
// The backend is authoritative; this is a client-side advisory + override gate.
export const AMENDMENT_MONTHS = [7, 10]; // July, October

export function isAmendmentWindowOpen(date = new Date()) {
  return AMENDMENT_MONTHS.includes(date.getMonth() + 1);
}

export default function AmendmentWarning({ isSuperAdmin = false, override = false, onToggleOverride }) {
  const open = isAmendmentWindowOpen();
  if (open) {
    return (
      <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">
        The amendment window is open (July / October). Statement, Indicator and Target can be amended.
      </div>
    );
  }

  return (
    <div className="space-y-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
      <p>This field can only be amended during the approved amendment window.</p>
      {isSuperAdmin && (
        <label className="flex items-center gap-2 text-xs font-medium text-amber-900">
          <input
            type="checkbox"
            checked={override}
            onChange={(e) => onToggleOverride?.(e.target.checked)}
          />
          Apply Super Admin override (BR-008) — this action is audited.
        </label>
      )}
    </div>
  );
}
