# Track 3 Research — MSME Financial Health Score (AI/ML "Financial Health Card")

**IDBI Innovate 2026 · Researched 2026-07-04**

> **Problem statement recap:** Build an AI/ML "Financial Health Card" for New-to-Credit (NTC) / New-to-Bank (NTB) MSMEs with thin/no paper trail. Aggregate alternate data (GST, UPI, Account Aggregator, EPFO, electricity, fuel, purchase-sale, digital footprint), compute a multidimensional **explainable** health score, visualize strengths and risks, integrate with ULI/OCEN/AA, deliver near-real-time assessment, bucket disciplined vs non-disciplined borrowers with a go/no-go signal — **while retaining the human underwriter**. Explainability is mandatory ("the auditor will ask why"). SMS data alone is insufficient; multiple sources must cross-validate each other.

---

## 1. Domain landscape

### 1.1 The credit gap — why this track exists

- **NITI Aayog (May 2025), "Enhancing Competitiveness of MSMEs in India":** only **~19% of MSME credit demand was met formally by FY21, leaving ~₹80 lakh crore (₹80 trillion) unmet**. Share of micro/small enterprises accessing scheduled-bank credit rose from 14% (2020) to 20% (2024); medium from 4% to 9% — improving, but the gap remains enormous. ([PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2126063&reg=3&lang=2), [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/indias-inr-80-lakh-crore-credit-problem-for-msmes/491098))
- **IFC / SME Finance Forum "MSME Finance Gap" update (March 2025)** gives the global methodology; India-specific citations circulate a figure of **~₹69.3 lakh crore** (e.g., CRIF India citing IFC). Use "₹69–80 lakh crore depending on estimate" in the pitch to be defensible. ([SME Finance Forum report PDF](https://www.smefinanceforum.org/sites/default/files/Data%20Sites%20downloads/IFC%20Report_MAIN%20Final%203%2025.pdf), [CRIF India LinkedIn](https://www.linkedin.com/posts/crif-india_crif-msme-msmegrowth-activity-7340278974981234688-8gmL))
- Root cause for NTC/NTB MSMEs: **no bureau footprint → no score → no loan → no footprint** (cold-start loop). The policy answer since 2022 has been **cash-flow-based lending** on digital public infrastructure (AA + GSTN-as-FIP + OCEN + ULI). RBI explicitly added GSTN as a Financial Information Provider "to facilitate cash flow-based lending to MSMEs." ([Sahamati](https://sahamati.org.in/gstn-as-financial-information-provider/))

### 1.2 Existing scores — what incumbents already do (and the gap we fill)

| Product | Who | Inputs | Output | Limitation vs Track 3 |
|---|---|---|---|---|
| **CIBIL MSME Rank (CMR)** | TransUnion CIBIL | Bureau repayment history; entities with credit exposure ₹10L–₹50Cr (extended below ₹10L from 2020, CMR 2.0) | Rank 1 (least risky) → 10 (most risky); ~7.5M MSMEs eligible | **Requires existing credit history — useless for NTC** ([CMR asset sheet](https://www.transunioncibil.com/content/dam/transunion-cibil/business/collateral/sheet/P-msme-rank-CMR2.0-asset-sheet.pdf), [Bajaj Markets](https://www.bajajfinservmarkets.in/cibil-score/what-is-cibil-msme-rank)) |
| **FIT Rank** (the closest prior art — study it) | TransUnion CIBIL + Online PSB Loans (OPL), under **SIDBI mentorship** | **F**inance (bank statements) + **I**ncome (ITR) + **T**rade (GST) — triangulated via ML | Rank 1–10 = probability of becoming NPA in next 12 months; claims **>5× risk differentiation in the medium-risk segment**; explicitly aimed at NTC MSMEs | Proprietary black box to the borrower/underwriter; 3 data rails only; no EPFO/utility/UPI; no visual health card, no reason codes, no what-if. Used for SIDBI Express Loans, GST Sahay, working capital. ([SIDBI](https://www.sidbi.in/finance-income-trade-rank-fit-rank), [TransUnion CIBIL newsroom](https://newsroom.transunioncibil.com/under-sidbis-mentorship-fit-rank-for-msmes-launched-by-transunion-cibil-and-online-psb-loans-limited-opl/), [OPL](https://www.oplinnovate.com/products/fit-rank.html)) |
| **CRIF High Mark / Experian commercial reports** | Bureaus | Commercial bureau + bureau scores | Reports/scores | Same NTC blindness |
| **Jocata Sumpoorn** | Jocata + SIDBI (Nov 2023) | Consent-led, anonymized monthly GSTN sales of 50,000+ credit-seeking MSMEs | **MSME Economic Activity Index** (relative-amplitude-adjusted composite diffusion index) — macro indicator, not a borrower score | Sector/macro-level; but a great idea to borrow: **peer/sector benchmarking as a scoring pillar** ([SIDBI](https://www.sidbi.in/jocata-sumpoorn), [Business Standard](https://www.business-standard.com/companies/news/sidbi-launches-sumpoorn-msme-economic-activity-index-with-jocata-123111001092_1.html)) |

### 1.3 Fintech practice — proof the approach works

- **Lendingkart:** cash-flow-based lending; application + bureau + bank-statement cash-flow data → **5,000+ derived variables** in ML underwriting; GST + transaction data instead of collateral. ([Lendingkart careers](https://www.lendingkartcareers.com/how-lendingkart-uses-machine-learning/), [AIM](https://analyticsindiamag.com/how-lendingkart-uses-machine-learning/))
- **Indifi:** ecosystem/platform data (Amazon, Zomato, MakeMyTrip partnerships) → sector-tailored products; transactional data as creditworthiness signal. ([Recur Club overview](https://www.recurclub.com/blog/fintech-lending-startups-digital-shift))
- **FlexiLoans:** unsecured SME term loans on digital underwriting + bank-statement analysis. GST-first underwriting is now the common thread across these NBFCs.
- **Perfios** (bank-statement analytics, fraud checks; acquired **Karza** — GST/KYC/Udyam analytics APIs): these are the "picks and shovels" vendors banks actually buy — position the hackathon build as an in-house IDBI alternative with superior explainability.
- **OCEN / GeM Sahay pilot (cash-flow lending validated in production):** launched May 2021; loans against GeM government invoices, **end-to-end sanction+disbursal in ~7 minutes**; 121 Finance alone crossed ₹10 crore / 2,600+ loans to 400+ MSMEs across 173 cities; network-wide **Q1-2026: 35,485 loans, ~₹1,125 crore**, monthly disbursements crossed ₹200 crore. ([OCEN previous pilots](https://ocen.dev/docs/previous_pilots/), [StartupTalky on 121 Finance](https://startuptalky.com/news/121-finance-crosses-10-crore-in-gem-sahay-disbursements-strengthening-msme-access-to-digital-credit/), [OCEN blog](https://ocen.dev/blog/new-headline-metrics-to-account-for-short-term-lending/))

**Positioning line:** "CMR can't see NTC borrowers. FIT Rank sees three data rails and returns an opaque 1–10. We see seven rails and return a **Health Card an auditor can read**."

---

## 2. Data rails in detail — what's real, what's mockable

| Rail | Real access path | Hackathon verdict |
|---|---|---|
| **GST — private (consent) APIs** | GSTR-1 (outward supplies) & GSTR-3B (summary + tax paid) via a **GSP** (GST Suvidha Provider — Vayana, Masters India, IRIS, Cleartax…) with taxpayer OTP consent ([Cleartax GST API access](https://cleartax.in/s/gst-api-access), [Masters India](https://www.mastersindia.co/goods-and-services-tax-gst-api/)) | **Mock** the JSON (public schemas exist); GSP onboarding takes weeks |
| **GST — public API** | GSTIN search: legal name, registration date, status, filing table — **no consent needed** ([Decentro GST API](https://decentro.tech/resources/goods-and-services-tax-gst-api)) | Could be **live** in demo (nice "one real API" flourish) |
| **GST via Account Aggregator** ⭐ | **GSTN is live as an FIP on the AA network** (RBI notified Nov 2022): GSTR-1 Table 4 + GSTR-3B for trailing **18 months** + profile, delivered in ReBIT-standard JSON schema ([Sahamati](https://sahamati.org.in/gstn-as-financial-information-provider/), [GSTN](https://www.gstn.org.in/account-aggregator), [ReBIT schema news](https://sahamati.org.in/rebit-publishes-gstn-data-schema-for-the-account-aggregator-framework/)) | Mock to the **ReBIT schema** — this is the architecturally correct consent rail; say so on stage |
| **Account Aggregator (bank data)** | Sahamati ecosystem: **24+ crore consent requests, 18+ crore linked accounts, ₹1.6 lakh crore of loans across 1.8+ crore loan accounts** ([Sahamati](https://sahamati.org.in/)); specs + FI schemas on [GitHub](https://github.com/Sahamati/account-aggregator-standards). Sandboxes: **Setu AA** (mock data for all 23 FI types; Setu FIP-2 static OTP `123456` — [docs](https://docs.setu.co/data/account-aggregator/quickstart)), **Finvu** (test-data entry APIs conforming to ReBIT FITypes — [sandbox](https://finvu.github.io/sandbox/)), **OneMoney** (UAT needs number whitelisting, 1–2 days) | **Setu/Finvu sandbox is genuinely usable in a hackathon** — a real AA consent flow on stage is a differentiator; else mock the ReBIT DEPOSIT schema |
| **UPI / bank transactions** | Arrives inside AA bank-statement data (narrations: `UPI/cred/...`) — no separate NPCI API for lenders | Synthesize realistic narration strings; classify counterparties (customer vs supplier vs personal) |
| **EPFO (payroll formality)** | No open lender API. Reality: (a) public **establishment search** on epfindia.gov.in shows monthly ECR payment status + employee counts; (b) commercial verification APIs (Surepass, Signzy, Decentro, Perfios) fetch UAN/establishment data ([Surepass](https://surepass.io/epfo-verification-api/), [Decentro](https://decentro.tech/resources/employment-verification-api), [EPFO ECR](https://www.epfindia.gov.in/site_en/Online_ECR.php)) | **Mock** monthly ECR series: employee count + contribution regularity = employment-stability pillar |
| **Udyam registration** | Verification APIs from AuthBridge/IDfy/Surepass/Gridlines against the official Udyam DB ([IDfy](https://www.idfy.com/udyam-verification-api/), [Surepass](https://surepass.io/udyam-registration-check-api/)) | Mock or live-ish; use as identity anchor + enterprise classification (micro/small/medium, NIC code) |
| **Electricity (DISCOM)** | **Fragmented — no unified API.** Realistic paths: BBPS bill-fetch APIs (billed-amount history by consumer number), state DISCOM portals, or borrower-uploaded bills (OCR). Recognized as alternate data in literature ([CredAble](https://credable.in/insights-by-credable/business-insights/a-deep-dive-into-credit-underwriting/)) | **Mock** 24-month kWh + billed-amount series for manufacturing archetypes; kWh→output correlation is a strong, hard-to-fake activity signal |
| **ULI (RBIH)** | As of Dec 2025: **64 lenders (41 banks + 23 NBFCs), 136+ data services, 12 loan journeys**; land records (8 states), satellite data, verification services ([Medianama, Jan 2026](https://www.medianama.com/2026/01/223-unified-lending-interface-64-lenders-136-data-services/), [RBIH](https://rbihub.in/projects/unified-lending-interface)). Cumulative **600k+ loans / ₹27,000 cr, of which ~160k loans / ₹14,500 cr to MSMEs** ([Business Standard](https://www.business-standard.com/economy/news/over-600k-loans-worth-rs-27-000-cr-disbursed-on-uli-platform-rbi-report-124122600872_1.html)); DFS is actively scaling it ([PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2139039&reg=3&lang=2)) | Not directly integrable in a hackathon. **Architectural claim:** expose the Health Score itself as a ULI data service; consume ULI verification services as inputs. IDBI is a ULI participant-class bank — judges will love this framing |
| **OCEN 4.0** | Roles: Borrower Agent, Lender, Technology/Derived-Data Providers; escrow-based collections ([ocen.dev](https://ocen.dev/blog/escrow-based-collections-in-ocen/), [FAQs](https://ocen.dev/docs/faqs/)) | Position the score engine as a **Derived Data Provider** in OCEN flows; show a stub JSON score-response API |
| **Commercial bureau** | CMR/FIT via TransUnion CIBIL contracts | Mock a "bureau: no-hit" response — that's precisely the NTC scenario |

**Key demo insight:** every rail above has a **published JSON schema or well-documented shape** — so high-fidelity mocks are credible. Explicitly show the ReBIT/GSTN schema compliance of your mocks.

---

## 3. Scoring methodology

### 3.1 Six-pillar design (multidimensional by construction)

| Pillar | Example features | Primary rails |
|---|---|---|
| **Sales & Growth** | GST turnover level/trend/YoY, seasonality-adjusted momentum, e-invoice volume | GST, AA |
| **Cash-flow discipline** | Bank credit regularity, inflow/outflow ratio, EOD-balance floor, bounce/return count, expense volatility | AA, UPI |
| **Compliance discipline** | GSTR filing punctuality (days-late distribution), 3B vs 1 consistency, ITR filed, Udyam current | GST, ITR, Udyam |
| **Employment stability** | EPFO headcount trend, ECR payment regularity, wage-bill/revenue ratio | EPFO |
| **Concentration & dependency risk** | Top-customer share of receipts (HHI), supplier concentration, geographic spread | GST B2B invoices, AA counterparties |
| **Utility-verified real activity** | kWh trend vs declared sales correlation, load factor, bill-payment punctuality; fuel spend for logistics | DISCOM, BBPS, fuel |

Pillar scores 0–100 → composite 300–900 (banker-familiar range) → **Green / Amber / Red** buckets + go/review/no-go recommendation. **Never auto-reject:** output = recommendation + reasons for the human underwriter (this is both the brief and RBI's expectation).

### 3.2 Model architecture — hybrid two-layer (recommended)

- **Layer 1 (per-pillar, interpretable):** WoE-binned **logistic scorecard** per pillar — the regulator-native format (points per bin, monotonic, auditable line-by-line). Evidence this is not a performance sacrifice: on Italian SME data XGBoost and logistic regression show **similar discrimination** ([Moscatelli et al., Research in International Business and Finance 2024](https://www.sciencedirect.com/science/article/pii/S0275531924001909)), and on small (<1k rows) imbalanced datasets LR frequently matches or beats tuned ensembles.
- **Layer 2 (composite + challenger):** transparent weighted aggregation of pillar scores (weights defensible: expert-set, exposed in UI) **plus** a gradient-boosting challenger model with **SHAP** attributions, shown side-by-side as "ML second opinion." If scorecard and GBM disagree beyond a threshold → automatic "refer to underwriter" flag. This is exactly the champion/challenger governance FREE-AI encourages.
- **Reason codes:** top-N signed SHAP values (challenger) and points-lost-per-bin (scorecard) → mapped to a fixed library of ~40 banker-language reason codes (e.g., `RC-07: GST filings late in 4 of last 6 periods (−32 pts)`). Deterministic mapping = auditable; LLM used **only** to phrase the narrative around already-computed codes (no LLM in the decision path).
- **Data-coverage / confidence indicator:** score confidence = f(rails present, history length, cross-validation agreement). A borrower with only GST+bank gets a "Coverage 62% — EPFO, utility missing" badge; low coverage widens the score's displayed confidence band and can force "review" instead of "go." This answers the brief's "SMS alone is insufficient" requirement structurally.
- **Peer benchmarking:** normalize sales/growth features within **HSN-code × state × turnover-band** peer cells (the Sumpoorn insight, applied at borrower level): a 15% dip is bad if peers grew 10%, fine if the sector fell 20%.
- **Fraud / anomaly cross-checks (cross-validation layer, run before scoring):**
  - GST-declared turnover vs AA bank credits ratio out of band → `MISMATCH` flag;
  - **Circular-trading heuristics:** high B2B sales concentration to entities that are also suppliers; invoice spikes just before loan application; round-number invoice clustering;
  - kWh flat while declared sales double (manufacturing) → activity-verification fail;
  - EPFO headcount = 0 while claiming 25 staff.
  - Any hard flag → score suppressed, card shows "Verification required" with the specific mismatch. This is a huge demo moment.

### 3.3 Supporting academic evidence

- **[arXiv 2510.16066](https://arxiv.org/abs/2510.16066) (AI-BAAM, Malaysian MSMEs, 611 applicants):** adding bank-statement cash-flow features → **AUROC 0.806, +24.6% over application-only models**. Cite honestly as Malaysian data, directionally validating cash-flow underwriting for thin-file MSMEs.
- LR-vs-ensemble nuance above ([Italian SME study](https://www.sciencedirect.com/science/article/pii/S0275531924001909)) justifies the scorecard-first hybrid: interpretability costs little AUC here, and cutoff choice matters more than model family.

---

## 4. Regulatory mapping

### 4.1 RBI FREE-AI (report released 13 Aug 2025) — sutra → product feature

7 sutras, 26 recommendations across 6 pillars (Infrastructure, Policy, Capacity / Governance, Protection, Assurance). ([KPMG](https://kpmg.com/in/en/insights/2025/08/rbi-free-ai-committee-report-on-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence.html), [humaineeti summary](https://www.humaineeti.ai/resources/rbi-free-ai-framework), [InsightsOnIndia](https://www.insightsonindia.com/2025/08/14/rbi-has-released-a-report-on-the-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence-free-ai/))

| Sutra | Feature in our Health Card |
|---|---|
| **Trust is the Foundation** | Full audit log: every score version, inputs, model hash, reason codes stored append-only |
| **People First** | Underwriter always decides; card is decision **support**; override with mandatory reason, fed back for model monitoring |
| **Innovation over Restraint** | Alternate-data rails expand access for NTC borrowers (financial-inclusion framing) |
| **Fairness & Equity** | Peer-cell benchmarking prevents sector penalty; bias check across sector/geography/gender-of-proprietor in model report |
| **Accountability** | Named model owner; champion/challenger governance; disagreement auto-escalates to human |
| **Understandable by Design** | Scorecard points table + SHAP reason codes + plain-language narrative on every card ("auditor will ask why" — answered) |
| **Safety, Resilience, Sustainability** | Coverage badge + degraded-mode scoring when a rail is down; input-drift monitors |

### 4.2 Digital lending & data protection

- **RBI Digital Lending Directions, 2025 (8 May 2025):** need-based data collection with **explicit, auditable consent**, purpose disclosure at each stage; borrower rights to withdraw consent, restrict third-party sharing, and seek deletion; device permissions one-time and KYC-only. Alternate-data/behavioural analytics use requires **specific, purpose-bound notice**. ([Argus Partners](https://www.argus-p.com/updates/updates/rbi-digital-lending-directions-2025-an-overview/), [Cyril Amarchand](https://corporate.cyrilamarchandblogs.com/2025/05/fig-paper-no-44-series-3-rbi-consolidates-directions-on-digital-lending-implications-for-res-lsps/))
- **DPDP Act:** proprietor data (sole proprietorships = personal data of the individual) needs notice + consent per purpose; AA framework is itself the consent artifact for financial data — show the consent receipt on the Health Card. ([Mondaq on DPDP for lending NBFCs](https://www.mondaq.com/india/privacy-protection/1733676/dpdp-act-compliance-for-physical-and-digital-lending-nbfcs))
- Demo artifact: a **"Consent & Compliance" tab** on the card listing each rail, its consent id/timestamp, purpose, and expiry.

---

## 5. Hackathon architecture (AWS)

```
[Mock rail generators]                [Ingestion]           [Feature & Score]              [Serve/UI]
GST JSON (ReBIT schema) ─┐
AA bank stmts (Setu-like)─┤   API GW + Lambda        Lambda/Step Functions:        FastAPI on Lambda/ECS
EPFO ECR series ─────────┼──▶ connectors ──▶ S3 ──▶  feature builder ──▶ scorecard  ──▶ React Health Card
DISCOM kWh series ───────┤   (per-rail adapter)  (raw+curated)  + XGBoost+SHAP        (Amplify/S3+CloudFront)
Udyam / bureau no-hit ───┘        │                     │(pandas)     │                     │
                              DynamoDB consent ledger   Feature store (DynamoDB)   Bedrock (Claude) narrative
```

- **Connectors:** one Lambda per rail, each validating against the published schema (ReBIT FI types, GSTR JSON) — proves "real-API-ready."
- **Feature pipeline:** deterministic pandas job → ~80–120 features tagged by pillar; run cross-validation/fraud checks first.
- **Models:** `scikit-learn` LR scorecard (WoE binning via `optbinning`) + `xgboost` challenger + `shap`. Train on synthetic dataset (below). Score latency <2s = "near-real-time."
- **Narrative:** Amazon Bedrock LLM converts computed reason codes into 4-sentence banker narrative (temperature 0, template-guarded, never invents numbers).
- **Health Card UI:** score dial (with confidence band), 6 pillar bars, RAG strengths/risks chips, coverage badge, consent tab, fraud-flag banner, **what-if simulator** (sliders: "if GST filings on time for 6 months → score 612 → 668") — the underwriter-empowerment feature judges remember.

### Synthetic dataset design (the credibility backbone)

Generate ~1,000–5,000 MSMEs from parameterized archetypes × discipline levels:

| Archetype | Signature |
|---|---|
| Kirana/retail | High-frequency small UPI credits, low GST B2B share, no EPFO, modest electricity |
| Small manufacturer | Lumpy B2B invoices, high kWh correlated to sales, EPFO 8–40 staff, seasonal raw-material outflows |
| Services firm | Few large invoices, high customer concentration, EPFO white-collar pattern |
| Seasonal (agri-linked/festive) | 3–4 month revenue spikes; tests seasonality handling |
| **Stressed/non-disciplined** | Late GSTR filings, cheque bounces, falling EOD balance, dropping headcount |
| **Fraud case** | GST turnover 3× bank credits, flat kWh, circular counterparties — for the anomaly demo |

Label = 12-month "stress event" simulated from latent discipline factor + noise → honest ROC/AUC slide on held-out data.

---

## 6. Pros/cons tables

**Model choice**

| Option | Pros | Cons |
|---|---|---|
| Pure WoE/logistic scorecard | Regulator-native, fully auditable, stable on small data | Misses interactions; "less impressive AI" optics |
| GBM + SHAP | Best raw discrimination; SHAP demo appeal | Post-hoc explanations; harder model-risk sign-off; overfits small synthetic data |
| **Hybrid two-layer (rec.)** | Scorecard auditability **and** ML lift; disagreement→human is a governance story | More build effort; must explain two artifacts crisply |

**Score presentation**

| Option | Pros | Cons |
|---|---|---|
| Single score only | Simple, familiar | Hides *why*; fails the multidimensional brief |
| **Pillar scores + composite (rec.)** | Diagnoses strengths/risks; maps to reason codes; matches brief verbatim | Slightly busier UI |

**Narrative**

| Option | Pros | Cons |
|---|---|---|
| Template reason codes only | Deterministic, auditable, zero hallucination | Robotic; underwriters skim past |
| LLM free-form | Fluent, contextual | Hallucination risk in a credit decision = fatal in Q&A |
| **LLM constrained to computed codes (rec.)** | Fluent + grounded; "LLM never decides, only phrases" is the perfect FREE-AI answer | Needs guardrails/eval demo |

**Integration**

| Option | Pros | Cons |
|---|---|---|
| Real APIs (GSP, AA prod) | Authenticity | Weeks of onboarding; demo fragility; GSP/EPFO not hackathon-feasible |
| **Schema-faithful mocks + 1 live touch (rec.)** | Reliable demo; ReBIT/GSTR schema compliance proves production path; live public GSTIN lookup or Setu AA sandbox flow adds authenticity | Judges may probe "is this real?" — pre-empt with the schema-compliance slide |

---

## 7. Winning strategy, demo script, competitive assessment

### Strategy

1. **Lead with the underwriter, not the model.** The brief says human retained; most teams will demo a model. Demo a *workday*: underwriter opens queue → card → reasons → what-if → decision + override log.
2. **Own explainability end-to-end:** scorecard points + SHAP + reason-code library + consent tab + audit log. Answer "why?" three different ways in Q&A.
3. **Cross-validation as theater:** the fraud archetype (GST≠bank, flat kWh) getting auto-flagged is the most memorable 30 seconds available in this track.
4. **Ecosystem fluency:** one slide placing the engine as an OCEN Derived-Data Provider / ULI data service / AA FIU — with the Dec-2025 ULI numbers cited. Few student teams will have this.
5. **FREE-AI table (above) verbatim on a slide.** Judges from a bank in 2026 will pattern-match instantly.

### 6-minute demo script

1. (0:30) NTC weaver with no CIBIL history — "the ₹80-lakh-crore problem" ([PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2126063&reg=3&lang=2)).
2. (1:00) Consent flow (AA-style) → rails light up → coverage badge 78%.
3. (1:30) Health Card: 668/900, Green; pillar bars; two strengths, two risks in plain language.
4. (1:00) Click a reason code → the exact GST filing dates behind it (auditor drill-down).
5. (1:00) What-if simulator + underwriter go/review decision with logged rationale.
6. (0:45) Stressed case (Amber) then fraud case → "Verification required: declared turnover 3.1× bank credits."
7. (0:15) Close: "CMR can't see her. FIT Rank scores her 1–10 in a black box. We hand the underwriter the *why*."

### Honest competitive assessment

- **Most "core-banking" track = likely the most crowded.** Expect many GST+bank-statement scoring demos; several will use GPT-wrappers for "explainability."
- Commonest weaknesses to exploit: single opaque score, no coverage/confidence handling, no fraud cross-validation, no regulatory mapping, LLM in the decision path (a Q&A landmine you can turn on rivals politely by contrast).
- Real risk to us: a team with actual production AA integration or a banker on the team. Mitigation: sandbox-live AA flow + deep FIT-Rank/FREE-AI literacy.
- This track rewards **credit-domain judgment over ML novelty** — the winning artifact is the Health Card an IDBI underwriter would actually use tomorrow.

---

## 8. Source index

Credit gap: [PIB/NITI Aayog](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2126063&reg=3&lang=2) · [IFC MSME Finance Gap 2025](https://www.smefinanceforum.org/sites/default/files/Data%20Sites%20downloads/IFC%20Report_MAIN%20Final%203%2025.pdf) — Scores: [SIDBI FIT Rank](https://www.sidbi.in/finance-income-trade-rank-fit-rank) · [TU CIBIL FIT launch](https://newsroom.transunioncibil.com/under-sidbis-mentorship-fit-rank-for-msmes-launched-by-transunion-cibil-and-online-psb-loans-limited-opl/) · [CMR 2.0](https://www.transunioncibil.com/content/dam/transunion-cibil/business/collateral/sheet/P-msme-rank-CMR2.0-asset-sheet.pdf) · [Jocata Sumpoorn](https://www.sidbi.in/jocata-sumpoorn) — Rails: [GSTN-as-FIP](https://sahamati.org.in/gstn-as-financial-information-provider/) · [ReBIT GSTN schema](https://sahamati.org.in/rebit-publishes-gstn-data-schema-for-the-account-aggregator-framework/) · [Sahamati stats](https://sahamati.org.in/) · [Setu AA docs](https://docs.setu.co/data/account-aggregator/quickstart) · [Finvu sandbox](https://finvu.github.io/sandbox/) · [Cleartax GST API](https://cleartax.in/s/gst-api-access) · [EPFO ECR](https://www.epfindia.gov.in/site_en/Online_ECR.php) · [Surepass EPFO](https://surepass.io/epfo-verification-api/) · [IDfy Udyam](https://www.idfy.com/udyam-verification-api/) — Ecosystems: [ULI 64 lenders/136 services](https://www.medianama.com/2026/01/223-unified-lending-interface-64-lenders-136-data-services/) · [ULI ₹27k cr](https://www.business-standard.com/economy/news/over-600k-loans-worth-rs-27-000-cr-disbursed-on-uli-platform-rbi-report-124122600872_1.html) · [RBIH ULI](https://rbihub.in/projects/unified-lending-interface) · [OCEN pilots](https://ocen.dev/docs/previous_pilots/) · [GeM Sahay/121 Finance](https://startuptalky.com/news/121-finance-crosses-10-crore-in-gem-sahay-disbursements-strengthening-msme-access-to-digital-credit/) — Regulatory: [KPMG FREE-AI](https://kpmg.com/in/en/insights/2025/08/rbi-free-ai-committee-report-on-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence.html) · [FREE-AI sutras](https://www.humaineeti.ai/resources/rbi-free-ai-framework) · [Digital Lending Directions 2025](https://www.argus-p.com/updates/updates/rbi-digital-lending-directions-2025-an-overview/) · [DPDP for lenders](https://www.mondaq.com/india/privacy-protection/1733676/dpdp-act-compliance-for-physical-and-digital-lending-nbfcs) — Evidence: [arXiv 2510.16066](https://arxiv.org/abs/2510.16066) · [Italian SME LR-vs-XGB](https://www.sciencedirect.com/science/article/pii/S0275531924001909) — Fintech: [Lendingkart ML](https://www.lendingkartcareers.com/how-lendingkart-uses-machine-learning/)
