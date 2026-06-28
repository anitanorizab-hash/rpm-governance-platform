// Import service (CP20F): wraps the CP6 Import history APIs (read-only here).
// Excel is initial input only; re-import requires explicit admin override (not exposed in this UI).
import { api } from "./api";

export const importService = {
  history: () => api.get("/imports/history"),
  getBatch: (id) => api.get(`/imports/${id}`),
};
