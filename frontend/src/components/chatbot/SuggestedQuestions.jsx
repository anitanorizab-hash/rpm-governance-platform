// SuggestedQuestions (CP20E): quick-start prompts; clicking sends the question.
const SUGGESTIONS = [
  "How many KPIs are high risk?",
  "Which KPIs have incomplete information?",
  "Summarise KPI performance by Teras.",
  "What does RPM 2026–2035 say about this Teras?",
];

export default function SuggestedQuestions({ onPick, disabled }) {
  return (
    <div className="flex flex-wrap gap-2">
      {SUGGESTIONS.map((q) => (
        <button
          key={q}
          onClick={() => onPick(q)}
          disabled={disabled}
          className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600 hover:bg-slate-50 disabled:opacity-50"
        >
          {q}
        </button>
      ))}
    </div>
  );
}
