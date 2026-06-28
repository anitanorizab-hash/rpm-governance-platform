// ChatMessage (CP20E): a single chat bubble. Assistant bubbles show grounding, citations and
// a human-review indicator. The fixed fallback string is rendered exactly as returned.
import CitationPanel from "./CitationPanel";
import GroundingBadge from "./GroundingBadge";

export default function ChatMessage({ msg }) {
  const isUser = msg.role === "user";
  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-br-sm bg-blue-600 px-4 py-2 text-sm text-white">
          {msg.text}
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="max-w-[85%] space-y-2">
        <div className="rounded-2xl rounded-bl-sm bg-white border border-slate-200 px-4 py-2 text-sm text-slate-800">
          <p className="whitespace-pre-line">{msg.text}</p>
        </div>
        <div className="flex flex-wrap items-center gap-2 pl-1">
          <GroundingBadge grounded={msg.grounded} fallback={msg.fallback} />
          {msg.humanReview && (
            <span className="rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-medium text-amber-700">
              Human review required
            </span>
          )}
          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-500">
            Advisory only
          </span>
        </div>
        <CitationPanel citations={msg.citations} />
      </div>
    </div>
  );
}
