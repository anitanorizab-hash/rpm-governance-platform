// LowCostHighImpactMatrix (CP20C): 2×2 cost/impact matrix (BR-011/046), highlighting the KPI quadrant.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

// quadrant key by (cost, impact)
const CELLS = [
  { cost: "low", impact: "high", name: "Priority Action", desc: "Low Cost + High Impact", tone: "green" },
  { cost: "high", impact: "high", name: "Strategic Investment", desc: "High Cost + High Impact", tone: "blue" },
  { cost: "low", impact: "low", name: "Optional / Quick Win", desc: "Low Cost + Low Impact", tone: "amber" },
  { cost: "high", impact: "low", name: "Avoid / Redesign", desc: "High Cost + Low Impact", tone: "red" },
];

const TONE = {
  green: "border-green-300 bg-green-50",
  blue: "border-blue-300 bg-blue-50",
  amber: "border-amber-300 bg-amber-50",
  red: "border-red-300 bg-red-50",
};

export default function LowCostHighImpactMatrix({ lchi }) {
  const selected = lchi?.quadrant;

  return (
    <Card>
      <CardHeader><CardTitle>Low Cost / High Impact Matrix</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        {lchi && (
          <p className="text-sm text-slate-600">
            This KPI: <span className="font-medium">{lchi.quadrant}</span> — cost {lchi.cost_level},
            impact {lchi.impact_level}
            {lchi.cost_total != null ? ` · allocation RM${Number(lchi.cost_total).toLocaleString()}` : ""}.
          </p>
        )}
        <div className="grid grid-cols-2 gap-3">
          {CELLS.map((c) => {
            const isSel = selected === c.name;
            return (
              <div
                key={c.name}
                className={`rounded-lg border-2 p-4 transition ${
                  isSel ? `${TONE[c.tone]} ring-2 ring-offset-1 ring-slate-400` : "border-slate-200 bg-white"
                }`}
              >
                <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{c.desc}</p>
                <p className="mt-1 text-sm font-semibold text-slate-800">{c.name}</p>
                {isSel && (
                  <span className="mt-2 inline-block rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-white">
                    Selected KPI
                  </span>
                )}
              </div>
            );
          })}
        </div>
        <p className="text-[11px] text-slate-400">Axes: cost (RM allocation) × impact (achievement vs target).</p>
      </CardContent>
    </Card>
  );
}
