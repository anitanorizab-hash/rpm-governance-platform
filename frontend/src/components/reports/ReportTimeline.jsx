// ReportTimeline (CP20D): HITL lifecycle stepper — Draft → Pending Review → Approved → Archived.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const STAGES = ["draft", "pending_review", "approved", "archived"];
const LABELS = {
  draft: "Draft", pending_review: "Pending Review", approved: "Approved", archived: "Archived",
};

export default function ReportTimeline({ status, rejectReason }) {
  const rejected = status === "rejected";
  const currentIdx = STAGES.indexOf(status);

  return (
    <Card>
      <CardHeader><CardTitle>Approval Lifecycle (HITL)</CardTitle></CardHeader>
      <CardContent>
        <ol className="flex flex-wrap items-center gap-2">
          {STAGES.map((s, i) => {
            const done = currentIdx >= i && !rejected;
            const isCurrent = status === s;
            return (
              <li key={s} className="flex items-center gap-2">
                <span className={`flex h-7 items-center rounded-full px-3 text-xs font-medium ${
                  isCurrent ? "bg-blue-600 text-white"
                  : done ? "bg-green-50 text-green-700"
                  : "bg-slate-100 text-slate-400"}`}>
                  {LABELS[s]}
                </span>
                {i < STAGES.length - 1 && <span className="text-slate-300">→</span>}
              </li>
            );
          })}
        </ol>
        {rejected && (
          <div className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            Rejected{rejectReason ? `: ${rejectReason}` : "."} A new draft is required.
          </div>
        )}
        <p className="mt-3 text-[11px] text-slate-400">
          Approval/rejection is performed by an authorised officer in the approvals workflow — not from this screen.
        </p>
      </CardContent>
    </Card>
  );
}
