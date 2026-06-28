"""CP6 tests: Excel parsing, warnings, KPI creation, audit, import-once + override, RBAC, no monthly updates."""
import io

import openpyxl
from sqlalchemy import select

from app.skills import excel_parsing_skill as parser
from app.models.operational.kpi import KPI, KPIMonthlyUpdate
from app.models.operational.imports import ImportBatch

PWD = "Password123!"

HEADERS = ["Teras", "KPI Code", "KPI Statement", "Indicator", "Target", "TOV",
           "PIC Name", "PIC Email", "Department", "Activity", "Object Code", "Amount"]


def _make_workbook(rows: list[list]) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pelan Taktikal"
    ws.append(["RANCANGAN PENDIDIKAN MALAYSIA 2026-2035"])  # noise row
    ws.append(HEADERS)
    for r in rows:
        ws.append(r)
    buf = io.BytesIO(); wb.save(buf); return buf.getvalue()


GOOD_ROW = [1, "TS1.S1.P1.KPI2", "Percentage of placed teachers", "% placed", "100%", "80%",
            "En. Rao", "rao@moe.gov.my", "BPSH", "Workshop", "OS29000", 9280]
MISSING_ROW = [2, "TS1.S1.P2.KPI2", "BM competency", None, None, "13%",
               "", "", "BPSH", "Bengkel", "OS29000", 2560]  # missing indicator/target/pic


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


# 1. Excel parsing works
def test_excel_parsing_works():
    data = _make_workbook([GOOD_ROW])
    out = parser.parse_workbook(data)
    assert out["rows"] and out["rows"][0]["kpi_code"] == "TS1.S1.P1.KPI2"
    assert out["rows"][0]["pic_email"] == "rao@moe.gov.my"


# 2. Missing fields generate warnings (V1.1.1: mandatory = statement, pic_name, teras;
#    pic_email is captured manually since it is absent from the source files).
def test_missing_fields_generate_warnings():
    rec = parser.parse_workbook(_make_workbook([MISSING_ROW]))["rows"][0]
    miss = parser.missing_fields(rec)
    assert "pic_name" in miss          # MISSING_ROW has an empty PIC name
    assert "pic_email" not in miss     # email is no longer mandatory at import


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


# 3 & 4. Valid rows create KPI records + audited
def test_execute_creates_kpi_and_audits(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    data = _make_workbook([GOOD_ROW, MISSING_ROW])
    r = client.post("/api/v1/imports/execute", headers=_auth(tok),
                    files={"file": ("pt.xlsx", data)}, data={"plan_type": "jpn"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "completed"
    assert body["rows_imported"] >= 1 and body["warnings_count"] >= 1
    # KPI persisted
    assert db_session.scalar(select(KPI).where(KPI.code == "TS1.S1.P1.KPI2")) is not None
    # audited
    audit = client.get("/api/v1/audit/logs", headers=_auth(tok)).json()
    assert any(a["action"] == "import_execute" for a in audit)


# 5 & 6. Duplicate blocked; override allows re-import
def test_duplicate_blocked_then_override(client, make_admin):
    tok = _admin_token(client, make_admin)
    data = _make_workbook([GOOD_ROW])
    files = {"file": ("pt.xlsx", data)}
    first = client.post("/api/v1/imports/execute", headers=_auth(tok), files=files, data={"plan_type": "jpn"})
    assert first.json()["status"] == "completed"
    dup = client.post("/api/v1/imports/execute", headers=_auth(tok),
                      files={"file": ("pt.xlsx", data)}, data={"plan_type": "jpn"})
    assert dup.json()["blocked"] is True and dup.json()["status"] == "blocked"
    ov = client.post("/api/v1/imports/execute", headers=_auth(tok),
                     files={"file": ("pt.xlsx", data)}, data={"plan_type": "jpn", "override": "true"})
    assert ov.json()["status"] == "completed" and ov.json()["blocked"] is False


# 7. Non-admin cannot execute import
def test_non_admin_cannot_import(client):
    _register(client, "plain@moe.gov.my")
    tok = _login(client, "plain@moe.gov.my")["access_token"]
    r = client.post("/api/v1/imports/execute", headers=_auth(tok),
                    files={"file": ("pt.xlsx", _make_workbook([GOOD_ROW]))}, data={"plan_type": "jpn"})
    assert r.status_code == 403


# 8. Import does not create monthly updates
def test_import_creates_no_monthly_updates(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    client.post("/api/v1/imports/execute", headers=_auth(tok),
                files={"file": ("pt.xlsx", _make_workbook([GOOD_ROW]))}, data={"plan_type": "jpn"})
    assert db_session.scalar(select(KPIMonthlyUpdate)) is None


# Preview shape
def test_preview(client, make_admin):
    tok = _admin_token(client, make_admin)
    r = client.post("/api/v1/imports/preview", headers=_auth(tok),
                    files={"file": ("pt.xlsx", _make_workbook([GOOD_ROW, MISSING_ROW]))},
                    data={"plan_type": "jpn"})
    assert r.status_code == 200
    body = r.json()
    assert body["total_rows"] == 2
    assert body["records_to_create"]["kpi"] >= 2
    assert len(body["warnings"]) >= 1
    assert body["duplicate_risk"] is False and body["file_hash"]
