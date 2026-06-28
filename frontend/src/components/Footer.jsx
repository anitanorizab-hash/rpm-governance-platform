// App footer (V1.2): corporate attribution beneath the content area.
export default function Footer() {
  return (
    <footer className="no-print border-t border-slate-200 bg-white/80 px-6 py-4 backdrop-blur">
      <div className="mx-auto flex max-w-[1600px] flex-col items-center justify-between gap-1 text-center text-xs text-slate-500 sm:flex-row sm:text-left">
        <p className="font-medium text-navy-700">Powered by Agentic AI</p>
        <p>Developed for Jabatan Pendidikan Negeri Perak</p>
        <p>Malaysia Education Plan (RPM) 2026–2035</p>
      </div>
    </footer>
  );
}
