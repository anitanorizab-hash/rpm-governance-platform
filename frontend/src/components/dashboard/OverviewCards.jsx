// OverviewCards (CP20A): headline KPI metrics from GET /dashboard/overview.
import { Card, CardContent } from "../ui/card";

function Stat({ label, value, sub, tone = "slate" }) {
  const tones = {
    slate: "text-slate-800",
    blue: "text-blue-700",
    red: "text-red-700",
    amber: "text-amber-700",
    green: "text-green-700",
  };
  return (
    <Card>
      <CardContent className="py-4">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{label}</p>
        <p className={`mt-1 text-2xl font-semibold ${tones[tone] || tones.slate}`}>{value}</p>
        {sub && <p className="mt-1 text-xs text-slate-500">{sub}</p>}
      </CardContent>
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
      <Stat label="Total KPIs" value={overview.total_kpis ?? 0} tone="blue" sub="Teras 1–7" />
      <Stat label="High Risk" value={highRisk} tone="red" sub="Require attention" />
      <Stat label="Incomplete / Not Updated" value={incomplete} tone="amber" sub="Missing information" />
      <Stat
        label="Missing Information"
        value={overview.missing_information ?? 0}
        tone="slate"
        sub={`${achieved} achieved / on-track`}
      />
    </div>
  );
}
