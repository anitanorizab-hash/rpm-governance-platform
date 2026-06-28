// OverviewCards (V1.2): executive KPI cards. Values and percentages are derived purely from the
// real GET /dashboard/overview counts (pct = n / total_kpis) — the same arithmetic pattern as
// SubmissionSummary. No values, trends or percentages are fabricated.
import { Card } from "../ui/card";
import { Target, AlertTriangle, ClipboardList, CheckCircle2 } from "lucide-react";

const TONES = {
  royal: { text: "text-royal-600", chip: "bg-royal-50 text-royal-600", bar: "bg-royal-500" },
  green: { text: "text-success",   chip: "bg-green-50 text-success",   bar: "bg-success" },
  red:   { text: "text-danger",    chip: "bg-red-50 text-danger",      bar: "bg-danger" },
  amber: { text: "text-amber-600", chip: "bg-amber-50 text-amber-600", bar: "bg-amber-500" },
};

function Stat({ label, value, pct, sub, tone = "royal", icon: Icon }) {
  const t = TONES[tone] || TONES.royal;
  return (
    <Card className="p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-card-hover">
      <div className="flex items-start justify-between">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{label}</p>
        {Icon && <span className={`flex h-10 w-10 items-center justify-center rounded-xl ${t.chip}`}><Icon className="h-5 w-5" /></span>}
      </div>
      <div className="mt-3 flex items-end gap-2">
        <p className={`font-display text-3xl font-bold leading-none ${t.text}`}>{value}</p>
        {pct != null && <span className={`mb-0.5 rounded-md px-1.5 py-0.5 text-xs font-semibold ${t.chip}`}>{pct}%</span>}
      </div>
      {pct != null && (
        <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
          <div className={`h-full rounded-full ${t.bar}`} style={{ width: `${Math.min(pct, 100)}%` }} />
        </div>
      )}
      {sub && <p className="mt-2 text-xs text-slate-500">{sub}</p>}
    </Card>
  );
}

export default function OverviewCards({ overview }) {
  if (!overview) return null;
  const ach = overview.achievement || {};
  const risk = overview.risk || {};
  const comp = overview.completion || {};
  const total = overview.total_kpis ?? 0;
  const achieved = ach.achieved || ach.on_track || 0;
  const highRisk = risk.high || 0;
  const incomplete = (comp.incomplete || 0) + (comp.not_updated || 0);
  const pct = (n) => (total > 0 ? Math.round((n / total) * 100) : null);

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <Stat label="Total KPIs" value={total} tone="royal" icon={Target}
            sub={`Teras 1–7 · ${overview.missing_information ?? 0} missing information`} />
      <Stat label="Achieved / On-Track" value={achieved} pct={pct(achieved)} tone="green" icon={CheckCircle2} sub="Meeting targets" />
      <Stat label="High Risk" value={highRisk} pct={pct(highRisk)} tone="red" icon={AlertTriangle} sub="Require attention" />
      <Stat label="Incomplete / Not Updated" value={incomplete} pct={pct(incomplete)} tone="amber" icon={ClipboardList} sub="Missing monthly updates" />
    </div>
  );
}
