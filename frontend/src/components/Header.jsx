// App header (CP19): shows user name + role and logout when authenticated.
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Button } from "./ui/button";

export default function Header() {
  const { user, roles, logout } = useAuth();
  const navigate = useNavigate();

  function onLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <h1 className="text-sm font-semibold text-slate-800">
        Agentic AI Strategic Governance Platform
      </h1>
      {user && (
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-sm font-medium text-slate-800">{user.name}</p>
            <p className="text-xs text-slate-500">{(roles || []).join(", ") || "—"}</p>
          </div>
          <Button variant="secondary" onClick={onLogout}>Logout</Button>
        </div>
      )}
    </header>
  );
}
