# Track 05 — Open Innovation (Wildcard)

Tags: Disruptive Tech · Open Innovation · Industry Transformation

## 1. Official Problem Statement

A blank-canvas track for original concepts that sit **outside** the four defined problems — a novel idea, business model or software architecture that can fundamentally transform banking.

## 2. Expected Outcome (official)

Out-of-the-box submissions welcome: decentralized identity, decentralized ledgers, next-gen security fabrics, omni-channel CX. Must show **long-term commercial scalability + real integration viability inside IDBI's ecosystem**.

## 3. AMA Clarifications (ground truth from mentors)

- Solve **real banking pain points**: regulatory requirements / advisories OR operational-efficiency issues bankers face daily.
- Must **not overlap** any of the other 4 tracks.
- Judged with help of subject-matter experts.
- **Openly-invited wishes: back-office reconciliations and KYC struggles.** ← strongest hint of what they want.

## 4. Research Findings (highlights)

> Full cited reference: [research/track-05-research.md](research/track-05-research.md)

- **Reconciliation pain quantified**: UPI hit 23.2B transactions / ₹29.9T in May 2026 (~738M/day); banks run 3-way recon (CBS vs UPI switch vs NPCI raw files) per settlement cycle; timeouts are the largest exception class. **RBI's 2019 TAT circular monetizes recon speed**: UPI auto-reversal by T+1, then ₹100/day automatic compensation — every unresolved break is a running penalty clock.
- **Vendor gap = the white space**: SmartStream/Cointab/Osfin *match* transactions but humans still *investigate and resolve* exceptions (TCC vs RET decisions, evidence gathering, adjustment drafting, URCS/UDIR actions). The agentic exception-resolution desk is unserved.
- **KYC pain quantified**: June 2025 KYC amendments set 2/8/10-year re-KYC tiers with mandated 3+3 intimations per customer; **the low-risk grace period ends 30 Jun 2026 — a backlog wave is cresting right now**. CKYCR imposes 10-day/7-day SLAs. AML name-screening false positives run 95–99%. MNRL consumption is an RBI mandate (17 Jan 2025 directive, deadline 31 Mar 2025) with monthly-list-vs-CBS matching burden.
- **The regulator itself ships ops-AI**: MuleHunter.AI (RBIH, announced Dec 2024, 23 banks implemented per RTI) — "the regulator wants you to do this" is the strongest argument in a PSU bank room. RBI's Jan 2024 circular explicitly directs banks to use technology for compliance monitoring.
- **IDBI runs Infosys Finacle CBS** (since 2001, 10.x upgrade 2016) → file-based day-1 integration with the same end-of-cycle extracts recon teams already pull; no core surgery. Credible integration slide.

## 5. Candidate Ideas & Pros / Cons

| Candidate | Verdict | Why |
|---|---|---|
| **A. "ReconPilot"** — 3-way UPI recon + agentic exception-resolution desk | **Primary pick** | Explicitly invited; quantified regulatory teeth (₹100/day); incumbents match-but-don't-resolve; recon-banker vocabulary demo (RRN, TCC/RET, suspense GL) |
| **B. "KYCOps Copilot"** — re-KYC lifecycle orchestration + MNRL mule triage + screening-alert adjudication | Strong second / roadmap modules | Invited theme; Jun-2026 backlog wave is *now*; 95–99% false-positive furnace is LLM-shaped; edge risk: keep messaging strictly re-KYC to avoid Track-2 resemblance |
| **C. "CircularSense"** — regulatory-change copilot (circular → obligation register → gap tracking) | Challenger / extensibility slide | RBI repealed 9,446 circulars into ~240 Master Directions (giant re-mapping job); Jan-2024 tech-for-compliance mandate; zero data-privacy risk; but less "wow" than money reconciling |
| Trade-finance LC document AI | Skip | Crowded vendor space (Cleareye/Traydstream), OCR-heavy demo risk |
| Collections / branch copilot / deposit tools | Skip | Overlap risk with Tracks 1/2/4 or reads as generic RAG chatbot |
| DID / DLT / security fabrics | Roadmap mention only | Thin 48h demo-ability; speculative next to CKYCR rails |

**ReconPilot architecture (AWS ap-south-1, satisfies payments data-localisation)**: S3 landing for NPCI/switch/CBS files → Glue normalization to canonical schema → deterministic match (RRN+amount) in Athena → ML fuzzy-match tail (AWS Entity Resolution/SageMaker) → DynamoDB break register with ageing + TAT-compensation clocks (EventBridge) → **Bedrock agent** with tools (`query_cbs`, `query_switch_log`, `query_npci_record`, `find_similar_breaks`, `draft_adjustment_voucher`, `draft_udir_action`, `compute_tat_compensation`), full reasoning trace persisted → NL rule authoring (prose → matching-rule JSON, dry-run tested) → ops dashboard with one-click approval.

**Synthetic demo**: 3 mock files for one settlement cycle (~50k rows) with seeded breaks (30 timeouts, 10 duplicates, 5 mismatches, 5 orphans, cross-cycle drift) → 99.7% auto-match in seconds → agent walks 3 exceptions live with root cause in plain English, drafts TCC/RET + voucher, shows the ₹100/day clock → supervisor approves → FTE-hours and penalty-₹ saved.

## 6. Winning Strategy & Demo Plan

Mentors *gave away the rubric* by inviting recon + KYC — treating those as the hidden problem statement converts Track 5 from high-variance to **arguably the most de-risked track**: you compete against unfocused chatbot/blockchain entries while building exactly what the judges asked for.

**SME-judge levers**: recognition shock (show *their* artifacts — NPCI file columns, TCC/RET, suspense GL ageing, re-KYC intimation letters); a number on every slide ("50 breaks/day × 25→4 min = ~3.5 FTE; ₹100/day × timeout backlog = ₹X lakh/yr; freeze-prevention protects ₹Y cr CASA"); explainability + human-in-the-loop by construction (agent proposes, human disposes, readable reasoning trace); integration realism (Finacle file-based day-1, API phases later); regulatory-tailwind framing (MuleHunter, TAT circular, compliance-tech circular).

**Risks & mitigations**: no anchor rubric → open with the pain in the judges' daily language; "vendors do this" → conceded and answered (they match, we resolve; they onboard, we run the lifecycle); scope sprawl → one polished UPI-recon stream end-to-end beats five shallow modules; synthetic-data credibility → mirror real NPCI column semantics, close with "works on your real files in a 2-week PoC."
