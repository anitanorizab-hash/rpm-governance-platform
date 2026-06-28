// useOrgScope (V1.1): shared organisation-scope state for org-aware pages.
// Loads the hierarchy once and derives the effective organisation_id + comparison flag,
// so every page reuses the same logic + the single OrgLevelFilter component (no duplication).
import { useEffect, useMemo, useState } from "react";
import { organisationService } from "../services/organisationService";

export function useOrgScope() {
  const [orgs, setOrgs] = useState([]);
  const [level, setLevel] = useState("all"); // all | jpn | ppd
  const [ppdId, setPpdId] = useState("");

  useEffect(() => {
    organisationService.list().then(setOrgs).catch(() => setOrgs([]));
  }, []);

  const jpnOrg = useMemo(() => orgs.find((o) => o.type === "JPN") || null, [orgs]);
  const ppdOptions = useMemo(
    () => orgs.filter((o) => o.type === "PPD").map((o) => ({ id: o.id, name: o.name })),
    [orgs]
  );
  const showComparison = level === "ppd" && !ppdId;
  const organisationId = useMemo(() => {
    if (level === "jpn") return jpnOrg?.id || null;
    if (level === "ppd") return ppdId || null;
    return null;
  }, [level, ppdId, jpnOrg]);
  const scopeLabel =
    level === "all" ? "All organisations"
      : level === "jpn" ? (jpnOrg?.name || "JPN")
        : (ppdId ? (ppdOptions.find((p) => p.id === ppdId)?.name || "PPD") : "All PPD (comparison)");

  const onLevelChange = (lvl) => { setLevel(lvl); setPpdId(""); };

  return {
    orgs, level, ppdId, setPpdId, onLevelChange,
    jpnOrg, ppdOptions, showComparison, organisationId, scopeLabel,
  };
}
