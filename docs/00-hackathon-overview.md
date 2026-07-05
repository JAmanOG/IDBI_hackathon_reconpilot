# IDBI Innovate 2026 — Hackathon Overview & Ground Rules

> Source of truth: official problem statements + AMA mentor Q&A clarifications (captured 2026-07).
> This file records the *given* facts. Research-derived material lives in the per-track docs.

## The 5 Tracks

| # | Track | One-liner | Domain tags |
|---|-------|-----------|-------------|
| 01 | Digital Wealth Management | Avatar-based AI wealth advisor inside the bank's mobile app | Wealth Advisory · Conversational AI · Mobile Banking |
| 02 | Prospect Assist AI | Behaviour-driven lead generation + real-income assessment for retail lending | Lead Generation · Behavioural Analytics · Retail Lending |
| 03 | Financial Health Score (MSME) | Alternate-data financial health card for NTC/NTB MSMEs | Financial Inclusion · Digital Lending · Credit Decisioning |
| 04 | Default Prediction Model | 12-month-ahead MSME probability-of-default with RAG buckets | MSME Credit · Predictive AI · Risk Management |
| 05 | Open Innovation (Wildcard) | Any real banking pain point outside tracks 1–4 | Disruptive Tech · Open Innovation · Industry Transformation |

## Prizes & Perks

- Total pool: **₹15 lakh**.
- Per track: Winner **₹2 lakh**, Runner-up **₹1 lakh**.
- Perks: sandbox access + **enterprise-scale pilot deployment with IDBI** (the real prize — a bank pilot).

## Environment (all tracks)

- **AWS-cloud sandbox** with internal APIs + **synthetic datasets** + dummy request/response sets.
- You may bring your own APIs if needed.
- **Prefer AWS services**; GCP tools only if callable via API.
- Deployment target: on-prem or cloud both acceptable to IDBI.

## Compliance (all tracks)

- Stay within **SEBI / RBI / IRDA / DPDP** norms.
- KYC, Aadhaar, MNRL tooling is OK to use.
- AI must follow **RBI AI norms** (see FREE-AI framework notes in per-track docs).
- AI coding agents (Claude Code, Cursor, ElevenLabs, etc.) are **allowed** — but no copyright issues and no copied code.

## State of Play at IDBI (from AMA)

- IDBI has **no LLM / AI in production yet** — everything is in UAT / testing.
- Implication: judges are buying a *credible first production AI*, not a moonshot. Explainability, auditability, and human-in-the-loop design are differentiators in every track.

## Cross-track judging signals (inferred from AMA language)

1. **Human-in-the-loop everywhere** — AI assists, humans decide (explicit in tracks 1, 3, 4).
2. **Explainability is non-negotiable** — "auditor will ask why" (track 3), reason + logic supplied to underwriter.
3. **Multi-source validation** — single-signal solutions (e.g. SMS-only) are explicitly called out as insufficient.
4. **Speak the bank's language** — RAG colour coding, loan-officer terminology, RM lead handoff.
5. **India-stack fluency** — AA, ULI, OCEN, GST, EPFO, UPI, credit bureaus.
6. **Commercial scalability + integration viability** inside IDBI's ecosystem.

## Contact

- Missed AMA question → mail support (per host).
