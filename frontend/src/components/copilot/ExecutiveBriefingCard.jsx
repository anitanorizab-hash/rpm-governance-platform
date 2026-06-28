// ExecutiveBriefingCard (CP20E): briefing container — summary, KPI highlights, suggested actions, citations.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import ExecutiveSummary from "./ExecutiveSummary";
import CitationViewer from "./CitationViewer";

const prettify = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function Dist({ data }) {
  const entries = Object.entries(data || {}).filter(([, v]) => v != null);
  if (!entries.length) return <span className="text-sm text-slate-500">—</span>;
  return (
    <div className="flex flex-wrap gap-2">
      {entries.map(([k, v]) => (
        <span key={k} className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs text-slate-600">
          {prettify(String(k))}: <span className="font-medium text-slate-800">{v}</span>
        </span>
      ))}
    </div>
  );
}

export default function ExecutiveBriefingCard({ briefing }) {
  if (!briefing) return null;
  const kh = briefing.kpi_highlights || {};
  const actions = briefing.suggested_strategic_actions || [];

  return (
    <Card className="border-blue-100 bg-blue-50/40">
      <CardHeader className="flex flex-row items-center justify-between border-blue-100">
        <CardTitle>Executive Briefing</CardTitle>
        <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-600">
          Advisory only
        </span>
      </CardHeader>
      <CardContent className="space-y-4">
        <ExecutiveSummary text={briefing.executive_summary} />

        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">KPI Highlights</p>
          <p className="mt-1 text-sm text-slate-700">Total KPIs: <span className="font-medium">{kh.total_kpis ?? 0}</span></p>
          <div className="mt-1"><Dist data={kh.by_teras} /></div>
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Suggested Strategic Actions</p>
          {actions.length ? (
            <ul className="mt-1 list-inside list-disc text-sm text-slate-700">
              {actions.map((a, i) => <li key={i}>{a}</li>)}
            </ul>
          ) : <p className="mt-1 text-sm text-slate-500">No specific actions suggested.</p>}
        </div>

        <CitationViewer citations={briefing.citations} evidenceNote={briefing.evidence_note} />
      </CardContent>
    </Card>
  );
}
