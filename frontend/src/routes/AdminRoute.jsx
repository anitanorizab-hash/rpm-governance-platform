// AdminRoute (CP20F): gates the Admin module to Super Admin / JPN Administrator.
// Renders an access-denied notice (not a redirect) when accessed without the role.
import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

const ADMIN_ROLES = ["super_admin", "jpn_admin"];

export default function AdminRoute() {
  const { hasRole } = useAuth();
  if (!hasRole(...ADMIN_ROLES)) {
    return (
      <Card>
        <CardHeader><CardTitle>Access denied</CardTitle></CardHeader>
        <CardContent className="text-sm text-slate-600">
          The Administration module is restricted to Super Admin and JPN Administrator roles.
        </CardContent>
      </Card>
    );
  }
  return <Outlet />;
}
