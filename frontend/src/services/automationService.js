// Automation service (V1.1.1): administrator-triggered, HITL-safe draft generation.
// Generates report/notification DRAFTS only — they still require approval before queue/send.
import { api } from "./api";

export const automationService = {
  run: ({ types, period, limit } = {}) =>
    api.post("/automation/run", { types, period, limit }),
};

export const AUTOMATION_TYPES = [
  { value: "monthly_report", label: "Monthly Report Draft" },
  { value: "pic_reminders", label: "PIC Reminder Drafts" },
  { value: "missing_info", label: "Missing-Info Reminder Drafts" },
  { value: "overdue_escalations", label: "Overdue Escalation Drafts" },
];
