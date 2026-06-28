// AdminUsers (CP20F): view users + assign/remove roles (Super Admin can edit).
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { adminService, ALL_ROLES } from "../services/adminService";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import UserRoleTable from "../components/admin/UserRoleTable";
import RoleAssignmentForm from "../components/admin/RoleAssignmentForm";

export default function AdminUsers() {
  const { hasRole } = useAuth();
  const canEdit = hasRole("super_admin");

  const [users, setUsers] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try { setUsers(await adminService.listUsers()); }
    catch (err) { setError(err.message || "Failed to load users."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function onSave(roles) {
    if (!selected) return;
    setSaving(true); setSaveError(null); setSaveSuccess(null);
    try {
      const updated = await adminService.setRoles(selected.id, roles);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      setSelected(updated);
      setSaveSuccess("Roles updated.");
    } catch (err) {
      setSaveError(err.message || "Failed to update roles.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <Loading label="Loading users…" />;

  return (
    <div className="space-y-4">
      <Link to="/app/admin" className="text-sm text-blue-700 hover:underline">← Back to administration</Link>
      <h1 className="text-xl font-semibold text-slate-800">User & Role Management</h1>
      {error && <ErrorMessage message={error} />}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_22rem]">
        <UserRoleTable users={users} selectedId={selected?.id} onSelect={(u) => { setSelected(u); setSaveSuccess(null); setSaveError(null); }} />
        <RoleAssignmentForm
          user={selected} allRoles={ALL_ROLES} canEdit={canEdit}
          onSave={onSave} saving={saving} error={saveError} success={saveSuccess}
        />
      </div>
    </div>
  );
}
