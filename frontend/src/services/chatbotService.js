// Chatbot service (CP20E): wraps the CP15 KPI Chatbot APIs.
// Answers are advisory, role-scoped and cited; the backend emits a fixed fallback when ungrounded.
import { api } from "./api";

export const chatbotService = {
  createSession: () => api.post("/chatbot/sessions", {}),
  listSessions: () => api.get("/chatbot/sessions"),
  getSession: (id) => api.get(`/chatbot/sessions/${id}`),
  sendMessage: (id, message, achievement, target) =>
    api.post(`/chatbot/sessions/${id}/messages`, {
      message,
      ...(achievement ? { achievement } : {}),
      ...(target ? { target } : {}),
    }),
  listMessages: (id) => api.get(`/chatbot/sessions/${id}/messages`),
};

// The fixed fallback string (BR-027) — used only to recognise the message, never to fabricate one.
export const FALLBACK_MESSAGE =
  "I cannot find this information in the available KPI data or knowledge sources.";
