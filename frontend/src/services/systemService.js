// System service (CP20F): wraps the health/readiness/provider endpoints. No secrets are returned.
import { api } from "./api";

export const systemService = {
  health: () => api.health(),                 // public liveness (no auth)
  ready: () => api.get("/health/ready"),
  providers: () => api.get("/health/providers"),
};
