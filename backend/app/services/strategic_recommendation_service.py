"""Strategic Recommendation draft (CP11; V1.1.2 enriched) — deterministic, advisory, human-review.

Produces a clear intervention: recommended action, reason, related activity/milestone, urgency,
expected impact, and a low-cost option. Advisory only — official use routes through approval (no AI).
"""
from __future__ import annotations

_IMPACT = {
    "Priority Action": "High impact at low cost — deliver now.",
    "Strategic Investment": "High impact; justify and optimise the cost.",
    "Avoid / Redesign": "Low impact for the cost — redesign or reallocate.",
    "Optional / Quick Win": "Incremental impact — keep cost minimal.",
}


def build(*, finance_risk: str, funding_gap: bool, quadrant: str, vfm: str,
          kpi_status: str | None = None, activity: str | None = None,
          milestone: str | None = None, remarks: str | None = None) -> dict:
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

    if kpi_status in ("off_track", "at_risk"):
        rationale_parts.append(f"KPI is {kpi_status.replace('_', ' ')}")

    # priority
    if finance_risk == "high" or quadrant in ("Priority Action", "Avoid / Redesign") \
            or kpi_status == "off_track":
        priority = 1
    elif finance_risk == "medium" or vfm == "moderate" or kpi_status == "at_risk":
        priority = 2
    else:
        priority = 3
    urgency = {1: "High", 2: "Medium", 3: "Low"}[priority]

    low_cost = ("Already low-cost — protect funding and scale."
                if quadrant == "Priority Action" else
                "Use shared / digital / low-cost delivery and pool resources across sectors and PPDs.")

    rationale = "Recommended because " + ", ".join(rationale_parts) + "."
    return {
        "recommended_action": "; ".join(actions),
        "rationale": rationale,
        "reason": rationale,                       # explicit "reason" (V1.1.2)
        "related_activity": activity,
        "related_milestone": milestone,
        "pic_remarks": remarks,
        "urgency": urgency,
        "expected_impact": _IMPACT.get(quadrant, "Moderate impact."),
        "low_cost_option": low_cost,
        "priority": priority,
        "human_review_required": True,             # always advisory (BR-015/028/037/046)
    }
