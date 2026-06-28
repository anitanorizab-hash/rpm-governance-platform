// LiveLinkManager (CP20F): register + validate admin-approved live links (BR-024).
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function LiveLinkManager({ onRegister, onValidate, registering, validating, lastLink, error, success }) {
  const [form, setForm] = useState({ title: "", url: "", category: "policy" });
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  function submit(e) {
    e.preventDefault();
    if (!form.title.trim() || !form.url.trim()) return;
    onRegister(form);
  }

  return (
    <Card>
      <CardHeader><CardTitle>Live Links (admin-validated)</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <form onSubmit={submit} className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div>
            <Label>Title</Label>
            <Input value={form.title} onChange={(e) => set("title", e.target.value)} required />
          </div>
          <div>
            <Label>Category</Label>
            <select className={selectCls} value={form.category} onChange={(e) => set("category", e.target.value)}>
              {["policy", "guideline", "circular", "rpm", "note"].map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="sm:col-span-2">
            <Label>URL</Label>
            <Input value={form.url} onChange={(e) => set("url", e.target.value)} placeholder="https://…" required />
          </div>
          <div className="sm:col-span-2 flex items-center gap-3">
            <Button type="submit" disabled={registering}>{registering ? "Registering…" : "Register Live Link"}</Button>
            {lastLink?.link_id && (
              <Button type="button" variant="outline" onClick={() => onValidate(lastLink.link_id)} disabled={validating}>
                {validating ? "Validating…" : "Validate Last Link"}
              </Button>
            )}
          </div>
        </form>
        {lastLink && (
          <p className="text-xs text-slate-500">
            Last link: <span className="font-medium">{lastLink.link_id}</span> — status {lastLink.status}
          </p>
        )}
        {error && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}
        {success && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{success}</div>}
      </CardContent>
    </Card>
  );
}
