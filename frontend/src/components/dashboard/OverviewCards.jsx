// OverviewCards (V1.2): premium KPI stat cards. Data binding unchanged from GET /dashboard/overview.
import { Card } from "../ui/card";
import { Target, AlertTriangle, ClipboardList, CheckCircle2 } from "lucide-react";

const TONES = {
  royal: { text: "text-royal-600", chip: "bg-royal-50 text-royal-600" },
  red:   { text: "text-danger",    chip: "bg-red-50 text-danger" },
  amber: { text: "text-amber-600", chip: "bg-amber-50 text-amber-600" },
  green: { text: "text-success",   chip: "bg-green-50 text-success" },
};

function Stat({ label, value, sub, tone = "royal", icon: Icon }) {
  const t = TONES[tone] || TONES.royal;
  return (
    <Card className="p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-card-hover">
      <div className="flex items-start justify-between">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{label}</p>
        {Icon && <span className={`flex h-9 w-9 items-center justify-center rounded-xl ${t.chip}`}><Icon className="h-5 w-5" /></span>}
      </div>
      <p className={`mt-3 font-display text-3xl font-bold ${t.text}`}>{value}</p>
      {sub && <p className="mt-1 text-xs text-slate-500">{sub}</p>}
    </Card>
  );
}

export default function OverviewCards({ overview }) {
  if (!overview) return null;
  const ach = overview.achievement || {};
  const risk = overview.risk || {};
  const comp = overview.completion || {};
  const achieved = ach.achieved || ach.on_track || 0;
  const highRisk = risk.high || 0;
  const incomplete = (comp.incomplete || 0) + (comp.not_updated || 0);

  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      <Stat label="Total KPIs" value={overview.total_kpis ?? 0} tone="royal" sub="Teras 1–7" icon={Target} />
      <Stat label="High Risk" value={highRisk} tone="red" sub="Require attention" icon={AlertTriangle} />
      <Stat label="Incomplete / Not Updated" value={incomplete} tone="amber" sub="Missing information" icon={ClipboardList} />
      <Stat label="Missing Information" value={overview.missing_information ?? 0} tone="green" sub={`${achieved} achieved / on-track`} icon={CheckCircle2} />
    </div>
  );
}
