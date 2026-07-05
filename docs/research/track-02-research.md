# Track 2 — Prospect Assist AI: Research Dossier
### Data-driven lead generation for retail lending (Personal / Home / Mortgage-LAP / Auto)

> **Problem restated:** IDBI converts ~1% of retail-lending leads today; target is >30%. For every prospect answer two questions — (1) is this person genuinely **interested** right now, and (2) do they have real **repayment capacity**? Work off the bank's transaction/statement sandbox DB. Go beyond FOIR: derive behaviour from spending, predict delinquency *before* it happens, separate window-shoppers from serious buyers, and handle salaried vs gig/self-employed differently. Core deliverable = a **model of customer behaviour** that drives lead and credit decisions.

---

## 1. Domain landscape: propensity modelling for cross-sell in Indian banking

### 1.1 Who does this today (vendor/case-study map)

| Player | What they do | Relevance to Track 2 |
|---|---|---|
| **TransOrg Analytics** | Built personal-loan propensity models for a leading Indian fintech — identify "loan-ready" customers from behavioural data to improve targeting and uptake ([case study](https://www.transorg.ai/case-study/predicting-customer-propensity-for-personal-loans-at-a-leading-fintech-company/)) | Direct template: propensity score on existing-customer base |
| **Valiance Solutions** | Risk-augmented personal-loan cross-sell: overlay **cross-sell propensity × delinquency-risk** models; campaign delivered **~10% higher conversion vs baseline and 10–20% higher ticket size** ([case study](https://valiancesolutions.com/case_study/risk-augmented-personal-loan-cross-sell/)) | Proof that the two-model (interest × risk) fusion is the industry pattern — exactly the track's two questions |
| **Lentra** | Cloud lending platform (used by HDFC, Federal, etc.); loan origination + "merchants as cross-sell agents" ([lentra.ai](https://lentra.ai/)) | Shows where a lead-gen model plugs into an LOS |
| **CreditVidya** (acq. by CRED) | Alternative-data underwriting: **10,000+ data points, claims 2× the power of bureau scores, underwrites ~15% more individuals** — thin-file/new-to-credit focus ([creditvidya.com](https://creditvidya.com/)) | The "beyond-FOIR / beyond-bureau" precedent in India |
| **Prism Data** (US analogue) | **CashScore** — default probability from *deposit-account* data alone; "as predictive as traditional scores standalone, orthogonal in combination"; detects gig income & transfers ([prismdata.com](https://www.prismdata.com/), [income product](https://www.prismdata.com/income/), [Giggle Finance case](https://www.prismdata.com/blog/giggle-finance-selects-prism-data-to-strengthen-cash-flow-underwriting/)) | Blueprint for the Capacity model: transaction-only credit signal |
| **Perfios** | India's largest financial-data platform; bank-statement analyser used by HDFC/ICICI/Axis/SBI + 900+ fintechs; auto-detects salary, business income, EMIs, fraud; 4,000+ statement formats ([perfios.com BSA](https://www.perfios.com/solutions/bank-statement-analyzer), [review](https://productgrowth.in/tools/banking-api/perfios/)) | Feature-extraction reference: what fields a production BSA emits |
| **FinBox** | BankConnect statement analyser + DeviceConnect; AA integration, fraud checks (tampering, round-tripping) ([finbox.in/bankconnect](https://www.finbox.in/products/bankconnect)) | Same; also risk-signal (not just parsing) framing |
| **Digitap** | AA + PDF-upload statement analysis, tamper detection, salary & SME underwriting dashboards ([tool comparison](https://hyperverge.co/blog/bank-statement-analysis-software/)) | Same |
| **Setu (Pine Labs)** | Account Aggregator APIs — consent screen, encrypted fetch from bank, returns clean JSON of statements ([setu.co AA](https://setu.co/data/financial-data-apis/account-aggregator/)) | The *legal rail* for getting statement data with consent — name-drop this in the demo for realism |
| **Precisa, HyperVerge, Ocrolus** | Competing BSA tools; 2026 comparisons stress tools that return **risk signals (income, cash flow, EMIs, fraud flags), not just extracted data** ([HyperVerge comparison](https://hyperverge.co/blog/bank-statement-analysis-software/), [Precisa vs FinBox](https://precisa.in/blog/precisa-vs-finbox-bank-statement-analysis-tool/)) | Positions your deliverable: signals > parsing |

### 1.2 What "1% → 30%" realistically means (critical framing for judges)

- **Cold-base reality:** untargeted cross-sell campaigns in banking convert ~1–3%. Published propensity case studies show *relative* lifts, e.g. Valiance's **+10% conversion vs prior-campaign baseline** with better ticket sizes ([source](https://valiancesolutions.com/case_study/risk-augmented-personal-loan-cross-sell/)); vendor literature commonly claims 2–5× lift from propensity targeting ([Pecan AI overview](https://www.pecan.ai/blog/predictive-cross-sell-upsell-strategies/)).
- **No model converts a random base at 30%.** The honest interpretation: >30% conversion **on the qualified lead list you hand the RM** — i.e., this is a **precision@k problem**, not a base-rate problem. If the top decile of a well-calibrated propensity×capacity score contains most true converters, 30%+ conversion on that decile is achievable, especially when leads are **pre-approved-eligible** (pre-qualified offers convert at 20–40% in industry practice because risk rejection is removed *before* contact).
- **Frame it as funnel re-engineering:** same base, but the bank only *spends contact effort* on scored-and-pre-screened leads. Conversion@contacted rises 30×; the model's job is to make the numerator dense.
- Academic backing that cross-sell follows a **sequential product ladder** (customers acquire products in a predictable order — savings → card → personal loan → auto → home), so "next product to buy" is learnable ([Cross-Selling Sequentially Ordered Products](https://www.researchgate.net/publication/242537131_Cross-Selling_Sequentially_Ordered_Products_An_Application_To_Consumer_Banking_Services); [Review of Financial Studies on cross-selling mechanisms](https://academic.oup.com/rfs/advance-article/doi/10.1093/rfs/hhad062/7241521)).

---

## 2. Techniques

### 2.1 Transaction categorization (need / want / luxury)

- **MCC codes** (ISO 18245, 4-digit) are the classical layer — see the [Citi MCC list](https://www.citibank.com/tts/solutions/commercial-cards/assets/docs/govt/Merchant-Category-Codes.pdf) and [Cashfree's India-context MCC guide](https://www.cashfree.com/blog/merchant-category-code-mcc-meaning-list-examples/). But MCCs alone are weak: they were never designed for categorisation, they describe the *merchant type not the purchase intent*, and P2P UPI has no MCC at all ([Tapix: why MCC codes don't help much](https://www.tapix.io/resources/post/why-mcc-codes-do-not-help-much-with-payment-categorization); [Finextra: beyond MCC codes](https://www.finextra.com/blogposting/31935/beyond-mcc-codes-why-transaction-categorisation-is-becoming-core-banking-infrastructure)).
- **Production pattern = layered rule + ML hybrid:** (1) exact merchant dictionary (e.g., `swiggy`, `zerodha`, `lic` in narration/VPA), (2) UPI **VPA parsing** — the handle (`merchant@ybl`, `9198...@paytm`) distinguishes P2M vs P2P and often names the merchant, (3) regex on narration tokens (`NEFT-SALARY`, `ACH-EMI`, `RENT`), (4) ML classifier (char-n-gram TF-IDF + LightGBM, or a small fine-tuned transformer) for the residual, (5) **LLM as categorizer** for long-tail narrations — modern option, great demo value, but pair it with a cache + rules so it's cheap and deterministic. Best-in-class systems categorize four layers deep: category → subcategory → merchant → item ([Finextra](https://www.finextra.com/blogposting/31935/beyond-mcc-codes-why-transaction-categorisation-is-becoming-core-banking-infrastructure)).
- **Need/Want/Luxury mapping** sits *on top of* category: rent/utilities/groceries/school-fees/insurance/EMIs = **need**; dining/OTT/travel/shopping = **want**; luxury retail, premium electronics, frequent fine dining, business-class travel = **luxury**. This split is your **discretionary-income lens**: `real disposable income = inflows − needs − committed obligations`, with wants/luxury as compressible spend that signals lifestyle headroom (and, if growing while balance shrinks, stress).

### 2.2 Income estimation from bank statements

- **Salary detection (salaried persona):** recurring credit, similar amount (±10%), fixed day-of-month window (25th–5th), narration keywords (`SAL`, `SALARY`, employer name via NEFT/ACH). Perfios and peers detect salary/business/investment income automatically ([Perfios BSA](https://www.perfios.com/solutions/bank-statement-analyzer)).
- **Gig income (Swiggy/Zomato/Uber/Ola/Urban Company):** *many small credits, weekly/daily cadence, platform VPAs/narrations* (`SWIGGY`, `ZOMATO PAYOUT`, `UBER BV`). Underwrite on **rolling 3–6-month average + volatility (CV of weekly income)** rather than last-month income. Prism Data explicitly "uncovers gig work, regular transfers, and other income sources beyond just the paycheck" ([Prism Income](https://www.prismdata.com/income/)); Indian fintechs (CASHe, KreditBee, etc.) already lend to gig workers on 3–6 months of statements with min ₹15–20k average monthly inflow instead of ITRs ([TapTap Loans overview](https://www.taptaploans.in/blog/personal-loan-without-income-proof-india/)).
- **Self-employed:** UPI P2M inflows ≈ turnover proxy → apply **industry gross-margin priors** (kirana ~8–12%, restaurant ~30–40%, services ~50%+) keyed off inferred business type (from counterparty mix, supply-side debits like wholesalers) → estimated net income. This is exactly the track's "industry margins + UPI turnover" hint; defend margin priors as a lookup table you'd calibrate from RBI/industry data in production.
- **Cash-flow underwriting** as the umbrella doctrine: analyse actual inflows/outflows, savings buffer, recurring obligations — complements bureau data and reaches thin-file/gig borrowers ([Plaid cash-flow underwriting](https://plaid.com/resources/lending/cash-flow-underwriting/), [LoanPro implementation guide](https://www.loanpro.io/blog/what-lenders-need-to-know-about-implementing-cash-flow-underwriting-in-2026/)).

### 2.3 FOIR vs cash-flow-based underwriting

- **FOIR** (Fixed Obligation to Income Ratio) = EMIs ÷ monthly income; the central Indian retail metric, typically capped ~40–55% ([FOIR explainer](https://www.techfinserv.com/blogs/foir-uw/); [Precisa on Indian underwriting stages](https://precisa.in/blog/credit-underwriting-process-india/)).
- **FOIR's blind spots** (say this verbatim to judges): (a) treats declared income as truth, (b) ignores *where* the non-EMI money goes (a 30% FOIR customer who burns the rest on luxury + ends the month at ₹500 balance is riskier than a 45% FOIR saver), (c) fails gig/self-employed with lumpy income, (d) static — no trend.
- **Your upgrade:** FOIR stays as a guardrail, but the Capacity model uses **discretionary-surplus ratio** (income − needs − obligations)/income, **end-of-month balance trajectory**, **savings/investment rate**, **income volatility**, **bounce/penalty events** — the CashScore idea ([Prism Data](https://www.prismdata.com/)).

### 2.4 Propensity models

- Standard stack: **XGBoost/LightGBM on RFM + trigger features** — recency/frequency/monetary of category spends, product-holding vector, balance trends, channel activity, demographic slots. This is what TransOrg/Valiance-style engagements build ([TransOrg case](https://www.transorg.ai/case-study/predicting-customer-propensity-for-personal-loans-at-a-leading-fintech-company/)).
- **Trigger events** are the highest-signal features (see 2.6): propensity spikes are event-driven, not static.
- Always pair with a **risk overlay** (Valiance pattern: propensity × delinquency-risk grid → target high-propensity/low-risk cell) ([Valiance](https://valiancesolutions.com/case_study/risk-augmented-personal-loan-cross-sell/)).

### 2.5 Uplift modelling — the sophisticated angle

- Propensity ranks *who will convert*; **uplift ranks who converts because you contacted them**. Four quadrants: Sure Things, Lost Causes, Do-Not-Disturbs, **Persuadables** — only Persuadables justify contact cost ([Towards Data Science primer](https://towardsdatascience.com/why-every-marketer-should-consider-uplift-modeling-1090235572ec/); [CDP.com glossary](https://cdp.com/glossary/uplift-modeling/)).
- **Meta-learners:** T-learner = two models (treated vs control) subtracted; **X-learner** = T-learner + models on imputed treatment effects blended by propensity weights — better when treatment/control groups are imbalanced ([large-scale meta-learner comparison, arXiv](https://arxiv.org/pdf/2604.06123); [multi-treatment benchmark, Springer](https://link.springer.com/article/10.1007/s10796-022-10283-4)).
- Practical lessons: needs randomized (or quasi-random) campaign logs; evaluate with **Qini/uplift curves**, not AUC ([CMR Berkeley: five lessons from uplift in campaigns](https://cmr.berkeley.edu/2025/11/to-treat-or-not-to-treat-five-lessons-learned-from-using-uplift-modeling-to-optimize-marketing-campaigns/)).
- **Hackathon stance:** ship propensity as core (data-feasible with synthetic campaign logs), *demonstrate* uplift as the "how we actually hit 30% without spamming Do-Not-Disturbs" slide + a small T-learner on simulated treatment logs. This differentiates you from every team that stops at propensity.

### 2.6 Clickstream / digital-intent models (window-shopper vs serious buyer)

- Feature families proven in industry: session count & recency on loan pages, **time-on-page, scroll depth, EMI-calculator interactions (amount/tenure entered!), eligibility-checker starts, application-form field progress, return visits within 7 days, channel source**. Capital One publishes work on clickstream-based customer-intent prediction ([Capital One tech blog](https://www.capitalone.com/tech/software-engineering/clickstream-data-advances-in-customer-intent-prediction/)).
- "**Digital body language**" — hesitation, cognitive load, familiarity, error rate, sequence — predicts intent and separates high-intent users from window shoppers in real time ([ForMotiv](https://formotiv.com/what-is-clickstream-data-and-why-should-insurers-care/)).
- Academic result: shopper intent is predictable **from minimal early-session clickstream** (first few interactions) ([Nature Scientific Reports](https://www.nature.com/articles/s41598-020-73622-y)) — supports a real-time intent score, not just batch.
- **Window-shopper signature:** single short session, calculator with default values, no eligibility check, bounced from rates page. **Serious-buyer signature:** repeat sessions, calculator with specific amount/tenure (e.g., ₹27.5L/20yr — matches a property budget), eligibility check started, documents page viewed.

### 2.7 Life-event detection from transactions

- **75% of customers who switch primary banks do so after a material life event** (move, marriage, child) ([Deluxe life-event marketing guide](https://www.deluxe.com/resources/guide-to-life-event-triggers-for-bank-marketing/); [ProSight on trigger-based marketing](https://www.prosightfa.org/insights/trigger-based-marketing-a-powerful-tool-for-attracting-and-retaining-customers/)).
- Transaction triggers used by banks: large home-improvement purchases → HELOC/LAP campaign; baby-product purchases → family products; deposit spikes, salary jumps ([BAI trigger-based marketing](https://www.bai.org/banking-strategies/trigger-based-marketing-a-powerful-tool-for-attracting-and-retaining-customers/); [Latinia NBA examples](https://latinia.com/en/resources/examples-next-best-actions-marketing-banking); [Netguru next-best-offer from transactional data](https://www.netguru.com/blog/next-best-offer-for-fintech)).
- **India-specific trigger library to implement:** new/increased **rent debit** → home-loan intent (rent→EMI pitch: "your ₹32k rent ≈ EMI on ₹38L"); **school/college fee** debits → education-adjacent PL; **jewellery + catering/banquet + travel cluster** → marriage → PL/gold-loan; **salary jump >20%** → upgrade propensity (auto/home); **fuel + cab-spend surge** → auto-loan intent; **broker/registration fee, property-portal payments** → home loan imminent; **maternity/hospital + baby retail** → bigger-home trigger.

---

## 3. Delinquency pre-screen at the lead stage

- **Pre-approved offer logic (Indian practice):** bank runs batch eligibility on its *own* base — internal behaviour score + bureau **soft pull** — and only then surfaces an offer. Checking a customer's profile to *make* a pre-approved offer is a **soft inquiry with zero CIBIL impact**; it becomes a **hard inquiry (≈5–10 point cost, visible to lenders, ~2-year record)** only when the customer actually applies ([BankBazaar on credit inquiries](https://www.bankbazaar.com/cibil/credit-inquires.html); [HonestMoney hard-vs-soft breakdown](https://honestmoney.in/credit-score/hard-inquiry-vs-soft-inquiry-cibil-score-impact-how-to-minimize/); [Zet explainer](https://zetapp.in/blog/difference-between-soft-and-hard-enquiry-in-cibil-report)). → Your Risk pre-screen legitimately runs at lead stage without harming prospects.
- **Cross-checking multiple accounts:** bureau report (CIBIL/Experian/CRIF) gives total live tradelines + enquiries across institutions — catches EMIs invisible in the sandbox statement (obligations held at other banks). In-demo: simulate a bureau JSON per persona (score, tradelines, enquiries-last-6m, overdue flags).
- **Delinquency-before-it-happens signals from statements:** EMI bounce/penalty narrations, rising utilisation of small-ticket BNPL, cheque returns, minimum-balance charges, month-end balance trending to zero, gambling/betting app spends, cash-withdrawal spikes right after salary, borrowing-from-P2P patterns (many small P2P credits late in month). CashScore-style deposit-data default prediction is proven "as predictive as traditional scores" ([Prism Data](https://www.prismdata.com/)).
- **RBI (Digital Lending) Directions, 2025** — consolidated code effective **May 8, 2025** (multi-lender rules Nov 1, 2025; DLA reporting on CIMS from Jun 15, 2025). Key points for this track: creditworthiness assessment must at minimum capture **age, occupation, income** before approval; data collection must be **need-based, purpose-specific, consent-based, minimal**; credit-limit increases require **explicit borrower request** (no auto-enhancement); LSP marketplaces must show **unbiased digital view of all offers, no dark patterns** ([Legal500 analysis](https://www.legal500.com/developments/thought-leadership/the-rbis-digital-lending-directions-2025-a-unified-code-for-a-fragmented-sector/); [AZB & Partners note (PDF)](https://www.azbpartners.com/wp-content/uploads/2025/05/AZB-Update-Digital-Lending-Directions-2025.pdf); [Argus Partners overview](https://www.argus-p.com/updates/updates/rbi-digital-lending-directions-2025-an-overview/); [RBI FAQ](https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3413)). Design consequence: your lead engine may *rank and route*, but the offer copy must be non-deceptive, and the credit decision itself must rest on assessed income/occupation — which your Capacity model directly strengthens.

---

## 4. Privacy & regulatory (DPDP + RBI) — make this a feature, not a footnote

- **DPDP Act 2023 + DPDP Rules 2025:** marketing, **profiling, analytics and preference tracking are NOT "legitimate uses"** — they need **free, specific, informed, unconditional, unambiguous consent via clear affirmative action**, itemised per purpose ([IndusLaw sector-specific FAQs](https://cms-induslaw.com/en/ind/publication/sector-specific-faqs-on-the-digital-personal-data-protection-act-2023-dpdp-act-and-digital-personal-data-protection-rules-rules-2025); [EY DPDP guide](https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023)). Consent to *banking services* does not bleed into consent to *behavioural profiling for cross-sell* — separate toggle.
- **Timeline:** phased — consent-manager registration opens **Nov 13, 2026**; consent/notice/security obligations fully effective **May 13, 2027** ([Seclore DPDP Rules guide](https://www.seclore.com/fundamentals/dpdp-rules-2025-compliance-guide/); [CookieYes DPDPA guide](https://www.cookieyes.com/blog/india-digital-personal-data-protection-act-dpdpa/)). Penalties up to **₹250 crore** for security failures, ₹200 crore for breach-notification failures ([Mitigata summary](https://mitigata.com/blog/what-is-dpdp-rules-2025/)). A 2026 hackathon build that is *already DPDP-ready* is a selling point.
- **Children/vulnerable:** behavioural monitoring & targeted ads at children are banned outright — age-gate the profiling pipeline ([DPDPA FAQ](https://www.dpdpa.com/dpdpa-faq.html)).
- **Geolocation:** high-sensitivity signal; use **coarse geography (pincode/city from spend location)** not GPS trails; process on purpose-limited consent; aggregate before display (e.g., "shops in premium-catchment areas" not a map of movements).
- **Explainability expectation:** RBI's model-risk posture and fair-lending scrutiny push toward **reason codes for every automated decision**; SHAP on gradient-boosted models is the accepted pattern in credit scoring (AUC ~0.89–0.92 with stable explanations reported) ([SHAP-calibrated ensembles study](https://ssrpublisher.com/wp-content/uploads/2025/09/Explainable-AI-for-Credit-Scoring-with-SHAP-Calibrated-Ensembles-A-Multi-Market-Evaluation-on-Public-Lending-Data.pdf); [SHAP stability in credit risk, MDPI](https://www.mdpi.com/2227-9091/13/12/238)). Matches the hackathon's explainability + human-in-the-loop judging theme.
- **Design artefacts to show judges:** consent ledger table (purpose, timestamp, status, expiry), "profiling: ON/OFF" per customer, data-minimisation note (no raw narration leaves the feature store), audit log of who viewed which lead.

---

## 5. Concrete hackathon architecture

### 5.1 Pipeline

```
Synthetic bank-statement DB (sandbox)      Clickstream events        Bureau JSON (mock)
        │                                        │                        │
        ▼                                        ▼                        ▼
┌──────────────────────────── FEATURE STORE (DuckDB/Postgres + dbt-style SQL) ───────────────┐
│ txn categorizer (rules→ML→LLM fallback) → need/want/luxury ledger                          │
│ income engine: salary detector | gig-payout detector | UPI-turnover × margin priors        │
│ obligation engine: EMI/rent/bounce detection · FOIR · discretionary surplus · balance path │
│ trigger engine: life events (rent↑, fees, marriage cluster, salary jump, property fees)    │
│ intent features: sessions, EMI-calc params, eligibility starts, recency                    │
└──────────────┬───────────────────────┬───────────────────────┬─────────────────────────────┘
               ▼                       ▼                       ▼
   INTENT / PROPENSITY model   CAPACITY / AFFORDABILITY   RISK PRE-SCREEN
   (LightGBM: will they take   (income estimate ± band,   (PD-at-lead: bounce history,
    THIS product in 30 days;    surplus ratio, stress-     bureau mock, stress signals)
    per-product heads)          adjusted eligible EMI)
               └───────────────┬───────┴───────────────────────┘
                               ▼
                LEAD QUALITY SCORE (fusion: propensity × capacity-fit × (1−risk))
                + SHAP reason codes per lead  + product & ticket recommendation
                               ▼
        RM / BRANCH DASHBOARD: ranked lead cards · Next Best Action ·
        LLM-generated talking points in loan-officer language · feedback loop
        (accept/contact/outcome) · consent status chip · PSI monitor panel
```

### 5.2 Three-model system (keep sub-scores visible)

1. **Intent/Propensity** — LightGBM per product (PL/HL/LAP/Auto), features = RFM + triggers + clickstream; output calibrated P(apply in 30d).
2. **Capacity** — estimated monthly income (with confidence band by persona type), discretionary surplus, stress-adjusted **max eligible EMI → suggested ticket & tenure** (this makes the lead card actionable, not just a score).
3. **Risk pre-screen** — P(60+ DPD in 12m) from statement behaviour + mock bureau; hard-blocks (recent bounces, overdue tradelines) gate the lead out regardless of intent.
4. **Fusion:** `LQS = 100 × P(intent) × capacity_fit × (1 − PD)` with the three sub-scores displayed — bankers distrust opaque single numbers (see §7 table).

### 5.3 Synthetic-data plan (personas × behaviours)

- **Personas:** (a) *Salaried-stable* (fixed salary, rent, SIPs), (b) *Salaried-stressed* (rising wants, EOM balance→0, one bounce), (c) *Gig rider* (daily Swiggy/Zomato payouts, volatile weeks, fuel spends), (d) *Self-employed kirana* (high UPI P2M turnover, wholesaler debits, thin declared income), (e) *Affluent upgrader* (salary jump, property-portal + broker fees — home-loan trigger), (f) *Window-shopper* (high clickstream, weak capacity or no trigger).
- Generate 12 months × ~200–1,000 customers via a Python generator with seasonality (Diwali spike, school fees in June), narration realism (`UPI/DR/427.../swiggy@icici`, `NEFT-SAL-INFY`), and *planted ground truth* (who took a loan, who defaulted) so metrics are computable.
- **Clickstream:** two archetype generators — window-shopper (1 session, default calculator values) vs serious (3+ sessions, specific amount, eligibility start).

### 5.4 RM dashboard (human-in-the-loop)

- Ranked lead cards: name/segment, LQS + three sub-scores, top-3 SHAP reasons in plain language ("Rent ₹32k paid 14 months on time", "Surplus ₹41k/mo", "No bounces; CIBIL 771 soft-pull"), recommended product + ticket, **Next Best Action** (call script angle, best contact time), consent chip, and **RM feedback buttons** (converted / not interested / wrong number) feeding retraining — this closes the loop and is the human-in-the-loop story judges want.
- **LLM talking points:** template-grounded generation *from the SHAP features only* (no hallucinated facts), e.g., "Customer pays ₹32,000 rent — a ₹38L home loan at 8.5%/20y gives an EMI of ₹32,978; opening line: …".

---

## 6. Metrics

| Metric | Why | Demo target |
|---|---|---|
| **Precision@k / conversion@decile** | Matches "30% on the delivered list"; standard for lead lists | Top-decile precision >30% on held-out synthetic truth |
| **Uplift/Qini curve** (if uplift model shown) | Proves incremental targeting, not cherry-picking Sure Things ([CMR](https://cmr.berkeley.edu/2025/11/to-treat-or-not-to-treat-five-lessons-learned-from-using-uplift-modeling-to-optimize-marketing-campaigns/)) | Qini > random |
| **AUC / KS + calibration** per sub-model | Credit-model convention ([risk-engine MLOps guide](https://www.appitsoftware.com/blog/how-to-build-risk-scoring-engine-mlops-financial-services)) | AUC ~0.8+ on synthetic |
| **Expected-conversion simulation** | Business translation: contact top-k, apply per-lead P, show funnel 1%→33% | Interactive slider in dashboard |
| **PSI / CSI drift** | Score-distribution stability monitoring; PSI >0.2 = investigate ([Coralogix PSI primer](https://coralogix.com/ai-blog/a-practical-introduction-to-population-stability-index-psi/)) | Live PSI panel with an injected drift demo |
| **Cost per acquired loan** | Executive framing: RM hours × contact cost ÷ conversions; show 10–20× reduction | ₹-denominated before/after tile |
| **Explanation stability** | SHAP consistency across retrains builds trust ([MDPI SHAP stability](https://www.mdpi.com/2227-9091/13/12/238)) | Mention in model card |

---

## 7. Pros/cons decision tables

### Propensity-only vs Uplift
| | Propensity | Uplift (T/X-learner) |
|---|---|---|
| Pros | Simple, needs only outcome labels; well-understood; fast to build | Targets **persuadables**, cuts wasted contact & Do-Not-Disturb damage; the true path to incremental 30% ([TDS](https://towardsdatascience.com/why-every-marketer-should-consider-uplift-modeling-1090235572ec/)) |
| Cons | Wastes budget on Sure Things; can annoy Do-Not-Disturbs; conversion gains not causal | Needs randomized campaign logs; noisier; harder to explain; X-learner adds complexity ([Springer benchmark](https://link.springer.com/article/10.1007/s10796-022-10283-4)) |
| **Verdict** | Core build | Show as roadmap + toy T-learner on simulated logs |

### Rules vs ML vs LLM transaction categorization
| | Rules/dictionary | ML classifier | LLM |
|---|---|---|---|
| Pros | Deterministic, auditable, fast, free | Generalises to unseen narrations; scalable | Handles messy long-tail; zero-shot; impressive demo |
| Cons | Long-tail misses; maintenance | Needs labels; drifts | Cost, latency, non-determinism, DPDP concerns if data leaves premises |
| **Verdict** | Layer 1 (covers ~70–80%) | Layer 2 | Layer 3 fallback with cache; run small/local for privacy |

### Batch vs real-time triggers
| | Batch (nightly) | Real-time/event-driven |
|---|---|---|
| Pros | Simple, cheap, fits RM workflow | Catches EMI-calculator moment, rent-spike day; intent decays in hours ([Capital One](https://www.capitalone.com/tech/software-engineering/clickstream-data-advances-in-customer-intent-prediction/)) |
| Cons | Misses hot intent | Infra complexity; alert fatigue |
| **Verdict** | Batch for statement features; **real-time only for clickstream intent** (simulated event stream in demo) |

### Single fused score vs three visible sub-scores
| | Single LQS | Three sub-scores (+fused) |
|---|---|---|
| Pros | Simple ranking, one threshold | Explainable; RM sees *why* (interested-but-risky ≠ capable-but-cold); maps to the track's two questions; regulator-friendly |
| Cons | Opaque; hides risk/intent trade-off; hard to audit | Slightly busier UI |
| **Verdict** | Show **both**: fused for sorting, sub-scores + SHAP on the card |

---

## 8. Winning strategy for bank-executive judges + demo script

### Strategy
1. **Speak funnel economics, not ML:** open with "1% means 100 calls per loan; we make it 3 calls per loan" — cost per acquired loan is the language of a GM-Retail.
2. **Answer the track's two questions with two visible dials** (Intent, Capacity) + a risk gate — literal mapping to the problem statement wins rubric points.
3. **Explainability everywhere:** every lead has reasons a loan officer can say aloud; every decline-from-list has a reason too (fair-lending optics).
4. **Compliance as a demo moment:** click the consent chip → show DPDP purpose-wise consent ledger; mention soft-pull-only at lead stage (zero CIBIL impact) and RBI DL Directions 2025 alignment.
5. **Human-in-the-loop:** RM feedback buttons retrain the model — judges' stated theme.
6. **One sophisticated flex:** the uplift/persuadables slide — "we don't just find likely converters; we find people who convert *because we called*."

### 6-minute demo script (persona walk-through)
1. **[0:00] Hook:** funnel tile — today 10,000 leads → 100 loans; with Prospect Assist, 300 contacted → 100+ loans.
2. **[0:45] Raw statement** of *Priya, salaried-stressed→upgrader*: scroll messy narrations. Click **Categorize** → need/want/luxury ledger animates; salary auto-detected ₹95k.
3. **[1:45] Income & capacity:** disposable-surplus card: income ₹95k − needs ₹41k (incl. **rent ₹32k**) − obligations ₹6k = surplus ₹48k; stress-adjusted eligible EMI ₹33k → ₹38L home loan headroom. FOIR shown alongside — "FOIR said 6%; our surplus view says she can carry a home loan comfortably."
4. **[2:45] Intent trigger fires:** timeline shows broker-fee debit + property-portal payments + 3 sessions on home-loan page with EMI calculator set to ₹38L/20y → Intent 91. Contrast card: *Rahul the window-shopper* — one session, default calculator, Intent 22, "do not contact — nurture only."
5. **[3:45] Risk gate:** Priya — no bounces, mock CIBIL 771 (soft pull, zero score impact), one hidden EMI found via bureau cross-check at another bank → capacity adjusted live. Third persona *gig rider Arjun*: volatile income handled with 6-month average + volatility band → smaller pre-approved PL instead of rejection ("financial inclusion" note).
6. **[4:45] Lead card + NBA:** LQS 87 (Intent 91 / Capacity 84 / Risk 8), top-3 SHAP reasons in officer language, LLM talking points ("Her rent ≈ the EMI on the home she's browsing"), RM clicks **Converted** → feedback logged.
7. **[5:30] Close:** metrics wall — precision@top-decile 34%, Qini curve, PSI monitor, cost-per-loan ₹9,800 → ₹700; DPDP consent ledger flash; "three models, one score, every decision explained."

---

## 9. Key sources (deduplicated)
- TransOrg PL propensity case: https://www.transorg.ai/case-study/predicting-customer-propensity-for-personal-loans-at-a-leading-fintech-company/
- Valiance risk-augmented cross-sell (+10% conversion): https://valiancesolutions.com/case_study/risk-augmented-personal-loan-cross-sell/
- CreditVidya (10k+ data points, +15% approvals): https://creditvidya.com/
- Prism Data CashScore / income: https://www.prismdata.com/ · https://www.prismdata.com/income/
- Perfios BSA: https://www.perfios.com/solutions/bank-statement-analyzer · FinBox: https://www.finbox.in/products/bankconnect · Setu AA: https://setu.co/data/financial-data-apis/account-aggregator/
- BSA tool landscape: https://hyperverge.co/blog/bank-statement-analysis-software/ · https://precisa.in/blog/precisa-vs-finbox-bank-statement-analysis-tool/
- Cash-flow underwriting: https://plaid.com/resources/lending/cash-flow-underwriting/ · https://www.loanpro.io/blog/what-lenders-need-to-know-about-implementing-cash-flow-underwriting-in-2026/
- FOIR: https://www.techfinserv.com/blogs/foir-uw/ · https://precisa.in/blog/credit-underwriting-process-india/
- MCC limits & categorization: https://www.tapix.io/resources/post/why-mcc-codes-do-not-help-much-with-payment-categorization · https://www.finextra.com/blogposting/31935/beyond-mcc-codes-why-transaction-categorisation-is-becoming-core-banking-infrastructure · https://www.cashfree.com/blog/merchant-category-code-mcc-meaning-list-examples/
- Uplift: https://towardsdatascience.com/why-every-marketer-should-consider-uplift-modeling-1090235572ec/ · https://cmr.berkeley.edu/2025/11/to-treat-or-not-to-treat-five-lessons-learned-from-using-uplift-modeling-to-optimize-marketing-campaigns/ · https://arxiv.org/pdf/2604.06123 · https://link.springer.com/article/10.1007/s10796-022-10283-4
- Clickstream intent: https://www.capitalone.com/tech/software-engineering/clickstream-data-advances-in-customer-intent-prediction/ · https://formotiv.com/what-is-clickstream-data-and-why-should-insurers-care/ · https://www.nature.com/articles/s41598-020-73622-y
- Life-event triggers/NBA: https://www.deluxe.com/resources/guide-to-life-event-triggers-for-bank-marketing/ · https://www.bai.org/banking-strategies/trigger-based-marketing-a-powerful-tool-for-attracting-and-retaining-customers/ · https://latinia.com/en/resources/examples-next-best-actions-marketing-banking · https://www.netguru.com/blog/next-best-offer-for-fintech
- RBI Digital Lending Directions 2025: https://www.legal500.com/developments/thought-leadership/the-rbis-digital-lending-directions-2025-a-unified-code-for-a-fragmented-sector/ · https://www.azbpartners.com/wp-content/uploads/2025/05/AZB-Update-Digital-Lending-Directions-2025.pdf · https://www.argus-p.com/updates/updates/rbi-digital-lending-directions-2025-an-overview/ · https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3413
- CIBIL soft vs hard pull: https://www.bankbazaar.com/cibil/credit-inquires.html · https://honestmoney.in/credit-score/hard-inquiry-vs-soft-inquiry-cibil-score-impact-how-to-minimize/ · https://zetapp.in/blog/difference-between-soft-and-hard-enquiry-in-cibil-report
- DPDP: https://cms-induslaw.com/en/ind/publication/sector-specific-faqs-on-the-digital-personal-data-protection-act-2023-dpdp-act-and-digital-personal-data-protection-rules-rules-2025 · https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023 · https://www.seclore.com/fundamentals/dpdp-rules-2025-compliance-guide/ · https://mitigata.com/blog/what-is-dpdp-rules-2025/ · https://www.dpdpa.com/dpdpa-faq.html
- Metrics/monitoring: https://coralogix.com/ai-blog/a-practical-introduction-to-population-stability-index-psi/ · https://www.mdpi.com/2227-9091/13/12/238 · https://ssrpublisher.com/wp-content/uploads/2025/09/Explainable-AI-for-Credit-Scoring-with-SHAP-Calibrated-Ensembles-A-Multi-Market-Evaluation-on-Public-Lending-Data.pdf · https://www.appitsoftware.com/blog/how-to-build-risk-scoring-engine-mlops-financial-services
