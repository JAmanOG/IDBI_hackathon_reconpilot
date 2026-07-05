# ReconPilot — agentic UPI reconciliation & exception-resolution desk

**IDBI Innovate 2026 · Track 5 (Open Innovation)**

Banks reconcile every UPI transaction three ways — core banking (Finacle) vs the UPI switch vs NPCI settlement files. Matching is a solved problem; **resolving the exceptions is not**: humans still investigate each break, decide TCC vs RET, draft vouchers, and race the RBI clock (UPI debit without credit must auto-reverse by T+1, then the bank owes the customer **₹100/day, automatically** — RBI circular DPSS.CO.PD No.629, 20 Sep 2019).

ReconPilot does the 3-way match deterministically, then puts an **agent on the exceptions desk**: it pulls all three records, checks precedent, computes the live penalty clock, drafts the adjustment voucher + UDIR action, and submits a resolution — **a human supervisor approves every action**, and every step lands in an append-only audit log.

```
 NPCI settlement file ─┐
 UPI switch log ───────┼─► normalize ─► 3-way match (RRN) ─► break register (SQLite)
 Finacle CBS dump ─────┘      │                                   │
                        rules JSON ◄── NL rule authoring          ▼
                        (dry-run before promote)          agent investigation
                                                          (Gemini tool-loop / offline mock)
                                                                  │ proposes only
                                                                  ▼
                                                   supervisor approve/reject ─► audit log
```

## Quickstart

```bash
# backend (Python 3.11+, uv)
cd backend
uv venv && uv pip install -e .
.venv/bin/uvicorn app.api.main:app --port 8000

# frontend (production build, served by the backend at :8000)
cd ../frontend
npm install && npm run build

# or frontend dev mode with hot reload (proxies /api to :8000)
npm run dev
```

Open http://localhost:8000 → **Generate files** → **Run recon**.

### Live agent vs offline mock

The exception agent runs a manual **Google Gemini** function-calling loop (`google-genai` SDK,
default model `gemini-2.5-flash`) when a key is available. With no key — or on any API failure —
it **falls back to a deterministic offline investigator that produces the identical trace/proposal
shape**, so the demo never depends on venue Wi-Fi. The UI labels which mode produced a proposal.
Same for the NL rule author (Gemini structured output / phrase parser).

```bash
export GEMINI_API_KEY=...                 # optional: live agent (GOOGLE_API_KEY also works)
export RECONPILOT_MODEL=gemini-2.5-pro    # optional model override
```

> Hackathon-rules note: the AMA allows GCP tools "if callable via API" — the Gemini API qualifies;
> everything else in the stack is cloud-agnostic and deploys on the AWS sandbox unchanged.

## What the demo shows (6 minutes)

1. **Generate files** — ~50,470 NPCI-style rows + switch log + Finacle GL dump for a 6-day settlement
   window, with 75 seeded breaks across 6 classes (`ground_truth.json` records every one).
2. **Run recon** — **99.85% auto-match in <0.5 s**; 75 exceptions land in the queue, sorted by
   severity × exposure. Detection is provably complete: found = seeded, zero false positives.
3. **Dashboard** — the ₹ story: penalty exposure with a live **₹100/day accrual clock**, amount at
   risk, desk minutes saved (25 → 4 min per break).
4. **Investigate a timeout break** — agent walks NPCI/switch/CBS, explains the root cause in
   recon-desk language, drafts the **reversal voucher + RET** and computes the compensation due.
   Show the reasoning trace and the audit log (every tool call journaled).
5. **Approve** — supervisor clicks ✓; status flips, audit trail extends. *Agent proposes, human disposes.*
6. **Rules tab** — type *"Tolerate 1-cycle date drift between NPCI and CBS"* → dry run shows
   **75 → 60 breaks** → promote → recon re-runs. A vendor change-request becomes a sentence.

## Repository map

```
backend/app/
  datagen/generate.py    synthetic 3-file generator + ground truth (seeded breaks)
  recon/normalize.py     per-source adapters → canonical legs (swap point for real APIs)
  recon/matcher.py       3-way match, break taxonomy, rules-driven tolerances
  recon/tat.py           RBI T+1 / ₹100-per-day compensation clock
  store/db.py            SQLite break register + append-only audit log
  agent/tools.py         typed agent tools (query_*, draft_*, submit_resolution)
  agent/agent.py         Gemini function-calling loop + deterministic offline mock
  api/main.py            FastAPI routes; serves frontend/dist
  api/rules_nl.py        NL → matching-rule JSON (Gemini structured output / phrase parser)
frontend/src/            React ops dashboard (queue, 3-way evidence, trace, rules lab)
```

## Honest notes

- All data is synthetic; file layouts mirror the *semantics* of NPCI/switch/CBS artefacts (RRN join
  key, response codes, cycles, Finacle narration format) without reproducing any proprietary format.
- Match-rate and detection numbers demonstrate the methodology on seeded data, not production
  performance. The pitch line for judges: *"works on your real files in a 2-week PoC."*
