// SubmissionSummary (CP20A): monthly submission status from GET /dashboard/submission-summary.
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function SubmissionSummary({ submissionSummary }) {
  const overall = submissionSummary?.overall || {};
  const submitted = overall.submitted || 0;
  const notSubmitted = overall.not_submitted || 0;
  const total = submitted + notSubmitted;
  const pct = total > 0 ? Math.round((submitted / total) * 100) : 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          Monthly Submissions
          {submissionSummary?.period && (
            <span className="ml-2 text-xs font-normal text-slate-400">{submissionSummary.period}</span>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-lg bg-green-50 px-4 py-3">
            <p className="text-xs font-medium uppercase tracking-wide text-green-700">Submitted</p>
            <p className="mt-1 text-2xl font-semibold text-green-700">{submitted}</p>
          </div>
          <div className="rounded-lg bg-amber-50 px-4 py-3">
            <p className="text-xs font-medium uppercase tracking-wide text-amber-700">Not Submitted</p>
            <p className="mt-1 text-2xl font-semibold text-amber-700">{notSubmitted}</p>
          </div>
        </div>
        <div>
          <div className="mb-1 flex justify-between text-xs text-slate-500">
            <span>Submission rate</span><span>{pct}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
            <div className="h-full rounded-full bg-blue-600" style={{ width: `${pct}%` }} />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
