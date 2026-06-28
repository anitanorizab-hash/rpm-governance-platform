// Admin landing (CP20F): overview cards linking to the admin sub-sections.
import { useCallback, useEffect, useState } from "react";
import { adminService } from "../services/adminService";
import { knowledgeService } from "../services/knowledgeService";
import { auditService } from "../services/auditService";
import { importService } from "../services/importService";
import { systemService } from "../services/systemService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import AdminSectionCard from "../components/admin/AdminSectionCard";
import AutomationPanel from "../components/admin/AutomationPanel";

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    // Each call is independent — tolerate partial failures so the landing still renders.
    const safe = async (fn) => { try { return await fn(); } catch { return null; } };
    const [users, sources, logs, imports, providers] = await Promise.all([
      safe(adminService.listUsers), safe(knowledgeService.listSources),
      safe(() => auditService.listLogs({ limit: 500 })), safe(importService.history),
      safe(systemService.providers),
    ]);
    const llmOk = providers?.llm?.configured;
    setStats({
      users: users?.length ?? "—",
      sources: sources?.length ?? "—",
      liveLinks: (sources || []).filter((s) => s.type === "live").length,
      logs: logs?.length ?? "—",
      imports: imports?.length ?? "—",
      providerStatus: providers ? (llmOk ? "Configured" : "Not configured") : "—",
    });
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) return <Loading label="Loading administration…" />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Administration</h1>
        <p className="text-sm text-slate-500">Users, knowledge, audit, imports and system health.</p>
      </div>
      {error && <ErrorMessage message={error} />}

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <AdminSectionCard title="Users" count={stats.users} hint="Manage roles" to="/app/admin/users" tone="blue" />
        <AdminSectionCard title="PIC Directory" count="Manage" hint="PICs, emails, KPI assignment" to="/app/admin/pics" tone="green" />
        <AdminSectionCard title="Knowledge Sources" count={stats.sources} hint="RAG sources + live links" to="/app/admin/knowledge" tone="green" />
        <AdminSectionCard title="Live Links" count={stats.liveLinks} hint="Admin-validated" to="/app/admin/knowledge" />
        <AdminSectionCard title="Audit Logs" count={stats.logs} hint="Append-only" to="/app/admin/audit" />
        <AdminSectionCard title="Import History" count={stats.imports} hint="Excel import-once" to="/app/admin/audit" />
        <AdminSectionCard title="Provider Health" count={stats.providerStatus} hint="LLM / embedding" to="/app/admin/system" tone="amber" />
        <AdminSectionCard title="System Health" count="View" hint="API + readiness" to="/app/admin/system" />
      </div>

      <AutomationPanel />
    </div>
  );
}
