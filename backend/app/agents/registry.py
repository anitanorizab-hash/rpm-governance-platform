"""Agent registry (CP13): the 11 approved primary agents (A2), discoverable by name."""
from __future__ import annotations

from app.agents.audit_trail_agent import AuditTrailAgent
from app.agents.executive_copilot_agent import ExecutiveCopilotAgent
from app.agents.financial_decision_support_agent import FinancialDecisionSupportAgent
from app.agents.knowledge_alignment_agent import KnowledgeAlignmentAgent
from app.agents.kpi_analysis_agent import KPIAnalysisAgent
from app.agents.kpi_chatbot_agent import KPIChatbotAgent
from app.agents.notification_agent import NotificationAgent
from app.agents.report_generation_agent import ReportGenerationAgent
from app.agents.risk_assessment_agent import RiskAssessmentAgent
from app.agents.strategic_recommendation_agent import StrategicRecommendationAgent
from app.agents.validation_agent import ValidationAgent

_AGENT_CLASSES = [
    KPIAnalysisAgent, ValidationAgent, FinancialDecisionSupportAgent, RiskAssessmentAgent,
    StrategicRecommendationAgent, KnowledgeAlignmentAgent, KPIChatbotAgent,
    ReportGenerationAgent, NotificationAgent, AuditTrailAgent, ExecutiveCopilotAgent,
]

REGISTRY = {cls.name: cls() for cls in _AGENT_CLASSES}


def get_agent(name: str):
    return REGISTRY.get(name)


def list_agents():
    return [a.metadata() for a in REGISTRY.values()]
