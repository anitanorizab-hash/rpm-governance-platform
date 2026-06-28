// AdminKnowledge (CP20F): knowledge sources + register/process + live links.
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { knowledgeService } from "../services/knowledgeService";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import KnowledgeSourceTable from "../components/admin/KnowledgeSourceTable";
import KnowledgeUploadForm from "../components/admin/KnowledgeUploadForm";
import LiveLinkManager from "../components/admin/LiveLinkManager";

export default function AdminKnowledge() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [processingId, setProcessingId] = useState(null);
  const [creating, setCreating] = useState(false);
  const [createMsg, setCreateMsg] = useState(null);
  const [createErr, setCreateErr] = useState(null);

  const [lastLink, setLastLink] = useState(null);
  const [registering, setRegistering] = useState(false);
  const [validating, setValidating] = useState(false);
  const [linkMsg, setLinkMsg] = useState(null);
  const [linkErr, setLinkErr] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try { setSources(await knowledgeService.listSources()); }
    catch (err) { setError(err.message || "Failed to load knowledge sources."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function onCreate(data) {
    setCreating(true); setCreateErr(null); setCreateMsg(null);
    try { const s = await knowledgeService.createSource(data); setCreateMsg(`Registered "${s.title}".`); await load(); }
    catch (err) { setCreateErr(err.message || "Registration failed."); }
    finally { setCreating(false); }
  }

  async function onProcess(id) {
    setProcessingId(id); setError(null);
    try { const r = await knowledgeService.processSource(id); await load();
      setCreateMsg(`Processed: ${r.chunks} chunk(s), mode ${r.mode}.`); }
    catch (err) { setError(err.message || "Processing failed."); }
    finally { setProcessingId(null); }
  }

  async function onRegisterLink(data) {
    setRegistering(true); setLinkErr(null); setLinkMsg(null);
    try { const r = await knowledgeService.createLiveLink(data); setLastLink(r); setLinkMsg(`Live link registered (status: ${r.status}).`); await load(); }
    catch (err) { setLinkErr(err.message || "Live link registration failed."); }
    finally { setRegistering(false); }
  }

  async function onValidateLink(linkId) {
    setValidating(true); setLinkErr(null); setLinkMsg(null);
    try { const r = await knowledgeService.validateLiveLink(linkId); setLastLink((l) => ({ ...l, status: r.status })); setLinkMsg(`Live link validated (status: ${r.status}).`); await load(); }
    catch (err) { setLinkErr(err.message || "Validation failed."); }
    finally { setValidating(false); }
  }

  if (loading) return <Loading label="Loading knowledge sources…" />;

  return (
    <div className="space-y-4">
      <Link to="/app/admin" className="text-sm text-blue-700 hover:underline">← Back to administration</Link>
      <h1 className="text-xl font-semibold text-slate-800">Knowledge Management</h1>

      <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
        Pelan Taktikal JPN/PPD are <span className="font-medium">operational import files, not RAG knowledge sources</span> (BR-012).
        Register only policy, RPM and guideline material here.
      </div>

      {error && <ErrorMessage message={error} />}

      <KnowledgeSourceTable sources={sources} onProcess={onProcess} processingId={processingId} />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <KnowledgeUploadForm onCreate={onCreate} creating={creating} error={createErr} success={createMsg} />
        <LiveLinkManager
          onRegister={onRegisterLink} onValidate={onValidateLink}
          registering={registering} validating={validating}
          lastLink={lastLink} error={linkErr} success={linkMsg}
        />
      </div>
    </div>
  );
}
