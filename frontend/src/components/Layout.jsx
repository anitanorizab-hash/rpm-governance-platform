// App layout (CP19): Sidebar + Header + content outlet.
// CP22: sets a per-page document title for presentation polish.
import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";

const TITLES = {
  dashboard: "Dashboard", kpis: "KPI Management", "monthly-updates": "Monthly Updates",
  fds: "Financial Decision Support", reports: "Reports", notifications: "Notifications",
  chatbot: "KPI Chatbot", copilot: "Executive Copilot", admin: "Administration",
};

export default function Layout() {
  const { pathname } = useLocation();
  useEffect(() => {
    const seg = pathname.split("/")[2] || "dashboard";
    const name = TITLES[seg] || "Governance Platform";
    document.title = `${name} · RPM 2026–2035`;
  }, [pathname]);

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header />
        <main className="flex-1 overflow-auto px-6 py-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
