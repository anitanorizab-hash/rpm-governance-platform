// CitationViewer (CP20E): supporting citations for briefing/ask (BR-025); honest empty state.
export default function CitationViewer({ citations, evidenceNote }) {
  const items = citations || [];
  if (items.length === 0) {
    return (
      <p className="text-xs text-slate-400">{evidenceNote || "No supporting citations available."}</p>
    );
  }
  return (
    <div>
      <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">Supporting Sources</p>
      <ul className="mt-1 space-y-1">
        {items.map((c, i) => (
          <li key={i} className="text-xs text-slate-600">
            <span className="font-medium text-slate-800">{c.title || c.source_id || c.ref || `Source ${i + 1}`}</span>
            {c.ref && c.title ? <span className="text-slate-400"> · {c.ref}</span> : null}
          </li>
        ))}
      </ul>
    </div>
  );
}
