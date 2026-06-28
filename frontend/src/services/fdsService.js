// FDS service (CP20C): wraps the CP11 Financial Decision Support APIs.
// All FDS outputs are advisory; FDS never approves/executes (BR-015/028).
import { api } from "./api";

export const fdsService = {
  summary: () => api.get("/fds/summary"),
  analysis: (kpiId) => api.get(`/fds/kpis/${kpiId}/analysis`),
  generate: (kpiId) => api.post(`/fds/kpis/${kpiId}/generate`, {}),
  listRecommendations: (kpiId) =>
    api.get(`/fds/recommendations${kpiId ? `?kpi_id=${encodeURIComponent(kpiId)}` : ""}`),
  getRecommendation: (recId) => api.get(`/fds/recommendations/${recId}`),
  submitForApproval: (recId) => api.post(`/fds/recommendations/${recId}/submit-for-approval`, {}),
};
