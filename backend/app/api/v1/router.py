"""Aggregate all /api/v1 routers (CP4)."""
from fastapi import APIRouter

from app.api.v1.routes import (
    agents, approvals, audit, auth, chatbot, dashboard, executive_copilot, fds, health, imports,
    knowledge, kpis, monthly_updates, notifications, organisations, reports, skills, users,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(audit.router)
api_router.include_router(imports.router)
api_router.include_router(kpis.router)
api_router.include_router(monthly_updates.router)
api_router.include_router(monthly_updates.kpi_scoped_router)
api_router.include_router(approvals.router)
api_router.include_router(dashboard.router)
api_router.include_router(organisations.router)
api_router.include_router(fds.router)
api_router.include_router(skills.router)
api_router.include_router(agents.router)
api_router.include_router(knowledge.router)
api_router.include_router(chatbot.router)
api_router.include_router(executive_copilot.router)
api_router.include_router(reports.router)
api_router.include_router(notifications.router)
