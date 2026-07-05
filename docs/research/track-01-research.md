# Track 01 — Digital Wealth Management: Research Reference

> Research compiled 2026-07-04 for IDBI Innovate 2026, Track 1 (avatar-based AI wealth advisor in the bank's mobile app; hybrid AI + human-RM model; Mass/HNI/NRI segments; MF + Insurance + NPS + RBI Bonds; multilingual pan-India).
> Every load-bearing claim carries an inline URL. Claims from general industry knowledge (not re-verified this session) are marked *(unverified)*.

---

## 1. Domain Landscape: India Wealth-Tech & Robo-Advisory

### 1.1 Market size and momentum

- Robo-advisor AUM in India is projected at **~US$23B in 2025**, growing ~4.3%/yr to ~US$27.2B by 2029 ([Statista](https://www.statista.com/outlook/fmo/wealth-management/digital-investment/robo-advisors/india)).
- India robo-advisory *software* market: ~US$345M (2025) → ~US$1.4B by 2035 ([Market Research Future](https://www.marketresearchfuture.com/reports/india-robo-advisory-software-market-61728)).
- Average robo-advisory fee in India ≈ **0.5% of AUM vs 1–2% for traditional advisors** ([Inventiva overview](https://www.inventiva.co.in/trends/robo-advisors-india-2025/)).
- Venture money is returning to wealth-tech: PowerUp Money raised **US$12M Series A (Dec 2025, Peak XV/Accel/Blume/8i)**; Stable Money raised in Feb 2026 ([India Fintech substack analysis](https://indiafintech.substack.com/p/indias-capital-markets-the-financialization)). The same analysis argues incumbents (INDmoney, Scripbox, Kuvera) sit on **older tech stacks, opening a window for AI-native challengers** — exactly the pitch position for this track.

### 1.2 Who's who (fintechs)

| Player | Model | Notes |
|---|---|---|
| **INDmoney (INDwealth)** | Super-app: net-worth aggregation, direct MF, US stocks | Tracks holdings across institutions (early AA adopter) *(unverified detail)* |
| **Scripbox** | Goal-based advisory + regular-plan distribution | "Goal-based investing for life stages" ([Decentro roundup](https://decentro.tech/blog/top-wealthtech-companies/)) |
| **Kuvera** | Free direct-plan platform | Acquired by CRED (~2022) *(unverified)*; zero-commission model made standalone monetization hard |
| **ET Money** | Automated MF recommendations, "Genius" subscription advisory | Acquired by 360 ONE WAM (2024) *(unverified)* |
| **Zerodha Coin** | Execution-only direct MF (broker platform) | The archetype of the SEBI EOP/broker route — *no advice*, pure execution |
| **Fi Money / Jupiter** | Neobanks bolting on wealth (MF, deposits, jars/goals) | UX benchmark for "salary account → SIP" nudges |
| **PowerUp Money, Dezerv, Wealthy, Fisdom** | Newer advisory/PMS-adjacent plays | Signal that "advice", not just execution, is the new battleground |

### 1.3 What banks have shipped

- **HDFC Bank SmartWealth** — dedicated wealth app (MF in regular plans via bank's distribution arm, goal planning, portfolio view). Bank acts as **distributor**, not RIA *(unverified detail; verify current scope before citing in pitch)*.
- **SBI YONO** — wealth/investments section inside super-app; SBI also runs a dedicated wealth RM programme for HNI ("SBI Wealth") *(unverified)*.
- **Bank of Baroda** — the **closest precedent to this track**: BoB launched GenAI assistant **"Aditi", a virtual relationship manager presented as a digital avatar** with **audio, video and chat support, 24×7, multilingual**, alongside the "ADI" chatbot and a GenAI knowledge assistant for employees ([BoB press release, May 2024 (PDF)](https://bankofbaroda.bank.in/-/media/project/bob/countrywebsites/india/content/media/press-releases/2024/24-09/adopts-generative-ai-to-transform-customer-experience-and-employee-efficiency-17-05.pdf); [coverage](https://cxovoice.com/bank-of-baroda-adopts-genai-to-enhance-its-digital-banking-operations/); live at [adi.bankofbaroda.bank.in](https://adi.bankofbaroda.bank.in/)).
- **Union Bank of India** — UVA voice assistant (Alexa skill) + UVConn WhatsApp banking ([Qorus innovation entry](https://www.qorusglobal.com/innovations/28423-union-virtual-connect-uvconn-whatsapp-banking-union-voice-assistant-uva-voice-banking); [Union Bank app services](https://www.unionbankofindia.bank.in/en/listing/app-banking)).
- **IndusInd** — IndusAssist on Alexa for transactions ([case study](https://www.gupshup.ai/resources/case-studies/induslnd-bank-leverages-omnichannel-conversational-support/)).
- Globally: NatWest "Cora" experimented with a Soul Machines **digital human** face as early as 2018 ([PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2018/cora-natwest-soul-machines-ai-avatar-digital-humans/)); Bank of America's Erica proved voice+chat assistant scale *(unverified)*.

**Implication for the pitch:** no Indian bank has yet shipped an avatar that *advises and transacts wealth products end-to-end with an RM handoff*. BoB's Aditi is service-oriented (queries), not suitability-driven advisory. That's the whitespace.

### 1.4 What failed and why (lessons)

- **Pure-play robo-advisors struggled to monetize**: Indian retail won't pay standalone advice fees; free direct-plan platforms (Kuvera, ET Money pre-acquisition) had thin revenue → most exited via acquisition (Kuvera→CRED, ET Money→360 ONE, Goalwise→Niyo, Clearfunds→MobiKwik) *(consolidation pattern; individual deals unverified this session)*.
- **SEBI RIA regime is heavy**: qualification/net-worth/audit requirements and the client-level segregation of advice vs distribution kept registered IA count low (~1,300 nationally) *(unverified)* — which is precisely why the **bank-distributor + AI hybrid** framing (not "AI RIA") is the pragmatic route.
- **Robo ≠ engagement**: static questionnaires + annual rebalancing emails don't retain mass users; conversational, event-driven engagement (salary credit detected → SIP nudge) is the differentiator the AMA clarifications point to.
- **Bancassurance mis-selling** is a documented regulatory sore point (IRDAI/FinMin criticism of banks pushing insurance to meet targets — see §2.4). An AI that *logs suitability rationale* turns this liability into a pitch strength.

---

## 2. Regulatory Landscape (the section judges from a bank will probe)

### 2.1 SEBI Investment Adviser vs Distributor vs Execution-Only — what an AI can legally say/do

Three legal postures exist for MF-touching platforms:

1. **SEBI-Registered Investment Adviser (RIA)** under the [SEBI (Investment Advisers) Regulations, 2013](https://www.sebi.gov.in/legal/regulations/feb-2023/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-february-07-2023-_69215.html): may give personalized, fee-based advice; must do **risk profiling and suitability assessment** (Regs. 16–17), keep records, follow the [2020 Guidelines for Investment Advisers](https://www.sebi.gov.in/legal/circulars/sep-2020/guidelines-for-investment-advisers_47640.html). **Robo-advisory falls squarely under IA regulations** — automated advice tools are treated as investment advice ([SEBI IA FAQs](https://www.sebi.gov.in/sebi_data/attachdocs/1424862077270.pdf); [analysis](https://medium.com/@rahul.goyl/do-robo-advisors-need-to-register-with-sebi-895f2eeba717)).
2. **Mutual Fund Distributor (ARN holder, AMFI-registered)**: may provide only **"basic advice incidental to distribution"** limited to the MF products distributed ([SEBI IA FAQs](https://www.sebi.gov.in/sebi_data/attachdocs/1424862077270.pdf)). Banks (including IDBI Bank) typically distribute MFs under an ARN as corporate distributors. Distributors earn trail commission on **regular plans** and must still follow AMFI's product-suitability code.
3. **Execution Only Platform (EOP)** — [SEBI circular, June 13 2023](https://www.sebi.gov.in/legal/circulars/jun-2023/regulatory-framework-for-execution-only-platforms-for-facilitating-transactions-in-direct-plans-of-schemes-of-mutual-funds_72479.html), effective Sept 1 2023: digital platforms transacting **direct plans** must register as **Category 1 EOP** (agent of AMCs, AMFI-registered — [AMFI guidelines](https://www.amfiindia.com/eops/amfi-guidelines)) or **Category 2 EOP** (agent of investor, stock-broker via exchange platforms). EOPs give **no advice** ([AZB summary](https://www.azbpartners.com/bank/sebi-introduces-comprehensive-framework-on-execution-only-platforms-for-transactions-in-direct-plans-of-mf-schemes/)).

**How the hackathon's hybrid maps on:**
- The bank already holds an MFD/corporate-distributor posture → the AI avatar can legally do **suitability-based "incidental advice" + direct transaction of the MFs it distributes** (this is the "AI advises + transacts vanilla" leg). Asset-allocation education + scheme suggestion from a bank-approved recommendation list = distributor-compatible.
- Anything crossing into holistic, fee-based, portfolio-level advice (esp. HNI) → **generate a lead for the human RM / bank's advisory arm** (the "regulated → RM" leg). This is not just the AMA instruction — it is the compliance-clean architecture.
- Frame the recommendation engine as producing suggestions from a **bank-curated, product-committee-approved scheme universe**, with the AI doing suitability *matching*, not independent research advice.

### 2.2 SEBI's AI rules (2024–2026) — the accountability regime

- **Feb 2025 amendments** to SEBI's intermediary regulations inserted **Regulation 16C-type provisions making the regulated entity solely responsible for outputs of any AI/ML tools it uses** — whether built in-house or procured from vendors — covering data privacy/security, integrity of AI outputs, and legal compliance ([IndiaLaw summary](https://www.indialaw.in/blog/securities-law/sebis-2025-ai-ml-framework-harmonising-market-oversight/); [Lexology: "Regulated Entities Responsible for Output of AI Usage"](https://www.lexology.com/library/detail.aspx?g=f2e36044-cc40-4c8f-8e74-79141d32031e)). **Translation: IDBI Bank is liable for what the avatar says.** Guardrails are not optional.
- **June 20 2025 consultation paper — "Guidelines for Responsible Usage of AI/ML in Indian Securities Markets"** ([SEBI](https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html)) proposes a framework on pillars of **ethics, accountability, transparency, auditability, data privacy, fairness**, requiring: skilled internal teams for human oversight, model testing/monitoring, fallback plans, vendor agreements, independent audits, disclosure to clients when AI is used, and **periodic reporting of AI/ML model accuracy to SEBI** ([IndiaCorpLaw analysis](https://indiacorplaw.in/2025/07/16/from-algorithms-to-accountability-analysing-sebis-ai-ml-governance-framework/); [HNLU critique of the liability design](https://hnluccls.in/2025/10/03/sebis-ai-liability-regulation-accountability-and-auditability-concerns/)).
- Since ~2019 SEBI has also required **quarterly AI/ML system reporting** by intermediaries to exchanges *(pre-existing reporting regime; unverified circular numbers)*.
- **Design consequences for the build** (say these words to judges): every recommendation must emit a **suitability log** (inputs → risk profile → rule/model → recommendation → disclosure shown), conversations must be **auditable**, the model must be **explainable** ("recommended because: age 52 → conservative band; goal horizon 3y; surplus ₹15k/mo"), and there must be a **human-in-the-loop fallback** (the RM).

### 2.3 IRDAI — insurance leg

- Banks distribute insurance as **Corporate Agents** under IRDAI's Registration of Corporate Agents Regulations (2015, amended; consolidated 2024) ([regulation text (PDF)](https://financialservices.gov.in/beta/sites/default/files/2024-11/IRDAI(Regn%20of%20Corporate%20Agents)%20Regulations-2015.pdf); [guide](https://advisou.com/blog/irdai-corporate-agents-regulations/)).
- **Open architecture**: a corporate agent may tie up with **up to 9 insurers per line** (life/general/health); composite agents capped at **27 total arrangements** ([RMA India guide](https://rmaindia.org/irdai-bancassurance-regulations-india-guide/)). IDBI Bank distributes for multiple insurers (historically incl. its former JV Ageas Federal) *(unverified)*.
- 2024 consolidation + master circulars emphasize **board oversight, disclosure, policyholder protection, and suitability checks to prevent mis-selling**; commissions sit under the insurer's EoM limits ([Lexology distribution guide](https://www.lexology.com/library/detail.aspx?g=674a853f-e479-494b-9c2a-a7140b1dfb5a); [bancassurance overview](https://clevercoins.org/bancassurance-in-india/)). In 2025–26 IRDAI floated moving bancassurance from commissions to customer-paid transaction fees (proposal stage) — cite as "regulatory direction of travel against pushy selling".
- **Mapping**: insurance is squarely "regulated product" → the avatar should do **needs analysis + education + lead creation**, and route to a **licensed Specified Person / RM** for solicitation. (Only individuals who pass the IRDAI exam can solicit insurance on the corporate agent's behalf.) This keeps the demo clean: AI never "sells" a policy, it books an RM appointment with a pre-filled needs profile.

### 2.4 NPS / Pension leg

- Banks act as **Points of Presence (PoP)** under PFRDA (Point of Presence) Regulations, 2018 — IDBI Bank is a registered PoP; onboarding/contributions can be done digitally (eNPS-style flows) *(framework well-established; specifics unverified this session)*.
- PFRDA has designated the NPS **Central Recordkeeping Agencies (CRAs) as Financial Information Providers** in the Account Aggregator system, so NPS balances are fetchable via AA ([Sahamati resources](https://sahamati.org.in/account-aggregator-key-resources/)).
- Mapping: NPS is regulated but PoP onboarding is standardized/form-driven → treat as **AI-assisted journey with RM confirmation**, or keep it lead-only for the demo; the safe pitch line is "AI educates on NPS tax benefits (80CCD(1B)) and initiates the PoP journey; KYC/confirmation with the bank."

### 2.5 RBI Bonds leg (the true "vanilla" product)

- **Floating Rate Savings Bonds (FRSB) 2020 (Taxable)**: GoI bond, min ₹1,000, 7-year tenor, rate = **NSC + 35 bps, reset half-yearly; 8.05% for Jul–Dec 2025** ([Business Standard](https://www.business-standard.com/finance/personal-finance/rbi-keeps-interest-rate-on-floating-rate-savings-bonds-unchanged-at-8-05-125010200691_1.html); [BondScanner explainer](https://bondscanner.com/blog/rbi-floating-rate-bond)).
- Sold through **Receiving Offices**: SBI, nationalised banks, **IDBI Bank Ltd** (explicitly a designated receiving office), Axis, HDFC, ICICI ([HDFC Securities](https://www.hdfcsec.com/rbi-bond); [SBI](https://sbi.bank.in/web/personal-banking/investments-deposits/govt-schemes/rbi-bonds); [BoB](https://bankofbaroda.bank.in/investments/government-deposit-schemes/floating-rate-savings-bonds)). Also via RBI Retail Direct.
- **Mapping**: sovereign, no market risk of capital, bank is already a receiving office → this is the cleanest product for the **AI-transacts-directly** demo leg (alongside bank FDs/RDs, which are fully in-house). Recommend FRSB for the 50+ / conservative persona.

### 2.6 One-slide compliance matrix (use in deck)

| Product | Regulator | Bank's licence | AI can… | RM needed? |
|---|---|---|---|---|
| Bank FD/RD | RBI (bank's own) | — | Advise + execute | No |
| RBI FRSB 2020 | RBI/GoI | Receiving Office | Advise + execute | No |
| Mutual Funds | SEBI | AMFI ARN distributor | Incidental suitability advice + execute from approved list, full logging | Optional (complex/HNI → RM) |
| Insurance | IRDAI | Corporate Agent | Needs analysis + educate + **lead** | Yes (Specified Person solicits) |
| NPS | PFRDA | Point of Presence | Educate + initiate journey / **lead** | Confirmation step |
| PMS/AIF/bonds beyond FRSB (HNI) | SEBI | Referral | Educate + **lead** | Yes |

---

## 3. Conversational Avatar Technology

### 3.1 Real-time avatar options (hosted APIs)

| Option | What | Latency | Cost | Verdict for hackathon |
|---|---|---|---|---|
| **HeyGen LiveAvatar / Streaming API** | Photoreal streaming avatar over WebRTC | markets itself among fastest; interactive-grade | ~**$0.10–0.20/min** streaming ([HeyGen API pricing](https://www.heygen.com/api-pricing); [LiveAvatar intro](https://help.heygen.com/en/articles/12758516-introducing-liveavatar)) | Best photoreal option; free/cheap tier enough for a demo |
| **D-ID (Agents / Streaming)** | Real-time talking-head streams, agent framework | interactive-grade | Build tier from **$18/mo (~32 streaming min)** ([comparison](https://www.veed.io/learn/best-avatar-apis)) | Cheapest paid entry; good docs |
| **Anam.ai** | Conversational avatar specialist | claims **~180 ms** response ([Anam vs HeyGen](https://anam.ai/blog/anam-vs-heygen)) | trial credits | Impressive latency story if you want to name-drop |
| **Tavus** | Conversational video ("CVI") | claims **<500 ms** end-to-end ([roundup](https://www.toughtongueai.com/blog/best-virtual-avatar-solutions-2026/)) | credit-based | Alternative to Anam |

### 3.2 Open-source / self-hosted

- **SadTalker** (talking head from one image + audio): free, but **offline-oriented — not real-time**; heavy GPU compute per clip ([SadTalker overview](https://sadtalkerai.com/); hosted inference via [fal.ai](https://fal.ai/models/fal-ai/sadtalker)). Same story for EchoMimic/Hallo-class models *(unverified specifics)*. Use only for pre-rendered intro videos, not live conversation.
- **Live2D / Rive 2D rigs**: fully client-side, zero per-minute cost, deterministic latency. A Rive state machine (idle / listening / thinking / talking / happy / concerned) driven by simple **viseme or amplitude-based lip-sync** plus an emotion tag emitted by the LLM gives an "emotionally intelligent" 2D avatar — which the AMA explicitly said is acceptable. Research directions like RITA ([arXiv](https://arxiv.org/pdf/2406.13093)) confirm real-time interactive avatars remain nontrivial; 2D rigs sidestep the whole problem.

### 3.3 Latency & cost realism for a live demo

Target conversational loop ≤ ~2.5 s perceived: ASR (streaming, ~300–500 ms tail) → LLM first token (~0.5–1.5 s with a fast model) → TTS first audio chunk (~200–500 ms) → avatar mouth-sync (client-side ≈ 0 ms for 2D; +500 ms–1 s for hosted video avatars). **Recommended demo posture:** 2D Rive/Live2D avatar with streamed TTS (bulletproof, offline-safe, free) and optionally a HeyGen/D-ID photoreal mode as a "wow" toggle — with a recorded backup video in case venue Wi-Fi kills WebRTC.

---

## 4. Voice Stack for Indian Languages

| Provider | ASR | TTS | Languages | Pricing | Notes |
|---|---|---|---|---|---|
| **Sarvam AI** | Saarika (STT), Saaras (speech-translate) | **Bulbul v3** | 11+ Indic TTS, 22 STT (per marketing) | STT ~**₹30/hr**, TTS ~**₹15–30/10K chars**, ₹1,000 free credits ([pricing](https://www.sarvam.ai/api-pricing); [docs](https://docs.sarvam.ai/api-reference-docs/pricing)) | In a Josh Talks blind study (20k+ votes) **Bulbul v3 beat ElevenLabs and Cartesia** on Indic quality ([Bulbul v3 blog](https://www.sarvam.ai/blogs/bulbul-v3)). Indian company = sovereignty talking point for a PSU-adjacent bank |
| **ElevenLabs** | Scribe | Multilingual v3 | 70–90+ langs incl. Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Bengali… ([ElevenLabs India](https://elevenlabs.io/india)) | Free 10k credits; Starter $6/mo; Creator $22 ([pricing](https://elevenlabs.io/pricing)) | Best-known voices; Meesho runs 60k calls/day on it ([case](https://elevenlabs.io/india)) |
| **AI4Bharat / Bhashini** | IndicConformer/IndicWhisper | **IndicTTS** (13+ languages, open-source) | 22 scheduled languages via Bhashini APIs | **Free/near-free** (govt DPI; discounted commercial) ([AI4Bharat](https://models.ai4bharat.org/); [Indic-TTS repo](https://github.com/AI4Bharat/Indic-TTS); [Bhashini API docs](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage)) | **"Built on India's Bhashini DPI"** is a strong judge line for pan-India branch coverage |
| **Amazon Polly/Transcribe** | Transcribe (hi-IN + several Indic) | Polly (Hindi/Indian-English Neural; thin coverage beyond) | Limited Indic depth *(unverified current list)* | AWS-native | Only if you want a 100%-AWS story; quality trails Sarvam/ElevenLabs for Indic |

**Recommended stack:** Sarvam Saarika (ASR) + Sarvam Bulbul v3 (TTS) as primary — Indic-first quality, rupee pricing, code-mixed Hindi-English handling; Bhashini/AI4Bharat cited as the scale/cost path for 22 languages; ElevenLabs as fallback for English/premium voices. Industry pattern matches this split: commercial Indic models for high-touch conversations, AI4Bharat/Bhashini self-hosted for cost-sensitive scale ([Caller.Digital comparison](https://www.caller.digital/blog/open-source-voice-ai-india-sarvam-ai4bharat-bhasini-2026)).

---

## 5. LLM Orchestration (Amazon Bedrock + Claude)

- **Claude on Amazon Bedrock**: use the Messages API surface with `anthropic.`-prefixed model IDs (e.g. `anthropic.claude-sonnet-4-6`, `anthropic.claude-haiku-4-5`); the official SDKs ship a Bedrock client (`AnthropicBedrockMantle` in Python/TS). Tool use / function calling, streaming, prompt caching, structured outputs and extended thinking all work on Bedrock; server-side web search/code execution and Managed Agents do **not** — so run your own tool loop (that's what you want anyway for auditability). Reference pricing (first-party): Sonnet-class ~$3/M input, $15/M output; Haiku-class ~$1/$5 — cheap enough that a full demo day costs cents.
- **Architecture: one agent, typed tools.** Do a plain tool-use loop (SDK "tool runner" or manual loop) rather than heavyweight orchestration: every consequential action is a **dedicated tool with a JSON schema**, which is precisely what gives you the per-action audit log SEBI's AI framework wants. Use `strict: true` tool schemas so transaction parameters (amount, scheme code, mandate date) are guaranteed-valid JSON.
- **Guardrails**: Amazon **Bedrock Guardrails** provides configurable content filters, denied topics (e.g., "guaranteed returns", specific stock tips), PII redaction, and contextual-grounding checks, applied model-agnostically around the LLM *(AWS product; capabilities from general knowledge — verify console specifics)*. Layer it with: (a) a system-prompt compliance persona; (b) deterministic post-checks (regex/state machine that blocks "guaranteed/assured returns", forces the MF risk disclaimer on any scheme mention); (c) the human-in-the-loop RM tool for out-of-scope asks. This "3-layer guardrail" diagram is a judge-pleaser.
- **Latency plan**: Haiku-class model for chit-chat/language detection and intent routing; Sonnet-class for suitability reasoning and recommendation explanations; stream tokens straight into streaming TTS.
- **Multilingual**: Claude handles Hindi/Hinglish and major Indic languages natively for text; still translate UI chrome via a translation layer, and keep numerals/amounts in the user's language convention. For low-resource languages, pipeline = ASR→(Bhashini translate)→LLM(en)→(translate)→TTS.

---

## 6. Personalization & Recommendation Engine

### 6.1 Risk profiling & suitability (regulatory anchor)

- SEBI IA Regs require documented **risk profiling (client capacity + tolerance) and suitability of every advice** ([IA Regulations](https://www.sebi.gov.in/legal/regulations/feb-2023/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-february-07-2023-_69215.html)); mirror this even in distributor mode — it's the audit trail.
- Inputs per the AMA: **age band** (50+ → conservative tilt), goals (short/long), **sparable amount** (income minus committed outflows from txn history), spending pattern, existing holdings (in-bank + via AA), segment (Mass/HNI/NRI).
- Compute a two-axis profile: **capacity** (surplus ratio, wealth, dependents, age) × **willingness** (3–5 conversational questions, not a 25-question form — the avatar asks them naturally). Map to 5 bands (Conservative → Aggressive). NRI adds FEMA/FATCA flags (US/Canada NRIs are restricted by many AMCs *(unverified)*), and repatriability (NRE vs NRO) considerations.

### 6.2 Goal-based investing framework

Standard, defensible math the avatar can *show*: goal corpus = FV(target, inflation); required SIP = PMT(expected return by asset mix, months). Asset-class allocation by horizon × risk band (e.g., <3y → debt/FRSB/FD; 3–7y → hybrid/balanced; >7y → equity-heavy with glide path). Age-based baseline (100 − age in equity) adjusted by band — simple, explainable, and matches the AMA's "recommend at asset-class level AND specific schemes."

### 6.3 Scheme recommendation approaches

| Approach | How | Pros | Cons |
|---|---|---|---|
| **Rule-based suitability matrix** (recommended core) | Bank-approved scheme list × {risk band, horizon, goal type, amount}; rank by rating/consistency filters | Deterministic, explainable, compliance-clean, demo-reliable | "Less AI" optics — mitigate by LLM-generated explanations |
| Collaborative filtering / ML ranking | "Customers like you hold…" from txn+holdings embeddings | Personalization story | Cold start, opaque, mis-selling risk, needs data you don't have |
| **LLM-RAG over factsheets** (recommended garnish) | Index scheme factsheets/KIMs; LLM answers "why this fund", compares two funds, explains exit load | Great conversational depth, cite-able | Hallucination risk → keep numbers from structured store, not generation |

**Winning combo:** rules pick the shortlist (auditable) → LLM explains and converses over it (RAG-grounded) → guardrails block anything off-list. This is "explainability by construction".

### 6.4 Live market/MF data sources (all free, demo-friendly)

- **AMFI official NAV feed**: `https://www.amfiindia.com/spages/NAVAll.txt` (daily, all schemes; plus historical download portal) ([Portfolio Performance docs](https://help.portfolio-performance.info/en/how-to/downloading-historical-prices/indian/)).
- **MFapi.in** — free, no-auth JSON API wrapping AMFI: `GET /mf/search`, `GET /mf/{scheme_code}`, `/latest` ([mfapi.in](https://www.mfapi.in/); [docs](https://www.mfapi.in/docs/)).
- **mftool** (Python lib) for NAV/scheme data ([docs](https://mftool.readthedocs.io/)); **mstarpy** scrapes Morningstar for holdings/ratings *(unverified maintenance status)*; mfdata.in (14k+ schemes, 18y history) ([mfdata.in](https://mfdata.in/)).
- Indices/market colour: NSE indices via public endpoints or yfinance (^NSEI) *(unverified ToS)* — enough for the "market-linked products need frequent updates" requirement (avatar opens with "Nifty is up 0.8% today…").
- Scheme metadata/factsheets: AMC factsheet PDFs → RAG index; Value Research/Morningstar categories for labels *(licensing: demo only)*.

---

## 7. Account Aggregator Angle (outside-bank holdings)

- The RBI-licensed **Account Aggregator (AA)** framework is the consent-based rail for pulling a customer's financial data across institutions: **780+ FIs live, 2.12B+ accounts enabled, 269M+ consents processed** ([Sahamati](https://sahamati.org.in/); [4th AA Day release](https://sahamati.org.in/sahamati-marks-4th-account-aggregator-foundation-day-indias-data-empowerment-revolution-scales-new-heights/)).
- **Asset-side FI types are live**: bank deposits, term/recurring deposits, **mutual funds, equities (via CDSL & NSDL as FIPs, live with 13 AAs), ETFs, insurance policies, NPS (PFRDA designated the CRAs as FIPs)** ([Sahamati FAQ](https://sahamati.org.in/faq/); [CASParser state-of-AA 2026](https://casparser.in/blog/state-of-account-aggregator-2026/); [key resources](https://sahamati.org.in/account-aggregator-key-resources/)).
- Insurance-sector AA usage grew in 2025 (underwriting etc.) ([Sahamati insurance paper (PDF)](https://sahamati.org.in/wp-content/uploads/2025/12/From-Consent-to-Cover-How-the-Account-Aggregator-Framework-can-Unlock-Value-in-Insurance.pdf)). Fair-use consent templates are enforced in real time since **June 1 2025** ([FAQ](https://sahamati.org.in/faq/)) — mention purpose-bound consent in the demo.
- **Alternative/complementary**: **MF Central CAS** (MFCentral by CAMS+KFintech) gives a consolidated MF statement across AMCs; parseable via casparser-style tooling ([CASParser](https://casparser.in/)). UTI's new "Wealth 360" shows the industry building exactly this aggregation UX ([BusinessToday](https://www.businesstoday.in/mutual-funds/story/uti-mutual-funds-wealth-360-opens-what-investors-should-know-about-the-new-platform-533441-2026-05-26)).
- **Bank angle**: IDBI Bank would act as **FIU** (data user). For the demo, simulate the AA consent screen (mock Anumati/Finvu-style flow) and return synthetic FI JSON — judges care that you *know the rail*, not that you wired production AA.
- Demo line: "With your consent via Account Aggregator, I can see your ₹4.2L of mutual funds at other institutions and your NPS corpus — your real equity exposure is already 38%, so I'm adjusting my recommendation."

---

## 8. Concrete Hackathon Architecture

### 8.1 Recommended shape

**Responsive web app styled as a mobile shell** (React/Next.js, 390px frame, installable PWA) — presents as "embedded in the bank's mobile app" without app-store friction; demo on a phone + mirrored screen.

```
[React mobile shell]
  ├─ Avatar layer: Rive/Live2D rig (states: idle/listen/think/talk + emotions)
  │    └─ optional HeyGen/D-ID photoreal toggle (WebRTC)
  ├─ Voice: mic → Sarvam Saarika ASR (streaming) ; Bulbul v3 TTS ← streamed LLM text
  ├─ Chat UI (text-first fallback; language switcher: EN/HI/+2 regional)
  ▼
[FastAPI/Node backend]
  ├─ Claude on Bedrock (anthropic.claude-sonnet-4-6 reasoning; haiku for routing)
  │    Tools (strict JSON schemas):
  │      get_customer_profile(customer_id)
  │      get_portfolio(customer_id, include_aa=true)   ← in-bank + AA mock
  │      compute_risk_profile(answers, txn_features)
  │      get_goal_plan(goal, horizon, amount)
  │      recommend(asset_alloc | schemes, risk_band, horizon)  ← rules engine
  │      get_market_data(scheme_code|index)             ← AMFI/MFapi live
  │      execute_transaction(product, amount, mode)     ← vanilla only: FD/FRSB/MF SIP; OTP mock
  │      create_rm_lead(product_type, context_summary)  ← regulated products
  │      log_suitability(record)                        ← writes audit trail
  ├─ Guardrails: Bedrock Guardrails + deterministic compliance post-filter
  ├─ Data: Postgres/SQLite — synthetic core-banking (txns, balances), scheme master
  └─ RAG: scheme factsheets + product FAQs + financial-literacy content (vector store)
[RM Console] – second screen: incoming leads with AI-written context, suitability log viewer
```

### 8.2 Synthetic personas (pre-seeded, switchable)

1. **Ravi, 28, Mass, salary account** (Hindi) — ₹65k salary credit detected, ~₹12k monthly surplus → risk band Moderate-Growth → goal "emergency fund + wealth" → AI recommends liquid fund + index SIP, **executes ₹5k SIP live**, then serves a 30-sec financial-literacy explainer ("what is a SIP?").
2. **Meera, 54, HNI** (English) — ₹2.1Cr across bank + AA-fetched external MFs; overweight equity for age → conservative rebalance to debt + **FRSB 8.05%** (AI executes FRSB), plus estate/insurance need → **RM lead created**, appointment booked.
3. **Arjun, 35, NRI (Dubai)** (English/Malayalam) — NRE surplus; wants India exposure; AI explains repatriation + suggests NRE-eligible MF allocation, flags tax/FEMA nuance → executes vanilla piece, routes portfolio advisory to NRI RM desk.

### 8.3 Build-order (what to cut first)

Must-have: chat+voice loop in 2 languages, risk profile conversation, portfolio view w/ AA mock, rules recommender w/ live NAVs, one live transaction (SIP or FRSB), RM lead + console, suitability log. Nice-to-have: photoreal avatar toggle, 4+ languages, literacy micro-videos, spend analytics chart. Cuttable: real AA sandbox, real payment rails, insurance premium quotes.

---

## 9. Pros/Cons Tables for the Big Choices

### 9.1 Avatar depth

| Option | Pros | Cons |
|---|---|---|
| Photoreal video-gen API (HeyGen/D-ID/Anam) | Wow factor; human-like trust | Network-fragile in demo halls; per-min cost; uncanny valley; latency +0.5–1s |
| **2D rig (Rive/Live2D) + emotion states** ✅ | Zero latency/cost; offline-safe; brand-ownable mascot; AMA explicitly allows 2D | Less flashy; needs design effort for polish |
| Animated chat UI (Siri-orb + emoji states) | Trivial to build | Fails the "avatar-based" brief |

### 9.2 Voice-first vs text-first

| | Pros | Cons |
|---|---|---|
| Voice-first | Accessibility (mass, low literacy); matches "branch RM" metaphor; demo drama | ASR errors in noisy hall; numbers/OTPs awkward by voice |
| **Text-first with voice toggle** ✅ | Reliable; voice where it shines (greetings, explanations); confirmations via UI cards | Slightly less theatrical |

(Hybrid = AMA's stated expectation: "mix of voice and text".)

### 9.3 Recommendation engine

| | Pros | Cons |
|---|---|---|
| Pure rules | Auditable, deterministic, SEBI-friendly | Judges may see it as static |
| Pure ML (CF/learning-to-rank) | "Data-driven" story | Cold start, opaque, liability under Reg 16C-style accountability |
| Pure LLM | Fast to build, conversational | Hallucinated funds/numbers = disqualifying in a bank |
| **Rules shortlist + LLM-RAG explanation layer** ✅ | Explainable AND conversational; hallucination-capped | Two components to build |

### 9.4 Build vs API for TTS/ASR

| | Pros | Cons |
|---|---|---|
| **APIs (Sarvam/ElevenLabs)** ✅ | Days-not-weeks; best Indic quality (Bulbul v3 beat ElevenLabs in blind Indic study — [Sarvam](https://www.sarvam.ai/blogs/bulbul-v3)) | Recurring cost; data leaves bank (flag: Sarvam offers sovereign/on-prem posture) |
| Self-host AI4Bharat/Bhashini | Free, sovereign, 22-language DPI story ([Bhashini](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage)) | GPU ops burden; quality/latency tuning eats hackathon time |
| Hybrid (API now, Bhashini roadmap) | Best pitch: "demo on Sarvam, scale on Bhashini DPI" | — |

---

## 10. Winning Strategy (bank-executive judges)

### 10.1 What this judge cohort rewards

1. **Compliance-by-design, not compliance-as-caveat.** Show the suitability log and audit trail on screen; name-drop SEBI's Feb 2025 AI-accountability amendments and the June 2025 responsible-AI consultation (§2.2) — "the bank is liable for the AI's output, so every output is logged, grounded, and guarded."
2. **Explainability.** Every recommendation card carries "Why this?" (age band, horizon, surplus, existing exposure). This is also the judging theme across the whole hackathon (per memory: explainability + human-in-the-loop).
3. **Human-in-the-loop as a feature.** The RM console isn't a fallback, it's a **lead-generation machine for the bank's RM force** — quantify it ("every avatar conversation ends in a transaction or a qualified RM lead; zero dead-ends").
4. **Revenue math.** Distributor trail on MF regular plans, bancassurance leads, FRSB/FD balance-sheet stickiness, RM productivity (AI pre-qualifies), CASA retention. Banks buy revenue + risk-reduction, not chatbots.
5. **Inclusion story.** Bhashini/22-language roadmap + financial-literacy micro-lessons for the mass segment = priority-sector-flavoured narrative a public-interest bank loves.
6. **Feasibility.** Live NAVs from AMFI, real language switch mid-conversation, and one real end-to-end transaction beat ten mocked screens.

### 10.2 Demo script (7 minutes)

1. (30s) Problem: "1 RM per ~2,000 customers; advice reaches only the top 2%."
2. (2m) **Ravi (mass, Hindi, voice)**: salary credit detected → avatar greets in Hindi, 3 conversational risk questions → "₹12,000 sparable" → asset-allocation ring + 2 schemes with live NAV → *why this?* card → executes ₹5,000 SIP with OTP mock → 30-sec "what is a SIP" literacy bite.
3. (2m) **Meera (HNI, English)**: AA consent screen → external holdings appear → "you're 68% equity at 54; let's move ₹3L to FRSB at 8.05%" → executes FRSB → insurance gap detected → **RM lead**; cut to RM console showing the AI-written brief + full suitability log.
4. (1m) **Compliance interlude**: attempt "guarantee me 15% returns / tell me a hot stock" → avatar declines gracefully (guardrail), offers RM. Show the audit-trail JSON.
5. (1m) Architecture slide + regulatory matrix (§2.6) + scale roadmap (Bhashini languages, AA production, per-conversation cost in paise).
6. (30s) Business impact numbers + close.

### 10.3 Anticipated judge questions (prep answers)

- "Who is liable if the AI mis-sells?" → Bank is (SEBI Feb 2025 amendments); hence rules-bounded recommendations, logging, guardrails, RM escalation.
- "Direct or regular plans?" → Regular (bank = ARN distributor; revenue); direct-plan EOP route exists but is advice-free by law (§2.1).
- "How is this different from BoB Aditi?" → Aditi is service Q&A; ours does suitability-driven advisory + transactions + RM handoff with audit trail.
- "Hallucinations?" → Numbers only ever come from tools (AMFI feed, scheme master); LLM narrates, never invents; grounding checks + denied topics.
- "NRI compliance?" → NRE/NRO sourcing, FEMA repatriation flags, US/Canada NRI restrictions handled as hard rules; NRI desk RM for tax treaty questions.

---

## 11. Key Sources

- SEBI IA Regulations 2013 (2023 consol.): https://www.sebi.gov.in/legal/regulations/feb-2023/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-february-07-2023-_69215.html
- SEBI IA FAQs (incidental advice, robo): https://www.sebi.gov.in/sebi_data/attachdocs/1424862077270.pdf
- SEBI EOP framework (13 Jun 2023): https://www.sebi.gov.in/legal/circulars/jun-2023/regulatory-framework-for-execution-only-platforms-for-facilitating-transactions-in-direct-plans-of-schemes-of-mutual-funds_72479.html
- SEBI AI/ML responsible-usage consultation (20 Jun 2025): https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html
- SEBI AI accountability (Reg 16C analysis): https://indiacorplaw.in/2025/07/16/from-algorithms-to-accountability-analysing-sebis-ai-ml-governance-framework/ ; https://www.indialaw.in/blog/securities-law/sebis-2025-ai-ml-framework-harmonising-market-oversight/
- IRDAI corporate agents / bancassurance: https://rmaindia.org/irdai-bancassurance-regulations-india-guide/ ; https://financialservices.gov.in/beta/sites/default/files/2024-11/IRDAI(Regn%20of%20Corporate%20Agents)%20Regulations-2015.pdf
- RBI FRSB 2020 (8.05%, IDBI as receiving office): https://www.business-standard.com/finance/personal-finance/rbi-keeps-interest-rate-on-floating-rate-savings-bonds-unchanged-at-8-05-125010200691_1.html ; https://www.hdfcsec.com/rbi-bond
- Account Aggregator: https://sahamati.org.in/faq/ ; https://casparser.in/blog/state-of-account-aggregator-2026/
- BoB Aditi avatar VRM: https://bankofbaroda.bank.in/-/media/project/bob/countrywebsites/india/content/media/press-releases/2024/24-09/adopts-generative-ai-to-transform-customer-experience-and-employee-efficiency-17-05.pdf
- Sarvam pricing/Bulbul v3: https://www.sarvam.ai/api-pricing ; https://www.sarvam.ai/blogs/bulbul-v3
- AI4Bharat / Bhashini: https://models.ai4bharat.org/ ; https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage
- Avatar APIs: https://www.heygen.com/api-pricing ; https://anam.ai/blog/anam-vs-heygen ; https://www.veed.io/learn/best-avatar-apis
- MF data: https://www.mfapi.in/ ; https://mftool.readthedocs.io/ ; AMFI NAVAll.txt
- Market sizing: https://www.statista.com/outlook/fmo/wealth-management/digital-investment/robo-advisors/india ; https://indiafintech.substack.com/p/indias-capital-markets-the-financialization
