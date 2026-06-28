// Admin (users/roles) service (CP20F): wraps the CP4 User & Role APIs.
// Passwords/secrets are never returned by these endpoints.
import { api } from "./api";

export const adminService = {
  listUsers: () => api.get("/users"),
  getUser: (id) => api.get(`/users/${id}`),
  setRoles: (id, roles) => api.patch(`/users/${id}/roles`, { roles }),
};

// The nine seeded roles (reference list for the assignment form).
export const ALL_ROLES = [
  "super_admin", "jpn_admin", "sector_admin", "ppd_admin", "kpi_pic",
  "finance_officer", "executive", "read_only", "internal_audit",
];
