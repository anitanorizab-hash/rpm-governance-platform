// Landing page (CP19): corporate intro + entry points; shows backend health.
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import { Button } from "../components/ui/button";

export default function Landing() {
  const [health, setHealth] = useState(null);
  useEffect(() => { api.health().then(setHealth).catch(() => setHealth(null)); }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <span className="font-semibold text-slate-800">RPM 2026–2035 Governance Platform</span>
          <div className="flex gap-2">
            <Link to="/login"><Button variant="secondary">Login</Button></Link>
            <Link to="/register"><Button>Register</Button></Link>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-6 py-20 text-center">
        <h1 className="text-3xl font-bold text-slate-900">
          Agentic AI Strategic Governance Platform
        </h1>
        <p className="mt-4 text-slate-600">
          KPI monitoring, monthly updates, budget intelligence, intervention, notification, reporting
          and executive decision support for RPM 2026–2035 across JPN, PPD and schools.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link to="/login"><Button>Get started</Button></Link>
        </div>
        <p className="mt-10 text-xs text-slate-400">
          Backend: {health ? `${health.app_name} v${health.version} (${health.mode})` : "not connected"}
        </p>
      </main>
    </div>
  );
}
