// KPI service (CP20B): wraps the CP7 KPI APIs.
import { api } from "./api";

function buildQuery(params = {}) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") q.append(k, v);
  });
  const s = q.toString();
  return s ? `?${s}` : "";
}

export const kpiService = {
  // filters: { teras, sector, pic, status, completeness, limit, offset }
  list: (filters = {}) => api.get(`/kpis${buildQuery(filters)}`),
  get: (id) => api.get(`/kpis/${id}`),
  patch: (id, body, override = false) =>
    api.patch(`/kpis/${id}${override ? "?override=true" : ""}`, body),
  completeness: (id) => api.get(`/kpis/${id}/completeness`),
  completenessSummary: () => api.get(`/kpis/completeness/summary`),
  // V1.1.1
  assignPic: (id, { name, email, sector }) =>
    api.post(`/kpis/${id}/assign-pic`, { name, email, sector }),
  updateActivity: (id, activityId, fields) =>
    api.patch(`/kpis/${id}/activities/${activityId}`, fields),
};
