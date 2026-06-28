// AppShell (CP22): clean fallback for unknown /app/* routes (all modules have real pages).
import { Link, useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

export default function AppShell() {
  const { module } = useParams();
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader><CardTitle>Page not found</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm text-slate-600">
            The section <span className="font-medium">“{module}”</span> doesn’t exist.
          </p>
          <Link to="/app/dashboard" className="text-sm font-medium text-blue-700 hover:underline">
            ← Return to the dashboard
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
