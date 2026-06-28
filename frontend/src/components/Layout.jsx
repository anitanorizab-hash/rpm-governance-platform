// App layout (V1.2): collapsible Sidebar + Header + content + Footer. Owns shell UI state only.
import { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import Footer from "./Footer";

const TITLES = {
  dashboard: "Dashboard", kpis: "KPI Management", "monthly-updates": "Monthly Updates",
  fds: "Financial Decision Support", reports: "Reports", notifications: "Notifications",
  chatbot: "KPI Chatbot", copilot: "Executive Copilot", admin: "Administration",
};

export default function Layout() {
  const { pathname } = useLocation();
  const [collapsed, setCollapsed] = useState(() => localStorage.getItem("rpm_sidebar_collapsed") === "1");
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const seg = pathname.split("/")[2] || "dashboard";
    document.title = `${TITLES[seg] || "Governance Platform"} · RPM 2026–2035`;
  }, [pathname]);
  useEffect(() => { setMobileOpen(false); }, [pathname]);

  function toggleCollapse() {
    setCollapsed((c) => { const n = !c; localStorage.setItem("rpm_sidebar_collapsed", n ? "1" : "0"); return n; });
  }

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar collapsed={collapsed} mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} onToggleCollapse={toggleCollapse} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header onMenuClick={() => setMobileOpen(true)} />
        <main className="flex-1 overflow-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-[1600px] animate-fade-up">
            <Outlet />
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
