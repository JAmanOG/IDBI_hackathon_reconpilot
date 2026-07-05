# Track 4 Research — MSME Default Prediction (Early Warning System)

**IDBI Innovate 2026** · Research date: 2026-07-04
Hackathon: launched 12 June 2026, theme "Build. Integrate. Transform.", ₹15 lakh prize pool, registration closes 9 July 2026 on Hack2skill ([hack2skill.com/event/idbinnovate](https://hack2skill.com/event/idbinnovate), [IDBI press release PR/1463](https://www.idbi.bank.in/press/PR1463.pdf), [BizzBuzz coverage](https://www.bizzbuzz.news/banking/idbi-innovate-2026-hackathon-1394096)). Participants get sandbox APIs and **synthetic datasets covering transactions, MSME financials and UPI patterns** — plan to plug those in, with our own synthetic loan-book generator as fallback.

**Track 4 brief (as given):** probability-of-default for EXISTING running MSME loan accounts, flag stress 12 months in advance; current "accuracy" 16–22%, bank wants ~90%; structured + unstructured data (borrower behaviour + internal bank DB + public domain); output High/Medium/Low buckets with Red/Amber/Green coding in loan-officer language; hybrid interpretation (per segment/locality + shared unified scale); score factors mentioned: vintage, occupation, experience, qualification, age group; human in the loop.

---

## TL;DR

1. This is an **Early Warning System (EWS) / behavioural-scoring / IFRS-9 12-month-PD problem**, not application scoring. Frame it in RBI + risk-team vocabulary: EWS triggers (RBI 2015 fraud framework, ~45 illustrative signals), SMA-0/1/2 ladder (maps 1:1 to Green→Amber→Red), and the Ind AS 109 "12-month PD" (the track's "12 months in advance" IS the IFRS-9 quantity).
2. The "16–22% accuracy" is almost certainly the **precision / hit-rate of today's rule-based EWS alerts** (rule engines routinely run 80–90% false positives). Never promise "90% accuracy" — at a ~5% default rate a model that predicts "no default" for everyone is ~95% accurate. Reframe honestly: **"capture ≥90% of eventual defaulters inside the Red+Amber buckets at a stated false-alarm budget"** — measurable, achievable, and respected by bank risk judges.
3. Recommended build: **point-in-time monthly-snapshot dataset (synthetic) → LightGBM/XGBoost 12-month PD with SHAP → per-segment calibration (isotonic) onto one unified master scale → RAG thresholds → loan-officer dashboard with plain-language reason codes, trend sparklines, recommended actions, and an officer feedback loop.** Optionally a survival-model challenger (time-to-default) and an LLM lane converting call memos / news / GST-filing lapses into structured features.
4. Governance is the differentiator: RBI's **Aug-2024 draft Model Risk Management in Credit circular** (independent validation, documentation, board oversight) and the **Aug-2025 FREE-AI framework** (explainability, human accountability, proportionate risk) give you a ready-made governance story that most teams will ignore.

---

## 1. Domain framing — what this problem actually is

### 1.1 EWS / behavioural scoring, not application scoring

- **Application (A-) scorecard:** scores a *new* applicant at origination using bureau + demographics + financials. Not this track.
- **Behavioural (B-) scorecard:** scores an *existing* account monthly using its own observed conduct (utilization, DPD, bounces, turnover). Standard bank practice; because conduct data is far more predictive than application data, behavioural scorecards typically show materially higher discrimination than application scorecards (industry rule of thumb: Gini ~0.6–0.8 behavioural vs ~0.4–0.6 application). Track 4 is a behavioural scorecard fused with an EWS.
- **EWS (Early Warning System):** a monitoring layer that raises named triggers on running accounts so the bank can act (restructure, tighten limits, step up monitoring) *before* NPA. Track 4 = "EWS with a calibrated PD engine behind it."

Say this framing out loud in the pitch — "we are building a behavioural 12-month PD model that powers your EWS" — because it tells the judges you know their internal vocabulary.

### 1.2 RBI EWS mandate — the 2015 loan-fraud framework and its ~45 signals

- RBI circular **DBS.CO.CFMC.BC.No.007/23.04.001/2014-15 dated 7 May 2015, "Framework for dealing with loan frauds"** requires banks to run EWS and to mark **Red Flagged Accounts (RFA)** when EWS triggers suggest possible fraud ([RBI notification](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=9713&Mode=0); [full circular PDF via CVC](https://cvc.gov.in/files/vigilance-manual-pdf/vm21ch8/vm17ch8/8.%20RBI_2014-15_590-DBS.CO.CFMC.BC.No.00723.04.0012014-15%20dated%2007.05.2015.PDF); [KPMG explainer](https://assets.kpmg.com/content/dam/kpmg/pdf/2015/06/Framework-Loan-fraud.pdf)).
- The annexed **illustrative EWS list is commonly counted as ~42–45 signals** (RBI later published an updated illustrative list of 45 — [Banking School summary](https://bankingschool.co.in/bank-news/rbi-releases-45-early-warning-signals-about-wrongdoingsfrauds-in-loan-accounts/); [RBI EWS notification](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=9878&Mode=0); [TaxGuru list](https://taxguru.in/rbi/early-warning-signals-red-flag-accounts.html)). The bank's "42 signals" in the brief refers to this list.
- Representative signals (use these verbatim as feature names — judges will recognise them): bouncing of high-value cheques; default in payment to banks/sundry creditors/statutory dues; devolvement of LCs / invocation of guarantees; heavy cash withdrawals in loan accounts; high-value RTGS to unrelated parties; delay in submission of stock statements; frequent ad-hoc/overlimit requests; reduction in credit summations (turnover) not commensurate with sales; raids by tax authorities; resignation of key personnel/auditors; dispute with statutory auditors; non-routing of sales proceeds through the financing bank.
- **July 2024 update:** RBI's revised **Master Directions on Fraud Risk Management** (15 July 2024) re-anchor EWS/RFA, require board-approved EWS policy and integration of EWS with core banking / data systems ([ELP summary of the Master Directions](https://elplaw.in/wp-content/uploads/2024/07/RBI-Revised-Master-Directions-on-Fraud-Risk-Management-July-2024.pdf); [Vinod Kothari analysis](https://vinodkothari.com/wp-content/uploads/2024/07/FRM.pdf); [Pirimid overview of what EWS means under the Directions](https://pirimidtech.com/what-is-ews-and-what-does-rbis-fraud-risk-management-direction-mean-for-financial-institutions/)). So an ML-powered EWS is not a nice-to-have for IDBI — it is a regulatory obligation they must discharge anyway. Position Track 4 as "regulatory-grade EWS, upgraded with ML."

### 1.3 SMA-0/1/2 and IRACP — the natural RAG ladder

RBI's IRACP clarification circular **RBI/2021-2022/125 DOR.STR.REC.68/21.04.048/2021-22, 12 Nov 2021** mandates day-end SMA/NPA flagging on running accounts ([circular text mirrored by RBL Bank](https://webassets.rbl.bank.in/document/pdfs/prudential-norms-iracp.pdf); [Satin Creditcare copy](https://satincreditcare.com/wp-content/uploads/2021/12/Guidelines-on-Income-Recognition-Asset-Classification-and-Provisioning.pdf)):

| Class | Term loans (overdue) | CC/OD (continuously beyond limit/DP) | Natural RAG reading |
|---|---|---|---|
| SMA-0 | 1–30 days | — (no SMA-0 for CC/OD) | Green→Amber boundary |
| SMA-1 | 31–60 days | 31–60 days | Amber |
| SMA-2 | 61–90 days | 61–90 days | Red |
| NPA | > 90 days | > 90 days | Default (the label) |

**Key insight for the pitch:** SMA is *lagging* (it fires only after the borrower has already missed payments). The track asks for stress **12 months before** that. So the value proposition is: *"SMA tells you the borrower has already stumbled; our model tells you 12 months earlier who is going to."* Define the model's default label as "slips to NPA (90+ DPD) within the next 12 months" and show the predicted-RAG vs realised-SMA migration matrix — it demonstrates the model front-runs the regulatory ladder.

### 1.4 IFRS 9 / Ind AS 109 — the "12-month PD" is a defined regulatory quantity

- Under IFRS 9 / Ind AS 109 ECL: **Stage 1** assets carry a **12-month ECL = 12-month PD × LGD × EAD**; a **Significant Increase in Credit Risk (SICR)** moves the asset to **Stage 2** (lifetime ECL); credit-impaired = **Stage 3** ([BIS FSI executive summary of IFRS 9](https://www.bis.org/fsi/fsisummaries/ifrs9.pdf); [PwC In-depth on SICR](https://www.pwc.com/hu/hu/szolgaltatasok/ifrs/ifrs_9/ifrs9_kiadvanyok/ifrs_9_impairment_significant_increase_in_credit_risk.pdf); [Institute of Actuaries of India note on ECL under Ind AS 109](https://actuariesindia.org/sites/default/files/inline-files/Expected%20Credit%20Loss%20Framework%20Under%20IND%20AS109.pdf)).
- IFRS 9 contains a **rebuttable presumption that 30 DPD = SICR** and **90 DPD = default** — i.e., the accounting standard itself endorses the SMA→stage→RAG mapping above.
- **The pitch line:** "The bank asked for stress 12 months ahead. That is *exactly* the IFRS-9 12-month PD. Our model is therefore dual-use: it powers the EWS dashboard *and* it is a Stage-1/Stage-2 SICR staging engine for Ind AS 109 provisioning." One model, two budget lines — a very strong story for bank judges.
- Nuance to mention if asked: IFRS-9 PD is **point-in-time (PIT)** and forward-looking (macro-conditioned), unlike Basel IRB's through-the-cycle PD — our monthly-snapshot behavioural PD is PIT by construction, which is the correct flavour.

### 1.5 Existing market practice (proof this is real and buildable)

- **Crediwatch** (used by SBI, IndusInd, Central Bank of India, etc.) sells exactly this product: an EWS combining event-driven alerts and predictive ML, with a **200+ configurable alert library**, public + consented data, and distress signals **"up to 12 months in advance"** ([Crediwatch EWS product page](https://about.crediwatch.com/about/product/early-warning-systems)). The 12-month horizon in the track brief is industry-standard, not arbitrary.
- Bank-statement-analytics vendors document the same transaction-level warning signals we propose (bounce patterns, turnover decline, balance erosion) ([Precisa: EWS in bank statements](https://precisa.in/blog/early-warning-signals-bank-statements/)).
- GST-based monitoring is mainstream in MSME lending: consented GSTR-1/GSTR-3B pulls via Account Aggregator; ML models flag "missed filings, declining output tax despite flat turnover, credit-note spikes, shifts in supplier/customer GSTIN network" **months before default** ([Bankopedia: GST data in MSME credit decisioning](https://www.bankopedia.co.in/banking/gst-data-in-msme-lending-credit-decisioning); [IRIS MSME on GST-powered lending](https://www.irismsme.com/blog/how-gst-data-can-power-lending-for-msmes-in-india/); [FinBox on GST + alternate data underwriting](https://www.finbox.in/blog/gst-invoices-alternate-data-and-cash-flow-underwriting-how-to-unlock-the-400-bn-msme-financing-opportunity)).

---

## 2. The "16–22% accuracy" claim — interpretation, the 90% trap, correct metrics

### 2.1 What 16–22% plausibly means

"Accuracy" from a business stakeholder almost never means classification accuracy. Most plausible readings:

1. **Precision / hit-rate of current rule-based EWS alerts** (most likely): of accounts the current EWS flags, only 16–22% actually default/slip. This matches the well-documented pathology of rule engines in banking — rule-based monitoring systems "generate a lot of false positive alerts", often 80–90%+ ([Springer, J. Supercomputing 2023: ML suppression of false positives in AML monitoring](https://link.springer.com/article/10.1007/s11227-023-05708-z); [ScienceDirect: rule induction to reduce false positives in bank anti-fraud systems](https://www.sciencedirect.com/science/article/abs/pii/S016740482200181X)). 16–22% precision is exactly what a threshold-rule EWS looks like.
2. **Recall / capture**: only 16–22% of accounts that eventually defaulted had been flagged 12 months earlier (alerts fire too late — typically at SMA-1/2, when it's already visible).
3. Accuracy *on the defaulter subset* (same as recall), reported loosely.

**In the pitch, say:** "We read 16–22% as the hit-rate of today's rule-based triggers. The fix is not '90% accuracy' — it's ranking every account by a calibrated 12-month PD so that the small Red bucket contains most future defaulters."

### 2.2 The 90%-accuracy trap (imbalanced data)

- MSME portfolio annual default/slippage rates are low single digits to low teens. At a **5% default rate, a model that predicts "no default" for every account is 95% accurate** and 0% useful. Promising "90% accuracy" is therefore either trivial (majority-class) or meaningless. Bank risk judges know this; naming the trap earns credibility.
- Corollary: never train/evaluate on artificially balanced samples and report those numbers; never use plain accuracy as the headline metric; handle imbalance via class weights / focal loss and evaluate on the natural prior.

### 2.3 The correct metric set (use risk-team vocabulary)

| Metric | What it measures | Typical good value (behavioural/SME) |
|---|---|---|
| **AUC-ROC** | Rank-ordering power | 0.75–0.85 for SME default models; behavioural models with rich conduct data can exceed 0.85 |
| **Gini = 2·AUC − 1** | Same, banker convention | 0.50–0.70 |
| **KS statistic** | Max separation of cumulative good/bad distributions | 30–60 (percentage points) |
| **PR-AUC** | Precision/recall trade-off under imbalance — more honest than ROC at low base rates | report vs. base-rate baseline |
| **Precision & recall at operating point** | Quality of the actual Red bucket | e.g. Red = top 10% of book |
| **Capture rate in top decile** | % of all eventual defaulters inside the riskiest 10% | 50–70%+ is strong |
| **Lift@k** | Capture ÷ base rate | 5–7× in top decile |
| **Calibration (Brier, reliability curve, ECE)** | Is a predicted 8% PD really 8%? Essential because RAG thresholds and ECL both consume the *probability* | reliability curve near diagonal |
| **Lead time** | Months between first Red/Amber flag and actual SMA/NPA event | maximize; show distribution |
| **PSI/CSI** | Population/characteristic stability over time (monitoring metric) | PSI < 0.1 stable, 0.1–0.25 watch, >0.25 shift |

### 2.4 Published benchmarks (calibrate expectations honestly)

- **SME default literature**: systematic methodology reviews cover 100+ studies; typical out-of-sample AUCs cluster ~0.75–0.85, with ML (RF/boosting) usually but not always beating logistic regression ([SME default prediction: a systematic methodology-focused review, 2023](https://www.researchgate.net/publication/376363979_SME_default_prediction_A_systematic_methodology-focused_review); [German SME random-forest study incl. non-financial features](https://www.researchgate.net/publication/372906738_SME_default_prediction_using_random_forest_including_nonfinancial_features_An_empiricial_analysis_of_German_enterprises); Altman & Sabato's classic US SME logistic model reported AUC ≈ 0.75).
- **Survival models**: the **Gradient Boosting Survival Tree (GBST)** paper (Bai, Zheng & Shen; JORS 2022 / [arXiv:1908.03385](https://arxiv.org/abs/1908.03385); [Edinburgh CRC PDF](https://crc.business-school.ed.ac.uk/sites/crc/files/2020-10/J35-Gradient-Boosting-Survival-Tree-with-Applications-in-Credit-Scoring-Bai-2.pdf)) benchmarks on **224,407 Lending Club loans**: GBST beat Cox PH, Random Survival Forest, CoxBoost, DeepHit and XGBoost on C-index/KS/AUC — but the margins are thin (C-index ≈ **0.6867 for GBST vs ≈ 0.6799 for Cox**). Lesson: fancy survival ML buys ~1 point of C-index over 1970s Cox regression on consumer loans.
- **Overfitting caution**: Fantazzini & Figini's **Random Survival Forests for SME credit risk** found RSF beat logit **in-sample but logit won out-of-sample** ([paper](https://www.researchgate.net/publication/225101879_Random_Survival_Forests_Models_for_SME_Credit_Risk_Measurement)). Quote this when justifying a strong, regularised, well-validated GBM + a logistic benchmark, rather than exotic architectures.
- **ML over rules in monitoring**: ML layers on top of rule engines cut false positives 30–80% while retaining 90%+ of true alerts in bank deployments ([Springer AML false-positive suppression](https://link.springer.com/article/10.1007/s11227-023-05708-z)) — this is the realistic "16–22% → better" story: same alert budget, several-fold precision improvement.

### 2.5 The honest reframe of "90%" (memorize this)

> "You can't have 90% accuracy — you can have something better: **~90% of accounts that will default in the next 12 months already sitting in your Red or Amber buckets today**, with the Red bucket small enough (top 1–2 deciles) that your officers can actually work it, at a false-alarm rate we choose together. We trade a meaningless metric for an operating point on a curve that you control."

Show the trade-off explicitly in the demo: a capture-vs-alert-budget curve (gain chart) with a slider.

---

## 3. Model options — pros/cons

### 3.1 WoE + logistic regression behavioural scorecard (the incumbent standard)

- **How:** bin each feature, compute Weight of Evidence, fit logistic regression, scale to points (e.g. 300–900, PDO=20). This is what bank model-risk teams have validated for decades.
- **Pros:** fully transparent points-based reason codes; monotonic by construction; trivially auditable under model-risk rules; stable; tiny; calibrates naturally to PD.
- **Cons:** misses interactions (utilization×vintage, bounce×season); manual binning effort; usually 2–5 AUC points below GBM on rich behavioural data.
- **Hackathon role:** the **benchmark/challenger** — "our GBM beats the classical scorecard by X Gini points on the same data" is a compelling slide, and having a scorecard shows fluency.

### 3.2 XGBoost / LightGBM + SHAP (recommended primary)

- **Pros:** industry default for tabular credit risk; handles missing values, mixed types, interactions; class-weighting for imbalance; monotonic constraints available (force PD non-decreasing in utilization/DPD — a big governance win); SHAP gives exact local attributions → per-account reason codes and waterfall plots; fast to train on a laptop.
- **Cons:** needs post-hoc calibration (raw scores are not PDs — apply isotonic/Platt); can overfit small synthetic data (limit depth, use early stopping); SHAP explanations must be translated out of feature-jargon into loan-officer language (build a phrase dictionary: `util_trend_3m ↑` → "borrower is running the limit harder each month").
- **Evidence:** ML models significantly outperform logistic baselines on balanced accuracy and PR-AUC in recent SME studies ([systematic review](https://www.researchgate.net/publication/376363979_SME_default_prediction_A_systematic_methodology-focused_review)) — but respect the Fantazzini/Figini out-of-sample caution (§2.4).

### 3.3 Survival analysis — time-to-default (elegant fit for "12 months ahead")

- **Options:** Cox PH (interpretable hazard ratios), Random Survival Forests, **Gradient Boosting Survival Trees** ([arXiv:1908.03385](https://arxiv.org/abs/1908.03385)), DeepSurv; Python: `scikit-survival`, `lifelines`, `pycox`.
- **Pros:** models *when*, not just *whether* → one model yields PD at 3/6/12/24 months, expected time-to-default per account ("this account is on a 7-month trajectory"), and handles censoring (accounts still alive, prepaid, matured) correctly instead of throwing them away. The survival curve per account is a beautiful demo visual and directly answers the "12 months in advance" phrasing.
- **Cons:** thin real-world gains over Cox/GBM binary (GBST 0.6867 vs Cox 0.6799 C-index, §2.4); harder to calibrate to bucket thresholds; scikit-survival is slower; risk-team judges are less used to C-index than Gini/KS.
- **Hackathon role:** **challenger + narrative garnish.** Primary = GBM binary classifier on "defaults within 12m"; survival model as the second engine that produces the time-to-default estimate shown on the account drill-down.

### 3.4 Sequence models (LSTM / GRU / small transformer over monthly aggregates)

- **Pros:** consume the raw 24–36-month snapshot sequence without hand-crafted trend features; can catch trajectory shapes (slow bleed vs cliff); "transformer" is demo-sexy.
- **Cons:** needs far more data than a synthetic hackathon set provides; opaque (attention ≠ explanation, and FREE-AI pushes "understandable by design"); GBMs on well-engineered trend/velocity features almost always match or beat RNNs on tabular monthly aggregates at this scale; harder to calibrate and govern.
- **Verdict:** skip as primary; at most mention as roadmap ("with 5+ years of real monthly data, a sequence encoder feeding the GBM is the natural upgrade").

### 3.5 Per-segment models + unified master scale (this IS their "hybrid interpretation" ask)

- **Design:** segment the book (e.g. manufacturing vs trading vs services; metro vs semi-urban/rural locality; CC/OD vs term loan; vintage bands). Either (a) train one pooled model with segment features + interactions, or (b) train per-segment models. Then **calibrate every segment's output onto ONE master PD scale** via per-segment isotonic regression or Platt scaling, so that "PD 8%" means the same thing for a Ludhiana textile trader and a Pune auto-component maker, while the *drivers and thresholds of stress remain segment-specific*.
- **Why this matters:** the track explicitly asks for "per segment/locality PLUS shared unified scale" — per-segment calibration onto a master scale is *precisely* the textbook solution, and knowing that term ("master scale" — the bank's internal rating grades are exactly this) signals deep domain fluency. RAG cutpoints are then set once, on the master scale, but you can *report* segment-relative percentile too ("Red for a trader; would be Amber for the manufacturing pool").
- **Practical hackathon compromise:** one pooled LightGBM (segment as categorical + interactions, more data-efficient on synthetic data) + per-segment isotonic calibration + segment-level calibration plots as proof.

### 3.6 Ensembles

- Average/stack GBM + scorecard + survival-derived 12m PD; usually +1–2 AUC points. Use only if time permits; complexity hurts the governance story. A clean champion (GBM) + challenger (scorecard, survival) framing is worth more than a stack.

### 3.7 Recommendation matrix

| Option | Discrimination | Explainability | Fit to "12m ahead" | Hackathon effort | Role |
|---|---|---|---|---|---|
| WoE-logistic scorecard | ★★★ | ★★★★★ | ★★★ | Low | Benchmark / challenger |
| LightGBM + SHAP + monotonic constraints | ★★★★★ | ★★★★ (SHAP) | ★★★★ | Low-Med | **Champion** |
| Survival (Cox / GBST) | ★★★★ | ★★★ | ★★★★★ (time-to-default) | Med | Challenger + drill-down visual |
| LSTM/transformer | ★★★★? | ★★ | ★★★ | High | Roadmap slide only |
| Per-segment + master-scale calibration | — (layer) | ★★★★★ | — | Low | **Mandatory layer** (their hybrid ask) |

---

## 4. Features — the heart of the build

### 4.1 Internal bank data (structured) — behaviour of the account itself

These mirror the RBI EWS list (§1.2), which is deliberate — every feature can cite its EWS ancestor:

| Feature family | Concrete features (monthly, point-in-time) |
|---|---|
| **Limit utilization** | CC/OD utilization level; 3m/6m utilization trend & volatility; days-at-max-limit; overlimit count; ad-hoc limit requests |
| **Repayment conduct** | Current DPD; max DPD in 3/6/12m; SMA-0/1/2 flag history; count of SMA episodes; months since last delinquency; interest-servicing delay days (interest debited vs serviced gap) |
| **Cheque / mandate bounces** | Outward cheque bounces (issued by borrower, technical vs financial); **inward cheque returns** (received by borrower — their customers failing = demand-side stress); NACH/ECS mandate failures; bounce trend |
| **Account turnover** | Credit summation vs sanctioned assumption; credit-turnover 3m/6m decline %; turnover-to-limit ratio; cash-withdrawal share; sudden RTGS to unrelated/new counterparties (EWS signal) |
| **Balance behaviour** | Min-balance breaches; average balance erosion; end-of-day negative/near-limit days; quick-succession deposit-withdrawal (round-tripping) |
| **Trade-finance conduct** | LC devolvement count; BG invocation; bill discounting overdues; stock-statement submission delays (days late); insurance lapse on collateral |
| **Relationship** | Vintage on book (their factor); number of facilities; collateral coverage drift; renewals overdue; concessions/restructuring history |
| **Borrower profile** (their listed factors) | Occupation/industry code, promoter experience years, qualification, age group, entity type, locality/branch geography — *static features; keep them but show SHAP proves conduct dominates demographics; also run a fairness check on age (FREE-AI fairness sutra)* |

### 4.2 Behavioural transaction features (velocity & network)

- Transaction velocity: counts/amounts per week, change vs trailing 6m baseline; sudden dormancy.
- **Counterparty concentration:** Herfindahl of inflows by counterparty; loss of top-1/top-3 customers (inflow from a GSTIN/account that used to be ≥20% of credits going to zero is a classic pre-default event).
- **Delayed salary payments to employees:** salary-batch date drift (paid on 1st → 9th → 15th), shrinking salary batch size (headcount cuts) — a strong, intuitive stress tell that also demos well.
- Supplier-payment stretching (payables ageing proxy from payment patterns), tax-payment (GST challan) skips from the bank account, EMI payments to *other* lenders visible in the account (cross-default early sign).
- Round-tripping / circular transfers among related accounts (EWS-fraud overlap).
- These transaction-level warning patterns are documented vendor practice ([Precisa: transaction patterns that precede default](https://precisa.in/blog/early-warning-signals-bank-statements/)).

### 4.3 Public-domain data (structured + unstructured) — the differentiator

| Source | Signal | Notes / citations |
|---|---|---|
| **GSTN (consented, via Account Aggregator or borrower OTP)** | GSTR-3B/GSTR-1 filing delays & misses; declining output tax vs flat turnover; credit-note spikes; supplier/customer GSTIN network shifts; bank-declared vs GST turnover mismatch | ML on GST compliance trends flags stress "months before default" ([Bankopedia](https://www.bankopedia.co.in/banking/gst-data-in-msme-lending-credit-decisioning); [IRIS MSME](https://www.irismsme.com/blog/how-gst-data-can-power-lending-for-msmes-in-india/); [FinBox](https://www.finbox.in/blog/gst-invoices-alternate-data-and-cash-flow-underwriting-how-to-unlock-the-400-bn-msme-financing-opportunity)) |
| **MCA21** | Annual-return/financial-statement filing lapses; charge creation by other lenders (new borrowing!); director resignations/DIN changes; auditor resignation | MCA filings + promoter-linked patterns surface risk earlier than financials ([Technowire on MSME BI gaps](https://blog.technowire.in/why-90-of-business-intelligence-platforms-miss-msme-lending-data-and-how-technowire-solves-it) — note: MCA covers only companies; most MSMEs are proprietorships, so treat as available-when-available) |
| **e-Courts / NCLT / SEBI / DRT** | New suits vs borrower (cheque-bounce 138 NI Act cases are gold), NCLT petitions, recovery suits, arbitration | Real-time court-case tracking is standard in commercial EWS products ([Crediwatch](https://about.crediwatch.com/about/product/early-warning-systems)) |
| **EPFO** | PF payment lapses / delayed ECR filings → payroll stress | Public establishment-level payment status; same "salary delay" logic as §4.2 |
| **Adverse media / news** | LLM-scored negative-news sentiment: fire/strike at plant, promoter fraud allegations, key-customer loss, sector news | Classic EWS component; in the demo, run an LLM over synthetic news snippets → structured `adverse_media_score` with quoted evidence |
| **Sector / macro overlays** | Commodity price stress for the borrower's input/output (e.g. steel, cotton, crude), sector NPA trend, district-level economic stress | Justifies the "locality" dimension of their hybrid ask; enter as segment-level features |
| **Bureau (CIBIL MSME Rank etc.)** | Commercial bureau score/rank, enquiries spike (shopping for credit), overdues with other lenders | Mention as production integration; simulate in synthetic data |

### 4.4 LLM-extracted signals from unstructured internal text (synthetic)

- Sources: **banker call memos, branch inspection/stock-audit notes, relationship-manager visit reports, customer emails**. Generate synthetic memos ("Unit visit 12/03: second shift discontinued, ~30% raw-material inventory vs last visit, promoter mentioned delayed payments from anchor buyer...").
- Pipeline: LLM (structured-output prompt) → fixed taxonomy of extracted flags (`capacity_underutilization`, `key_customer_stress`, `promoter_health`, `inventory_drawdown`, `diversion_suspicion`...) with severity + verbatim evidence quote → these become model features AND display as "what the field already knew" on the drill-down.
- **Why this wins:** it's the cleanest possible demo of "structured + unstructured fusion", it keeps the human visible (the memo was written by an officer; the LLM only structures it), and evidence-quoted extraction satisfies FREE-AI explainability expectations. Guardrail to state: LLM output is a *feature*, never the decision; hallucination risk contained by quote-grounding + officer confirmation.

---

## 5. Regulatory & governance — the differentiator most teams will skip

### 5.1 RBI draft circular on Model Risk Management in Credit (5 Aug 2024)

"Regulatory Principles for Management of Model Risks in Credit" ([draft circular PDF](https://www.fidcindia.org.in/wp-content/uploads/2024/08/RBI-DRAFT-MANAGEMENT-OF-MODEL-RISK-IN-CREDIT-05-08-24.pdf); [Lexology summary](https://www.lexology.com/library/detail.aspx?g=2e3e5197-a3ec-4b08-9048-8c70dfd82be4); [Enterslice analysis](https://enterslice.com/learning/rbi-new-guidelines-model-risk-management-credit/)) requires regulated entities to:

- have a **board-approved model governance policy** covering the whole model lifecycle;
- run **independent validation** before deployment and after material changes — assumptions review, data-accuracy verification, **back-testing**, with results reported to the board's Risk Management Committee;
- document every model (purpose, data, methodology, limitations) — including **third-party/vendor models**, which RBI may have externally validated;
- validate existing models within six months of the circular taking effect.

**Deliverable idea:** ship a 2-page **"Model Card + Validation Report"** with the hackathon submission (purpose, data lineage, performance by segment, calibration plots, stability tests, limitations, monitoring plan). Judges from a bank's risk function will recognise the artifact instantly.

### 5.2 RBI FREE-AI framework (13 Aug 2025)

The **Framework for Responsible and Ethical Enablement of AI** — committee report published 13 Aug 2025, 7 "Sutras" and 26 recommendations across 6 pillars ([full report, RBI](https://rbidocs.rbi.org.in/rdocs/PublicationReport/Pdfs/FREEAIR130820250A24FF2D4578453F824C72ED9F5D5851.PDF); [KPMG summary](https://kpmg.com/in/en/insights/2025/08/rbi-free-ai-committee-report-on-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence.html); [Dvara Research summary](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/)). Sutras to name-check and how our design satisfies each:

| Sutra | Our design answer |
|---|---|
| Trust is the foundation | calibrated PDs, validation report, backtesting |
| People first | officer overrides the RAG; alert queue, not auto-action |
| Fairness & equity | fairness audit on age-group/locality features; document any exclusions |
| Accountability | human sign-off on Red actions; audit log of overrides |
| **Understandable by design** | SHAP reason codes rendered in loan-officer language, not feature names |
| Safety, resilience, sustainability | PSI/CSI drift monitors, champion–challenger, kill-switch to rule-based fallback |
| Innovation over restraint | proportionate: model *prioritises* attention; credit decisions stay with humans |

The report recommends **proportionate regulation** — stricter scrutiny for high-risk AI uses. A PD model that only routes monitoring attention (human in the loop) sits in a lower risk tier than auto-decisioning — say this explicitly.

### 5.3 Ongoing governance mechanics (weave into architecture slide)

- **Champion–challenger:** LightGBM champion vs WoE-scorecard + survival challengers, evaluated quarterly on fresh outcomomes; promotion criteria pre-defined.
- **Backtesting:** every month, score-at-T vs realised default in (T, T+12]; rolling Gini/KS/capture; calibration backtest per RAG bucket (did ~2% of Greens really slip?).
- **Stability monitoring:** **PSI** on score distribution, **CSI** on each feature, alert at PSI > 0.1, retrain/investigate at > 0.25.
- **Override analytics:** track officer agree/disagree on RAG flags; systematic overrides in a segment = model weakness signal — this closes the human-in-the-loop feedback circle the track demands.

---

## 6. Concrete hackathon architecture

### 6.1 Pipeline (buildable in a hackathon weekend)

```
[Synthetic Loan-Book Generator]                       [Unstructured Lane]
  5–10k MSME accounts ──► 24–36 monthly snapshots       synthetic call memos / news /
  per account, injected stress trajectories             GST-filing events
        │                                                     │ LLM extractor (structured
        ▼                                                     ▼  JSON w/ evidence quotes)
[Point-in-Time Feature Store]  ◄──────────────────────  flag features
  features use ONLY data ≤ T; label = NPA in (T, T+12]
        │
        ▼
[Models]  LightGBM champion (class-weighted, monotonic constraints)
          + WoE-logistic challenger + Cox/GBST survival challenger
        │
        ▼
[Per-segment Isotonic Calibration → Unified Master Scale (PD grades 1–10)]
        │
        ▼
[RAG Bucketing]  Green / Amber / Red thresholds on calibrated PD
        │
        ▼
[Loan-Officer Dashboard + Alert Queue + Feedback Loop]
```

### 6.2 Synthetic loan-book generator (the foundation — invest here)

- 5–10k accounts × 24–36 monthly snapshots. Segments: industry (manufacturing/trading/services/agro), locality (metro/semi-urban/rural), facility (CC/OD/term), vintage, plus the brief's borrower factors (occupation, experience, qualification, age group).
- **Trajectory archetypes:** (a) healthy-stable; (b) healthy-growing; (c) **slow-bleed defaulter** — utilization creeps to 100%, turnover −5%/month, bounces appear ~m-9, GST filing slips ~m-7, salary delays ~m-5, SMA-1 ~m-3, NPA at m-0; (d) **cliff defaulter** — key-customer loss event, inflow concentration collapse, rapid 4-month slide; (e) **stressed-but-recovers** (crucial! prevents the model from being trivially perfect and makes the Amber bucket meaningful); (f) seasonal businesses (so naive rules false-alarm on them but the model doesn't — a great demo beat).
- Default rate ~5–8% annualized. Add noise, missingness (GST consent absent for 30%, memos for 20%). **Keep the generator's stress logic hidden from the feature engineer** (two-notebook discipline) so results stay honest; disclose in the write-up that data is synthetic and metrics demonstrate methodology, not production performance — judges will respect the honesty.
- Backup: splice in the organisers' provided synthetic MSME/transaction datasets ([Hack2skill event page](https://hack2skill.com/event/idbinnovate)).

### 6.3 Point-in-time correctness (leakage is the #1 credibility killer)

- Every feature at snapshot T computed strictly from data ≤ T (trailing windows: 1/3/6/12m).
- Label: first NPA event in (T, T+12]. Accounts already NPA at T excluded; closed/prepaid handled as censored (for survival lane) or excluded-after-exit (binary lane).
- **Out-of-time validation split** (train on snapshots ≤ month 24, test on months 25–36), not random row split — random splits leak the same account across train/test. Also group-split by account ID. Saying "out-of-time, out-of-sample" in the demo is another credibility marker.
- No post-outcome fields (no "provision amount", no restructuring flags dated after T).

### 6.4 RAG thresholds & the officer-facing layer

- Buckets on calibrated PD, e.g. Green < 4%, Amber 4–15%, Red > 15% — but make thresholds a **policy dial**, and show both options: fixed-PD thresholds (stable meaning; bucket sizes float) vs portfolio-quantile (fixed workload; meaning floats) — see §7.4. Recommend fixed-PD for meaning + a workload cap for the alert queue (hybrid).
- **Dashboard (the demo centerpiece):**
  1. **Portfolio heat-map:** branch/segment/locality grid coloured by Red-share and RAG-migration arrows month-over-month.
  2. **Account drill-down:** RAG badge + calibrated 12m PD + *expected time-to-default* (survival lane); **SHAP waterfall translated to loan-officer sentences** ("Top drivers: limit utilization above 95% for 4 straight months (+), 3 inward cheque returns last quarter (+), GSTR-3B late twice (+), promoter vintage 12 years (−)"); **trend sparklines** (utilization, turnover, bounces, balance); unstructured evidence panel (memo quotes, news snippet); **recommended action** (rule-mapped: Red → unit visit + stock audit + limit review within 15 days; Amber → enhanced monitoring, GST re-pull; Green → routine).
  3. **Alert queue:** Red/Amber worklist sorted by PD × exposure (₹-weighted triage — bank thinking), with officer actions: Acknowledge / Investigate / Override-with-reason. Overrides feed the retraining set (§5.3) — the feedback loop the brief demands.
  4. **Model-health tab:** gain chart with alert-budget slider, calibration curve, PSI monitor — governance made visible.

### 6.5 Suggested stack

Python: `pandas`/`polars`, `lightgbm`, `scikit-learn` (isotonic calibration), `scikit-survival` or `lifelines`, `shap`; dashboard in Streamlit (fastest) or a React front-end if the team has one; LLM extraction via any available API with JSON-schema output; everything runs local/laptop — no infra risk on demo day.

---

## 7. Pros/cons decision tables

### 7.1 Survival analysis vs binary 12-month classification

| | Binary (default within 12m) | Survival (time-to-default) |
|---|---|---|
| Direct answer to brief | ✔ exactly the IFRS-9 12m PD | ✔✔ gives PD at *every* horizon + expected time-to-default |
| Censoring handling | crude (drop/ignore) | ✔ principled |
| Tooling/speed | ✔✔ trivial (LightGBM) | slower, niche libs |
| Calibration to buckets | ✔ standard (isotonic) | harder |
| Judge familiarity (Gini/KS) | ✔✔ | C-index less familiar |
| Evidence of gain | — | thin: GBST C-index 0.6867 vs Cox 0.6799 ([arXiv:1908.03385](https://arxiv.org/abs/1908.03385)); RSF lost to logit OOS ([Fantazzini & Figini](https://www.researchgate.net/publication/225101879_Random_Survival_Forests_Models_for_SME_Credit_Risk_Measurement)) |
| **Verdict** | **Champion** | Challenger + "months-to-stress" display feature |

### 7.2 Per-segment models vs pooled model

| | Pooled (one model, segment features) | Per-segment models |
|---|---|---|
| Data efficiency | ✔✔ (crucial on hackathon-scale data) | thin segments overfit |
| Segment-specific drivers | via interactions/SHAP-by-segment | ✔ explicit |
| Maintenance/governance | 1 model to validate | N models to validate |
| Brief's "hybrid" ask | needs added layer | natural, but scales badly |
| **Verdict** | **Pooled GBM + per-segment isotonic calibration onto one master scale** = hybrid ask satisfied with pooled robustness | use only for 2–3 fat segments if time allows |

### 7.3 LLM/unstructured signals vs structured-only

| | Structured-only | + LLM unstructured lane |
|---|---|---|
| Reliability/reproducibility | ✔✔ | LLM variance; mitigate w/ fixed taxonomy + quotes |
| Lift | high already (conduct data dominates) | incremental, but earliest signals (memos/news often precede numbers) |
| Track-brief compliance | ✗ brief *explicitly requires* unstructured | ✔ |
| Demo wow-factor | low | ✔✔ memo → flag → SHAP contribution on screen |
| Governance | simple | needs "feature-not-decision" guardrail (state it) |
| **Verdict** | insufficient for this track | **Include, scoped: 4–6 flag types, evidence-grounded** |

### 7.4 Fixed RAG thresholds vs portfolio-quantile thresholds

| | Fixed calibrated-PD thresholds | Portfolio-quantile (top-k%) |
|---|---|---|
| Meaning of "Red" | stable ("PD > 15%") — audit-friendly, ECL-consistent | drifts with portfolio mix |
| Officer workload | floats with the cycle (Red bucket can explode in a downturn) | ✔ fixed, plannable |
| Downturn behaviour | honestly reports more Reds | masks systemic deterioration (always 10% Red) |
| Regulatory fit | ✔ maps to SICR/staging logic | weak |
| **Verdict** | **Primary: fixed PD cutpoints** | overlay a workload cap on the *queue*, and show portfolio-level Red-share as the macro dial |

---

## 8. Winning strategy & demo script

### 8.1 Strategy — five judge-facing differentiators

1. **Speak risk-team language:** SMA ladder, IFRS-9/Ind AS 109 12-month PD & SICR staging, EWS/RFA, Gini/KS/capture, master scale, champion–challenger, PSI. Every term above is standard at a bank; most hackathon teams will say "accuracy" and "AI".
2. **Honestly kill the 90% number, then beat it on the metric that matters** (§2.5). Rehearse the reframe; deliver it early, respectfully ("we assume 16–22% refers to alert hit-rate — here's why, and here's the curve that fixes it").
3. **Dual-use economics:** same model = EWS alerts + Ind AS 109 staging input + collections triage. One build, three consumers.
4. **Governance-in-the-box:** model card, validation report, monitoring tab — aligned to the Aug-2024 model-risk draft and FREE-AI. Human-in-the-loop is architected (override queue + feedback retraining), not asserted.
5. **The unstructured lane with receipts:** live demo of a banker memo + a GST filing lapse becoming quantified SHAP contributions on a real account screen.

### 8.2 Demo script (~6–7 minutes)

1. **(45s) Problem re-frame:** "Your EWS flags fire at SMA-1 — too late — and only ~1 in 5 flags is real. We move detection 12 months earlier and put most future defaulters inside a Red bucket small enough to work."
2. **(60s) Portfolio heat-map:** open dashboard on the whole synthetic book; point at a semi-urban trading cluster turning Amber; month-slider shows RAG migration over time.
3. **(2 min) Account drill-down — the hero moment:** pick "Sharda Fabricators" (slow-bleed archetype). Today: fully regular, zero DPD, Green on the bank's current rules. Our model: **Red, PD 22%, est. 8 months to stress.** Walk the SHAP waterfall in plain words; show sparklines (utilization ↑, turnover ↓, salary-batch drift); show the memo quote + late GSTR-3B in the evidence panel. Then hit "fast-forward": the synthetic future shows the account hitting SMA-2 seven months later. "We flagged it while every existing rule said Green."
4. **(60s) Contrast account:** seasonal business the *rule engine* flags (turnover dip) but our model keeps Green (seasonality recognised) → "fewer false alarms, not just more alerts."
5. **(60s) Numbers slide:** out-of-time gain chart — "at a 20%-of-book alert budget: ~85–90% capture of 12-month defaulters, ~4× lift; vs the incumbent's 16–22% hit-rate at similar workload"; calibration curve; champion-vs-challenger table.
6. **(45s) Human-in-the-loop + governance:** officer overrides a Red with reason → lands in the feedback log; flash the model card and PSI monitor. Close: "Explainable by design, governed by default — FREE-AI-ready."
7. **(15s) Roadmap:** Account Aggregator GST pulls, bureau feed, sequence encoder as data deepens; per-segment sub-models for the two largest segments.

### 8.3 Anticipated judge questions (prepare answers)

- *"How do you know it works on real data?"* → "Metrics on synthetic data prove the methodology, not production performance. The pipeline is point-in-time correct and validation-ready; on real data we'd expect AUC in the published SME range 0.75–0.85+, and we'd calibrate to your realised default rates."
- *"Why not deep learning?"* → GBM ≥ deep nets on tabular at this scale; explainability + model-risk validation cost; cite the RSF/logit out-of-sample result and the thin GBST-over-Cox margin.
- *"What about consent/privacy for GST/EPFO?"* → GST via borrower-consented Account Aggregator pulls (established practice — [Bankopedia](https://www.bankopedia.co.in/banking/gst-data-in-msme-lending-credit-decisioning)); EPFO/MCA/e-courts are public-domain; adverse media is public. DPDP-compliant by design; purpose-limited features.
- *"Age group as a factor — is that fair?"* → We test it: fairness audit per FREE-AI's Fairness sutra; if disparate impact appears we drop/constrain it — conduct features carry the model anyway.

---

## Source index

**Regulatory**
- RBI, Framework for dealing with loan frauds (7 May 2015): https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=9713&Mode=0 · full PDF: https://cvc.gov.in/files/vigilance-manual-pdf/vm21ch8/vm17ch8/8.%20RBI_2014-15_590-DBS.CO.CFMC.BC.No.00723.04.0012014-15%20dated%2007.05.2015.PDF
- RBI, Early Warning Signals notification: https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=9878&Mode=0 · 45-signal list: https://bankingschool.co.in/bank-news/rbi-releases-45-early-warning-signals-about-wrongdoingsfrauds-in-loan-accounts/ · https://taxguru.in/rbi/early-warning-signals-red-flag-accounts.html · KPMG: https://assets.kpmg.com/content/dam/kpmg/pdf/2015/06/Framework-Loan-fraud.pdf
- RBI Master Directions on Fraud Risk Management (Jul 2024): https://elplaw.in/wp-content/uploads/2024/07/RBI-Revised-Master-Directions-on-Fraud-Risk-Management-July-2024.pdf · https://vinodkothari.com/wp-content/uploads/2024/07/FRM.pdf · https://pirimidtech.com/what-is-ews-and-what-does-rbis-fraud-risk-management-direction-mean-for-financial-institutions/
- RBI IRACP/SMA clarification (12 Nov 2021): https://webassets.rbl.bank.in/document/pdfs/prudential-norms-iracp.pdf · https://satincreditcare.com/wp-content/uploads/2021/12/Guidelines-on-Income-Recognition-Asset-Classification-and-Provisioning.pdf
- IFRS 9 / ECL: BIS FSI summary https://www.bis.org/fsi/fsisummaries/ifrs9.pdf · PwC SICR in-depth https://www.pwc.com/hu/hu/szolgaltatasok/ifrs/ifrs_9/ifrs9_kiadvanyok/ifrs_9_impairment_significant_increase_in_credit_risk.pdf · IAI Ind AS 109 note https://actuariesindia.org/sites/default/files/inline-files/Expected%20Credit%20Loss%20Framework%20Under%20IND%20AS109.pdf
- RBI draft Model Risk in Credit circular (5 Aug 2024): https://www.fidcindia.org.in/wp-content/uploads/2024/08/RBI-DRAFT-MANAGEMENT-OF-MODEL-RISK-IN-CREDIT-05-08-24.pdf · https://www.lexology.com/library/detail.aspx?g=2e3e5197-a3ec-4b08-9048-8c70dfd82be4 · https://enterslice.com/learning/rbi-new-guidelines-model-risk-management-credit/
- RBI FREE-AI report (13 Aug 2025): https://rbidocs.rbi.org.in/rdocs/PublicationReport/Pdfs/FREEAIR130820250A24FF2D4578453F824C72ED9F5D5851.PDF · KPMG https://kpmg.com/in/en/insights/2025/08/rbi-free-ai-committee-report-on-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence.html · Dvara https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/

**Modelling literature**
- GBST credit-scoring survival paper (Lending Club, 224k loans): https://arxiv.org/abs/1908.03385 · https://crc.business-school.ed.ac.uk/sites/crc/files/2020-10/J35-Gradient-Boosting-Survival-Tree-with-Applications-in-Credit-Scoring-Bai-2.pdf
- Fantazzini & Figini, RSF for SME credit risk (logit wins out-of-sample): https://www.researchgate.net/publication/225101879_Random_Survival_Forests_Models_for_SME_Credit_Risk_Measurement
- SME default prediction — systematic methodology review: https://www.researchgate.net/publication/376363979_SME_default_prediction_A_systematic_methodology-focused_review
- German SME RF with non-financial features: https://www.researchgate.net/publication/372906738_SME_default_prediction_using_random_forest_including_nonfinancial_features_An_empiricial_analysis_of_German_enterprises
- ML false-positive suppression on rule-based bank monitoring: https://link.springer.com/article/10.1007/s11227-023-05708-z · https://www.sciencedirect.com/science/article/abs/pii/S016740482200181X

**Data & market practice**
- Crediwatch EWS (12-month lead, 200+ alerts; SBI/IndusInd clients): https://about.crediwatch.com/about/product/early-warning-systems
- GST data in MSME lending: https://www.bankopedia.co.in/banking/gst-data-in-msme-lending-credit-decisioning · https://www.irismsme.com/blog/how-gst-data-can-power-lending-for-msmes-in-india/ · https://www.finbox.in/blog/gst-invoices-alternate-data-and-cash-flow-underwriting-how-to-unlock-the-400-bn-msme-financing-opportunity
- Bank-statement EWS patterns: https://precisa.in/blog/early-warning-signals-bank-statements/
- MSME data-coverage gaps (MCA vs proprietorships): https://blog.technowire.in/why-90-of-business-intelligence-platforms-miss-msme-lending-data-and-how-technowire-solves-it

**Hackathon**
- IDBI Innovate 2026: https://hack2skill.com/event/idbinnovate · https://www.idbi.bank.in/press/PR1463.pdf · https://www.bizzbuzz.news/banking/idbi-innovate-2026-hackathon-1394096

