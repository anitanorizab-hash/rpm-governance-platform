// Notification service (CP20D): wraps the CP18 Notification APIs.
// HITL: draft → submit-for-review (CP9) → approved → queue (dry-run send). Never sends without approval.
import { api } from "./api";

export const notificationService = {
  list: () => api.get("/notifications"),
  get: (id) => api.get(`/notifications/${id}`),
  draft: (data) => api.post("/notifications/draft", data),
  patch: (id, fields) => api.patch(`/notifications/${id}`, fields),
  submitForReview: (id) => api.post(`/notifications/${id}/submit-for-review`, {}),
  queue: (id) => api.post(`/notifications/${id}/queue`, {}),
  cancel: (id) => api.post(`/notifications/${id}/cancel`, {}),
  emailQueue: () => api.get("/notifications/email-queue"),
  retry: (id) => api.post(`/notifications/email-queue/${id}/retry`, {}),
};

// Approved notification-type vocabulary (must match backend NOTIFICATION_TYPES).
export const NOTIFICATION_TYPES = [
  { value: "reminder", label: "Reminder" },
  { value: "missing_info", label: "Missing Information" },
  { value: "approval", label: "Approval" },
  { value: "report", label: "Report" },
  { value: "escalation", label: "Escalation" },
  { value: "fds_review", label: "FDS Review" },
];
