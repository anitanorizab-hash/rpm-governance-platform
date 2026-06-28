// Chatbot page (CP20E; V1.1 organisation-aware): role-scoped, grounded, cited KPI assistant (advisory).
// The organisation selector sets the conversation scope; the selection is woven into the sent message
// so the backend's organisation detection scopes the answer (no API change). Comparison questions work
// directly ("compare PPD performance", "which PPD has the highest achievement", ...).
import { useCallback, useEffect, useState } from "react";
import { chatbotService } from "../services/chatbotService";
import { useOrgScope } from "../hooks/useOrgScope";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import OrgLevelFilter from "../components/common/OrgLevelFilter";
import ChatSessionList from "../components/chatbot/ChatSessionList";
import ChatWindow from "../components/chatbot/ChatWindow";
import ChatInput from "../components/chatbot/ChatInput";
import SuggestedQuestions from "../components/chatbot/SuggestedQuestions";

function conversationToBubbles(c) {
  const bubbles = [];
  if (c.question) bubbles.push({ id: `${c.id}-q`, role: "user", text: c.question });
  if (c.answer != null) bubbles.push({
    id: `${c.id}-a`, role: "assistant", text: c.answer,
    grounded: c.grounded, fallback: c.fallback, citations: [],
  });
  return bubbles;
}

export default function Chatbot() {
  const { level, ppdId, setPpdId, onLevelChange, ppdOptions, scopeLabel } = useOrgScope();
  const [sessions, setSessions] = useState([]);
  const [active, setActive] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);
  const [sending, setSending] = useState(false);

  // Weave the selected organisation scope into the question so the backend scopes the answer.
  const orgPrefix = useCallback(() => {
    if (level === "jpn") return "For JPN, ";
    if (level === "ppd" && ppdId) {
      const name = ppdOptions.find((p) => p.id === ppdId)?.name || "the selected PPD";
      return `For ${name}, `;
    }
    if (level === "ppd" && !ppdId) return "Across all PPDs, ";
    return "";
  }, [level, ppdId, ppdOptions]);

  const loadMessages = useCallback(async (sessionId) => {
    const convs = await chatbotService.listMessages(sessionId);
    setMessages(convs.flatMap(conversationToBubbles));
  }, []);

  const init = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const list = await chatbotService.listSessions();
      setSessions(list);
      if (list.length > 0) { setActive(list[0]); await loadMessages(list[0].id); }
    } catch (err) {
      setError(err.message || "Failed to load chatbot.");
    } finally {
      setLoading(false);
    }
  }, [loadMessages]);

  useEffect(() => { init(); }, [init]);

  async function onNew() {
    setCreating(true); setError(null);
    try {
      const s = await chatbotService.createSession();
      setSessions((prev) => [s, ...prev]); setActive(s); setMessages([]);
    } catch (err) {
      setError(err.message || "Could not start a conversation.");
    } finally {
      setCreating(false);
    }
  }

  async function onSelect(s) {
    setActive(s); setMessages([]);
    try { await loadMessages(s.id); } catch (err) { setError(err.message); }
  }

  async function send(text, achievement, target) {
    let session = active;
    if (!session) {
      try { session = await chatbotService.createSession(); setSessions((p) => [session, ...p]); setActive(session); }
      catch (err) { setError(err.message); return; }
    }
    const sentText = `${orgPrefix()}${text}`;          // scoped for the backend
    setMessages((prev) => [...prev, { id: `u-${Date.now()}`, role: "user", text }]);  // show the user's words
    setSending(true); setError(null);
    try {
      const res = await chatbotService.sendMessage(session.id, sentText, achievement, target);
      setMessages((prev) => [...prev, {
        id: `a-${Date.now()}`, role: "assistant", text: res.answer,
        grounded: res.grounded, fallback: res.fallback_used,
        citations: res.citations, humanReview: res.human_review_required,
      }]);
    } catch (err) {
      setMessages((prev) => [...prev, {
        id: `e-${Date.now()}`, role: "assistant", text: `(Unable to answer: ${err.message})`,
        grounded: false, fallback: false, citations: [],
      }]);
    } finally {
      setSending(false);
    }
  }

  if (loading) return <Loading label="Loading chatbot…" />;

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">KPI Chatbot</h1>
          <p className="text-sm text-slate-500">
            Grounded, cited answers about KPI data and RPM 2026–2035 · Scope: <span className="font-medium text-slate-600">{scopeLabel}</span>.
            Responses are advisory and role-scoped.
          </p>
        </div>
        <OrgLevelFilter level={level} onLevelChange={onLevelChange} ppdId={ppdId} onPpdChange={setPpdId} ppdOptions={ppdOptions} />
      </div>

      {error && <ErrorMessage message={error} />}

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[260px_1fr]">
        <div className="h-[34rem] lg:h-[36rem]">
          <ChatSessionList sessions={sessions} activeId={active?.id} onSelect={onSelect} onNew={onNew} creating={creating} />
        </div>

        <div className="flex h-[34rem] flex-col gap-3 lg:h-[36rem]">
          <ChatWindow messages={messages} sending={sending} />
          {messages.length === 0 && <SuggestedQuestions onPick={(q) => send(q)} disabled={sending} />}
          <ChatInput onSend={send} disabled={sending} />
        </div>
      </div>
    </div>
  );
}
