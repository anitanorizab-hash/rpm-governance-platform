// Dashboard service (CP20A; V1.1 organisation-aware): wraps the CP10 dashboard APIs.
// All calls accept an optional organisationId to scope a view to a single org (JPN or one PPD).
// V1.2: submissionSummary forwards the existing backend `year` query param (no new endpoint).
import { api } from "./api";

function qs(params) {
  const parts = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== "")
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`);
  return parts.length ? `?${parts.join("&")}` : "";
}

function orgQ(organisationId) {
  return organisationId ? `?organisation_id=${encodeURIComponent(organisationId)}` : "";
}

export const dashboardService = {
  overview: (organisationId) => api.get(`/dashboard/overview${orgQ(organisationId)}`),
  terasSummary: (organisationId) => api.get(`/dashboard/teras-summary${orgQ(organisationId)}`),
  riskSummary: (organisationId) => api.get(`/dashboard/risk-summary${orgQ(organisationId)}`),
  budgetSummary: (organisationId) => api.get(`/dashboard/budget-summary${orgQ(organisationId)}`),
  // year is an existing backend query param on submission-summary (dashboard.py).
  submissionSummary: (organisationId, year) =>
    api.get(`/dashboard/submission-summary${qs({ organisation_id: organisationId, year })}`),
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
