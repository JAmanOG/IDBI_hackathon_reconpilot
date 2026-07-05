# Track 04 — Default Prediction Model (MSME)

Tags: MSME Credit · Predictive AI · Risk Management

## 1. Official Problem Statement

Current default-prediction accuracy is only **16–22%**, uses **only structured data**, and methodologies are fragmented across loan types and borrower segments.

## 2. Expected Outcome (official)

Build a robust model that estimates **probability of default** to flag stress **12 months in advance**, with accuracy raised to **~90%**. Use structured AND unstructured data, methods tuned per loan type / borrower profile, and one common interpretation framework → consistent, comparable, actionable outputs across all MSME loans.

## 3. AMA Clarifications (ground truth from mentors)

- Scope = **existing running loan accounts**; predict default 12 months ahead to contain stress.
- Must combine: borrower behaviour + internal bank DB + **public-domain data**.
- Output = risk **buckets**: High / Medium / Low, shown as **RAG (Red / Amber / Green)** coding, in language loan officers use.
- Common interpretation = **hybrid**: per segment / locality PLUS a shared unified scale.
- Score factors: vintage, occupation, experience, qualification, age group → a unified score (not one flat number).
- **Human intervention retained** (AI assists, does not auto-decide).

## 4. Research Findings (highlights)

> Full cited reference: [research/track-04-research.md](research/track-04-research.md)

- **Correct framing**: this is an **EWS / behavioural-scoring / IFRS-9 12-month-PD problem**, not application scoring. RBI's 2015 loan-fraud framework mandates EWS (~45 illustrative signals, refreshed by the July 2024 Fraud Risk Master Directions — so an ML EWS is a regulatory obligation IDBI must discharge anyway). SMA-0/1/2 maps 1:1 onto Green/Amber/Red, and "12 months in advance" is literally the Ind AS 109 12-month PD — the model is dual-use as a SICR staging engine.
- **The 16–22% number** is best read as the precision/hit-rate of today's rule-based EWS alerts (rule engines routinely run 80–90% false positives). **The 90% trap**: at a ~5% default rate, predicting "no default" for everyone is ~95% accurate. Honest reframe (memorize): *"~90% of accounts that will default in 12 months already sitting in Red+Amber today, at an alert budget you choose."*
- **Benchmarks**: SME default models cluster at AUC 0.75–0.85. Survival-ML gains are thin (GBST C-index 0.6867 vs Cox 0.6799 on 224k Lending Club loans); Fantazzini & Figini found logit beat Random Survival Forests out-of-sample — justifying a regularized GBM champion + simple challengers over exotica.
- **Market proof**: Crediwatch sells exactly this (SBI, IndusInd clients; "distress up to 12 months in advance", 200+ alert library). GST-compliance-trend monitoring flags stress months before default.
- **Governance is the differentiator**: RBI Aug-2024 draft Model Risk Management in Credit circular (independent validation, documentation, board oversight) + FREE-AI sutras → ship a Model Card + Validation Report with the submission.
- **Logistics**: hackathon launched 12 Jun 2026, registration closes 9 Jul 2026 (Hack2skill); organisers provide synthetic MSME/transaction/UPI datasets.

## 5. Proposed Architecture

Synthetic loan-book generator (5–10k accounts × 24–36 monthly snapshots; trajectory archetypes: healthy, slow-bleed defaulter, cliff defaulter, **stressed-but-recovers**, seasonal false-alarm case) → **point-in-time feature store** (features strictly ≤ T; label = NPA in (T, T+12]; out-of-time validation split — leakage is the #1 credibility killer) → **LightGBM champion** (class-weighted, monotonic constraints) + WoE-scorecard and Cox/GBST survival challengers → **per-segment isotonic calibration onto one unified master scale** (this IS the brief's "hybrid interpretation" ask — say "master scale" out loud) → RAG bucketing on calibrated PD (fixed cutpoints + workload cap on the queue).

**Feature catalogue**: internal conduct (utilization trend, DPD/SMA history, cheque/NACH bounces, inward returns, LC devolvement, stock-statement delays, turnover decline — each citing its RBI EWS ancestor), transaction behaviour (counterparty concentration HHI, salary-batch date drift), public domain (GSTR filing lapses, MCA charges/auditor resignations, e-courts §138 cases, EPFO lapses, adverse media), and an **LLM unstructured lane**: synthetic banker call-memos → fixed flag taxonomy with verbatim evidence quotes → model features + drill-down display ("feature, never decision").

**Dashboard**: portfolio heat-map with RAG migration; account drill-down (calibrated PD + expected time-to-default, SHAP waterfall in loan-officer sentences, trend sparklines, memo evidence, recommended action); alert queue sorted by PD × exposure with Acknowledge/Investigate/Override-with-reason feeding retraining; model-health tab (gain chart with alert-budget slider, calibration curve, PSI).

## 6. Pros / Cons of Approach Options (decisions)

| Choice | Decision | Why |
|---|---|---|
| Survival vs binary | **Binary GBM champion; survival as challenger + "months-to-stress" display** | Thin evidence of survival gains; binary = IFRS-9 12m PD; judges know Gini/KS not C-index |
| Per-segment vs pooled | **Pooled GBM + per-segment isotonic calibration to master scale** | Data-efficient; satisfies the hybrid ask with pooled robustness |
| Unstructured lane | **Include, scoped: 4–6 flag types, evidence-grounded** | Brief explicitly requires unstructured; earliest signals precede the numbers |
| RAG thresholds | **Fixed calibrated-PD cutpoints + workload cap overlay** | Stable audit-friendly meaning; quantile masks downturn deterioration |

## 7. Winning Strategy & Demo Plan

**Five differentiators**: speak risk-team language (SMA, SICR, master scale, champion–challenger, PSI); honestly kill the 90% number then beat it on capture-at-budget; dual-use economics (EWS + Ind AS 109 staging + collections triage — one build, three consumers); governance-in-the-box (model card, validation report, monitoring tab); the unstructured lane with receipts.

**6–7 minute demo**: problem reframe ("your EWS fires at SMA-1 — too late — and 1 in 5 flags is real") → portfolio heat-map with month-slider RAG migration → **hero moment**: "Sharda Fabricators", zero DPD, Green on current rules — our model says Red, PD 22%, ~8 months to stress; SHAP waterfall in plain words, sparklines, memo quote; fast-forward shows SMA-2 seven months later → contrast: seasonal business the rule engine false-flags but the model keeps Green → numbers slide (out-of-time gain chart: ~85–90% capture at 20%-of-book budget, ~4× lift; calibration curve) → officer override with reason lands in feedback log; model card + PSI flash → roadmap (AA GST pulls, bureau feed, sequence encoder).

**Prepped answers**: synthetic-data honesty ("metrics prove methodology, not production performance"), why-not-deep-learning (tabular GBM + validation cost + OOS caution), GST/EPFO consent (AA-consented + public domain, DPDP-by-design), age-group fairness (FREE-AI fairness audit; conduct features dominate anyway).
