// QuickActions (V1.2): navigation shortcuts to existing modules. Pure navigation — no data,
// no new routes (every target is an existing page registered in App.jsx).
import { Link } from "react-router-dom";
import { Target, Wallet, FileText, Bell, MessagesSquare, Compass, ChevronRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const ACTIONS = [
  { to: "/app/kpis", label: "KPI Management", icon: Target },
  { to: "/app/fds", label: "Financial Decision Support", icon: Wallet },
  { to: "/app/reports", label: "Reports", icon: FileText },
  { to: "/app/notifications", label: "Notifications", icon: Bell },
  { to: "/app/chatbot", label: "KPI Chatbot", icon: MessagesSquare },
  { to: "/app/copilot", label: "Executive Copilot", icon: Compass },
];

export default function QuickActions() {
  return (
    <Card className="flex h-full flex-col">
      <CardHeader><CardTitle>Quick Actions</CardTitle></CardHeader>
      <CardContent className="space-y-2">
        {ACTIONS.map(({ to, label, icon: Icon }) => (
          <Link
            key={to}
            to={to}
            className="group flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/60 px-3 py-2.5 text-sm font-medium text-navy-700 transition-all hover:border-royal-200 hover:bg-royal-50"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-royal-600 shadow-sm">
              <Icon className="h-4 w-4" />
            </span>
            <span className="flex-1">{label}</span>
            <ChevronRight className="h-4 w-4 text-slate-400 transition-transform group-hover:translate-x-0.5 group-hover:text-royal-600" />
          </Link>
        ))}
      </CardContent>
    </Card>
  );
}
