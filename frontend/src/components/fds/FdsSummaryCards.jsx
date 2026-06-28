// FdsSummaryCards (CP20C): headline FDS metrics from GET /fds/summary.
// The FDS summary groups finance statuses into risk bands:
//   high = insufficient / not received · medium = pending / will be received · low = received / not required.
import { Card, CardContent } from "../ui/card";

function Stat({ label, value, sub, tone = "slate" }) {
  const tones = {
    slate: "text-slate-800", blue: "text-blue-700", red: "text-red-700",
    amber: "text-amber-700", green: "text-green-700",
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

export default function FdsSummaryCards({ summary }) {
  if (!summary) return null;
  const dist = summary.financial_risk_distribution || {};
  const high = dist.high || 0;
  const medium = dist.medium || 0;
  const low = dist.low || 0;
  const issues = high + medium;
  const byStatus = summary.by_status || {};
  const pendingApproval = byStatus.pending_approval || 0;

  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-3 xl:grid-cols-6">
      <Stat label="KPIs w/ Financial Issues" value={issues} tone="amber" sub="High + medium risk" />
      <Stat label="High Financial Risk" value={high} tone="red" sub="Insufficient / not received" />
      <Stat label="Medium Risk" value={medium} tone="amber" sub="Pending / will be received" />
      <Stat label="Low Risk" value={low} tone="green" sub="Received / not required" />
      <Stat label="Strategic Recommendations" value={summary.total_recommendations ?? 0} tone="blue" sub={`${pendingApproval} pending approval`} />
      <Stat label="Pending Approval" value={pendingApproval} tone="slate" sub="Awaiting authorised officer" />
    </div>
  );
}
