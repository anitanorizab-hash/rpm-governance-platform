// Role-aware sidebar (CP19). Menu items are placeholders; feature pages arrive in later prompts.
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { cn } from "../lib/utils";

const MENU = [
  { to: "/app/dashboard", label: "Dashboard", icon: "📊" },
  { to: "/app/kpis", label: "KPI Management", icon: "🎯" },
  { to: "/app/monthly-updates", label: "Monthly Updates", icon: "🗓️" },
  { to: "/app/fds", label: "Financial Decision Support", icon: "💰" },
  { to: "/app/reports", label: "Reports", icon: "📄" },
  { to: "/app/notifications", label: "Notifications", icon: "🔔" },
  { to: "/app/chatbot", label: "Chatbot", icon: "💬" },
  { to: "/app/copilot", label: "Executive Copilot", icon: "🧭" },
  { to: "/app/admin", label: "Admin", icon: "⚙️", roles: ["super_admin", "jpn_admin"] },
];

export default function Sidebar() {
  const { hasRole } = useAuth();
  const items = MENU.filter((m) => !m.roles || hasRole(...m.roles));
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-200 bg-white md:flex">
      <div className="px-5 py-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">RPM 2026–2035</p>
        <p className="text-sm font-semibold text-slate-800">Governance Platform</p>
      </div>
      <nav className="flex-1 px-2 py-2">
        {items.map((m) => (
          <NavLink
            key={m.to}
            to={m.to}
            className={({ isActive }) =>
              cn("flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium",
                 isActive ? "bg-blue-50 text-blue-700" : "text-slate-600 hover:bg-slate-100")
            }
          >
            <span className="text-base leading-none">{m.icon}</span>
            <span>{m.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-slate-100 px-5 py-3">
        <p className="text-[11px] text-slate-400">v1.0.0 · Advisory AI · Human-approved</p>
      </div>
    </aside>
  );
}
