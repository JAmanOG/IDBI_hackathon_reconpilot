# Track Comparison & Recommendation — IDBI Innovate 2026

> Synthesized from the five research dossiers (2026-07-04). Registration closes **9 July 2026** on Hack2skill — pick fast.

## 1. Scoring matrix

Scores 1–5 (5 = best for us). "Competition" = 5 means *least* crowded.

| Factor | T1 Wealth Avatar | T2 Prospect AI | T3 MSME Health | T4 Default EWS | T5 ReconPilot |
|---|---|---|---|---|---|
| Competition (expected crowd) | 3 | 3 | **1** (most crowded) | 4 | **5** (unfocused entries) |
| Judge-rubric clarity | 4 (AMA very specific) | 4 | 4 | 4 | **5** (mentors gave the rubric away: recon+KYC) |
| Demo wow-factor | **5** (talking avatar, live SIP) | 4 | 3 | 4 (hero drill-down) | 4 (money reconciling live + ₹ clock) |
| Build risk in hackathon window | 2 (voice+avatar+LLM+rules = many moving parts) | 4 | 4 | 4 | 4 |
| Domain-fluency barrier to entry (our moat if we do the homework) | 3 | 3 | 3 | **5** (SMA/IFRS-9/master-scale vocabulary) | **5** (RRN/TCC/URCS vocabulary) |
| Synthetic-data burden | 3 | 3 | 3 | 2 (loan-book generator is the hard part) | 4 (3 files, seeded breaks) |
| Business-case punch (₹ on slides) | 4 (RM productivity, trail revenue) | 4 (cost/loan 10–20×) | 4 (₹80L-cr gap) | 4 (NPA containment) | **5** (₹100/day penalty clock + FTE math) |
| Regulatory-story strength | 5 (SEBI AI liability mapped) | 4 | 5 (FREE-AI mapped) | 5 (model-risk + FREE-AI) | 5 (TAT circular + MuleHunter precedent) |

## 2. Ranked recommendation

1. **Track 5 — ReconPilot** (best odds). The mentors explicitly invited reconciliation; the field will be unfocused chatbots; the ROI is a literal regulatory penalty clock; the demo is buildable (3 mock files, seeded breaks, Bedrock agent resolving them live); IDBI's Finacle stack gives a credible zero-core-change integration story. Risk: requires genuine recon-domain fluency — the research doc supplies it.
2. **Track 4 — Default EWS** (best for an ML-strong team). Fewest teams will speak SMA/IFRS-9/champion-challenger; the honest "90% reframe" earns respect; the governance artifacts (model card, validation report) are cheap to produce and rare in hackathons. Risk: point-in-time synthetic loan-book generator is the single hardest build item; leakage mistakes are fatal.
3. **Track 1 — Wealth Avatar** (best for a full-stack/product team). Real whitespace (BoB Aditi is Q&A-only), highest stage drama, and the compliance matrix is a moat. Risk: most moving parts (ASR/TTS/avatar/LLM/rules/RM console) — cut ruthlessly to the 3-persona script.
4. **Track 2 — Prospect Assist** (solid, less differentiated). Great architecture (3 visible models + fusion) and the uplift-modelling flex, but several analytics vendors' case studies make it feel "known"; winning needs polish + the persuadables story.
5. **Track 3 — MSME Health Score** (most crowded). Only enter with deep credit-domain judgment: underwriter-workday demo, fraud cross-validation theater, FIT-Rank/FREE-AI literacy. Otherwise you're one of a dozen GST+statement scoring demos.

## 3. Cross-track reusable assets (build once, whichever track)

- **Synthetic Indian bank-statement/UPI generator** (personas, VPA/narration realism, seasonality) — needed by T2, T3, T4; useful in T1 (spend patterns) and T5 (CBS leg).
- **Bedrock tool-loop agent skeleton** with strict JSON-schema tools + audit logging + Guardrails — T1 (advisor), T4 (memo extraction), T5 (exception desk).
- **Scorecard + GBM + SHAP + reason-code pipeline** — T2, T3, T4.
- **React dashboard shell** (cards, drill-down, RAG chips, consent/audit tabs) — all tracks.
- **FREE-AI sutra → feature mapping slide** — all tracks (verbatim table in regulatory-landscape.md).

## 4. Universal judging themes (say these in any track)

1. Human-in-the-loop *architected* (override queues, feedback retraining), not asserted.
2. Explainability three ways: model-level (scorecard/SHAP), decision-level (reason codes), narrative-level (LLM phrases, never decides).
3. Multi-source cross-validation (the AMA's "SMS alone is not enough").
4. India-stack + regulator fluency: AA/ULI/OCEN/GSTN numbers, FREE-AI sutras, the relevant circular by name and date.
5. ₹-quantified ROI on every slide.
6. "IDBI has no AI in production" → position as the credible *first* production AI: governed, auditable, fallback-equipped.
