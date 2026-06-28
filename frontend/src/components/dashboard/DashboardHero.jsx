// DashboardHero (V1.2): full-width executive banner over the RPM photo (/2.jpg).
// KPM crest (/1.jpg) on the left; an optional MADANI logo (/madani.png) appears on the
// right ONLY if the asset is present — it is never fabricated. Year is a display badge.
import { CalendarDays, Building2 } from "lucide-react";

export default function DashboardHero({ year, scopeLabel }) {
  return (
    <section className="relative overflow-hidden rounded-3xl shadow-card">
      <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: "url('/2.jpg')" }} aria-hidden="true" />
      <div className="absolute inset-0 bg-gradient-to-r from-navy-900/85 via-navy-800/70 to-navy-700/55" aria-hidden="true" />

      <div className="relative z-10 flex flex-col gap-5 px-6 py-7 sm:px-10 sm:py-9">
        <div className="flex items-start justify-between gap-4">
          <img src="/1.jpg" alt="Kementerian Pendidikan Malaysia" className="h-14 w-14 rounded-xl bg-white object-contain p-1.5 shadow-lg sm:h-16 sm:w-16" />
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/25 bg-white/10 px-3 py-1.5 text-xs font-semibold text-gold-300 backdrop-blur">
              <CalendarDays className="h-4 w-4" /> {year}
            </span>
            <img
              src="/madani.png"
              alt="Malaysia MADANI"
              onError={(e) => { e.currentTarget.style.display = "none"; }}
              className="h-14 w-auto rounded-xl bg-white object-contain p-1.5 shadow-lg sm:h-16"
            />
          </div>
        </div>

        <div className="max-w-3xl">
          <h1 className="font-display text-2xl font-bold leading-tight text-white sm:text-4xl">
            Strategic Governance Support System
          </h1>
          <p className="mt-2 text-sm font-medium text-blue-100 sm:text-base">
            Agentic AI for Intelligent Monitoring &amp; Strategic Intervention
          </p>
          <p className="mt-1 text-xs uppercase tracking-widest text-gold-300 sm:text-sm">
            Malaysia Education Plan (RPM) 2026–2035
          </p>
          <p className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-white/10 px-3 py-1.5 text-xs font-medium text-white/90 backdrop-blur">
            <Building2 className="h-3.5 w-3.5" /> Scope: {scopeLabel}
          </p>
        </div>
      </div>
    </section>
  );
}
