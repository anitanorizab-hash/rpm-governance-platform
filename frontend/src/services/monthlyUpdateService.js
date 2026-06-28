// Monthly Update service (CP20B): wraps the CP8 monthly-update APIs (in-system only; no Excel).
import { api } from "./api";

export const monthlyUpdateService = {
  // body: { kpi_id, reporting_year, reporting_month, achievement_value, finance_status,
  //         evidence_ref, remarks, issue_description, proposed_action }
  create: (body, override = false) =>
    api.post(`/monthly-updates${override ? "?override=true" : ""}`, body),
  listForKpi: (kpiId) => api.get(`/kpis/${kpiId}/monthly-updates`),
  summary: () => api.get(`/monthly-updates/summary`),
};

// Approved finance-status vocabulary (must match backend FINANCE_STATUSES).
export const FINANCE_STATUSES = [
  { value: "received", label: "Received" },
  { value: "will_be_received", label: "Will be received" },
  { value: "pending", label: "Pending" },
  { value: "not_received", label: "Not received" },
  { value: "not_required", label: "Not required" },
  { value: "insufficient", label: "Insufficient" },
];
