// PIC Directory service (V1.1.1): admin CRUD, KPI assignment, Excel bulk import/export.
import { api, tokenStore } from "./api";

function qs(params = {}) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => { if (v) q.append(k, v); });
  const s = q.toString();
  return s ? `?${s}` : "";
}

export const picService = {
  list: (filters) => api.get(`/pics${qs(filters)}`),
  get: (id) => api.get(`/pics/${id}`),
  create: (data) => api.post("/pics", data),
  update: (id, data) => api.patch(`/pics/${id}`, data),
  remove: (id) => api.del(`/pics/${id}`),
  assignKpis: (id, kpiIds) => api.post(`/pics/${id}/assign-kpis`, { kpi_ids: kpiIds }),

  importFile: async (file) => {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${api.baseUrl}/pics/import`, {
      method: "POST",
      headers: { Authorization: `Bearer ${tokenStore.get()}` },
      body: fd,
    });
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || "Import failed");
    return res.json();
  },

  exportFile: async () => {
    const res = await fetch(`${api.baseUrl}/pics/export`, {
      headers: { Authorization: `Bearer ${tokenStore.get()}` },
    });
    if (!res.ok) throw new Error("Export failed");
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "pic_directory.xlsx"; a.click();
    URL.revokeObjectURL(url);
  },
};
