// Dashboard service (CP20A): wraps the CP10 dashboard APIs.
import { api } from "./api";

export const dashboardService = {
  overview: () => api.get("/dashboard/overview"),
  terasSummary: () => api.get("/dashboard/teras-summary"),
  riskSummary: () => api.get("/dashboard/risk-summary"),
  budgetSummary: () => api.get("/dashboard/budget-summary"),
  submissionSummary: () => api.get("/dashboard/submission-summary"),
  highRiskKpis: () => api.get("/dashboard/high-risk-kpis"),
  kpiMapping: () => api.get("/dashboard/kpi-mapping"),
  executiveSummary: () => api.get("/dashboard/executive-summary"),
};
