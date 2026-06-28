"""Dashboard service (CP10): deterministic Teras 1–7 aggregation. NO AI provider is called here."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.organisation_repository import OrganisationRepository
from app.services import completeness_service

SEE_ALL_ROLES = {"super_admin", "jpn_admin", "executive", "read_only", "ppd_admin"}


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DashboardRepository(db)

    # ---------- scoping ----------
    def _scoped_kpis(self, current_user, organisation_id=None):
        kpis = self.repo.active_kpis()
        if organisation_id:
            kpis = [k for k in kpis if k.organisation_id == organisation_id]
        roles = set(current_user.role_names)
        if roles & SEE_ALL_ROLES:
            return kpis
        if "sector_admin" in roles:
            return [k for k in kpis if k.sector and k.sector == current_user.scope]
        if "kpi_pic" in roles:
            return [k for k in kpis if k.pic and k.pic.email == current_user.email]
        return kpis  # default: read (authenticated)

    # ---------- derivations (deterministic) ----------
    @staticmethod
    def _teras_no(k):
        return k.teras.number if k.teras else 0

    def _build(self, current_user, organisation_id=None):
        kpis = self._scoped_kpis(current_user, organisation_id=organisation_id)
        ids = [k.id for k in kpis]
        latest = self.repo.latest_updates_by_kpi(ids)
        any_update = self.repo.has_any_update(ids)
        rows = []
        for k in kpis:
            upd = latest.get(k.id)
            status = (upd.achievement_status if upd and upd.achievement_status else "not_updated")
            risk = k.risk_level or "unknown"
            finance = (upd.finance_status if upd and upd.finance_status else "not_reported")
            missing = completeness_service.kpi_missing_fields(k)
            if k.id not in any_update:
                completion = "not_updated"
            else:
                completion = "complete" if not missing else "incomplete"
            rows.append({
                "kpi": k, "teras": self._teras_no(k), "status": status, "risk": risk,
                "finance": finance, "missing": missing, "completion": completion,
                "organisation_id": k.organisation_id,
            })
        return rows

    # ---------- public aggregations ----------
    @staticmethod
    def _overview_from_rows(rows) -> dict:
        """Deterministic overview aggregation from a prebuilt rows list (reused for org grouping)."""
        by_teras = Counter(r["teras"] for r in rows)
        return {
            "total_kpis": len(rows),
            "by_teras": {n: by_teras.get(n, 0) for n in range(1, 8)},
            "achievement": dict(Counter(r["status"] for r in rows)),
            "risk": dict(Counter(r["risk"] for r in rows)),
            "completion": dict(Counter(r["completion"] for r in rows)),
            "missing_information": sum(1 for r in rows if r["missing"]),
            "finance": dict(Counter(r["finance"] for r in rows)),
        }

    def overview(self, current_user, organisation_id=None):
        return self._overview_from_rows(self._build(current_user, organisation_id=organisation_id))

    def teras_summary(self, current_user, organisation_id=None):
        rows = self._build(current_user, organisation_id=organisation_id)
        by_teras = defaultdict(list)
        for r in rows:
            by_teras[r["teras"]].append(r)
        out = []
        for n in range(1, 8):           # always Teras 1–7
            group = by_teras.get(n, [])
            out.append({
                "teras_number": n,
                "kpi_count": len(group),
                "achievement": dict(Counter(g["status"] for g in group)),
                "risk": dict(Counter(g["risk"] for g in group)),
                "completion": dict(Counter(g["completion"] for g in group)),
                "missing_information": sum(1 for g in group if g["missing"]),
                "finance": dict(Counter(g["finance"] for g in group)),
            })
        return out

    def risk_summary(self, current_user, organisation_id=None):
        rows = self._build(current_user, organisation_id=organisation_id)
        overall = dict(Counter(r["risk"] for r in rows))
        by_teras = {n: dict(Counter(r["risk"] for r in rows if r["teras"] == n)) for n in range(1, 8)}
        return {"overall": overall, "by_teras": by_teras}

    def budget_summary(self, current_user, organisation_id=None):
        rows = self._build(current_user, organisation_id=organisation_id)
        overall = dict(Counter(r["finance"] for r in rows))
        by_teras = {n: dict(Counter(r["finance"] for r in rows if r["teras"] == n)) for n in range(1, 8)}
        return {"overall": overall, "by_teras": by_teras}

    def submission_summary(self, current_user, year: int | None = None, month: int | None = None,
                           organisation_id=None):
        now = datetime.now(timezone.utc)
        year = year or now.year
        month = month or now.month
        kpis = self._scoped_kpis(current_user, organisation_id=organisation_id)
        ids = [k.id for k in kpis]
        submitted_ids = self.repo.updates_for_period(ids, year, month)
        by_teras = {n: Counter() for n in range(1, 8)}
        overall = Counter()
        for k in kpis:
            n = self._teras_no(k)
            state = "submitted" if k.id in submitted_ids else "not_submitted"
            overall[state] += 1
            if n in by_teras:
                by_teras[n][state] += 1
        return {
            "period": f"{year}-{month:02d}",
            "overall": dict(overall),
            "by_teras": {n: dict(c) for n, c in by_teras.items()},
        }

    def high_risk_kpis(self, current_user, levels=("high",), organisation_id=None):
        rows = self._build(current_user, organisation_id=organisation_id)
        return [
            {"kpi_id": r["kpi"].id, "code": r["kpi"].code, "statement": r["kpi"].statement,
             "teras_number": r["teras"] or None,
             "pic_email": (r["kpi"].pic.email if r["kpi"].pic else None), "risk_level": r["risk"]}
            for r in rows if r["risk"] in levels
        ]

    def kpi_mapping(self, current_user, organisation_id=None):
        rows = self._build(current_user, organisation_id=organisation_id)
        return [
            {"kpi_id": r["kpi"].id, "code": r["kpi"].code, "teras_number": r["teras"] or None,
             "pic": (r["kpi"].pic.name if r["kpi"].pic else None),
             "sector": r["kpi"].sector,
             "organisation_type": (r["kpi"].organisation.type if r["kpi"].organisation else None),
             "organisation_name": (r["kpi"].organisation.name if r["kpi"].organisation else None),
             "status": r["status"], "risk": r["risk"], "finance_status": r["finance"]}
            for r in rows
        ]

    def executive_summary(self, current_user, organisation_id=None):
        """Deterministic text only (AI summary connected in a later prompt)."""
        ov = self.overview(current_user, organisation_id=organisation_id)
        ts = self.teras_summary(current_user, organisation_id=organisation_id)
        top = max(ts, key=lambda t: t["kpi_count"]) if ts else None
        high_risk = ov["risk"].get("high", 0)
        incomplete = ov["completion"].get("incomplete", 0) + ov["completion"].get("not_updated", 0)
        text = (
            f"There are {ov['total_kpis']} KPIs across Teras 1–7. "
            f"{high_risk} KPI(s) are high-risk and require attention. "
            f"{ov['missing_information']} KPI(s) have incomplete information. "
            + (f"Teras {top['teras_number']} has the most KPIs ({top['kpi_count']})." if top and top['kpi_count'] else "")
        )
        return {
            "generated_by": "deterministic",
            "text": text.strip(),
            "highlights": {
                "total_kpis": ov["total_kpis"],
                "high_risk": high_risk,
                "missing_information": ov["missing_information"],
                "incomplete_or_not_updated": incomplete,
                "top_teras": (top["teras_number"] if top else None),
            },
        }

    # ---------- organisation-aware comparison (V1.1) ----------
    def ppd_comparison(self, current_user, parent_organisation_id=None):
        """Per-PPD aggregates for comparison (top/lowest/high-risk/budget/Teras).

        Role-scoped like every dashboard method. Rows are built ONCE and grouped by organisation,
        so PPDs are compared without duplicating the aggregation logic. PPDs with no KPIs yet are
        included with zeroed metrics so the hierarchy is fully represented.
        """
        ppds = OrganisationRepository(self.db).list(type_="PPD", parent_id=parent_organisation_id)
        rows = self._build(current_user)
        by_org = defaultdict(list)
        for r in rows:
            by_org[r.get("organisation_id")].append(r)

        items = []
        for org in ppds:
            ov = self._overview_from_rows(by_org.get(org.id, []))
            total = ov["total_kpis"]
            achieved = ov["achievement"].get("achieved", 0)
            items.append({
                "organisation_id": org.id, "code": org.code, "name": org.name, "type": org.type,
                "total_kpis": total,
                "achieved": achieved,
                "achievement_rate": round(achieved / total, 4) if total else 0.0,
                "high_risk": ov["risk"].get("high", 0),
                "missing_information": ov["missing_information"],
                "achievement": ov["achievement"],
                "risk": ov["risk"],
                "finance": ov["finance"],
                "by_teras": ov["by_teras"],
            })

        # Rank: best achievement_rate first; tie-break by achieved count, then fewer high-risk.
        ranked = sorted(items, key=lambda x: (x["achievement_rate"], x["achieved"], -x["high_risk"]),
                        reverse=True)
        for i, it in enumerate(ranked):
            it["rank"] = i + 1
        return {
            "parent_organisation_id": parent_organisation_id,
            "ppd_count": len(ranked),
            "ppds": ranked,
            "top_performer": ranked[0] if ranked else None,
            "lowest_performer": ranked[-1] if ranked else None,
            "highest_risk": (max(items, key=lambda x: x["high_risk"]) if items else None),
        }
