// App header (V1.2): executive top bar with mobile menu toggle, user chip, logout.
import { useNavigate } from "react-router-dom";
import { Menu, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Button } from "./ui/button";

function initials(name) {
  if (!name) return "U";
  return name.split(" ").filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join("");
}

export default function Header({ onMenuClick }) {
  const { user, roles, logout } = useAuth();
  const navigate = useNavigate();
  function onLogout() { logout(); navigate("/login"); }

  return (
    <header className="no-print sticky top-0 z-30 flex items-center justify-between border-b border-slate-200 bg-white/90 px-4 py-3 backdrop-blur sm:px-6">
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} aria-label="Open menu" className="rounded-lg p-2 text-navy-700 hover:bg-slate-100 md:hidden">
          <Menu className="h-5 w-5" />
        </button>
        <div>
          <h1 className="font-display text-sm font-semibold text-navy-700 sm:text-base">Strategic Governance Support System</h1>
          <p className="hidden text-xs text-slate-500 sm:block">Agentic AI · Monitoring &amp; Strategic Intervention</p>
        </div>
      </div>
      {user && (
        <div className="flex items-center gap-3">
          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium text-navy-700">{user.name}</p>
            <p className="text-xs text-slate-500">{(roles || []).join(", ") || "—"}</p>
          </div>
          <div aria-hidden="true" className="flex h-9 w-9 items-center justify-center rounded-full bg-navy-700 text-xs font-semibold text-white">{initials(user.name)}</div>
          <Button variant="outline" onClick={onLogout} className="gap-1.5">
            <LogOut className="h-4 w-4" /> <span className="hidden sm:inline">Logout</span>
          </Button>
        </div>
      )}
    </header>
  );
}
