"""S15 RALPH LOOP Review Skill (CP12) — internal QA on an AI output before the HITL gate.

Deterministic checks: grounding, citation presence, advisory-only compliance, human-review
requirement, and unsafe direct-action detection. Bounded (single pass). NEVER approves/sends.
"""
from __future__ import annotations

import re

from app.skills.base import Skill

UNSAFE_PATTERNS = re.compile(
    r"\b(send (the )?email|deleting|delete|approve(d)?|reject(ed)?|execute|dispatch|finalis[ez]e|"
    r"issue (the )?report|pay(ment)?)\b", re.I,
)


class RalphLoopReviewSkill(Skill):
    name = "ralph_loop_review"
    description = "QA an AI output (grounding/citation/advisory/human-review/unsafe-action). Never acts."
    deterministic = True

    def run(self, payload: dict) -> dict:
        text = str(payload.get("text") or "")
        citations = payload.get("citations") or []
        advisory_only = payload.get("advisory_only", True)
        human_review_required = payload.get("human_review_required", True)
        action = str(payload.get("action") or "")

        unsafe = bool(UNSAFE_PATTERNS.search(text) or UNSAFE_PATTERNS.search(action))
        # An output is "actionable" if it is explicitly flagged so, or it attempts an action.
        actionable = bool(payload.get("actionable", False)) or unsafe

        # Citation/grounding checks apply to knowledge-grounded outputs (chatbot/copilot),
        # not to operational drafts (notifications/reports). Callers opt out via requires_citation=False.
        requires_citation = payload.get("requires_citation", True)

        issues = []
        if requires_citation and not payload.get("grounded", bool(citations)):
            issues.append("not_grounded")
        if requires_citation and not citations:
            issues.append("missing_citation")
        if advisory_only is not True:
            issues.append("not_advisory_only")
        # Human-review is only required for actionable outputs (recommendations/actions),
        # not for info-only answers (e.g. a grounded chatbot reply).
        if actionable and human_review_required is not True:
            issues.append("human_review_not_required")
        if unsafe:
            issues.append("unsafe_direct_action")

        passed = len(issues) == 0
        return {
            "passed": passed,
            "issues": issues,
            "verdict": "pass" if passed else "revise",
            "note": "Advisory QA only — human makes the final decision (ASM-11).",
        }
