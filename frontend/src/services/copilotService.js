// Executive Copilot service (CP20E): wraps the CP16 APIs.
// Advisory only — never approves/sends. Recommendations route to the CP9 approval engine.
import { api } from "./api";

const orgQ = (organisationId) =>
  organisationId ? `?organisation_id=${encodeURIComponent(organisationId)}` : "";

export const copilotService = {
  briefing: (organisationId) => api.post(`/executive-copilot/briefing${orgQ(organisationId)}`, {}),
  ask: (question, organisationId) => api.post(`/executive-copilot/ask${orgQ(organisationId)}`, { question }),
  createRecommendation: (data) => api.post("/executive-copilot/recommendations", data),
  submitForApproval: (recId) =>
    api.post(`/executive-copilot/recommendations/${recId}/submit-for-approval`, {}),
  history: () => api.get("/executive-copilot/history"),
};
