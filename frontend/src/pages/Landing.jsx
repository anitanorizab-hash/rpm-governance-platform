// Landing page (V1.2): full corporate hero over the RPM students photo.
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { api } from "../services/api";
import { Button } from "../components/ui/button";

export default function Landing() {
  const [health, setHealth] = useState(null);
  useEffect(() => { api.health().then(setHealth).catch(() => setHealth(null)); }, []);

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: "url('/2.jpg')" }} aria-hidden="true" />
      <div className="absolute inset-0 bg-gradient-to-br from-navy-900/85 via-navy-800/75 to-navy-700/70" aria-hidden="true" />

      <div className="relative z-10 flex min-h-screen flex-col">
        <header className="flex items-center justify-between px-6 py-5 sm:px-10">
          <div className="flex items-center gap-3">
            <img src="/1.jpg" alt="Jabatan Pendidikan Negeri Perak" className="h-12 w-12 rounded-xl bg-white object-contain p-1.5 shadow-lg" />
            <div className="text-white">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-gold-400">RPM 2026–2035</p>
              <p className="text-sm font-semibold">Governance Platform</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Link to="/login"><Button variant="gold">Login</Button></Link>
            <Link to="/register"><Button variant="outline" className="border-white/40 bg-white/10 text-white hover:bg-white/20">Register</Button></Link>
          </div>
        </header>

        <main className="flex flex-1 flex-col items-center justify-center px-6 py-16 text-center">
          <div className="max-w-3xl animate-fade-up">
            <span className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-xs font-medium text-gold-300 backdrop-blur">
              <ShieldCheck className="h-4 w-4" /> Advisory AI · Human-in-the-loop approval
            </span>
            <h1 className="font-display text-4xl font-bold leading-tight text-white sm:text-5xl">Strategic Governance Support System</h1>
            <p className="mt-4 text-lg font-medium text-blue-100">Agentic AI for Intelligent Monitoring &amp; Strategic Intervention</p>
            <p className="mt-2 text-sm uppercase tracking-widest text-gold-300">Malaysia Education Plan (RPM) 2026–2035</p>
            <div className="mt-10 flex flex-wrap justify-center gap-3">
              <Link to="/login"><Button variant="gold" className="px-6 py-2.5">Get started <ArrowRight className="ml-1.5 h-4 w-4" /></Button></Link>
            </div>
          </div>
        </main>

        <footer className="px-6 py-5 text-center text-xs text-blue-100/70">
          <p>Developed for Jabatan Pendidikan Negeri Perak · Powered by Agentic AI</p>
          <p className="mt-1 text-blue-100/50">Backend: {health ? `${health.app_name} v${health.version} (${health.mode})` : "not connected"}</p>
        </footer>
      </div>
    </div>
  );
}
