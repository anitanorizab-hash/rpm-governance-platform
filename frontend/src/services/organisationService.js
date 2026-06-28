// Organisation service (V1.1): wraps GET /organisations (JPN → PPD hierarchy).
import { api } from "./api";

export const organisationService = {
  list: (params = {}) => {
    const qs = new URLSearchParams();
    if (params.type) qs.append("type", params.type);
    if (params.parent_id) qs.append("parent_id", params.parent_id);
    const s = qs.toString();
    return api.get(`/organisations${s ? `?${s}` : ""}`);
  },
};
