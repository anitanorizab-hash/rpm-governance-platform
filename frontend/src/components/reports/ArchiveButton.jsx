// ArchiveButton (CP20D): archive an APPROVED report. Disabled until approved.
import { Button } from "../ui/button";

export default function ArchiveButton({ status, canManage, archiving, onArchive }) {
  if (!canManage) return null;
  if (status === "archived") {
    return <span className="text-xs font-medium text-blue-700">Archived.</span>;
  }
  if (status !== "approved") {
    return <span className="text-xs text-slate-500">Archive available only after approval.</span>;
  }
  return (
    <Button variant="outline" onClick={onArchive} disabled={archiving}>
      {archiving ? "Archiving…" : "Archive"}
    </Button>
  );
}
