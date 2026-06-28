"""Financial Decision Support Agent (CP13) — composes fds/lchi/obb/strategic skills. Advisory + HITL."""
from __future__ import annotations

from app.agents.base import Agent


class FinancialDecisionSupportAgent(Agent):
    name = "financial_decision_support"
    description = "Budget Intelligence + Low Cost High Impact + OBB + strategic recommendation (advisory)."
    uses_skills = ["fds", "low_cost_high_impact", "obb_analysis", "strategic_recommendation"]
    human_review_required = True

    def run(self, context: dict) -> dict:
        achievement, target = context.get("achievement"), context.get("target")
        cost_total = context.get("cost_total", 0.0)

        bi = self.skill("fds", {"finance_status": context.get("finance_status")})
        m = self.skill("low_cost_high_impact", {"cost_total": cost_total,
                                                "achievement": achievement, "target": target})
        obb = self.skill("obb_analysis", {
            "expected_outcome": context.get("expected_outcome"), "statement": context.get("statement"),
            "cost_total": cost_total, "expenditure": context.get("expenditure", 0.0),
            "achievement": achievement, "target": target,
            "cost_level": m.get("cost_level"), "impact_level": m.get("impact_level"),
        })
        rec = self.skill("strategic_recommendation", {
            "finance_risk": bi.get("financial_risk"), "funding_gap": bi.get("funding_gap"),
            "quadrant": m.get("quadrant"), "vfm": obb.get("value_for_money"),
        })
        return self._wrap({"budget_intelligence": bi, "low_cost_high_impact": m,
                           "obb_analysis": obb, "strategic_recommendation": rec})
