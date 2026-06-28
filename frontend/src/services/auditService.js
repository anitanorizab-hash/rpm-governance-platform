// Audit service (CP20F): wraps the CP5 read-only Audit APIs. No update/delete exists.
import { api } from "./api";

function qs(params = {}) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") q.append(k, v);
  });
  const s = q.toString();
  return s ? `?${s}` : "";
}

export const auditService = {
  // filters: { entity_type, action, limit, offset }
  listLogs: (filters = {}) => api.get(`/audit/logs${qs(filters)}`),
  getLog: (id) => api.get(`/audit/logs/${id}`),
};
