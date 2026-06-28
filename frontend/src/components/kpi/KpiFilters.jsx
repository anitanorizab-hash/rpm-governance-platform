// KpiFilters (CP20B): search + Teras/Department/PIC/Status/Completeness filters.
// Server-side filters (teras/sector/pic/status/completeness) are passed to GET /kpis;
// the free-text `search` box filters the loaded rows client-side.
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function KpiFilters({ filters, onChange, onApply, onReset, departments = [], pics = [] }) {
  const set = (k, v) => onChange({ ...filters, [k]: v });

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div className="lg:col-span-3">
          <Label>Search (statement / code)</Label>
          <Input
            value={filters.search || ""}
            onChange={(e) => set("search", e.target.value)}
            placeholder="Type to filter loaded KPIs…"
          />
        </div>

        <div>
          <Label>Teras</Label>
          <select className={selectCls} value={filters.teras || ""} onChange={(e) => set("teras", e.target.value)}>
            <option value="">All Teras</option>
            {[1, 2, 3, 4, 5, 6, 7].map((n) => (
              <option key={n} value={n}>Teras {n}</option>
            ))}
          </select>
        </div>

        <div>
          <Label>Department / Sector</Label>
          <select className={selectCls} value={filters.sector || ""} onChange={(e) => set("sector", e.target.value)}>
            <option value="">All Departments</option>
            {departments.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div>
          <Label>PIC (email)</Label>
          <select className={selectCls} value={filters.pic || ""} onChange={(e) => set("pic", e.target.value)}>
            <option value="">All PICs</option>
            {pics.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>

        <div>
          <Label>Achievement Status</Label>
          <Input
            value={filters.status || ""}
            onChange={(e) => set("status", e.target.value)}
            placeholder="e.g. on_track, not_updated"
          />
        </div>

        <div>
          <Label>Completeness</Label>
          <select className={selectCls} value={filters.completeness || ""} onChange={(e) => set("completeness", e.target.value)}>
            <option value="">All</option>
            <option value="complete">Complete</option>
            <option value="incomplete">Incomplete</option>
          </select>
        </div>

        <div className="flex items-end gap-2">
          <Button onClick={onApply}>Apply</Button>
          <Button variant="outline" onClick={onReset}>Reset</Button>
        </div>
      </div>
    </div>
  );
}
