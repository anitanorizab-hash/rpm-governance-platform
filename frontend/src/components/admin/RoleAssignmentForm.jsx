// RoleAssignmentForm (CP20F): assign/remove roles for a user (PATCH /users/{id}/roles).
// Role changes require Super Admin (backend-enforced). At least one role is required.
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";

export default function RoleAssignmentForm({ user, allRoles, canEdit, onSave, saving, error, success }) {
  const [selected, setSelected] = useState([]);
  useEffect(() => { setSelected(user?.roles || []); }, [user]);

  if (!user) {
    return (
      <Card><CardContent className="py-10 text-center text-sm text-slate-500">
        Select a user to view or manage roles.
      </CardContent></Card>
    );
  }

  const toggle = (r) =>
    setSelected((cur) => (cur.includes(r) ? cur.filter((x) => x !== r) : [...cur, r]));

  return (
    <Card>
      <CardHeader><CardTitle>Roles — {user.name}</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <p className="text-xs text-slate-500">{user.email}</p>
        <div className="grid grid-cols-2 gap-2">
          {allRoles.map((r) => (
            <label key={r} className={`flex items-center gap-2 rounded-md border px-2 py-1.5 text-sm ${
              selected.includes(r) ? "border-blue-300 bg-blue-50" : "border-slate-200"} ${canEdit ? "cursor-pointer" : "opacity-70"}`}>
              <input type="checkbox" checked={selected.includes(r)} disabled={!canEdit} onChange={() => toggle(r)} />
              {r}
            </label>
          ))}
        </div>
        {canEdit ? (
          <div className="flex items-center gap-3">
            <Button onClick={() => onSave(selected)} disabled={saving || selected.length === 0}>
              {saving ? "Saving…" : "Save Roles"}
            </Button>
            {selected.length === 0 && <span className="text-xs text-amber-600">At least one role is required.</span>}
          </div>
        ) : (
          <p className="text-xs text-slate-500">Role assignment requires the Super Admin role.</p>
        )}
        {error && <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}
        {success && <div className="rounded-md border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{success}</div>}
      </CardContent>
    </Card>
  );
}
