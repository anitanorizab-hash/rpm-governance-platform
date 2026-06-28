// DashboardFilterBar (V1.2): premium executive filter bar — Level / Organisation (reuses
// OrgLevelFilter) / Reporting Year / Refresh / Export. Export uses window.print() (no new API);
// the Year list covers the RPM 2026–2035 cycle and is forwarded to the submission-summary call.
import { Download, RefreshCw } from "lucide-react";
import { Button } from "../ui/button";
import OrgLevelFilter from "../common/OrgLevelFilter";

const YEARS = [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035];
const selectCls =
  "rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-royal focus:outline-none focus:ring-2 focus:ring-royal/30";

export default function DashboardFilterBar({
  level, onLevelChange, ppdId, onPpdChange, ppdOptions,
  year, onYearChange, onRefresh, onExport,
}) {
  return (
    <div className="no-print flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white/80 p-3 shadow-card backdrop-blur lg:flex-row lg:items-end lg:justify-between">
      <div className="flex flex-wrap items-end gap-3">
        <OrgLevelFilter
          level={level} onLevelChange={onLevelChange}
          ppdId={ppdId} onPpdChange={onPpdChange} ppdOptions={ppdOptions}
        />
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Reporting Year</label>
          <select className={selectCls} value={year} onChange={(e) => onYearChange(Number(e.target.value))}>
            {YEARS.map((y) => <option key={y} value={y}>{y}</option>)}
          </select>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="outline" onClick={onRefresh} className="gap-1.5">
          <RefreshCw className="h-4 w-4" /> Refresh
        </Button>
        <Button variant="gold" onClick={onExport} className="gap-1.5">
          <Download className="h-4 w-4" /> Export
        </Button>
      </div>
    </div>
  );
}
