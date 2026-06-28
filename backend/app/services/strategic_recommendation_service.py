"""Strategic Recommendation draft (CP11) — deterministic, advisory, human-review-required. No AI."""
from __future__ import annotations

# priority: 1 = highest
def build(*, finance_risk: str, funding_gap: bool, quadrant: str, vfm: str) -> dict:
    actions, rationale_parts = [], []

    if funding_gap:
        actions.append("Address funding gap (reallocate / seek low-cost delivery / collaboration)")
        rationale_parts.append("allocation is pending/insufficient/not received")

    if quadrant == "Priority Action":
        actions.append("Prioritise delivery and protect funding")
        rationale_parts.append("low cost with high impact")
    elif quadrant == "Avoid / Redesign":
        actions.append("Redesign, consolidate, or reallocate budget")
        rationale_parts.append("high cost with low impact")
    elif quadrant == "Strategic Investment":
        actions.append("Phase delivery and pursue shared resources")
        rationale_parts.append("high impact justifies investment if cost is optimised")
    else:  # Optional / Quick Win
        actions.append("Deliver via low-cost / digital channels")
        rationale_parts.append("low impact — keep cost minimal")

    # priority
    if finance_risk == "high" or quadrant in ("Priority Action", "Avoid / Redesign"):
        priority = 1
    elif finance_risk == "medium" or vfm == "moderate":
        priority = 2
    else:
        priority = 3

    return {
        "recommended_action": "; ".join(actions),
        "rationale": "Recommended because " + ", ".join(rationale_parts) + ".",
        "priority": priority,
        "human_review_required": True,   # always advisory (BR-015/028/037/046)
    }
