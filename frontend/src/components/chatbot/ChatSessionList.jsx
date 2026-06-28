// ChatSessionList (CP20E): conversation list + new chat. No provider/system details exposed.
import { Button } from "../ui/button";

const fmt = (s) => {
  if (!s) return "Session";
  const d = new Date(s);
  return isNaN(d) ? "Session" : d.toLocaleString();
};

export default function ChatSessionList({ sessions, activeId, onSelect, onNew, creating }) {
  const rows = sessions || [];
  return (
    <div className="flex h-full flex-col rounded-xl border border-slate-200 bg-white">
      <div className="border-b border-slate-100 p-3">
        <Button className="w-full" onClick={onNew} disabled={creating}>
          {creating ? "Starting…" : "+ New Conversation"}
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto p-2">
        {rows.length === 0 ? (
          <p className="px-2 py-6 text-center text-xs text-slate-400">No conversations yet.</p>
        ) : (
          <ul className="space-y-1">
            {rows.map((s) => (
              <li key={s.id}>
                <button
                  onClick={() => onSelect(s)}
                  className={`w-full rounded-md px-3 py-2 text-left text-sm ${
                    activeId === s.id ? "bg-blue-50 text-blue-700" : "text-slate-600 hover:bg-slate-100"}`}
                >
                  <span className="block truncate font-medium">Conversation</span>
                  <span className="block truncate text-[11px] text-slate-400">{fmt(s.started_at)}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
