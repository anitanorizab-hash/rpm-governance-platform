// ChatInput (CP20E): message box + optional KPI figures (achievement/target) for analysis.
import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");
  const [showFigures, setShowFigures] = useState(false);
  const [achievement, setAchievement] = useState("");
  const [target, setTarget] = useState("");

  function submit(e) {
    e.preventDefault();
    const t = text.trim();
    if (!t || disabled) return;
    onSend(t, achievement.trim() || null, target.trim() || null);
    setText("");
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      {showFigures && (
        <div className="flex gap-2">
          <Input value={achievement} onChange={(e) => setAchievement(e.target.value)} placeholder="Achievement (optional)" />
          <Input value={target} onChange={(e) => setTarget(e.target.value)} placeholder="Target (optional)" />
        </div>
      )}
      <div className="flex items-end gap-2">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) submit(e); }}
          rows={2}
          placeholder="Type your question…  (Enter to send, Shift+Enter for a new line)"
          disabled={disabled}
          className="flex-1 resize-none rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        <Button type="submit" disabled={disabled || !text.trim()}>Send</Button>
      </div>
      <button type="button" onClick={() => setShowFigures((v) => !v)}
              className="text-[11px] text-slate-400 hover:text-slate-600">
        {showFigures ? "Hide KPI figures" : "Add KPI figures (optional)"}
      </button>
    </form>
  );
}
