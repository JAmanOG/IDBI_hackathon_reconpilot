# Track 03 — Financial Health Score (MSME)

Tags: Financial Inclusion · Digital Lending · Credit Decisioning

## 1. Official Problem Statement

MSME credit relies on traditional financial docs that many New-to-Credit (NTC) and New-to-Bank (NTB) firms lack. Rich alternate data (GST, UPI, AA, EPFO…) exists but there is **no unified assessment framework** → high rejections, missed viable borrowers, weak portfolio diversity, slow financial inclusion.

## 2. Expected Outcome (official)

Design an AI/ML **MSME Financial Health Card** that:
- aggregates alternate data (GST, UPI, AA, EPFO);
- computes a **multidimensional health score**;
- visualizes strengths & risks;
- integrates with **ULI / OCEN / AA** ecosystems;
- enables near real-time credit assessment;
- onboards credit-invisible MSMEs and lifts portfolio quality.

## 3. AMA Clarifications (ground truth from mentors)

- Focus = **new-to-bank / new-to-credit MSMEs** with thin or no paper trail.
- Alternate / side signals: **electricity consumption** (mfg units), EPFO contributions, fuel cost, power usage, purchase-sale data, digital footprint.
- Bucket customers: **disciplined vs non-disciplined**; go / no-go.
- Underwriter is **not replaced** — AI supplies the reason + logic; a human takes the final credit call.
- **Explainability required** (auditor will ask "why").
- Aim for quick, easy, reliable results.
- **SMS data alone is not enough** — can be stale or a wrong number. Validate and cross-check with multiple data points.

## 4. Research Findings (highlights)

> Full cited reference: [research/track-03-research.md](research/track-03-research.md)

- **The gap**: only ~19% of MSME credit demand is met formally (NITI Aayog, May 2025); unmet gap ₹69–80 lakh crore depending on estimate. NTC cold-start loop: no bureau footprint → no score → no loan.
- **Closest prior art is FIT Rank** (TU CIBIL + OPL, SIDBI-mentored): Finance (bank) + Income (ITR) + Trade (GST) ML rank 1–10 predicting 12-month NPA, aimed at NTC. Our differentiation: more rails (7 vs 3) + an auditable Health Card with reason codes and what-if, vs an opaque rank. CMR needs existing credit history — useless for NTC.
- **Data rails reality check**: GSTN is live as an AA FIP (GSTR-1/3B, 18 months, ReBIT schema) — mock to that schema; Setu/Finvu AA sandboxes are genuinely hackathon-usable (Setu static OTP); EPFO/DISCOM have no open lender APIs — mock to published shapes; the free public GSTIN-lookup API can be the one live call.
- **Ecosystem numbers for the pitch**: ULI at 64 lenders, 136+ data services, ₹27,000 cr disbursed (~₹14,500 cr MSME); AA at ₹1.6 lakh crore of loans enabled; GeM Sahay validated 7-minute cash-flow loans, ₹200 cr/month.
- **Evidence**: cash-flow features lift MSME scoring to AUROC 0.806 (+24.6% over application-only, arXiv 2510.16066); on small imbalanced datasets logistic regression matches or beats tuned ensembles — justifying scorecard-first.
- **FREE-AI mapping done** (7 sutras → concrete card features — see research doc table); Digital Lending Directions 2025 + DPDP demand purpose-bound consent → consent-ledger tab on the card.

## 5. Proposed Architecture

**Six pillars**: Sales & Growth (GST) · Cash-flow discipline (AA/UPI) · Compliance discipline (GSTR punctuality, Udyam) · Employment stability (EPFO ECR) · Concentration risk (counterparty HHI) · Utility-verified activity (kWh vs declared sales). Pillar scores 0–100 → composite 300–900 → Green/Amber/Red + go/review/no-go recommendation. **Never auto-reject.**

**Hybrid two-layer model**: WoE logistic scorecard per pillar (regulator-native, auditable) + XGBoost/SHAP challenger as "ML second opinion"; scorecard-vs-challenger disagreement auto-escalates to the underwriter. Reason codes from a fixed ~40-entry banker-language library; LLM (Bedrock, temperature 0) only *phrases* computed codes — never decides. **Data-coverage badge** (score confidence from rails present) structurally answers "SMS alone is insufficient." **Peer benchmarking** within HSN-code × state × turnover-band cells. **Fraud cross-checks before scoring**: GST turnover vs bank credits mismatch, flat kWh vs doubling sales, circular-trading heuristics, EPFO headcount = 0 — hard flag suppresses the score ("Verification required").

AWS: Lambda per-rail connectors validating published schemas → S3/DynamoDB → pandas feature pipeline (~80–120 features) → scorecard + challenger + SHAP → React Health Card (score dial with confidence band, pillar bars, RAG chips, consent tab, **what-if simulator**). Synthetic dataset: 1,000–5,000 MSMEs from archetypes (kirana, manufacturer, services, seasonal, stressed, fraud case) with simulated 12-month stress labels for an honest AUC slide.

## 6. Pros / Cons of Approach Options (decisions)

| Choice | Decision | Why |
|---|---|---|
| Model | **Hybrid two-layer** (scorecard + GBM/SHAP challenger) | Scorecard auditability AND ML lift; disagreement→human is a FREE-AI governance story |
| Presentation | **Pillar scores + composite** | Single score hides *why*; pillars map to the brief verbatim |
| Narrative | **LLM constrained to computed reason codes** | Fluent + grounded; "LLM never decides, only phrases" is the perfect FREE-AI answer |
| Integration | **Schema-faithful mocks + 1 live touch** (public GSTIN lookup or Setu AA sandbox) | GSP/EPFO onboarding takes weeks; ReBIT/GSTR schema compliance proves the production path |

## 7. Winning Strategy & Demo Plan

**Lead with the underwriter, not the model** — demo a workday: queue → card → reasons → drill-down to raw GST filing dates → what-if → decision with logged override. Own explainability three ways (scorecard points, SHAP, reason codes). **Fraud cross-validation is the theater moment** (declared turnover 3.1× bank credits → auto-flag). Ecosystem slide: engine as OCEN Derived-Data Provider / ULI data service / AA FIU with Dec-2025 numbers. FREE-AI sutra table verbatim on a slide.

**6-minute demo**: NTC weaver with no CIBIL (0:30) → AA-style consent, rails light up, coverage 78% (1:00) → Health Card 668/900 Green with pillar bars (1:30) → reason-code drill-down to exact filing dates (1:00) → what-if simulator + underwriter decision log (1:00) → Amber stressed case, then fraud case auto-flagged (0:45) → close: "CMR can't see her. FIT Rank scores her in a black box. We hand the underwriter the *why*." (0:15)

**Honest assessment**: most crowded track (many GST+statement scoring demos expected). Exploit common weaknesses: single opaque score, no coverage handling, no fraud cross-validation, LLM in the decision path. This track rewards credit-domain judgment over ML novelty.
