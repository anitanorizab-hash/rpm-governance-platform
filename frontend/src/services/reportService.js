// Report service (CP20D): wraps the CP17 Report APIs.
// HITL: draft → submit-for-review (CP9) → approved → archived. No approve/reject/auto-issue here.
import { api } from "./api";

export const reportService = {
  list: () => api.get("/reports"),
  get: (id) => api.get(`/reports/${id}`),
  generate: (period, type = "monthly", organisationId) =>
    api.post(
      `/reports/generate${organisationId ? `?organisation_id=${encodeURIComponent(organisationId)}` : ""}`,
      { period, type }
    ),
  patch: (id, fields) => api.patch(`/reports/${id}`, fields),
  submitForReview: (id) => api.post(`/reports/${id}/submit-for-review`, {}),
  archive: (id) => api.post(`/reports/${id}/archive`, {}),
};
