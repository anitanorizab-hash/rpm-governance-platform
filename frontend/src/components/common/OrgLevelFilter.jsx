// OrgLevelFilter (V1.1): reusable organisation-level selector (All / JPN / PPD) with a
// conditional PPD picker. Presentational only — the page maps the selection to an organisation_id.
import { Label } from "../ui/input";

const selectCls =
  "rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function OrgLevelFilter({ level, onLevelChange, ppdId, onPpdChange, ppdOptions = [] }) {
  return (
    <div className="flex items-end gap-3">
      <div>
        <Label>Organisation Level</Label>
        <select className={selectCls} value={level} onChange={(e) => onLevelChange(e.target.value)}>
          <option value="all">All</option>
          <option value="jpn">JPN</option>
          <option value="ppd">PPD</option>
        </select>
      </div>
      {level === "ppd" && (
        <div>
          <Label>PPD</Label>
          <select className={selectCls} value={ppdId} onChange={(e) => onPpdChange(e.target.value)}>
            <option value="">All PPD (comparison)</option>
            {ppdOptions.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}
