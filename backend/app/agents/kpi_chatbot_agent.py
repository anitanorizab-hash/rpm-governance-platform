"""KPI Chatbot Agent (CP15) — RAG retrieval + role-scoped KPI data + citation grounding + RALPH LOOP.

Composes an advisory, cited answer from two grounding sources: (a) knowledge chunks retrieved via RAG
and (b) role-scoped operational KPI data passed in by the service (the agent never touches the DB).
When an LLM provider is configured the answer is synthesised over that grounding via the provider
adapter (S13/§13, provider-agnostic); otherwise a deterministic factual composition is used. Either
way: only provided grounding is used (never invented), sources are cited (BR-025), no grounding yields
the fixed fallback string (BR-027), and the RALPH LOOP reviews the answer. Info-only — no formal action.
"""
from __future__ import annotations

from app.agents.base import Agent
from app.skills.base import safe_chat

_OPERATIONAL_SOURCE = {"title": "Operational KPI data (role-scoped)",
                       "source_id": "operational", "chunk_id": None, "ref": "kpi-summary"}

_SYSTEM = (
    "You are an advisory KPI governance assistant for RPM 2026-2035. Answer the user's question "
    "USING ONLY the grounding provided below — never invent figures or facts. Be concise and direct; "
    "lead with the specific number or fact asked for. If the grounding does not contain the answer, "
    "say you cannot find it in the available data. You do not approve, send, or execute anything."
)


class KPIChatbotAgent(Agent):
    name = "kpi_chatbot"
    description = "Grounded Q&A: RAG + role-scoped KPI context, cited, RALPH-reviewed, safe fallback."
    uses_skills = ["rag_retrieval", "citation_grounding", "ralph_loop_review", "kpi_analysis"]

    def run(self, context: dict) -> dict:
        query = context.get("query", "")
        db = context.get("_db")
        operational_context = context.get("operational_context", []) or []   # role-filtered upstream
        operational_summary = context.get("operational_summary")             # role-scoped aggregates

        # 1) knowledge retrieval
        retrieval = self.skill("rag_retrieval", {"query": query, "db": db})
        results = retrieval.get("results", []) or []

        # 2) optional KPI analysis if numeric context supplied
        analysis = None
        if context.get("achievement") is not None and context.get("target") is not None:
            analysis = self.skill("kpi_analysis", {"achievement": context["achievement"],
                                                   "target": context["target"]})

        # 3) assemble grounding (operational KPI data + knowledge chunks)
        op_facts = self._operational_facts(operational_summary, operational_context)
        sources = list(results)
        if op_facts:
            sources = [_OPERATIONAL_SOURCE, *sources]   # operational data is a cited grounding source

        # No grounding at all → deterministic fixed fallback (BR-027), enforced by the skill below.
        if not op_facts and not results:
            answer_text = None
        else:
            answer_text = self._compose(query, op_facts, results)

        # 4) ground + cite (deterministic; emits the fixed fallback when ungrounded)
        grounded = self.skill("citation_grounding", {"answer": answer_text, "sources": sources})

        # 5) RALPH LOOP QA on the produced answer (advisory; info-only chatbot)
        ralph = self.skill("ralph_loop_review", {
            "text": grounded["answer"], "citations": grounded["citations"],
            "advisory_only": True, "human_review_required": False, "action": "",
        })

        return self._wrap({
            "query": query,
            "answer": grounded["answer"],
            "citations": grounded["citations"],
            "grounded": grounded["grounded"],
            "fallback_used": grounded["fallback"],
            "fallback": grounded["fallback"],   # alias (back-compat with CP13/CP14)
            "retrieval_mode": retrieval.get("mode"),
            "answer_source": "fallback" if grounded["fallback"] else self._answer_source,
            "operational_context": operational_context,
            "kpi_analysis": analysis,
            "ralph_review": ralph,
            "human_review_required": False,   # informational answer; no formal action
        })

    # ---- grounding helpers (operate only on passed-in context; no DB access) ----
    @staticmethod
    def _operational_facts(summary: dict | None, context: list[dict]) -> str:
        """Render role-scoped KPI data as plain grounding text. Empty string when none."""
        lines: list[str] = []
        if summary:
            lines.append(
                f"KPI portfolio ({summary.get('scope', 'role-scoped')}): "
                f"{summary.get('total_kpis', 0)} KPIs total; "
                f"{summary.get('high_risk', 0)} high-risk, {summary.get('medium_risk', 0)} medium-risk, "
                f"{summary.get('low_risk', 0)} low-risk; "
                f"{summary.get('missing_information', 0)} with incomplete information."
            )
            by_teras = summary.get("by_teras") or {}
            if by_teras:
                lines.append("KPIs by Teras: "
                             + ", ".join(f"Teras {n}: {c}" for n, c in by_teras.items() if c))
            hr = summary.get("high_risk_kpis") or []
            if hr:
                lines.append("High-risk KPIs: "
                             + ", ".join(f"{h['code']} (Teras {h['teras']})" for h in hr if h.get("code")))
            # V1.1: organisation-aware PPD comparison grounding (rendered only when present).
            comp = summary.get("ppd_comparison")
            if comp:
                ppds = comp.get("ppds") or []
                if ppds:
                    lines.append(
                        "PPD comparison — "
                        + "; ".join(
                            f"{p['name']}: {p['total_kpis']} KPIs, {p['achieved']} achieved, "
                            f"{p['high_risk']} high-risk" for p in ppds
                        )
                    )
                if comp.get("top_performer"):
                    lines.append(f"Top-performing PPD: {comp['top_performer']}.")
                if comp.get("lowest_performer"):
                    lines.append(f"Lowest-performing PPD: {comp['lowest_performer']}.")
                if comp.get("highest_risk"):
                    lines.append(f"Highest-risk PPD: {comp['highest_risk']}.")
        for k in context:
            lines.append(
                f"KPI {k.get('code')}: status {k.get('status')}, risk {k.get('risk')}, "
                f"Teras {k.get('teras')}."
            )
        return "\n".join(lines)

    def _compose(self, query: str, op_facts: str, results: list[dict]) -> str:
        """Synthesise an answer over the grounding via the provider adapter; deterministic fallback."""
        knowledge = "\n\n".join((r.get("text") or "") for r in results[:3]).strip()
        # Deterministic fallback (also the answer when no LLM key/SDK): operational facts lead, then
        # the most relevant knowledge snippet. Mirrors what the LLM is asked to produce.
        det_parts = [p for p in (op_facts, (knowledge[:600] if knowledge else "")) if p]
        deterministic = "\n\n".join(det_parts) if det_parts else (knowledge[:600] if knowledge else "")

        grounding = ""
        if op_facts:
            grounding += f"[Operational KPI data]\n{op_facts}\n\n"
        if knowledge:
            grounding += f"[Knowledge sources]\n{knowledge[:2000]}"

        result = safe_chat(
            [{"role": "system", "content": _SYSTEM},
             {"role": "user", "content": f"Question: {query}\n\nGrounding:\n{grounding}"}],
            fallback=deterministic,
        )
        self._answer_source = result["source"]   # "ai" when synthesised, else "fallback"
        return result["text"]

    _answer_source = "fallback"
