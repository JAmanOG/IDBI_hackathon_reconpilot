# Track 5 Research — Open Innovation (Wildcard)

**IDBI Innovate 2026 · Researched 2026-07-04**

Track brief: original concepts OUTSIDE tracks 1–4 (wealth advisory, retail-lending leads, MSME health score, MSME default prediction). Must solve real banking pain points — regulatory requirements/advisories OR daily operational-efficiency issues. Judged with subject-matter experts. **Mentors explicitly invited (a) back-office reconciliation and (b) KYC struggles.** Brief also name-drops decentralized identity, decentralized ledgers, next-gen security fabrics, omni-channel CX. Must show long-term commercial scalability + integration viability inside IDBI's ecosystem. Context: IDBI has no LLM/AI in production; judging themes across the event are explainability + human-in-the-loop.

---

## 1. Reconciliation pain deep-dive (invited theme #1)

### 1.1 What a bank like IDBI reconciles every day

| Recon stream | What is matched | Pain characteristics |
|---|---|---|
| **UPI settlement recon** | CBS entries vs bank UPI switch logs vs NPCI raw/settlement files (per settlement cycle) | Highest volume by far; multiple intraday settlement cycles; debit/credit legs can land in different cycles; timeouts and "deemed approved" states create breaks |
| **IMPS / NEFT / RTGS recon** | CBS vs NPCI (IMPS) / RBI (NEFT-RTGS) settlement reports | IMPS shares UPI-style timeout ambiguity; NEFT batch returns (N07/N10) |
| **ATM / switch recon** | CBS vs ATM switch vs electronic journal (EJ) vs cash-replenishment agency counts vs NFS (NPCI) network files | Cash-out disputes, partial dispense, acquirer-vs-issuer legs; RBI TAT of T+5 for failed ATM txns |
| **Card-network settlement** | CBS/card management system vs Visa (BASE II/SMS) / Mastercard (IPM) / RuPay (NPCI) clearing files | Interchange & fee validation, chargeback lifecycle |
| **Nostro/vostro** | Internal mirror accounts vs SWIFT MT940/MT950 statements from correspondent banks | Aged open items attract audit/RBI comment; FX legs |
| **GL-to-subledger / inter-branch** | GL control accounts vs product processors (loans, cards, trade, treasury) | Classic "office accounts" problem; RBI inspections routinely flag un-reconciled inter-branch/office accounts |
| **Suspense & sundry accounts** | Ageing of parked entries | RBI requires review/ageing of suspense accounts; long-pending entries → provisioning and audit findings; unclaimed balances eventually go to the DEA Fund |

### 1.2 The 3-way UPI recon burden (this is the demo-able core)

Oracle's payments documentation describes the canonical process: NPCI provides extracts of transactions per settlement cycle; the **bank's UPI switch** generates corresponding extracts; the **CBS** generates its own; the bank reconciles all three — NPCI file vs switch vs CBS ([Oracle UPI Reconciliation Extraction](https://docs.oracle.com/en/industries/financial-services/banking-payments-cloud-service/14.8.1.0.0/pcupi/upi-reconciliation-extraction.html)). NPCI's UPI settlement process doc details the cycle mechanics ([NPCI UPI Settlement Process PDF](https://www.npci.org.in/PDF/npci/others/UPI-Settlement-Process.pdf)).

Break taxonomy (what recon teams chase daily):
- Present in NPCI file, missing in CBS (switch accepted, CBS posting failed) → customer debited/credited wrongly or bank out-of-pocket.
- Present in CBS, missing in NPCI (orphan posting).
- Amount/response-code mismatch; duplicate postings; wrong-leg reversals.
- Timeout transactions ("deemed" status) — the single largest exception class in UPI.
- Cross-cycle timing differences (txn in cycle N at NPCI, cycle N+1 in CBS).

Each break must be classified, aged, journaled to a UPI settlement/suspense GL, and resolved via adjustment (TCC — transaction credit confirmation, RET — returns, chargeback/pre-arbitration) within NPCI's dispute TATs.

### 1.3 Scale in 2026 — why this is existential, not cosmetic

- UPI hit a record **23.2 billion transactions worth ₹29.9 trillion in May 2026 ≈ 737.8 million transactions/day** ([ANI](https://www.aninews.in/news/business/upi-hits-new-high-in-may-2026-with-232-billion-transactions-worth-rs-299-trillion-npci-data-shows20260602155337/), [Tribune](https://www.tribuneindia.com/news/business/upi-hits-new-high-in-may-2026-with-23-2-billion-transactions-worth-rs-29-9-trillion-npci-data-shows/), [NPCI product statistics](https://www.npci.org.in/product/upi/product-statistics)).
- Even at a modest ~1–2% share of ecosystem volume, a mid-size PSU bank like IDBI processes **millions of UPI legs/day**; a 0.1% exception rate = thousands of breaks/day for a manual back-office team.
- Failure/decline rates on UPI fluctuate with bank downtime; every failed-but-debited txn becomes a recon exception **and** a regulatory compensation clock (next section).

### 1.4 Regulatory teeth: RBI TAT-harmonisation circular (2019)

RBI circular **RBI/2019-20/67, DPSS.CO.PD No.629/02.01.014/2019-20, dated 20 Sep 2019** — "Harmonisation of Turn Around Time (TAT) and customer compensation for failed transactions using authorised Payment Systems" ([RBI notification](https://www.rbi.org.in/commonman/English/scripts/Notification.aspx?Id=3074), [Medianama summary](https://www.medianama.com/2019/09/223-rbi-penalties-failed-transaction/)):
- **UPI** (account debited, beneficiary not credited): auto-reversal by beneficiary bank within **T+1**; thereafter **₹100/day compensation, automatically, without the customer asking**.
- **ATM**: reversal within T+5, then ₹100/day.
- **IMPS, card, PPI, NACH, Aadhaar Pay** have analogous TATs.
- Implication: **recon speed is directly monetized** — every day a timeout break sits unresolved past TAT accrues ₹100/txn liability plus RB-IOS complaint risk. This is the quantifiable ROI hook for judges.

### 1.5 NPCI dispute machinery: URCS + UDIR

- **URCS** (UPI Real-time Clearing & Settlement) is NPCI's back-office system through which banks raise/act on disputes and adjustments ([Dvara on UDIR](https://upigrm.dvararesearch.com/npcis-udir/)).
- **UDIR** (Unified Dispute & Issue Resolution), NPCI circular OC-98 of 2020-21, moved complaint/dispute handling from manual file-based flows to **API-based online resolution**; banks had to modify switch, CBS, and recon processes to support online status-check and pending-transaction actions ([NPCI Circular 98 PDF](https://www.npci.org.in/PDF/npci/upi/circular/2020/Circular-98-UDIR-Enhancing-Complaint-handling-and-resolution.pdf), [Oracle UDIR notes](https://docs.oracle.com/en/industries/financial-services/banking-payments/14.8.0.0.0/payrn/upi-unified-dispute-and-issue-resolution-udir.html), [Razorpay explainer](https://razorpay.com/blog/all-you-need-to-know-about-npci-led-udir/)).
- Practical pain: dispute queues in URCS still need humans to decide TCC vs RET vs chargeback deflection, attach evidence, and post CBS adjustments — a copilot can sit exactly there.

### 1.6 Vendor landscape (know it to differentiate)

- **SmartStream TLM** — incumbent enterprise recon at 70+ of the world's top 100 banks; strong but heavy, rule-based, expensive to reconfigure ([Gresham comparison blog](https://www.greshamtech.com/blog/best-reconciliation-software-for-financial-institutions-in-2026), [Optimus vs SmartStream](https://optimus.tech/blog/optimus-vs-smartstream-for-bank-reconciliation)).
- **Broadridge, ReconArt, Gresham (Clareti)** — international recon platforms.
- **Cointab** — India; automated recon incl. suspense & exception account recon, AI-assisted matching, audit-ready reports ([Cointab](https://www.cointab.net/business/suspense-exception-account-reconciliation/)).
- **Osfin.ai** — India; high-volume payment recon for banks/fintechs; one-to-many matching, fees, chargebacks ([Osfin blog](https://www.osfin.ai/blog/enterprise-reconciliation-software)).
- **Recko** — Indian recon startup acquired by Stripe (2021) — evidence of category value.
- Gap all of them leave: they **match**; humans still **investigate and resolve**. Exception *resolution* (root-cause, evidence gathering across CBS/switch/URCS, adjustment drafting, TAT-compensation math) is still manual. That is the LLM/agentic white space.

### 1.7 Where AI genuinely helps (vs. where rules suffice)

1. **ML auto-matching / entity resolution** for fuzzy legs (narration variants across banks/apps — a documented India pain: the same payer via PhonePe/HDFC vs GPay/Axis produces different narrations ([aiaccountant buyer's guide](https://www.aiaccountant.com/blog/multi-bank-reconciliation-platform-india))). Deterministic keys (RRN/UTR) match 95%+; ML lifts the stubborn tail.
2. **Exception classification** — auto-label breaks into taxonomy (timeout, duplicate, missing-leg, amount mismatch) with confidence + explanation.
3. **Break-resolution copilot** — for each break, an agent pulls CBS posting, switch log, NPCI record, prior similar cases; proposes the resolution (TCC/RET/adjustment voucher), drafts the entry, computes TAT-compensation exposure; human approves (human-in-the-loop = judging theme).
4. **Agentic investigation** — multi-step: query 3 sources → hypothesize root cause → verify → recommend; audit-logged reasoning = explainability theme.
5. **Natural-language recon-rule authoring** — ops manager types "match on RRN, then amount±0, tolerate 1-cycle date drift; route timeouts >T+1 to Team B" → generates/updates matching config. Kills the vendor-change-request bottleneck that makes TLM reconfiguration slow.

---

## 2. KYC pain deep-dive (invited theme #2)

### 2.1 Periodic re-KYC burden — the numbers

RBI **KYC (Amendment) Directions, 2025** to the Master Direction on KYC, issued **12 Jun 2025 (RBI/2025-26/51, DOR.AML.REC.30/14.01.001/2025-26)** ([circular PDF](https://pdicai.org/Docs/RBI-2025-26-51_1262025151347878.pdf), [Signzy summary](https://www.signzy.com/blogs/RBI-KYC-Master-Directions-2025-key-changes), [HyperVerge breakdown](https://hyperverge.co/blog/breaking-down-the-new-rbi-amendments-to-the-kyc-master-direction/)):
- Periodic updation at least every **2 years (high-risk), 8 years (medium), 10 years (low)**.
- Banks must send **3 advance intimations (≥1 by letter) before due date and 3 reminders (≥1 by letter) after** — an enormous outreach/tracking workload across channels, per customer, with escalation language mandated.
- Low-risk individual customers get grace up to 1 year past due or **30 Jun 2026**, whichever is later — i.e., **a re-KYC backlog wave crests exactly in 2026**, with accounts otherwise facing debit-freeze → CASA attrition + branch congestion.
- Banks may now use **BCs/field agents** for KYC updates and self-declaration via digital channels — but that creates a new coordination/verification workflow to manage.
- **V-CIP** (video KYC) permitted for onboarding and periodic updation; operationally painful: assisted-mode staffing of concurrent video calls, drop-offs on low bandwidth, liveness/geotag checks, mandated data-ownership controls (no data resting on third-party cloud after the call) ([Lexology](https://www.lexology.com/library/detail.aspx?g=1bb2051f-d366-4f38-a4fd-f2ea09e20dc6), [ZIGRAM](https://www.zigram.tech/article/rbis-faqs-amendment-kyc-june-2025/)).

### 2.2 CKYCR / CERSAI obligations (2024 rules)

- PML (Maintenance of Records) **Amendment Rules 2024** + RBI's Nov 2024 alignment: verify identity via **KYC Identifier (14-digit KIN)** from CKYCR instead of re-collecting documents; upload new KYC within **10 days** of account opening; push any customer-detail change to CERSAI within **7 days**; **CKYCRR 2.0** mandates API submission in structured JSON/XML with document scan quality floors (150–200 DPI) ([Signzy CKYCRR guide](https://www.signzy.com/blogs/what-is-ckycrr-complete-guide), [ixsight CKYCRR 2.0](https://ixsight.com/blogs/what-is-ckycrr-2-0/), [ZIGRAM on CKYC reliance](https://www.zigram.tech/article/rbi-ckyc-reliance-guidance-india-2025/)).
- Operational pain: rejected uploads (format/DPI), mismatch between CBS demographics and CKYCR record, 7-day update SLA breaches surfacing in compliance testing.

### 2.3 AML name screening — the false-positive furnace

- Industry data: **up to 99% of sanctions-screening alerts are false positives** ([WorkFusion](https://www.workfusion.com/blog/how-ai-agents-de-risk-aml-and-sanctions-compliance-operations/)); a documented case: 10 analysts drowning in 600–800 name alerts/day ([WorkFusion](https://www.workfusion.com/blog/false-positives-do-not-matter-in-aml/)); root causes are transliteration variants, common Indian surnames, thin identifiers ([Facctum](https://www.facctum.com/blog/false-positive-rates-in-aml-screening), [sanctions.io](https://www.sanctions.io/blog/the-problem-of-false-positives-in-aml-screening)).
- India specifics: UNSC/OFAC lists + MHA/UAPA lists + PEP screening; every list update triggers full-book re-screening; explainable-AI triage has shown up to **94% false-positive reduction** claims ([Flagright](https://www.flagright.com/post/how-to-minimize-false-positives-in-aml-screening)).
- The adjudication decision ("is Mohammed Khan the OFAC Mohammed Khan?") is an evidence-synthesis task — exactly what an LLM copilot with an audit trail does well, with the human analyst signing off (explainability + HITL both satisfied).

### 2.4 Rails available for a solution

- **Aadhaar e-KYC / OTP-based updation, DigiLocker** documents — RBI's 2025 amendment explicitly blesses digital re-KYC channels ([Ujjivan explainer](https://www.ujjivansfb.bank.in/banking-blogs/personal-finance/rbi-revises-kyc-rules)).
- **MNRL (TRAI/DoT Mobile Number Revocation List)** — hosts mentioned this explicitly. RBI (17 Jan 2025 directive on financial frauds via voice/SMS) requires regulated entities to consume MNRL via DoT's **Digital Intelligence Platform (DIP)** and act by **31 Mar 2025**: verify/clean RMNs, and monitor accounts linked to revoked numbers as potential **mule accounts** ([Business Standard](https://www.business-standard.com/finance/personal-finance/rbi-asks-banks-to-uses-tool-that-identifies-phone-numbers-to-curb-fraud-125012400390_1.html), [Signzy MNRL FAQ](https://www.signzy.com/blogs/complying-rbis-new-mnrl-guidelines-11-key-questions-answered), [ZIGRAM](https://www.zigram.tech/article/mobile-number-revocation-list-aml-india/)). MNRL is published monthly; matching it against tens of millions of CBS records and deciding actions per account is an ongoing ops burden — and a natural module in a KYC-ops platform.
- **Dedupe/entity resolution across CBS**: legacy banks carry duplicate CIFs (name spelling variants, missing PAN linkage); the RBI push for unique customer identification makes CIF dedupe + household/entity resolution a real, unsexy, high-value problem.

### 2.5 Vendor landscape

**IDfy, Signzy, HyperVerge, Digio, Karza (now Perfios)** dominate Indian KYC onboarding APIs (doc OCR, face-match, V-CIP tooling, registry lookups). Gap: they solve **onboarding**; the invited pain is **lifecycle ops** — re-KYC campaign orchestration at millions-of-accounts scale, CKYCR sync-repair, screening-alert adjudication, MNRL-driven mule triage. That back-book ops layer is far less served — good differentiation story vs "yet another eKYC API".

### 2.6 AI angles that fit IDBI

1. **Agentic vernacular re-KYC outreach**: agent plans the RBI-mandated 3+3 contact sequence per customer, drafts vernacular SMS/WhatsApp/IVR scripts, routes to Aadhaar-OTP/V-CIP/BC-visit journey by customer segment, tracks completion, escalates to freeze-prevention worklists. Directly monetizes the June-2026 backlog wave.
2. **Screening-alert adjudication copilot**: gathers candidate-match evidence (DOB, address, PAN, adverse media), writes a reasoned disposition memo, analyst approves; full audit trail for RBI/FIU-IND inspection.
3. **Document-forgery detection** on re-KYC uploads (tamper/quality/EXIF checks) before CKYCR submission — cuts CERSAI rejections.
4. **CKYCR reconciliation agent**: diff CBS vs CKYCR record, auto-prepare 7-day updates, flag KIN mismatches (nice bridge: it is *also* a reconciliation problem — lets one platform narrative span both invited themes).

---

## 3. Other credible wildcard candidates (scan)

### 3.1 The precedent that legitimizes ops-AI: MuleHunter.AI
RBI Governor announced **MuleHunter.ai** (built by Reserve Bank Innovation Hub, Bengaluru) in the 6 Dec 2024 Monetary Policy Statement: an ML model replacing static rule-based mule-account detection, trained on **19 mule-behavior patterns** identified with partner banks; piloted with two large PSU banks, and per an RTI response **23 banks had implemented it by late 2025** ([RBIH project page](https://rbihub.in/projects/mulehunter), [Business Standard](https://www.business-standard.com/finance/personal-finance/explained-rbi-has-a-new-ai-tool-mulehunter-ai-to-reduce-digital-frauds-124120900250_1.html), [Medianama RTI](https://www.medianama.com/2025/12/223-rti-23-banks-mulehunter-mule-accounts/)). **Use in pitch**: the regulator itself ships operations-AI to banks — an IDBI ops copilot rides a sanctioned wave, and MNRL+mule triage can integrate with/complement MuleHunter outputs rather than compete.

### 3.2 Agentic regulatory-compliance copilot
- Pain: RBI recently **repealed 9,446 circulars and consolidated the rulebook into ~238–244 Master Directions** ([DD News](https://www.newsonair.gov.in/rbi-repeals-9000-circulars-consolidates-rules-into-244-master-directions-to-ease-compliance/), [ThePrint](https://theprint.in/india/rbi-consolidates-over-9000-circulars-to-reduce-compliance-burden/2794738/)) — but new circulars/amendments still flow weekly (RBI's own circular index runs to hundreds of notifications a year across departments: [RBI circular index](https://rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx)), and the consolidation itself forces every bank to re-map its internal policies to renumbered Master Directions — a one-time, giant, LLM-shaped mapping job.
- RBI's 31 Jan 2024 circular "Streamlining of Internal Compliance monitoring function — leveraging use of technology" **explicitly directs banks to use tech for compliance monitoring** ([ricago summary](https://www.ricago.com/blog/how-ricago-cms-empowers-banks-nbfcs-to-adhere-to-rbi-guidelines)) — a regulatory mandate for exactly this product.
- Concept: circular lands → agent extracts obligations, maps to owner departments/policies, drafts gap analysis + action items with deadlines, tracks closure, generates board-compliance MIS. Pros: universal, judges (compliance bankers) feel it daily; text-native so LLM-perfect; easy demo (real public circulars = no data problem). Cons: several regtech startups circling (ricago, Complinity, non-India: Norm.ai); output quality hard to eyeball-verify in 3 minutes; less "wow" than watching money reconcile.
- Demo feasibility: **high** (public RBI PDFs in, obligation register out).

### 3.3 Audit / RBI-inspection response automation
Pain: RBI's Risk Based Supervision (and internal/concurrent audits) generate hundreds of requisitions and observations; branches scramble to compile evidence. Agent drafts responses from policy repo + core data, tracks compliance-closure of findings. Pros: acute, unserved. Cons: needs confidential artifacts to feel real; harder synthetic demo; overlaps partially with 3.2. Feasibility: medium.

### 3.4 RB-IOS / complaint & Ombudsman triage
RBI Integrated Ombudsman Scheme complaint volumes run ~1 million/year system-wide and rising; banks face deemed-acceptance penalties on TAT misses. Agent: classify complaint, fetch txn context, draft resolution letter, flag TAT-compensation cases (links back to §1.4). Pros: customer-visible ROI. Cons: brushes against omni-channel CX (fine) but also feels like generic "support AI"; several vendors. Feasibility: high.

### 3.5 Trade-finance document AI (LC scrutiny under UCP600)
Checking LC documents against UCP600/ISBP discrepancy rules takes trained checkers hours per docset; discrepancy disputes are costly. Vendors already deep here (Cleareye.ai with J.P. Morgan, Traydstream, Conpend). Pros: high-value, IDBI has trade ops. Cons: crowded vendor space, judges may not be trade specialists, OCR-heavy demo risk. Feasibility: medium.

### 3.6 DAKSH/CIMS regulatory-reporting automation
RBI collects fixed-format **returns** (daily→annual frequencies) via **CIMS**, and supervisory workflows run on **DAKSH** ([RBI list of returns](https://www.rbi.org.in/scripts/BS_Listofallreturns.aspx), [IRIS RegTech on CIMS](https://irisregtech.com/iris-ideal/en-in/rbi-cims-solution/), [Taxmann on CIMS returns](https://www.taxmann.com/post/blog/rbi-cims-reporting-framework-new-rules-for-internet-mobile-banking-returns)). Banks file dozens-to-hundreds of returns; data assembly from CBS/GL is manual-ish. Agent validates, explains variances, drafts return commentary. Pros: real, chronic. Cons: needs internal data models to demo; ADF/CIMS formats are gnarly; incumbents (IRIS, Surya/ADEPT) exist. Feasibility: low-medium for a hackathon.

### 3.7 Agentic collections / branch-ops copilot / deposit mobilization
- **Collections**: vernacular voice/WhatsApp agents for early-bucket follow-up — but skirts Track 4 (default prediction) adjacency; also RBI FREE-AI-era sensitivity on AI contacting customers about dues. Weak non-overlap story. Skip.
- **Branch-ops copilot**: staff Q&A over circulars/product manuals ("can an NRO account holder do X?"). Easy, useful, but reads as "RAG chatbot" — low originality score. Keep only as a *module* of 3.2.
- **Deposit mobilization**: leads/analytics for CASA — collides conceptually with Track 1/2 (advisory/leads). Skip.
- **Decentralized identity / DLT / security fabrics** (from the brief): thin demo-ability in 48h, no clear IDBI integration story, and DID for KYC in India is speculative next to CKYCR rails. Mention as future roadmap slide only.

**Scan verdict**: the invited themes dominate. Strongest three: **(A) UPI/payments reconciliation + exception-resolution copilot**, **(B) KYC lifecycle-ops + screening copilot**, **(C) regulatory-compliance copilot** (as challenger/backup or as a thin third module).

---

## 4. Full concepts for the strongest candidates

### 4.A "ReconPilot" — agentic payments reconciliation & exception resolution (primary recommendation)

**One-liner**: A 3-way UPI/IMPS/ATM recon engine with an agentic exceptions desk: ML matches the tail, agents investigate breaks across CBS/switch/NPCI data, draft the adjustment + UDIR action, and compute live ₹100/day TAT-compensation exposure — human approves every action.

**Why it wins Track 5**: explicitly invited theme; quantified regulatory teeth (§1.4); ~738M txns/day system context (§1.3); incumbent tools match but don't resolve (§1.6); explainability + HITL native to the design.

**AWS architecture** (all in ap-south-1 Mumbai — RBI payment-data localisation, 2018 directive, satisfied):
- **Ingest**: S3 landing buckets for NPCI raw/settlement files (CSV/fixed-width), switch logs, CBS GL extracts → AWS Glue jobs normalize to a canonical transaction schema (RRN/UTR, txn ID, VPA, amount, response code, cycle).
- **Match**: deterministic pass in Glue/Athena SQL (RRN+amount+direction); residual tail → **AWS Entity Resolution** / SageMaker fuzzy-matching model (narration variants, cross-cycle drift).
- **Exceptions store**: DynamoDB/Aurora break register with ageing + TAT clocks (EventBridge schedulers fire compensation-accrual alerts).
- **Agent layer**: **Amazon Bedrock Agents** (Claude) with tools: `query_cbs`, `query_switch_log`, `query_npci_record`, `find_similar_breaks`, `draft_adjustment_voucher`, `draft_udir_action`, `compute_tat_compensation`. Bedrock Guardrails + full reasoning trace persisted (CloudTrail + case file) → the **explainability artifact** judges can read.
- **NL rule authoring**: Bedrock converts ops-manager prose to matching-rule JSON, versioned, dry-run-tested against yesterday's files before promotion.
- **UI**: ops dashboard (break queue by class/age/₹-exposure, one-click approve of agent-drafted resolutions).
- **Optional**: Textract only if demoing scanned vouchers/EJ prints.

**Synthetic demo plan**: generate 3 mock files for one settlement cycle — NPCI-style raw file (~50k rows), switch log, CBS dump — with seeded breaks: 30 timeouts (debit-no-credit), 10 duplicates, 5 amount mismatches, 5 orphans, cross-cycle drift. Show: 99.7% auto-match in seconds → 50 exceptions → agent walks 3 of them live (pulls all three records, explains root cause in plain English, drafts TCC/RET + voucher, shows ₹100/day clock) → supervisor approves → dashboard shows FTE-hours and penalty-₹ saved. Judges = recon bankers: use their vocabulary (RRN, TCC, URCS cycle, suspense GL).

**Finacle integration story** (verified: IDBI runs Infosys **Finacle** — live since 2001, major upgrade to Finacle 10.x with Oracle RAC in 2016, separate instances for domestic/commercial/Dubai/IBU: [FinTech Futures](https://www.fintechfutures.com/2016/05/idbi-bank-in-major-tech-upgrade-and-business-process-re-engineering/), [Finacle case study](https://www.finacle.com/client-stories/case-studies/idbi-bank/), [Infosys 2001 PR](https://www.infosys.com/newsroom/press-releases/documents/2001/idbi-21june01.pdf)): consume the same end-of-cycle GL/txn extracts recon teams already pull from Finacle (file-based, zero core change, day-1 viable); phase 2 posts approved vouchers back via Finacle Integrator/FI APIs; phase 3 wires UDIR API actions. No CBS surgery required = credible integration slide.
**Commercial scalability**: every bank + every PSP + NBFC-PPIs reconcile NPCI files; same engine extends to NEFT/RTGS, cards, nostro; SaaS or on-prem license; recon spend already proven by SmartStream/Osfin market.
**Non-overlap vs Tracks 1–4**: pure back-office payments ops — no lending, no advisory, no MSME scoring. Cleanest possible separation.

### 4.B "KYCOps Copilot" — re-KYC lifecycle + screening adjudication (strong second)

**One-liner**: An agentic back-book KYC platform: plans and executes the RBI-mandated re-KYC contact sequence in vernacular across channels, routes customers to Aadhaar-OTP/V-CIP/BC journeys, repairs CKYCR sync gaps, screens MNRL for mule risk, and adjudicates AML name-alerts with reasoned, audit-trailed memos.

**Pain anchors**: 2/8/10-year re-KYC cycles + 3+3 mandated intimations + Jun-2026 low-risk deadline wave (§2.1); CKYCR 7/10-day SLAs (§2.2); 95–99% screening false positives (§2.3); MNRL mandate the hosts themselves cited (§2.4).
**AWS architecture**: S3 + Aurora customer-book replica → segmentation (due-date waves, risk tier) → Bedrock agent plans per-customer outreach (SMS/WhatsApp/IVR templates in 8 languages, Pinpoint/Connect for channels) → journey router (Aadhaar-OTP link / V-CIP scheduler / BC task) → Textract + forgery checks on uploaded docs → CKYCR JSON payload builder → screening module: candidate matches from watchlist index (OpenSearch) → Bedrock adjudication memo with cited evidence → analyst approve/reject → immutable audit log.
**Synthetic demo**: 10k-row synthetic customer book with due-dates, revoked MNRL numbers, 20 seeded name-alert cases (transliteration traps like "Md. Salim" vs "Mohammed Saleem"); show the agent clearing 18 as false positives with written rationale, escalating 2.
**Finacle integration**: CIF extract out, KYC-status flag back; V-CIP/eKYC via existing vendor APIs (IDfy/Signzy class); CKYCR via CERSAI APIs.
**Scalability**: every RE (banks, NBFCs, MFs, insurers) shares the same PML-rules burden.
**Non-overlap**: compliance ops, not credit/advisory. Watch one edge: keep messaging strictly re-KYC (not marketing) to avoid Track-2 "customer outreach" resemblance.

### 4.C "CircularSense" — regulatory-change copilot (challenger / third module)

Circular → obligation extraction → mapped owners/policies → gap register → task tracking → board MIS; grounded in the Jan-2024 RBI tech-for-compliance mandate and the Master-Direction renumbering churn (§3.2). Best used either as a fallback (if mentors steer away from recon/KYC) or as a thin third pane proving platform extensibility ("one agentic ops fabric: money-ops, customer-ops, rule-ops"). Demo: feed 3 real public circulars, output an obligation register with deadlines and RACI. Zero data-privacy risk — its unique advantage.

**Recommended play**: Lead with **4.A ReconPilot** (deepest quantified pain + explicit invitation + cleanest demo), position **4.B** modules (MNRL screen, CKYCR-recon) as the roadmap of the same platform, keep **4.C** as one slide of extensibility. If the team splits effort, A alone > A+B shallow.

---

## 5. Strategy analysis — is Track 5 worth it?

**Competition shape**: Open tracks at bank hackathons attract the largest number of entries but the shallowest median — generic chatbots, vague "blockchain for banking", repackaged fintech demos. Variance is high because there is no anchor rubric; but the mentors here *gave away the rubric informally* by explicitly inviting reconciliation and KYC. Treating those invitations as the hidden problem statement converts Track 5 from high-variance to **arguably the most de-risked track**: you compete against unfocused entries while building exactly what the judges asked for.

**What wins with SME judges (career ops/compliance bankers)**:
1. **Recognition shock** — the demo shows *their* artifacts (NPCI raw file columns, TCC/RET, suspense GL ageing, re-KYC intimation letters). Domain fluency beats model sophistication.
2. **Quantified ROI** — e.g., "50 breaks/day × 25 min → 4 min = ~3.5 FTE saved; ₹100/day × unresolved-timeout backlog = ₹X lakh/yr penalty avoidance; re-KYC freeze-prevention protects ₹Y crore CASA." Put a number on every slide.
3. **Explainability + human-in-the-loop by construction** (stated judging themes): agent proposes, human disposes; every action carries a readable reasoning trace — also the honest answer to "IDBI has no AI in production, how do we trust this?"
4. **Integration realism**: file-based day-1 integration with Finacle (verified stack, §4.A), API phases later; Mumbai-region deployment for data-localisation. Banks' committees kill projects on integration risk — pre-empt it.
5. **Regulatory tailwind framing**: MuleHunter (regulator ships ops-AI), Jan-2024 compliance-tech circular, TAT circular — "the regulator wants you to do this" is the strongest argument in a PSU bank room.

**Risks & mitigations**:
- *No rubric / judge taste variance* → anchor to invited themes; open the pitch with the pain in the judges' own daily language, not with the tech.
- *"Vendors already do this" challenge* → conceded and answered: incumbents match, we resolve; incumbents onboard, we run the lifecycle (§1.6, §2.5).
- *Scope sprawl* → one polished stream (UPI recon) end-to-end beats five shallow ones.
- *Synthetic-data credibility* → mirror real NPCI file column semantics; state assumptions on a slide; offer a "works on your real files in a 2-week PoC" close.

**Bottom line**: Track 5 with ReconPilot is a lower-competition, judge-aligned bet — provided the build shows real recon-domain fluency and monetized ROI, not generic LLM glue.

