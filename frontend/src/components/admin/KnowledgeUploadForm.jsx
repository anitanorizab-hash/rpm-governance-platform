// KnowledgeUploadForm (CP20F): register a static knowledge source (POST /knowledge/sources).
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input, Label } from "../ui/input";
import { Button } from "../ui/button";
import { SOURCE_CATEGORIES, SOURCE_FORMATS } from "../../services/knowledgeService";

const selectCls =
  "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500";

export default function KnowledgeUploadForm({ onCreate, creating, error, success }) {
  const [form, setForm] = useState({
    title: "", category: "rpm", format: "txt", reliability: "trusted", description: "", content: "",
  });
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  function submit(e) {
    e.preventDefault();
    if (!form.title.trim()) return;
    onCreate({ type: "static", ...form });
  }

  return (
    <Card>
      <CardHeader><CardTitle>Register Knowledge Source</CardTitle></CardHeader>
      <CardContent>
        <form onSubmit={submit} className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <Label>Title</Label>
            <Input value={form.title} onChange={(e) => set("title", e.target.value)} required />
          </div>
          <div>
            <Label>Category</Label>
            <select className={selectCls} value={form.category} onChange={(e) => set("category", e.target.value)}>
              {SOURCE_CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <Label>Format</Label>
            <select className={selectCls} value={form.format} onChange={(e) => set("format", e.target.value)}>
              {SOURCE_FORMATS.map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <div className="sm:col-span-2">
            <Label>Description (optional)</Label>
            <Input value={form.description} onChange={(e) => set("description", e.target.value)} />
          </div>
          <div className="sm:col-span-2">
            <Label>Content (txt/md raw text; base64 for pdf/docx)</Label>
            <textarea className={selectCls} rows={3} value={form.content} onChange={(e) => set("content", e.target.value)} />
          </div>
          <div className="sm:col-span-2">
            <Button type="submit" disabled={creating}>{creating ? "Registering…" : "Register Source"}</Button>
          </div>
        </form>
        {error && <div className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}
        {success && <div className="mt-3 rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{success}</div>}
      </CardContent>
    </Card>
  );
}
