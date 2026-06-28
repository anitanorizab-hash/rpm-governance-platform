// AdminSystemHealth (CP20F): API liveness/readiness + provider health. No secrets.
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { systemService } from "../services/systemService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Button } from "../components/ui/button";
import SystemHealthCard from "../components/admin/SystemHealthCard";
import ProviderHealthCard from "../components/admin/ProviderHealthCard";

export default function AdminSystemHealth() {
  const [health, setHealth] = useState(null);
  const [ready, setReady] = useState(null);
  const [providers, setProviders] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    const safe = async (fn) => { try { return await fn(); } catch { return null; } };
    const [h, r, p] = await Promise.all([
      safe(systemService.health), safe(systemService.ready), safe(systemService.providers),
    ]);
    setHealth(h); setReady(r); setProviders(p);
    if (!h && !r && !p) setError("Unable to reach system health endpoints.");
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) return <Loading label="Loading system health…" />;

  return (
    <div className="space-y-4">
      <Link to="/app/admin" className="text-sm text-blue-700 hover:underline">← Back to administration</Link>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-800">System Health</h1>
        <Button variant="outline" onClick={load}>Refresh</Button>
      </div>
      {error && <ErrorMessage message={error} />}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <SystemHealthCard health={health} ready={ready} />
        <ProviderHealthCard providers={providers} />
      </div>
    </div>
  );
}
