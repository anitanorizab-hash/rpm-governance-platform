// ProtectedRoute (CP19): redirects unauthenticated users to /login.
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";

export default function ProtectedRoute() {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <Loading label="Checking session…" />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}
