// Role-aware sidebar (V1.2): navy gradient, collapsible (desktop), off-canvas drawer (mobile), Lucide icons.
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard, Target, CalendarClock, Wallet, FileText,
  Bell, MessagesSquare, Compass, Settings, ChevronLeft, X,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { cn } from "../lib/utils";

const MENU = [
  { to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/kpis", label: "KPI Management", icon: Target },
  { to: "/app/monthly-updates", label: "Monthly Updates", icon: CalendarClock },
  { to: "/app/fds", label: "Financial Decision Support", icon: Wallet },
  { to: "/app/reports", label: "Reports", icon: FileText },
  { to: "/app/notifications", label: "Notifications", icon: Bell },
  { to: "/app/chatbot", label: "Chatbot", icon: MessagesSquare },
  { to: "/app/copilot", label: "Executive Copilot", icon: Compass },
  { to: "/app/admin", label: "Admin", icon: Settings, roles: ["super_admin", "jpn_admin"] },
];

function Brand({ collapsed }) {
  return (
    <div className={cn("flex items-center gap-3 px-4 py-4", collapsed && "justify-center px-0")}>
      <img src="/1.jpg" alt="Jabatan Pendidikan Negeri Perak" className="h-10 w-10 shrink-0 rounded-lg bg-white object-contain p-1 shadow" />
      {!collapsed && (
        <div className="min-w-0">
          <p className="truncate text-[11px] font-semibold uppercase tracking-wider text-gold-400">RPM 2026–2035</p>
          <p className="truncate text-sm font-semibold text-white">Governance Platform</p>
        </div>
      )}
    </div>
  );
}

function NavItems({ items, collapsed }) {
  return (
    <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-3">
      {items.map((m) => {
        const Icon = m.icon;
        return (
          <NavLink
            key={m.to}
            to={m.to}
            title={collapsed ? m.label : undefined}
            className={({ isActive }) =>
              cn(
                "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive ? "bg-white/10 text-white" : "text-navy-100/70 hover:bg-white/10 hover:text-white",
                collapsed && "justify-center px-0",
              )
            }
          >
            {({ isActive }) => (
              <>
                {isActive && <span className="absolute left-0 top-1/2 h-6 w-[3px] -translate-y-1/2 rounded-r-full bg-gold-500" />}
                <Icon className="h-5 w-5 shrink-0" strokeWidth={2} />
                {!collapsed && <span className="truncate">{m.label}</span>}
              </>
            )}
          </NavLink>
        );
      })}
    </nav>
  );
}

export default function Sidebar({ collapsed, mobileOpen, onCloseMobile, onToggleCollapse }) {
  const { hasRole } = useAuth();
  const items = MENU.filter((m) => !m.roles || hasRole(...m.roles));

  return (
    <>
      {/* Desktop */}
      <aside className={cn("sticky top-0 hidden h-screen shrink-0 flex-col bg-gradient-to-b from-navy-800 to-navy-700 transition-[width] duration-300 md:flex", collapsed ? "w-20" : "w-64")}>
        <Brand collapsed={collapsed} />
        <NavItems items={items} collapsed={collapsed} />
        <div className="px-3 py-3">
          <button onClick={onToggleCollapse} className="flex w-full items-center justify-center gap-2 rounded-xl py-2 text-xs font-medium text-navy-100/70 transition hover:bg-white/10 hover:text-white">
            <ChevronLeft className={cn("h-4 w-4 transition-transform", collapsed && "rotate-180")} />
            {!collapsed && <span>Collapse</span>}
          </button>
          {!collapsed && <p className="mt-2 px-1 text-[10px] leading-relaxed text-navy-100/50">Advisory AI · Human-approved</p>}
        </div>
      </aside>

      {/* Mobile drawer */}
      <div className={cn("fixed inset-0 z-50 md:hidden", mobileOpen ? "pointer-events-auto" : "pointer-events-none")}>
        <div className={cn("absolute inset-0 bg-navy-900/60 backdrop-blur-sm transition-opacity duration-300", mobileOpen ? "opacity-100" : "opacity-0")} onClick={onCloseMobile} />
        <aside className={cn("absolute left-0 top-0 flex h-full w-72 flex-col bg-gradient-to-b from-navy-800 to-navy-700 shadow-2xl transition-transform duration-300", mobileOpen ? "translate-x-0" : "-translate-x-full")}>
          <div className="flex items-center justify-between pr-3">
            <Brand collapsed={false} />
            <button onClick={onCloseMobile} aria-label="Close menu" className="rounded-lg p-2 text-white/80 hover:bg-white/10 hover:text-white">
              <X className="h-5 w-5" />
            </button>
          </div>
          <NavItems items={items} collapsed={false} />
          <p className="px-4 py-3 text-[10px] text-navy-100/50">Advisory AI · Human-approved</p>
        </aside>
      </div>
    </>
  );
}
