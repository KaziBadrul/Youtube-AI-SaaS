# Completed architecture feasibility gates

Frozen v1 — 2026-10-05. Product discovery and S1–S9 are closed. This is the **current status index**, not a request to rerun experiments. Historical reports retain original plans, failures, conditional language and superseded statuses. Feasibility PASS is not production acceptance, provider activation or invitation readiness.

| Gate | Current verdict | Adopted evidence | Important limitation |
| --- | --- | --- | --- |
| S1 — Python/web boundary | PASS | [S1](architecture/evidence/local-feasibility/S1.md) | Django auth/media/range/autosave/focused JS fixture; not device/browser acceptance |
| S2 — SQLite | PASS | [S2](architecture/evidence/local-feasibility/S2.md) | Single-host WAL, short transactions, CAS/integer money; no arbitrary-scale guarantee |
| S3 — Worker recovery | PASS | [S3](architecture/evidence/local-feasibility/S3.md) | Fake external outcomes plus real child groups; live provider reconciliation remains gated |
| S4 — Provider safety | PASS after remediation | [Original S4 FAIL](architecture/evidence/provider-feasibility/S4.md), [S4-R PASS](architecture/evidence/research-feasibility/S4-R.md) | Application-bounded Tavily Basic + tool-free Gemini; exact adapters/account terms before activation |
| S5 — Narration/mapping | PASS | [Final B + B](architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/README.md) | Reviewed existing coherent audio; not general unattended alignment or acoustic restoration/reorder proof |
| S6 — Rendering/captions | PASS | [S6](architecture/evidence/rendering-feasibility/S6/README.md) | Validated 3/5/10 fixtures, shaped PNG captions, controls and process recovery; synthetic inputs are not narration quality |
| S7 — Publication/restoration | PASS | [S7](architecture/evidence/local-feasibility/S7.md) | Crash/selection/structural restoration, not audible joins |
| S8 — Backup/deletion | PASS | [S8](architecture/evidence/local-feasibility/S8.md) | Local protocol; actual off-machine restore/key custody/all historical-copy purge before invitations |
| S9 — Operating economics | PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY | [V14 closure](architecture/evidence/operating-economics/S9/CREDITS-v14.md), [V13 financial controls](architecture/evidence/operating-economics/S9/CREDITS-v13.md), [V11 host qualification](architecture/evidence/operating-economics/S9/CREDITS-v11.md) | Conditional bounded planning, not live quotes/empirical expected costs/quality/profitability |

Active ceiling **$40 USD per Asia/Dhaka calendar month**. Locally qualified **2 vCPU / 4 GiB** host sizing is closed unless later failure; neither a vendor nor SKU is selected. S9 V14 reference: three-minute N≤36/K≤2 initial bound $6.598836, nominal fixed $24.017182, required cash-coverage capacity $9.383982. These are planning parameters, not production caps, credits or tester allowances. Five minutes remains conditional; conservative ten-minute fallback exceeds this envelope and blocks/replans pending sufficient authority. See COST_MODEL.md for financial rules.

Before activation implement/independently verify the accepted finite caps, one-send transport, durable reservations/unknown liability/fencing, source-bound mapping review, render validation and private storage/backup rules. Before invitations exercise VALIDATION_PLAN.md and actual restore/purge/ownership/allowance procedures. None of these prerequisites reopens S1–S9 or fabricates empirical evidence. V1–V14 stay historical; no V15 exists or is authorized.
