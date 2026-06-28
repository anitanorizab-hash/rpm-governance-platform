# TRACEABILITY_REGISTER.md

> **Single Source of Truth — End-to-End Traceability**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
The backbone that links every layer of the project so nothing is orphaned and nothing is built
without a reason. Maps each need from problem framing through to verification.

## Traceability chain
```
HMW → BRD (BRQ) → TRD (FRQ/NFRQ) → User Story → Feature → AI Agent → Skill → API → Frontend → Test Case
```

## When updated
- As each layer is produced (HMW, BRD, TRD, stories, design, build, tests).
- Every new requirement must get a row; every built artifact must reference its requirement.

## Relationship with other documents
- **Draws from:** all KB registers and every produced artifact.
- **Governs:** completeness checks at each freeze gate (no requirement without trace).

## Register columns
| HMW ID | BRD Req (BRQ) | TRD Req (FRQ/NFRQ) | User Story | Feature | AI Agent | Skill | API | Frontend | Test Case | Status |
|--------|---------------|--------------------|-----------|---------|----------|-------|-----|----------|-----------|--------|
| _(to be populated from HMW phase onward)_ | | | | | | | | | | |

### Seed linkage examples (illustrative, pre-HMW)
| HMW ID | BRD Req | TRD Req | User Story | Feature | AI Agent | Skill | API | Frontend | Test Case | Status |
|--------|---------|---------|-----------|---------|----------|-------|-----|----------|-----------|--------|
| TBD | BRQ-005 | TBD | TBD | Finance allocation tracking | Budget Intelligence | LowCostHighImpact scoring | TBD | TBD | TBD | Not started |
| TBD | AIRQ-001 | TBD | TBD | KPI chatbot | KPI Chatbot | RAG retrieval | TBD | TBD | TBD | Not started |

> Rows are placeholders until the HMW and BRD phases generate real IDs.
