# Track 01 — Digital Wealth Management

Tags: Wealth Advisory · Conversational AI · Mobile Banking

## 1. Official Problem Statement

Wealth advisory is fragmented and inaccessible to most customers. There is no comprehensive view of investment behaviour + spending habits, so guidance is not timely, personalized or data-driven.

## 2. Expected Outcome (official)

AI-powered Digital Wealth Management app with an **avatar-based interface**, embedded into the bank's mobile app. Delivers personalized + scalable advisory through an intuitive digital experience.

## 3. AMA Clarifications (ground truth from mentors)

- **Hybrid model**: AI advises on vanilla (non-regulated) products and can convert directly into a transaction. Regulated products → AI generates a **lead** → handed to a seasoned Relationship Manager.
- Phase 1 = **mobile app**; AI + human hybrid.
- Avatar = **mix of voice + text** (not fully voice; 2D / emotionally-intelligent text is acceptable).
- **Multi-language** support required (pan-India branch network).
- Segments: **Mass, HNI, NRI**; age-based risk (50+ = lower risk; salary account → SIPs).
- Products: **Mutual Funds (SEBI), Insurance (IRDA), NPS / Pension, RBI Bonds**.
- Suitability derived from: short/long-term goals, amount sparable, spending + investment pattern, holdings at **our bank AND other institutions**.
- Market-linked products need **frequent market updates** (dynamic data).
- Recommend at **asset-class level AND specific schemes**.
- Bundle **financial literacy / education** for the mass / low-income segment.

## 4. Research Findings (highlights)

> Full cited reference: [research/track-01-research.md](research/track-01-research.md)

- **Whitespace confirmed**: no Indian bank ships an avatar that advises + transacts + hands off to an RM. Closest precedent is Bank of Baroda's "Aditi" GenAI avatar (May 2024) — service Q&A only, not suitability-driven advisory. That's our differentiation line.
- **The hybrid model is the legally-correct design, not just a preference**: banks are AMFI-ARN MF *distributors* allowed only "incidental advice" — so the AI does suitability-matched recommendations from a bank-approved scheme list and transacts; holistic/fee advice and insurance solicitation must route to a human (IRDAI: only licensed Specified Persons can solicit insurance; corporate agents capped at 9 insurers/line).
- **SEBI Feb 2025 amendments (Reg 16C-type)**: the regulated entity is *fully liable* for AI outputs; June 2025 consultation adds ethics/accountability/auditability pillars → suitability logs + guardrails + grounded numbers are mandatory design, and a strong pitch angle.
- **RBI FRSB 2020** (8.05% Jul–Dec 2025; IDBI Bank is an explicitly designated Receiving Office) is the perfect "AI-transacts-vanilla" product alongside FD/RD and MF SIPs.
- **Account Aggregator now covers the full asset side**: MF, equities (CDSL+NSDL live as FIPs), insurance, NPS (CRAs are FIPs) — 780+ FIs, 2.12B accounts. Mock the AA consent flow to show outside-bank holdings.
- **Voice**: Sarvam AI (Saarika ASR ~₹30/hr; Bulbul v3 TTS beat ElevenLabs in a 20k-vote Indic blind study) as primary; Bhashini/AI4Bharat as the free 22-language scale story. **Avatar**: 2D Rive/Live2D rig with emotion states (free, offline-safe, AMA-approved) + optional HeyGen/D-ID photoreal toggle (~$0.10–0.20/min).
- **Live MF data is free**: AMFI NAVAll.txt + mfapi.in JSON API — enough for the "frequent market updates" requirement.

## 5. Proposed Architecture

React mobile-shell PWA → avatar layer (Rive 2D rig; photoreal toggle) → Sarvam ASR/TTS streaming → FastAPI backend → **Claude on Bedrock in a plain tool-use loop** with strict-schema tools:

`get_customer_profile` · `get_portfolio(include_aa)` · `compute_risk_profile` · `get_goal_plan` · `recommend` (rules engine over bank-approved scheme list) · `get_market_data` (AMFI live) · `execute_transaction` (vanilla only: FD/FRSB/SIP, OTP mock) · `create_rm_lead` · `log_suitability` (audit trail)

Plus: Bedrock Guardrails + deterministic compliance post-filter (blocks "guaranteed returns" etc.), RAG over scheme factsheets + literacy content, and a second-screen **RM console** showing AI-written lead briefs and the suitability log. Three pre-seeded personas: Ravi (28, mass, Hindi, voice, SIP execution), Meera (54, HNI, AA holdings → FRSB + insurance RM lead), Arjun (35, NRI Dubai, FEMA/NRE flags).

**Build order**: chat+voice in 2 languages → risk-profile conversation → portfolio w/ AA mock → rules recommender w/ live NAVs → one live transaction → RM lead + console → suitability log. Cut first: real AA sandbox, real payments, insurance quotes.

## 6. Pros / Cons of Approach Options (decisions)

| Choice | Decision | Why |
|---|---|---|
| Avatar depth | **2D rig (Rive/Live2D) + emotion states**; photoreal API as toggle | Zero latency/cost, offline-safe, AMA explicitly allows 2D; video-gen APIs are network-fragile in demo halls |
| Voice vs text | **Text-first with voice toggle** (hybrid = AMA's stated expectation) | ASR errors in noisy halls; voice for greetings/explanations, cards for numbers/confirmations |
| Recommendation engine | **Rules shortlist + LLM-RAG explanation layer** | Auditable AND conversational; hallucination-capped (numbers only from tools); pure-LLM = disqualifying in a bank |
| TTS/ASR | **APIs now (Sarvam), Bhashini DPI as scale roadmap** | Days-not-weeks; best Indic quality; sovereignty pitch for a PSU-adjacent bank |

## 7. Winning Strategy & Demo Plan

**Judge levers**: compliance-by-design shown on screen (suitability log, audit JSON), explainability ("Why this?" card on every recommendation), RM console framed as a lead-gen machine (not a fallback), revenue math (MF trail, bancassurance leads, FRSB stickiness, RM productivity), inclusion story (Bhashini languages + literacy micro-lessons).

**7-minute demo**: problem (30s) → Ravi mass/Hindi/voice: risk questions → allocation → live-NAV schemes → execute ₹5k SIP → literacy bite (2m) → Meera HNI: AA consent → external holdings → FRSB 8.05% execution → insurance gap → RM lead on console with suitability log (2m) → compliance interlude: "guarantee me 15%" refused by guardrail, audit trail shown (1m) → architecture + regulatory matrix + cost-in-paise scale slide (1m) → business numbers close (30s).

**Prepped judge answers**: liability (bank's, per SEBI Feb 2025 — hence rules-bounded + logged), direct vs regular plans (regular; ARN distributor revenue), vs BoB Aditi (service Q&A vs advisory+transactions+handoff), hallucinations (numbers only from tools), NRI (NRE/NRO, FEMA flags as hard rules).
