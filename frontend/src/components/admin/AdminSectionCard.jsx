// AdminSectionCard (CP20F): overview tile linking to an admin sub-section.
import { Link } from "react-router-dom";
import { Card, CardContent } from "../ui/card";

export default function AdminSectionCard({ title, count, hint, to, tone = "slate" }) {
  const tones = { slate: "text-slate-800", blue: "text-blue-700", green: "text-green-700", amber: "text-amber-700" };
  const body = (
    <Card className={to ? "transition hover:border-blue-300 hover:shadow" : ""}>
      <CardContent className="py-4">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{title}</p>
        <p className={`mt-1 text-2xl font-semibold ${tones[tone] || tones.slate}`}>{count}</p>
        {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
      </CardContent>
    </Card>
  );
  return to ? <Link to={to} className="block">{body}</Link> : body;
}
