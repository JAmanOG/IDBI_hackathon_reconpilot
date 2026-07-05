# Regulatory Landscape — IDBI Innovate 2026 (Cross-Track Compliance Reference)

> Prepared July 2026. Cross-cutting reference for all 5 tracks. Hackathon rules require solutions to stay within SEBI / RBI / IRDAI / DPDP norms; "AI must follow RBI AI norms"; KYC, Aadhaar and MNRL tooling is allowed.
> Judging themes to design for: **explainability** and **human-in-the-loop**. Every regulation below is mapped to a concrete, demo-able feature in §8.

**Status caveats (as of July 2026):**
- RBI's FREE-AI is a **committee report** (Aug 2025), not yet a binding circular — but it is what "RBI AI norms" means in practice, and RBI has said future AI regulation will follow it.
- RBI's model-risk-in-credit circular is still formally a **draft** (Aug 2024); design to it anyway.
- DPDP Rules are notified (Nov 2025) with substantive obligations phasing in to **13 May 2027** — banks are expected to comply early; a hackathon demo that is already DPDP-ready is a differentiator.

---

## 1. RBI FREE-AI — Framework for Responsible and Ethical Enablement of AI

**The document:** *FREE-AI Committee Report — Framework for Responsible and Ethical Enablement of Artificial Intelligence*, released **13 August 2025** by an 8-member committee chaired by **Dr. Pushpak Bhattacharyya** (IIT Bombay), constituted by RBI in **December 2024** (announced in the Statement on Developmental and Regulatory Policies, 6 Dec 2024).
- Official PDF: https://rbidocs.rbi.org.in/rdocs/PublicationReport/Pdfs/FREEAIR130820250A24FF2D4578453F824C72ED9F5D5851.PDF
- Good summaries: KPMG (https://kpmg.com/in/en/insights/2025/08/rbi-free-ai-committee-report-on-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence.html), Dvara Research (https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/), IndiaAI/MeitY (https://indiaai.gov.in/article/rbi-s-framework-for-responsible-and-ethical-enablement-towards-ethical-ai-in-finance)

**Scope:** all RBI-regulated entities (REs) — scheduled commercial banks, co-op banks, NBFCs, payment system operators — and, via them, their fintech partners.

### 1.1 The 7 Sutras (exact names as in the report)

1. **Trust is the Foundation**
2. **People First** — AI augments human judgement; humans retain final authority over consequential decisions
3. **Innovation over Restraint** — enable responsibly rather than prohibit
4. **Fairness and Equity** — no discriminatory outcomes; bias testing
5. **Accountability** — the RE deploying AI is accountable, regardless of vendor
6. **Understandable by Design** — explainability of AI decisions to customers, auditors, supervisors
7. **Safety, Resilience and Sustainability** — fail-safes, fallback, kill-switch, monitoring drift

(Note: the hackathon brief's shorthand "Trust, People First, Innovation, Fairness, Accountability, Explainability, Resilience" maps 1:1 onto these.)

### 1.2 The 6 Pillars and the 26 recommendations (selection most relevant to a demo)

Innovation-enablement side:
- **Infrastructure**: shared/digital public infrastructure for AI, high-quality curated financial datasets, integration of AI with DPI (Aadhaar/UPI/AA), indigenous financial-sector AI models, **AI Innovation Sandbox** (supervised, time-bound testing environment).
- **Policy**: adaptive, risk-proportionate AI policy; enabling data lifecycle guidance; tolerant supervisory stance for good-faith AI failures that are disclosed and remediated.
- **Capacity**: AI skills building inside REs and inside RBI; frameworks for smaller REs to access AI on fair terms.

Risk-mitigation side:
- **Governance**: **board-approved AI policy** at each RE; AI inventory/registry of all models in use; model lifecycle governance (approval → testing → deployment → change control); independent validation; senior-management accountability; vendor/third-party AI risk clauses in contracts.
- **Protection**: consumer-protection framework for AI-driven products; **disclosure to customers when they interact with AI**; grievance redressal extended to AI decisions (ombudsman coverage); bias/fairness audits; data-privacy alignment with DPDP.
- **Assurance**: AI audit framework (internal + external); **incident reporting** for AI failures; red-teaming; AI-related **disclosures in annual reports** (governance framework, adoption areas, consumer-protection measures); kill-switch / business-continuity fallback when a model misbehaves.

### 1.3 Status through mid-2026

- No binding "FREE-AI Directions" circular has been issued yet; RBI is following a phased "learn–adapt–implement" approach (see scrut.io analysis: https://www.scrut.io/post/rbi-framework-for-responsible-and-ethical-enablement-of-artificial-intelligence).
- RBI's **Financial Stability Report (June 2026)** flags rapid AI advances as a force reshaping financial-system risk.
- Media/industry reports (June 2026) say RBI has asked banks for a **board-approved AI/cyber gap assessment and time-bound action plan by 30 June 2026** (e.g., https://rmaindia.org/rbi-asks-banks-to-assess-ai-risk-gaps/ — *industry report, not verified against an RBI circular number; do not over-claim in the pitch, phrase as "RBI has reportedly asked banks…"*).
- Safe claim for judges: *"RBI's FREE-AI report is the announced blueprint for forthcoming AI regulation; we built the 7 sutras in from day one."*

### 1.4 Sutra → demo feature map (use verbatim in decks)

| Sutra | Concrete product feature to demo |
|---|---|
| Trust is the Foundation | Immutable audit log of every AI recommendation/decision (who, what, when, model version, inputs hash) |
| People First | Human-in-the-loop: RM/credit-officer approval screen for consequential actions; customer can always reach a human; override button that logs the human's reason |
| Innovation over Restraint | Sandbox/pilot mode with guardrails, feature flags, capped exposure; documented pilot-learnings export |
| Fairness and Equity | Bias dashboard: approval/score distributions across gender/age/geography; periodic fairness test report artifact |
| Accountability | Model registry card (owner, version, validation date, vendor); "bank remains liable" banner in ops console; vendor-model provenance shown |
| Understandable by Design | Reason codes on every score/recommendation (e.g., SHAP top-5 factors in plain language); customer-facing "why am I seeing this?" explainer |
| Safety, Resilience, Sustainability | Kill-switch demo (disable model → rule-based fallback); drift monitor alert; incident log + simulated incident report |

---

## 2. RBI — Model Risk, Digital Lending, EWS, and Supporting Directions

### 2.1 Regulatory Principles for Management of Model Risks in Credit (draft circular, 5 Aug 2024)

- Draft circular released **5 August 2024**; comments closed 4 Sep 2024; **final directions still pending as of mid-2026** — treat the draft as the design standard. Official draft on rbi.org.in: https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4479 ; PDF copy: https://www.fidcindia.org.in/wp-content/uploads/2024/08/RBI-DRAFT-MANAGEMENT-OF-MODEL-RISK-IN-CREDIT-05-08-24.pdf ; analysis: https://taxguru.in/rbi/rbi-draft-circular-regulatory-principles-management-model-risks-credit.html
- Applies to all models used in **credit appraisal, borrower selection, pricing, risk management, credit-loss provisioning** — squarely covering Tracks 2, 3, 4.
- Key requirements:
  - **Board-approved model risk management policy** covering the entire model lifecycle.
  - Models must be **validated independently** (by a function not involved in development) **before deployment and after any material change**, plus periodic revalidation; validation covers assumptions, data accuracy, back-testing, outcome analysis.
  - **Documentation**: every model documented so a third party can understand design, assumptions, limitations.
  - **Vendor/third-party models**: RE remains fully responsible; contracts must permit RBI/external-expert evaluation of vendor models; no black-box exemption.
  - Timelines in draft: effective 3 months from issuance; existing models validated within 6 months.
- **Demo implication:** ship a one-page **"model card"** per model (purpose, data, features, validation metrics, back-test results, limitations, owner, version) + a validation-workflow screen.

### 2.2 RBI (Digital Lending) Directions, 2025 — consolidated

- Issued **8 May 2025**, consolidating the 2022 Digital Lending Guidelines and 2023 Default Loss Guarantee (DLG) guidelines. Official: https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12848&Mode=0 ; overview: https://www.argus-p.com/updates/updates/rbi-digital-lending-directions-2025-an-overview/
- Effective 8 May 2025; multi-lender-arrangement provisions from 1 Nov 2025; DLA reporting on RBI's **CIMS portal** from 15 Jun 2025.
- Relevant rules for Track 2 (lead-gen) and any lending front-end:
  - Loan disbursal/repayment only **directly between borrower's bank account and the RE** — no LSP pass-through.
  - **Key Facts Statement (KFS)** with APR before contract execution; **cooling-off period** (minimum 1 day) with penalty-free exit.
  - **Data**: LSP/DLA data collection must be **need-based, with explicit borrower consent**, auditable; **no access to phone contacts, call logs, media files** (one-time camera/mic/location access only for onboarding needs); borrower can revoke consent and demand deletion; explicit alignment with **DPDPA 2023**; **data stored on servers located in India** — if processed abroad, it must be deleted there and brought back within 24 hours.
  - In multi-lender aggregation (effective 1 Nov 2025), borrower must see a **digital view of all matching offers from all willing lenders**, with the **ranking/comparison metric disclosed** (no dark-pattern steering).
  - RE fully responsible for its Lending Service Providers (LSPs); LSP fees paid by RE, not borrower; **Default Loss Guarantee capped at 5%** of the loan portfolio, only from Companies-Act-incorporated LSPs/REs.
  - **Track-2 alert:** a lead-gen platform feeding a lender is an **LSP**, and any customer-facing lending app is a **DLA** that must be reported on RBI's CIMS portal (public directory) — due-diligence, contract and grievance-officer obligations attach.

### 2.3 Fraud EWS / Red-Flagging — Master Directions on Fraud Risk Management (15 Jul 2024)

- **RBI Master Directions on Fraud Risk Management in Commercial Banks (incl. RRBs) and AIFIs**, DOS.CO.FMG.SEC.No.5/23.04.001/2024-25, dated **15 July 2024** — one of **three parallel Master Directions issued the same day** (banks/AIFIs; NBFCs incl. HFCs; cooperative banks) — replaced the 2016 Master Direction on Frauds (rooted in the **"Framework for dealing with loan frauds", 7 May 2015**, which introduced EWS/RFA and the illustrative list of 40+ EWS indicators) and rescinded 36 circulars. Official: https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702 ; analysis: https://www.azbpartners.com/bank/master-directions-on-fraud-risk-management-in-banks-and-nbfcs/
- Directly the regulatory home of **Track 4 (EWS)**:
  - Banks must run a framework of **Early Warning Signals (EWS)** and **Red-Flagged Accounts (RFA)**, **integrated with the Core Banking Solution** for real-time transaction monitoring.
  - RFA to be reported to **CRILC** within **7 days**; fraud-or-not decision within **180 days** of red-flagging.
  - Board's **Risk Management Committee** oversees EWS/RFA; a Special Committee of the Board for monitoring high-value frauds.
  - **Natural-justice requirement** (post *SBI v. Rajesh Agarwal*, SC 2023): borrower must get a show-cause and hearing before being classified as fraud — i.e., an EWS system needs a **human decision + borrower-communication step**, not auto-classification.
- **Demo implication (Track 4):** EWS alert → evidence pack with reason codes → RFA recommendation → human committee screen → CRILC-report stub → 180-day clock tracker.

### 2.4 SMA / IRACP norms (context for Tracks 3 & 4)

- **Prudential Framework for Resolution of Stressed Assets** (7 Jun 2019): SMA-0 (1–30 days overdue), SMA-1 (31–60), SMA-2 (61–90); NPA at 90+ days. https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11580
- Clarified by circular of **12 Nov 2021** (day-end process, daily SMA/NPA stamping) and the **Master Circular on IRACP norms** (updated annually, latest consolidation 1 Apr 2025 on rbi.org.in).
- **Demo implication:** an MSME health score / EWS should show predicted **days-to-SMA-1/SMA-2** and align labels to SMA buckets — judges from the bank will instantly recognize the vocabulary.

### 2.5 IT Governance Direction 2023

- **RBI Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices**, dated **7 November 2023**, effective **1 April 2024** (rbi.org.in Master Directions). Requires board-level IT Strategy Committee, IT risk framework, vendor/outsourcing controls, audit trails, DR/BCP.
- Companion: **RBI Master Direction on Outsourcing of IT Services** (10 Apr 2023) — any hackathon SaaS/cloud component delivered to a bank becomes a regulated IT outsourcing arrangement (audit rights, exit plans, data location).

### 2.6 Payments data localisation (6 Apr 2018)

- **Storage of Payment System Data**, DPSS circular dated **6 April 2018**: entire payment-system data must be stored **only in India** (end-to-end transaction data); data processed abroad must be brought back within 24 hours. https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11244
- Combined with V-CIP data-in-India rule (§6) and DPDP localisation power for SDFs (§5): **demo claim — "all data and models hosted in India."**

---

## 3. SEBI — Advice, Distribution, and AI Accountability

### 3.1 Investment Advisers Regulations 2013 + 2024/25 amendments

- **SEBI (Investment Advisers) Regulations, 2013** — consolidated text as amended to 16 Dec 2024: https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-december-16-2024-_90151.html
- **Second Amendment Regulations, 2024** (gazetted **16 Dec 2024**): https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-second-amendment-regulations-2024_89980.html
  - New **part-time investment adviser** category (max 75 clients); relaxed qualification (graduate + NISM certifications, experience requirement removed); net-worth requirement replaced by a deposit-based requirement; **dual registration as IA + Research Analyst** permitted.
  - Operationalised by SEBI circular **"Guidelines for Investment Advisers", 8 Jan 2025** (fee limits, agreement terms, compliance) — see https://taxguru.in/sebi/sebi-updates-guidelines-investment-advisers-2025.html
- Core IA obligations that bind an AI advisor equally: **fiduciary duty, risk profiling, suitability assessment, fee-only (no commissions on advised products), record-keeping of advice for 5 years, annual audit**.

### 3.2 Robo-advisory legal status

- There is **no separate robo-advice licence**. Reg. 2(1)(l) defines investment advice as advice "through any means of communication"; SEBI has clarified IA Regulations apply **technology-neutrally** — a robo/AI adviser must sit inside a registered IA (or the bank's IA-registered arm) and meet the *same* risk-profiling, suitability and record-keeping duties. The Jan 2025 IA guidelines expressly cover use of AI tools by IAs: **the IA is solely responsible for advice given using AI**, and must disclose AI use to clients.
- IDBI Bank context: banks typically hold MF-distribution (AMFI ARN) and corporate-agency licences, not IA registration — see §3.4 for the distribution route, which changes what the avatar may *say*.

### 3.3 SEBI's AI/ML rulebook timeline (Track 1's core compliance story)

| Date | Instrument | Effect |
|---|---|---|
| 4 Jan 2019 | Circular SEBI/HO/MIRSD/DOS2/CIR/P/2019/10 — **Reporting of AI/ML applications** by stock brokers & DPs | Quarterly reporting of any AI/ML system offered/used |
| 31 Jan 2019 | Parallel circular for MIIs (exchanges, depositories) | Same reporting for market infrastructure |
| 9 May 2019 | Circular SEBI/HO/IMD/DF5/CIR/P/2019/63 for **Mutual Funds/AMCs** | Same reporting for AMCs |
| 13 Nov 2024 | **Consultation paper** on assigning responsibility for AI use by regulated entities (https://corporate.cyrilamarchandblogs.com/2024/12/sebis-proposed-new-amendments-on-usage-of-ai-tools-by-regulated-entities/) | Proposed liability amendments |
| **10 Feb 2025** | **SEBI (Intermediaries) (Amendment) Regulations, 2025** — new **Reg. 16C** (https://www.sebi.gov.in/legal/regulations/feb-2025/securities-and-exchange-board-of-india-intermediaries-amendment-regulations-2025_91809.html) | Regulated entity using AI/ML — in-house **or vendor-procured** — is **solely responsible** for (a) privacy, security, integrity of investor/stakeholder data, and (b) **all outputs** of the AI it relies on. Parallel amendments to Stock Exchanges/Clearing Corps and Depositories regulations. Analysis: https://www.scconline.com/blog/post/2025/02/11/sebi-introduces-concept-of-ai/ |
| 20 Jun 2025 | **Consultation paper "Guidelines for Responsible Usage of AI/ML in Indian Securities Markets"** (https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html) | Proposes 5-principle framework: governance & human oversight (internal AI committee, model documentation, **audit trail of AI decisions ≥5 yrs**), investor protection & disclosure (**tell clients when AI is used in advice/distribution**), testing (pre-deployment + continuous, shadow testing), fairness/bias controls, data privacy & cybersecurity (breach reporting). Tiered: lighter regime for purely internal AI; full regime when AI affects customers. |

**What Track 1 must therefore demo:** IDBI (as intermediary/distributor) owns every avatar utterance → AI-usage disclosure at session start → decision/audit log with model version → human escalation path → documented testing evidence.

### 3.4 Advice vs distribution vs execution-only (what the avatar may legally do)

- **Investment Adviser (IA)**: fee-only fiduciary advice; full suitability duty (§3.1).
- **Research Analyst (RA)**: SEBI (Research Analysts) Regulations 2014 — general, non-personalised recommendations; 2024/25 amendments relaxed entry and allowed dual IA/RA registration.
- **MF Distributor (AMFI ARN)**: registered with AMFI under SEBI's 2012 distributor framework; earns commissions; may give **"incidental advice"** limited to the products distributed (IA Regs reg. 4 exemption). Each human/entity needs ARN + EUIN. Bank distribution arms live here. An avatar working under the bank's ARN must stay within **product-appropriateness (suitability-lite)** and may not present itself as an unbiased adviser; commission disclosure required.
- **Execution Only Platform (EOP)**: SEBI circular **13 Jun 2023** (effective 1 Sep 2023) for platforms transacting in **direct MF plans**: https://www.sebi.gov.in/legal/circulars/jun-2023/regulatory-framework-for-execution-only-platforms-for-facilitating-transactions-in-direct-plans-of-schemes-of-mutual-funds_72479.html — Category 1 (AMC agent, AMFI-registered) or Category 2 (investor agent, registered as stock broker). EOPs may **not** advise.
- **Other Track-1 products:** insurance → IRDAI corporate agency (§4); **NPS** → PFRDA (Point of Presence) Regulations 2018 (banks as PoPs) and PFRDA (Retirement Adviser) Regulations 2016 for NPS advice; **RBI Floating Rate Savings Bonds** → distributed by agency banks / RBI Retail Direct (no separate advice licence, but fair-dealing norms apply).
- **Design consequence:** the avatar needs a **"regulatory persona" switch** — distributor mode (suitability + commission disclosure) vs advisory mode (only if routed through an IA-registered arm) — and must label which mode it is in. Showing that switch is a strong judge-facing feature.

## 4. IRDAI — Bancassurance, Online Sale, Misselling, Bima Sugam

### 4.1 Corporate-agent (bancassurance) limits

- Banks distribute insurance as **corporate agents** under the IRDAI (Registration of Corporate Agents) Regulations, 2015, as amended by the **IRDAI (Insurance Intermediaries) (Amendment) Regulations, 2022** (gazetted 2022): a corporate agent may tie up with **up to 9 life + 9 general + 9 health insurers** (composite agents up to 27 tie-ups), up from 3 per line. Sources: https://taxguru.in/corporate-law/irdai-insurance-intermediaries-amendment-regulations-2022.html ; https://cafemutual.com/news/insurance/25112-banks-can-have-tie-ups-with-9-insurers-imfs-can-have-6-tie-ups-irdai ; regs text: https://www.theactuaryindia.org/assets/files/news/IRDAI%20(Insurance%20intermediaries)%20(Amendment)%20Regulations,%202022.pdf
- Consequence for Track 1: the avatar recommends only from the bank's **empanelled panel (≤9 per line)** and must **disclose the panel and the commission basis** — an honest "we can only offer these insurers" screen is itself a compliance feature.

### 4.2 Online sale — ISNP

- **IRDAI Guidelines on Insurance e-commerce** (Ref: IRDA/INT/GDL/ECM/055/03/2017, **9 March 2017**) create the **Insurance Self-Network Platform (ISNP)** regime: any digital platform selling/servicing insurance (including a bank's app or an AI avatar journey) must be registered as an ISNP with board-approved conduct, security and grievance standards (irdai.gov.in → Guidelines).

### 4.3 Misselling / suitability norms (what an AI recommender must respect)

- **IRDAI (Protection of Policyholders' Interests, Operations and Allied Matters of Insurers) Regulations, 2024** (gazetted 20 Mar 2024) + **Master Circular on PPHI (5 Sep 2024)**: mandatory **needs/suitability analysis** before recommending (esp. life/ULIP), a standardised **Customer Information Sheet**, **free-look period of 30 days** for all policies, benefit illustrations at prescribed rates, ban on forced bundling of insurance with banking products, misselling penalties on both insurer and corporate agent (irdai.gov.in → Regulations/Master Circulars).
- Corporate agents' conduct norms prohibit inducement and require recommendation records to be preserved — an AI avatar's insurance suggestion needs a **stored suitability questionnaire + recommendation rationale**.

### 4.4 Bima Sugam status (2026)

- **Bima Sugam — Insurance Electronic Marketplace Regulations, 2024** approved **March 2024** (under Insurance Act 1938 / IRDAI Act 1999); a not-for-profit company (industry-owned) runs the marketplace for buying, selling, servicing and claims.
- Status mid-2026: portal soft-launched **17 September 2025**; IRDAI Chairman **Ajay Seth** (June 2026) — initial products to go live by **end-September 2026**, phased: **motor first (June–July 2026), health (August), pure term life (September 2026)**. Source: https://www.business-standard.com/finance/insurance/bima-sugam-to-launch-initial-products-by-sept-end-irdai-chairman-seth-126063000744_1.html
- Pitch angle: design the avatar's insurance module to be **Bima Sugam-ready** (marketplace API abstraction) — timely, judge-friendly detail.

---

## 5. DPDP Act 2023 + DPDP Rules 2025

### 5.1 Instruments and timeline

- **Digital Personal Data Protection Act, 2023** — assented **11 Aug 2023**. Text: https://www.meity.gov.in/writereaddata/files/Digital%20Personal%20Data%20Protection%20Act%202023.pdf
- **Draft DPDP Rules** published for consultation **3 Jan 2025** (MeitY). **Final DPDP Rules, 2025 notified 14 Nov 2025**: PIB summary https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf
- **Phased enforcement** (https://www.india-briefing.com/news/india-dpdp-compliance-timeline-enforcement-2026-27-44740.html/):
  - **Nov 2025 (immediate)**: definitional rules + Data Protection Board provisions (Rules 1, 2, 17–21); Board operational, complaint mechanism live.
  - **Nov 2026 (+12 months)**: Consent Manager **registration** provisions (Rule 4) take effect.
  - **13 May 2027 (+18 months)**: all substantive obligations — itemised notice/consent standards, security safeguards, 72-hour-style breach notification to Board + affected principals, retention/erasure, data-principal rights, verifiable parental consent, SDF duties — fully in force. No further grace period expected; banks are expected to be early movers.

### 5.2 Core obligations relevant to the hackathon

- **Notice & consent** (Act §5–6; Rules): consent must be **free, specific, informed, unconditional, unambiguous, by clear affirmative action**; notice must be a **standalone, plain-language document**, itemising each purpose and the personal data collected, with the **option to view it in English or any of the 22 Eighth-Schedule languages**, and a link to withdraw consent (as easy as giving it) and to complain to the Data Protection Board.
- **Purpose limitation & data minimisation**: process only data necessary for the specified purpose; erase when purpose served or consent withdrawn.
- **Legitimate uses (§7)** cover employment, statutory functions, emergencies — **not marketing**. Behavioural profiling for cross-sell (Track 2) and alternate-data scoring of individuals/proprietors (Track 3) **need consent**.
- **Children (§9)**: no tracking, behavioural monitoring or targeted advertising directed at children; verifiable parental consent.
- **Significant Data Fiduciary (SDF)** — large banks like IDBI will almost certainly be notified as SDFs: appoint a **Data Protection Officer (in India, reporting to board)**, **annual Data Protection Impact Assessment (DPIA)** + annual independent data audit, **algorithmic due diligence** (verify that algorithmic processing does not risk data principals' rights — the DPDP hook for AI models), and possible **localisation** of notified data categories.
- **Consent Managers** (Act §6(7)–(9); Rule 4 + First Schedule): board-registered intermediaries through whom consent can be given/managed/withdrawn — must be an **Indian company with ≥₹2 crore net worth**, interoperable platform, data-blind (fiduciary–principal conduit). This deliberately mirrors RBI's **Account Aggregator** rail (Master Direction NBFC-AA, 2 Sep 2016): AAs are the working prototype of consent-managed data flow, and a demo that uses an **AA-style consent artefact** (purpose, data range, expiry, revocable) speaks both DPDP and RBI language at once.
- **Penalties** (Schedule): up to **₹250 crore** per violation for failure of security safeguards; ₹200 cr for breach-notification and children-related failures; ₹150 cr for SDF-obligation breaches; **₹50 cr residual tier** for other violations; violations can stack.

### 5.3 What a demo should show (DPDP-by-design)

1. **Consent screen** at data capture: itemised purposes with per-purpose toggles (e.g., "score my account data for a loan offer" separate from "marketing communications"), language switcher.
2. **Purpose tags in the data model**: every stored attribute carries `purpose`, `consent_id`, `retention_until`; queries filtered by purpose.
3. **Consent ledger**: append-only log of grants/withdrawals; withdrawal instantly gates processing (show a lead disappearing from the Track-2 funnel on withdrawal).
4. **Data-minimisation statement**: features used by the model listed; no contacts/media scraping (also a Digital Lending Directions rule).
5. **DPIA-lite one-pager** and an **algorithmic due-diligence note** for the model — SDF artefacts judges can hold.

---

## 6. Aadhaar / KYC Rails — What Tooling Is Legal

- **Aadhaar e-KYC for banks**: Aadhaar Act 2016 + **Aadhaar and Other Laws (Amendment) Act, 2019** + PMLA §11A permit banks (reporting entities notified by the government) to do **OTP/biometric Aadhaar e-KYC with informed consent**; voluntary use, offline verification (XML/QR) as alternative (uidai.gov.in).
- **KYC Master Direction**: RBI **Master Direction – Know Your Customer, 25 Feb 2016**, continuously amended: https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566
  - **V-CIP** (Video-based Customer Identification Process, introduced Jan 2020): live, secure, consent-based audio-visual interaction by an authorised official = equivalent to face-to-face onboarding; **all V-CIP data/recordings must be stored in systems located in India**; geo-tagging, liveness, random-question checks required.
  - **Amendment of 6 Nov 2024**: on re-KYC/periodic update, REs must **fetch records from CKYCR using the KYC Identifier** instead of re-collecting documents where nothing changed.
  - **RBI (KYC) (Amendment) Directions, 12 June 2025** (RBI/2025-26/53 DOR.AML.REC.31/14.01.001/2025-26): tiered/risk-based **re-KYC** — low-risk individuals get **1 year (or till 30 Jun 2026, whichever later)** to update while account stays operational; **Business Correspondents** may collect self-declarations (with biometric e-KYC authentication) for no-change/address-change re-KYC; **minimum 3 advance notices (≥1 physical letter)** before KYC falls due; updated FAQs 9 Jun 2025. Circular copy: https://www.fidcindia.org.in/wp-content/uploads/2025/06/RBI-UPATION-OF-KYC-12-06-25.pdf ; summary: https://www.zigram.tech/article/rbis-faqs-amendment-kyc-june-2025/
- **CKYCR/CERSAI**: Central KYC Records Registry under PML (Maintenance of Records) Rules, 2005 — Rule 9(1A) — managed by CERSAI; REs must upload KYC records and use the **14-digit KYC Identifier (KIN)** for retrieval. The **PML (Maintenance of Records) Amendment Rules, 2024** require REs to retrieve records via the KYC Identifier instead of re-collecting documents, and to **upload any additional/updated client information to CKYCR within 7 days**; the 2024-25 **CKYCRR 2.0** upgrade tightened search/access (masked KIN, explicit customer authorisation) after data-scraping concerns.
- **DigiLocker**: documents issued to DigiLocker are **deemed equivalent to originals** (IT Act r/w DigiLocker Rules 2016); KYC MD accepts equivalent e-documents (incl. digitally signed OVDs from DigiLocker) in V-CIP and regular onboarding.
- **PAN validation**: mandatory PAN or Form 60 for account opening; online PAN verification via Protean (NSDL e-Gov)/Income-tax API; PAN-Aadhaar linkage status check.
- **MNRL (Mobile Number Revocation List)**: TRAI-maintained list on DoT's **Digital Intelligence Platform (DIP)** of disconnected/revoked/fraud-flagged numbers (refreshed monthly; includes numbers taken on forged documents and numbers used in cybercrime). RBI circular **RBI/2024-25/105, "Prevention of financial frauds perpetrated using voice calls and SMS — Regulatory prescriptions and Institutional Safeguards", 17 Jan 2025**: REs must use MNRL to clean registered-mobile-number databases, monitor accounts linked to revoked numbers (mule-account risk), use **1600-xx** series for transactional/service calls and **140-xx** for promotional calls — compliance by **31 Mar 2025**. Sources: https://blog.digitap.ai/rbis-mobile-number-revocation-list-mnrl-mandate-digitap/ ; https://www.signzy.com/blogs/complying-rbis-new-mnrl-guidelines-11-key-questions-answered ; https://www.business-standard.com/finance/personal-finance/rbi-asks-banks-to-uses-tool-that-identifies-phone-numbers-to-curb-fraud-125012400390_1.html
- **UIDAI face authentication**: Aadhaar **FaceRD** app-based face-auth is a UIDAI-approved authentication modality (widely used in banking/pension since 2022-23) — legitimate for the avatar to authenticate a customer without biometric hardware.
- **Related for Track-2 outreach**: TRAI **TCCCPR 2018** (DLT registration, consent categories for commercial messaging) governs promotional SMS/calls to leads.

---

## 7. Credit Bureau Rules (CICRA) — Who May Pull What, When

- **Credit Information Companies (Regulation) Act, 2005 (CICRA)** + CIC Rules/Regulations 2006: credit reports may be furnished only to **specified users** (credit institutions that are members of the CIC, plus notified entities such as insurers, telecoms, SEBI-regd. brokers); every credit institution must be a member of **all four CICs** (CIBIL, Experian, Equifax, CRIF High Mark).
- **Purpose limits**: CICRA confines access to credit-decisioning/permitted purposes. India has no formal "soft-pull/hard-pull" statute, but in practice: a **lender's enquiry** on application is recorded and can affect scores ("hard"), while **consumer self-pulls and consented prescreen/monitoring enquiries** are not scored ("soft"). **Marketing prescreen requires explicit customer consent** — bureaus offer consent-based prequalification products; pulling a CIR for a person who hasn't applied or consented violates CICRA. Track 2 must show a **consent checkpoint before any bureau call**, and prefer **bank-internal data first, bureau only after consent**.
- **RBI, "Strengthening of customer service rendered by Credit Information Companies and Credit Institutions", 26 Oct 2023** (effective 26 Apr 2024):
  - CICs must **alert customers (SMS/email) whenever their CIR is accessed** by specified users; CIs must alert when default/DPD data is submitted.
  - **Free Full Credit Report** including score, **once a calendar year**, via an easy link on each CIC's website.
  - **Data-correction timelines**: complainant must be resolved within **30 days** (CI: 21 days to correct and send to CIC; CIC: 9 days), failing which **compensation of ₹100 per calendar day of delay** is payable to the complainant; CIs must give **reasons for rejecting** a correction request.
- **Fortnightly reporting**: RBI circular **8 Aug 2024** — credit institutions must report borrower data to CICs **fortnightly** (by the 7th day after each fortnight) **effective 1 Jan 2025**, halving the staleness of bureau data. https://www.business-standard.com/finance/news/rbi-mandates-fortnightly-credit-information-reporting-to-boost-transparency-124080801505_1.html ; https://www.xbrl.org/news/rbi-mandates-fortnightly-credit-information-reporting-to-boost-transparency/
- **Demo implications**: consent-gated bureau pull with the SMS-alert simulated; a "your data, your rights" screen (free annual report, dispute button, 30-day/₹100-per-day promise); for Tracks 3-4, show fortnightly-refresh awareness in feature engineering.

---

## 8. Compliance-by-Design Checklist — Track × Regulation × Demo Feature

*The centrepiece: each row = something judges can see on screen.*

### Track 1 — Avatar AI Wealth Advisor (MF / Insurance / NPS / RBI Bonds)

| # | Regulation (date) | Requirement | Concrete feature to demo |
|---|---|---|---|
| 1 | SEBI Intermediaries Amendment Regs 2025, Reg 16C (10 Feb 2025) | Intermediary solely liable for AI outputs & data | "AI oversight console": every avatar response logged with model version, retrievable by compliance officer |
| 2 | SEBI AI/ML consultation (20 Jun 2025) + Jan 2025 IA guidelines | Disclose AI use to client; ≥5-yr audit trail | Session-start disclosure banner "You are speaking with an AI assistant of IDBI Bank"; exportable audit log |
| 3 | SEBI IA Regs 2013 (as amended 16 Dec 2024) / AMFI distributor framework | Advice needs IA registration; distributor limited to incidental advice + suitability | "Regulatory persona" switch: distributor mode shows commission disclosure + product-appropriateness check; advisory-mode gated |
| 4 | SEBI reporting circulars (4 Jan / 9 May 2019) | Report AI/ML systems to SEBI | Auto-generated quarterly AI/ML reporting form stub |
| 5 | IRDAI corporate-agent regs (2022 amendment) | ≤9 insurers per line; panel disclosure | Panel-transparency screen: "we distribute for these N insurers"; commission basis shown |
| 6 | IRDAI PPHI Regs 2024 + Master Circular (5 Sep 2024) | Suitability analysis; 30-day free look; CIS | Stored suitability questionnaire → recommendation rationale; auto-generated Customer Information Sheet; free-look reminder |
| 7 | IRDAI ISNP guidelines (9 Mar 2017) | Digital insurance sale via registered platform | Architecture slide: avatar journeys run on bank's ISNP |
| 8 | RBI FREE-AI (13 Aug 2025) — People First / Understandable by Design | Human authority over consequential decisions; explainability | "Talk to a human" always visible; every recommendation carries plain-language reason codes; RM override with logged reason |
| 9 | DPDP Act 2023 + Rules (14 Nov 2025) | Itemised consent, purpose limitation | Consent screen with per-purpose toggles; vernacular notice; consent ledger |
| 10 | PFRDA PoP Regs 2018 (NPS) | NPS sale via registered PoP | NPS journey labelled as PoP service, risk disclosure |

### Track 2 — Retail-Lending Lead-Gen from Behavioural/Transaction Data

| # | Regulation (date) | Requirement | Concrete feature to demo |
|---|---|---|---|
| 1 | DPDP Act §6 + Rules (13 May 2027 deadline) | Marketing profiling needs specific consent; withdrawal as easy as grant | Per-purpose consent toggle "use my transactions for offers"; live demo of withdrawal removing lead from funnel; consent ledger |
| 2 | DPDP SDF obligations | DPIA + algorithmic due diligence | One-page DPIA + model due-diligence note as demo artefacts |
| 3 | RBI Digital Lending Directions 2025 (8 May 2025) | Need-based data, no contacts/media access, KFS, cooling-off | Data-map slide (only account/consented data); KFS with APR generated for accepted offer; 1-day cooling-off shown |
| 4 | RBI draft Model Risk circular (5 Aug 2024) | Board policy, independent validation, documentation | Propensity-model "model card" + validation report with back-test |
| 5 | CICRA 2005 + RBI CIC circular (26 Oct 2023) | Bureau pull only with consent; customer alerted | Consent checkpoint before bureau call; simulated SMS alert "your CIR was accessed" |
| 6 | RBI MNRL circular (17 Jan 2025) + TRAI TCCCPR 2018 | Scrub revoked numbers; 140-series for promos | MNRL scrub step in lead pipeline UI; outreach shown from 140-xx sender |
| 7 | FREE-AI — Fairness & Equity | No discriminatory targeting | Fairness dashboard: offer rates by gender/age/geo; excluded-features list (no caste/religion proxies) |
| 8 | FREE-AI — Understandable by Design | Explainable propensity | Reason codes per lead ("salary credit up 20%, rent debit stable"); RM sees *why* before calling |
| 9 | FREE-AI — People First | Human before customer contact | Leads queue for RM review; no fully automated solicitation |

### Track 3 — MSME Alternate-Data Health Score

| # | Regulation (date) | Requirement | Concrete feature to demo |
|---|---|---|---|
| 1 | RBI draft Model Risk circular (5 Aug 2024) | Lifecycle governance, independent validation, vendor-model liability | Model card + validation workflow screen; version registry; "bank-owned model" provenance |
| 2 | DPDP Act/Rules | Consent for proprietor/individual data (GST, account, utility) | Consent screen listing each alternate-data source with purpose tags; Account Aggregator-style consent artefact |
| 3 | RBI Account Aggregator framework (NBFC-AA Master Directions 2016) | Consented financial-data sharing rail | Fetch bank-statement data via AA consent flow (mock) instead of scraping |
| 4 | SMA/IRACP norms (7 Jun 2019 framework) | Standard stress vocabulary | Score output mapped to predicted SMA-0/1/2 probability bands |
| 5 | FREE-AI — Understandable by Design | Explainability to borrower and officer | Top-5 reason codes per score (GST filing gap, cash-flow seasonality); borrower-facing "improve your score" tips |
| 6 | FREE-AI — Fairness | No sectoral/regional bias | Bias check across sector/region/enterprise-size in validation report |
| 7 | RBI CIC directions (26 Oct 2023 / 8 Aug 2024) | Accurate, fresh bureau data; correction rights | Data-freshness stamp (fortnightly cycle); dispute-flow mock for wrong GST/bureau record |
| 8 | FREE-AI — People First | Score assists, not decides | Credit-officer screen: score + evidence → human sanction decision with override log |

### Track 4 — MSME Default-Prediction Early Warning System

| # | Regulation (date) | Requirement | Concrete feature to demo |
|---|---|---|---|
| 1 | RBI Master Directions on Fraud Risk Management (15 Jul 2024) | EWS integrated with CBS; RFA governance; CRILC in 7 days; 180-day decision | Alert → evidence pack → RFA recommendation → committee approval screen → CRILC report stub → 180-day countdown tracker |
| 2 | Natural justice (SC 2023, embedded in 2024 MD) | Borrower heard before fraud classification | Show-cause letter generator + borrower response tracking in workflow |
| 3 | SMA/IRACP + Prudential Framework (7 Jun 2019) | Daily stamping; SMA buckets | Portfolio heat-map by SMA bucket; days-to-SMA-2 prediction |
| 4 | RBI draft Model Risk circular (5 Aug 2024) | Validated, documented, back-tested model | EWS model card; back-test vs last 12 months of actual slippages |
| 5 | FREE-AI — Understandable by Design + Accountability | Explainable alerts, auditable pipeline | Every alert carries triggering signals (e.g., "LC devolvement + 40% drop in credits + statutory dues unpaid"); immutable alert-audit log |
| 6 | FREE-AI — Safety & Resilience | Fallback and drift control | Kill-switch to rule-based EWS (the 42 illustrative EWS signals in the MD annex); drift alert demo |
| 7 | DPDP | Purpose limitation on monitoring data | Monitoring restricted to loan-covenant purpose tags; no unrelated cross-use |
| 8 | RBI IT Governance MD (7 Nov 2023) | Audit trails, access control | Role-based access shown (maker-checker on alert closure) |

### Track 5 — Open Innovation (Reconciliation / KYC Ops)

| # | Regulation (date) | Requirement | Concrete feature to demo |
|---|---|---|---|
| 1 | RBI KYC MD (25 Feb 2016, amended to 12 Jun 2025) | V-CIP standards; risk-based re-KYC tiers; 3 advance notices | Re-KYC workbench: due-date tiers, notice scheduler (2 digital + 1 letter), V-CIP queue with India-hosted storage note |
| 2 | KYC Amendment (6 Nov 2024) — CKYCR-first | Fetch by KYC Identifier before asking customer | "CKYCR fetch" step in onboarding flow; only deltas requested from customer |
| 3 | KYC Amendment (12 Jun 2025) — BC-assisted re-KYC | BC self-declaration + biometric e-KYC | BC tablet flow mock: biometric auth → self-declaration → acknowledgment → bank-system update intimation |
| 4 | Aadhaar Act + PMLA §11A; DigiLocker Rules 2016 | Lawful e-KYC rails, deemed-original e-docs | Consent-first Aadhaar OTP e-KYC; DigiLocker document pull with issuer signature check; UIDAI FaceRD face-auth option |
| 5 | RBI MNRL circular (17 Jan 2025) | Scrub RMN database by 31 Mar 2025 | MNRL batch-scrub job with exception queue for accounts on revoked numbers (mule-risk flags) |
| 6 | Payments data localisation (6 Apr 2018) + IT Outsourcing MD (10 Apr 2023) | Data in India; auditable vendors | Architecture slide: India-region hosting, audit-rights clause noted |
| 7 | FREE-AI — Accountability + Assurance | AI in ops still audited | If AI does doc-matching/recon: match-confidence + reason shown; maker-checker for low-confidence matches; exception audit log |
| 8 | DPDP | Retention limits | Purge scheduler: KYC docs retention per PMLA (5 yrs post-relationship) with auto-erasure preview |

---

## 9. Master Document List (for the deck's "regulatory grounding" slide)

| Regulator | Instrument | Date | Link |
|---|---|---|---|
| RBI | FREE-AI Committee Report | 13 Aug 2025 | https://rbidocs.rbi.org.in/rdocs/PublicationReport/Pdfs/FREEAIR130820250A24FF2D4578453F824C72ED9F5D5851.PDF |
| RBI | Draft circular: Regulatory Principles for Management of Model Risks in Credit | 5 Aug 2024 | https://www.fidcindia.org.in/wp-content/uploads/2024/08/RBI-DRAFT-MANAGEMENT-OF-MODEL-RISK-IN-CREDIT-05-08-24.pdf |
| RBI | RBI (Digital Lending) Directions, 2025 | 8 May 2025 | https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12848&Mode=0 |
| RBI | Master Directions on Fraud Risk Management (Banks & AIFIs) | 15 Jul 2024 | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702 |
| RBI | Prudential Framework for Resolution of Stressed Assets (SMA) | 7 Jun 2019 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11580 |
| RBI | Master Direction — IT Governance, Risk, Controls & Assurance | 7 Nov 2023 (eff. 1 Apr 2024) | rbi.org.in → Master Directions |
| RBI | Storage of Payment System Data (localisation) | 6 Apr 2018 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11244 |
| RBI | Master Direction — KYC (with amendments incl. 6 Nov 2024, 12 Jun 2025) | 25 Feb 2016+ | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566 |
| RBI | KYC (Amendment) Directions 2025 | 12 Jun 2025 | https://www.fidcindia.org.in/wp-content/uploads/2025/06/RBI-UPATION-OF-KYC-12-06-25.pdf |
| RBI | MNRL / fraud-calls circular | 17 Jan 2025 | rbi.org.in (see https://www.signzy.com/blogs/complying-rbis-new-mnrl-guidelines-11-key-questions-answered) |
| RBI | CIC customer-service circular (₹100/day, free report, alerts) | 26 Oct 2023 (eff. 26 Apr 2024) | rbi.org.in → Notifications |
| RBI | Fortnightly credit reporting to CICs | 8 Aug 2024 (eff. 1 Jan 2025) | https://www.xbrl.org/news/rbi-mandates-fortnightly-credit-information-reporting-to-boost-transparency/ |
| SEBI | IA Regulations 2013 (consolidated to 16 Dec 2024) | 2013/2024 | https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-december-16-2024-_90151.html |
| SEBI | IA (Second Amendment) Regulations 2024 | 16 Dec 2024 | https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-second-amendment-regulations-2024_89980.html |
| SEBI | Intermediaries (Amendment) Regulations 2025 — Reg 16C AI liability | 10 Feb 2025 | https://www.sebi.gov.in/legal/regulations/feb-2025/securities-and-exchange-board-of-india-intermediaries-amendment-regulations-2025_91809.html |
| SEBI | EOP framework circular | 13 Jun 2023 | https://www.sebi.gov.in/legal/circulars/jun-2023/regulatory-framework-for-execution-only-platforms-for-facilitating-transactions-in-direct-plans-of-schemes-of-mutual-funds_72479.html |
| SEBI | Consultation: Responsible AI/ML usage in securities markets | 20 Jun 2025 | https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html |
| SEBI | AI/ML reporting circulars (brokers/DPs; MIIs; AMCs) | 4 Jan / 31 Jan / 9 May 2019 | sebi.gov.in → Circulars |
| IRDAI | Insurance Intermediaries (Amendment) Regulations 2022 (9 insurers/line) | 2022 | https://www.theactuaryindia.org/assets/files/news/IRDAI%20(Insurance%20intermediaries)%20(Amendment)%20Regulations,%202022.pdf |
| IRDAI | ISNP / insurance e-commerce guidelines | 9 Mar 2017 | irdai.gov.in → Guidelines |
| IRDAI | PPHI Regulations 2024 + Master Circular | 20 Mar / 5 Sep 2024 | irdai.gov.in → Regulations |
| IRDAI | Bima Sugam Marketplace Regulations 2024; go-live Sept 2026 | Mar 2024 / 2026 | https://www.business-standard.com/finance/insurance/bima-sugam-to-launch-initial-products-by-sept-end-irdai-chairman-seth-126063000744_1.html |
| MeitY | DPDP Act 2023 | 11 Aug 2023 | https://www.meity.gov.in/writereaddata/files/Digital%20Personal%20Data%20Protection%20Act%202023.pdf |
| MeitY | DPDP Rules 2025 (final) | 14 Nov 2025 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf |
| Parliament | CICRA 2005 | 2005 | indiacode.nic.in |

### Open items to verify closer to the event
1. Whether RBI has issued **final** Model Risk in Credit directions (check rbi.org.in → Notifications).
2. Whether the June 2025 SEBI AI/ML consultation has become a **final circular** (check sebi.gov.in → Circulars, "AI").
3. Any **FREE-AI implementation circular** post-June 2026 (check RBI Statements on Developmental and Regulatory Policies from each MPC).
4. Exact DPDP **SDF notification** — has MeitY notified banks as SDFs yet?
5. The reported RBI "AI gap assessment by 30 Jun 2026" directive — confirm against an official circular number before citing to judges.

