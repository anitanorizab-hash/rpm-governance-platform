// AdminAudit (CP20F): read-only audit trail + import history (both oversight views).
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { auditService } from "../services/auditService";
import { importService } from "../services/importService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import AuditLogTable from "../components/admin/AuditLogTable";
import ImportHistoryTable from "../components/admin/ImportHistoryTable";

const EMPTY = { entity_type: "", action: "" };

export default function AdminAudit() {
  const [filters, setFilters] = useState(EMPTY);
  const [applied, setApplied] = useState(EMPTY);
  const [logs, setLogs] = useState([]);
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async (f) => {
    setLoading(true); setError(null);
    try {
      const [l, b] = await Promise.all([
        auditService.listLogs({ ...f, limit: 200 }),
        importService.history().catch(() => []),
      ]);
      setLogs(l); setBatches(b);
    } catch (err) {
      setError(err.message || "Failed to load audit data.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(applied); }, [load, applied]);

  return (
    <div className="space-y-4">
      <Link to="/app/admin" className="text-sm text-blue-700 hover:underline">← Back to administration</Link>
      <h1 className="text-xl font-semibold text-slate-800">Audit & Import History</h1>
      {error && <ErrorMessage message={error} />}
      {loading ? <Loading label="Loading audit logs…" /> : (
        <>
          <AuditLogTable
            logs={logs} filters={filters} onChange={setFilters}
            onApply={() => setApplied(filters)} onReset={() => { setFilters(EMPTY); setApplied(EMPTY); }}
          />
          <ImportHistoryTable batches={batches} />
        </>
      )}
    </div>
  );
}
