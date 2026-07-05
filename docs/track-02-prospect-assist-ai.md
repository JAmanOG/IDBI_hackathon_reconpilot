# Track 02 — Prospect Assist AI

Tags: Lead Generation · Behavioural Analytics · Retail Lending

## 1. Official Problem Statement

Retail lending leans on traditional metrics → low conversions (~1% today) and little insight into real customer intent. Need a data-driven way to find eligible, genuinely-interested prospects with real repayment capacity.

## 2. Expected Outcome (official)

Generate **high-quality leads with conversion > 30%**, plus accurate assessment of a borrower's **actual income** for prudent underwriting of: Personal, Home, Mortgage and Auto loans.

## 3. AMA Clarifications (ground truth from mentors)

- Answer two questions per prospect: (1) Is the customer genuinely **interested**? (2) Do they have real **repayment capacity**?
- Work off the transaction / bank-statement DB (sandbox). Go **beyond traditional FOIR** maths.
- Derive a **behaviour pattern** from spending; predict likely delinquency before it happens.
- Detect **window-shoppers vs serious buyers** via time-on-site and browsing behaviour.
- Salaried vs gig / self-employed: infer real disposable income = money retained after **need vs want vs luxury** spends.
- Self-employed: use **industry margins + UPI turnover** → estimate gross margins.
- Signals: geolocation, spend location, balance left, full UPI footprint.
- Cross-check multiple accounts via **credit-bureau data** (request extra bank statements).
- Core deliverable = a **model of customer behaviour** that drives the lead / credit decision.

## 4. Research Findings (highlights)

> Full cited reference: [research/track-02-research.md](research/track-02-research.md)

- **Critical framing of "1% → 30%"**: no model converts a cold base at 30%. The honest interpretation is **precision@k on the qualified, pre-screened lead list handed to RMs** — pre-approved leads convert at 20–40% in industry practice because risk rejection happens *before* contact. Frame it as funnel re-engineering: same base, contact effort spent only on scored leads.
- **The two-model fusion is the proven industry pattern**: Valiance's risk-augmented cross-sell (propensity × delinquency-risk grid) delivered ~10% higher conversion and 10–20% higher tickets; Prism Data's CashScore proves deposit-data-only default prediction is "as predictive as traditional scores." CreditVidya (10k+ data points, 2× bureau power) is the Indian beyond-FOIR precedent.
- **MCC codes alone are insufficient** for categorization (no MCC on P2P UPI; merchant-type ≠ purchase intent). Production pattern = layered: merchant dictionary → UPI VPA parsing → narration regex → ML classifier → LLM fallback with cache.
- **Soft-pull at lead stage has zero CIBIL impact** — the legal basis for the risk pre-screen; hard inquiry only at application.
- **Uplift modelling (T/X-learner)** is the sophistication flex: target *persuadables*, not sure-things; evaluate with Qini curves.
- **DPDP**: profiling/marketing require separate explicit consent (not "legitimate use"); phased enforcement Nov 2026–May 2027; ₹250 cr penalties; geolocation must be coarsened to pincode/city.
- **RBI Digital Lending Directions 2025** (effective 8 May 2025): creditworthiness must capture age/occupation/income; data collection need-based and consent-based; no dark patterns in offers.
- **Life-event trigger library** (India-specific): rent debit → home-loan intent ("your ₹32k rent ≈ EMI on ₹38L"); school fees, marriage spend cluster (jewellery+catering+travel), salary jump >20%, broker/property-portal fees, maternity spends.

## 5. Proposed Architecture

Feature store (DuckDB/Postgres) over synthetic statements + clickstream + mock bureau JSON, feeding **three visible models**:

1. **Intent/Propensity** — LightGBM per product (PL/HL/LAP/Auto) on RFM + trigger events + clickstream (EMI-calculator params, session recency); calibrated P(apply in 30d).
2. **Capacity** — income engine (salary detector / gig-payout detector / UPI-turnover × industry-margin priors) → discretionary surplus (income − needs − obligations) → stress-adjusted max eligible EMI → **suggested ticket & tenure**.
3. **Risk pre-screen** — P(60+ DPD in 12m) from statement behaviour + mock bureau; hard-blocks gate leads out regardless of intent.

Fusion: `LQS = 100 × P(intent) × capacity_fit × (1 − PD)`, with sub-scores + SHAP reason codes displayed. Downstream: **RM dashboard** with ranked lead cards, Next Best Action, LLM talking points generated *only from SHAP features* (no hallucinated facts), consent chip, and RM feedback buttons (converted / not interested) feeding retraining.

**Synthetic data**: 6 personas × 12 months (salaried-stable, salaried-stressed, gig rider, kirana self-employed, affluent upgrader, window-shopper) with seasonality, realistic narrations (`UPI/DR/…/swiggy@icici`, `NEFT-SAL-INFY`) and planted ground truth so metrics are computable.

## 6. Pros / Cons of Approach Options (decisions)

| Choice | Decision | Why |
|---|---|---|
| Propensity vs uplift | **Propensity core; uplift as roadmap + toy T-learner** | Uplift needs randomized campaign logs; show the persuadables slide as differentiation |
| Categorization | **Rules (70–80%) → ML → LLM fallback with cache** | Deterministic + auditable base; LLM only for long-tail; DPDP-safer |
| Batch vs real-time | **Batch for statement features; real-time only for clickstream intent** | Intent decays in hours; statements don't |
| Score presentation | **Fused LQS for sorting + three sub-scores on the card** | Bankers distrust opaque single numbers; maps literally to the track's two questions |

## 7. Winning Strategy & Demo Plan

**Judge levers**: speak funnel economics ("1% means 100 calls per loan; we make it 3"), answer the track's two questions with two visible dials + a risk gate, explainability everywhere (reasons an officer can say aloud), compliance as a demo moment (DPDP consent ledger, soft-pull-only), human-in-the-loop feedback retraining, one sophistication flex (uplift/persuadables).

**6-minute demo**: funnel hook → Priya's raw statement categorized live (salary ₹95k detected) → capacity card (surplus ₹48k; FOIR said 6%, surplus view says home-loan ready) → intent trigger fires (broker fee + property-portal + EMI calculator at ₹38L/20y → Intent 91) vs Rahul the window-shopper (Intent 22, nurture only) → risk gate (CIBIL 771 soft pull; hidden EMI found via bureau cross-check; gig rider Arjun gets a right-sized PL instead of rejection — inclusion note) → lead card with LQS 87, SHAP reasons, LLM talking points, RM clicks Converted → metrics wall (precision@decile 34%, Qini, PSI, cost per loan ₹9,800 → ₹700).
