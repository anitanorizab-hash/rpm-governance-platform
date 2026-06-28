// ReportPreview (CP20D): narrative/summary preview of the report (advisory, pre-approval).
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function ReportPreview({ report }) {
  const c = report?.content || {};
  return (
    <Card>
      <CardHeader><CardTitle>Report Preview</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <h2 className="text-lg font-semibold text-slate-800">{report?.title || c.title || "Untitled Report"}</h2>
        <p className="text-xs text-slate-500">Reporting period: {report?.period || c.reporting_period || "—"}</p>
        {report?.summary || c.summary ? (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Summary</p>
            <p className="mt-0.5 text-sm text-slate-700">{report?.summary || c.summary}</p>
          </div>
        ) : null}
        {c.narrative && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Narrative</p>
            <p className="mt-0.5 whitespace-pre-line text-sm text-slate-700">{c.narrative}</p>
          </div>
        )}
        {Array.isArray(c.citations) && c.citations.length > 0 && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Citations</p>
            <ul className="mt-0.5 list-inside list-disc text-sm text-slate-600">
              {c.citations.map((cit, i) => <li key={i}>{typeof cit === "string" ? cit : JSON.stringify(cit)}</li>)}
            </ul>
          </div>
        )}
        <p className="text-[11px] text-slate-400">
          Advisory draft — not an official record until approved by an authorised officer (ASM-11).
        </p>
      </CardContent>
    </Card>
  );
}
