// UserRoleTable (CP20F): users with MOE email + roles. No passwords/secrets are shown.
export default function UserRoleTable({ users, selectedId, onSelect }) {
  const rows = users || [];
  if (rows.length === 0) {
    return <div className="rounded-xl border border-slate-200 bg-white py-10 text-center text-sm text-slate-500">No users.</div>;
  }
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="max-h-[30rem] overflow-auto">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Name</th>
              <th className="px-4 py-2 font-medium">Email (MOE domain)</th>
              <th className="px-4 py-2 font-medium">Roles</th>
              <th className="px-4 py-2 font-medium">Active</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((u) => (
              <tr key={u.id} onClick={() => onSelect?.(u)}
                  className={`cursor-pointer hover:bg-slate-50 ${selectedId === u.id ? "bg-blue-50/50" : ""}`}>
                <td className="px-4 py-2 font-medium text-slate-700">{u.name}</td>
                <td className="px-4 py-2 text-slate-600">{u.email}</td>
                <td className="px-4 py-2">
                  <div className="flex flex-wrap gap-1">
                    {(u.roles || []).map((r) => (
                      <span key={r} className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">{r}</span>
                    ))}
                    {(u.roles || []).length === 0 && <span className="text-xs text-slate-400">—</span>}
                  </div>
                </td>
                <td className="px-4 py-2 text-slate-600">{u.active ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
