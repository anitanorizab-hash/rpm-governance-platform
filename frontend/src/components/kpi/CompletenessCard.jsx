// CompletenessCard (CP20B): completeness status from GET /kpis/{id}/completeness.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const prettify = (s) =>
  String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

export default function CompletenessCard({ completeness }) {
  if (!completeness) return null;
  const missing = completeness.missing_fields || [];

  return (
    <Card>
      <CardHeader><CardTitle>Completeness</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        {completeness.is_complete ? (
          <div className="rounded-md bg-green-50 px-3 py-2 text-sm font-medium text-green-700">
            ✓ This KPI record is complete.
          </div>
        ) : (
          <>
            <div className="rounded-md bg-amber-50 px-3 py-2 text-sm font-medium text-amber-700">
              Incomplete — {missing.length} field{missing.length === 1 ? "" : "s"} missing.
            </div>
            <ul className="flex flex-wrap gap-2">
              {missing.map((f) => (
                <li key={f} className="rounded-md border border-amber-200 bg-white px-2.5 py-1 text-xs text-amber-700">
                  {prettify(f)}
                </li>
              ))}
            </ul>
          </>
        )}
      </CardContent>
    </Card>
  );
}
