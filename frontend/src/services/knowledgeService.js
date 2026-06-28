// Knowledge service (CP20F): wraps the CP14 Knowledge / RAG admin APIs.
// Pelan Taktikal JPN/PPD are operational import files, NOT RAG knowledge sources (BR-012).
import { api } from "./api";

export const knowledgeService = {
  listSources: () => api.get("/knowledge/sources"),
  getSource: (id) => api.get(`/knowledge/sources/${id}`),
  createSource: (data) => api.post("/knowledge/sources", data),
  processSource: (id) => api.post(`/knowledge/sources/${id}/process`, {}),
  createLiveLink: (data) => api.post("/knowledge/live-links", data),
  validateLiveLink: (id) => api.post(`/knowledge/live-links/${id}/validate`, {}),
};

export const SOURCE_CATEGORIES = ["rpm", "policy", "guideline", "circular", "note", "project"];
export const SOURCE_FORMATS = ["txt", "md", "pdf", "docx"];
