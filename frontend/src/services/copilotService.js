// Executive Copilot service (CP20E): wraps the CP16 APIs.
// Advisory only — never approves/sends. Recommendations route to the CP9 approval engine.
import { api } from "./api";

export const copilotService = {
  briefing: () => api.post("/executive-copilot/briefing", {}),
  ask: (question) => api.post("/executive-copilot/ask", { question }),
  createRecommendation: (data) => api.post("/executive-copilot/recommendations", data),
  submitForApproval: (recId) =>
    api.post(`/executive-copilot/recommendations/${recId}/submit-for-approval`, {}),
  history: () => api.get("/executive-copilot/history"),
};
