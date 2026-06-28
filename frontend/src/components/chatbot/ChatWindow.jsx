// ChatWindow (CP20E): scrollable conversation area with auto-scroll + typing indicator.
import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";

export default function ChatWindow({ messages, sending, emptyHint }) {
  const endRef = useRef(null);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, sending]);

  return (
    <div className="flex-1 space-y-3 overflow-y-auto rounded-xl border border-slate-200 bg-slate-50 p-4">
      {messages.length === 0 && !sending ? (
        <div className="flex h-full items-center justify-center py-12 text-center text-sm text-slate-500">
          {emptyHint || "Ask a question about KPI data or RPM 2026–2035."}
        </div>
      ) : (
        messages.map((m, i) => <ChatMessage key={m.id || i} msg={m} />)
      )}
      {sending && <TypingIndicator />}
      <div ref={endRef} />
    </div>
  );
}
