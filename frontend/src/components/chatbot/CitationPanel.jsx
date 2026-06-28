// CitationPanel (CP20E): renders source citations {title, source_id, chunk_id, ref} (BR-025).
export default function CitationPanel({ citations }) {
  const items = citations || [];
  if (items.length === 0) return null;
  return (
    <div className="mt-2 rounded-md border border-slate-200 bg-white px-3 py-2">
      <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">Sources</p>
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
