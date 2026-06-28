// RecommendationList (CP20C): persisted strategic recommendations from GET /fds/recommendations.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const STATUS_TONE = {
  draft: "bg-slate-100 text-slate-600",
  pending_approval: "bg-amber-50 text-amber-700",
  approved: "bg-green-50 text-green-700",
  rejected: "bg-red-50 text-red-700",
};
const PRIORITY_TONE = {
  1: "bg-red-50 text-red-700", 2: "bg-amber-50 text-amber-700", 3: "bg-slate-100 text-slate-600",
};
const prettify = (s) => (s == null ? "—" : String(s).replace(/_/g, " "));

export default function RecommendationList({ recommendations, selectedId, onSelect }) {
  const rows = recommendations || [];
  return (
    <Card>
      <CardHeader><CardTitle>Strategic Recommendations ({rows.length})</CardTitle></CardHeader>
      <CardContent className="px-0 py-0">
        {rows.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">
            No recommendations generated yet. Select a KPI and generate one.
          </p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {rows.map((r) => (
              <li
                key={r.id}
                onClick={() => onSelect?.(r)}
                className={`cursor-pointer px-5 py-3 hover:bg-slate-50 ${selectedId === r.id ? "bg-blue-50/50" : ""}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-slate-800">{r.content || "(no action)"}</p>
                    <p className="mt-0.5 truncate text-xs text-slate-500">{r.rationale || ""}</p>
                  </div>
                  <div className="flex shrink-0 flex-col items-end gap-1">
                    <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${STATUS_TONE[r.status] || "bg-slate-100 text-slate-600"}`}>
                      {prettify(r.status)}
                    </span>
                    {r.priority != null && (
                      <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${PRIORITY_TONE[r.priority] || "bg-slate-100 text-slate-600"}`}>
                        P{r.priority}
                      </span>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
