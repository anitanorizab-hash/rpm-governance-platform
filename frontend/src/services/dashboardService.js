// Dashboard service (CP20A; V1.1 organisation-aware): wraps the CP10 dashboard APIs.
// All calls accept an optional organisationId to scope a view to a single org (JPN or one PPD).
import { api } from "./api";

function orgQ(organisationId) {
  return organisationId ? `?organisation_id=${encodeURIComponent(organisationId)}` : "";
}

export const dashboardService = {
  overview: (organisationId) => api.get(`/dashboard/overview${orgQ(organisationId)}`),
  terasSummary: (organisationId) => api.get(`/dashboard/teras-summary${orgQ(organisationId)}`),
  riskSummary: (organisationId) => api.get(`/dashboard/risk-summary${orgQ(organisationId)}`),
  budgetSummary: (organisationId) => api.get(`/dashboard/budget-summary${orgQ(organisationId)}`),
  submissionSummary: (organisationId) => api.get(`/dashboard/submission-summary${orgQ(organisationId)}`),
  highRiskKpis: (organisationId) => api.get(`/dashboard/high-risk-kpis${orgQ(organisationId)}`),
  kpiMapping: (organisationId) => api.get(`/dashboard/kpi-mapping${orgQ(organisationId)}`),
  executiveSummary: (organisationId) => api.get(`/dashboard/executive-summary${orgQ(organisationId)}`),
  // V1.1: cross-PPD comparison (optionally scoped to PPDs under one JPN parent).
  ppdComparison: (parentOrganisationId) =>
    api.get(
      `/dashboard/ppd-comparison${
        parentOrganisationId ? `?parent_organisation_id=${encodeURIComponent(parentOrganisationId)}` : ""
      }`
    ),
};
