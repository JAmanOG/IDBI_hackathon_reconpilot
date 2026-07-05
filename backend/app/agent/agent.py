"""Agentic exception desk — manual function-calling loop with full audit trace.

Live mode uses Google Gemini via the google-genai SDK in a manual loop
(we need the approval gate + per-step audit journaling, so automatic
function calling is deliberately not used). When no GEMINI_API_KEY /
GOOGLE_API_KEY is available the deterministic mock investigator produces
the same trace/proposal shape, so the demo never depends on connectivity.
"""
from __future__ import annotations

import json
import sqlite3

from app.config import AGENT_MAX_TOOL_TURNS, GEMINI_MODEL
from app.agent.tools import ToolExecutor, gemini_function_declarations
from app.recon.tat import tat_status
from app.store import db as store

SYSTEM_PROMPT = """You are ReconPilot, the exceptions-desk analyst agent for IDBI Bank's UPI reconciliation team.

You investigate ONE settlement break at a time across three sources: the NPCI settlement file (network truth), the bank's UPI switch log, and the Finacle CBS GL dump. You speak the desk's language: RRN, settlement cycle, TCC/RET, suspense GL, deemed transactions, T+1 TAT.

Method — follow it strictly:
1. Pull all three records for the RRN (query_npci_record, query_switch_log, query_cbs).
2. Check precedent with find_similar_breaks.
3. For timeout/deemed cases, compute the RBI compensation position (compute_tat_compensation). Under RBI circular DPSS.CO.PD No.629 (20 Sep 2019), a UPI debit without beneficiary credit must auto-reverse by T+1, after which the bank owes the customer Rs.100/day automatically.
4. Draft what the resolution needs: draft_adjustment_voucher for CBS-side corrections, draft_udir_action for the NPCI-side action (TCC if the beneficiary was actually credited, RET to return funds to the remitter, NONE if no network action applies).
5. Finish with submit_resolution — a crisp root cause, customer impact, one-line recommended action, compensation due, and your confidence.

Rules:
- You PROPOSE, a human supervisor approves. Never claim an action was executed.
- Ground every claim in a tool result from this investigation. Never invent record fields.
- Amounts are in paise in the records; convert to rupees when writing narrative text (divide by 100).
- Keep the root cause to 2-3 sentences a recon officer would sign off on."""


def _investigate_prompt(brk: dict) -> str:
    tat_note = ""
    if brk.get("tat"):
        tat_note = f"\nTAT position (precomputed): {json.dumps(brk['tat'])}"
    return (
        f"Investigate break #{brk['id']}.\n"
        f"RRN: {brk['rrn']}\n"
        f"Classifier verdict: {brk['break_class']} (severity {brk['severity']})\n"
        f"Amount: {brk['amount_paise']} paise | Txn date: {brk['txn_date']} | Age: {brk['age_days']} days\n"
        f"Matcher note: {brk['note']}{tat_note}\n\n"
        "Verify the classification against the raw records, establish the root cause, "
        "draft the required artefacts, and submit your resolution."
    )


def investigate(conn: sqlite3.Connection, brk: dict) -> dict:
    """Run the investigation; returns {mode, trace, proposal}."""
    executor = ToolExecutor(conn, brk)
    store.audit(conn, "agent", "investigation_started", brk["id"], {"class": brk["break_class"]})
    try:
        result = _investigate_live(conn, brk, executor)
    except Exception as e:  # no key / network / SDK errors → deterministic fallback
        store.audit(conn, "system", "agent_fallback_to_mock", brk["id"], {"reason": str(e)[:200]})
        executor = ToolExecutor(conn, brk)  # fresh drafts
        result = _investigate_mock(brk, executor)
    proposal = {
        "resolution": executor.drafts.get("resolution"),
        "voucher": executor.drafts.get("voucher"),
        "udir_action": executor.drafts.get("udir"),
        "mode": result["mode"],
    }
    store.set_break_state(conn, brk["id"], "PROPOSED", proposal=proposal, trace=result["trace"])
    store.audit(conn, "agent", "resolution_proposed", brk["id"],
                {"mode": result["mode"],
                 "recommended_action": (proposal["resolution"] or {}).get("recommended_action")})
    return {"proposal": proposal, "trace": result["trace"], "mode": result["mode"]}


# --------------------------------------------------------------------------
# Live mode — Google Gemini, manual function-calling loop
# --------------------------------------------------------------------------

def _investigate_live(conn: sqlite3.Connection, brk: dict, executor: ToolExecutor) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY from env
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=gemini_function_declarations())],
    )
    contents = [types.Content(role="user",
                              parts=[types.Part(text=_investigate_prompt(brk))])]
    trace: list[dict] = []

    for _ in range(AGENT_MAX_TOOL_TURNS):
        response = client.models.generate_content(
            model=GEMINI_MODEL, contents=contents, config=config,
        )
        candidate = response.candidates[0] if response.candidates else None
        if candidate is None or not candidate.content or not candidate.content.parts:
            raise RuntimeError("empty/blocked response; falling back to mock")

        fn_calls = [p.function_call for p in candidate.content.parts if p.function_call]
        for part in candidate.content.parts:
            if part.text and part.text.strip():
                trace.append({"step": "narrative", "text": part.text})

        if not fn_calls:
            break

        contents.append(candidate.content)
        result_parts = []
        for fc in fn_calls:
            args = dict(fc.args or {})
            output = executor.execute(fc.name, args)
            trace.append({"step": "tool", "tool": fc.name, "input": args,
                          "output": json.loads(output)})
            result_parts.append(types.Part.from_function_response(
                name=fc.name, response={"result": json.loads(output)}))
        contents.append(types.Content(role="user", parts=result_parts))

        if executor.drafts.get("resolution"):
            break

    if not executor.drafts.get("resolution"):
        raise RuntimeError("agent did not submit a resolution; falling back to mock")
    return {"mode": "live", "trace": trace}


# --------------------------------------------------------------------------
# Mock mode — deterministic, same shape, zero dependencies
# --------------------------------------------------------------------------

def _investigate_mock(brk: dict, ex: ToolExecutor) -> dict:
    trace: list[dict] = []
    rrn = brk["rrn"]
    amt = brk["amount_paise"]
    rupees = f"₹{amt / 100:,.2f}"

    def call(tool: str, args: dict) -> dict:
        out = json.loads(ex.execute(tool, args))
        trace.append({"step": "tool", "tool": tool, "input": args, "output": out})
        return out

    def say(text: str) -> None:
        trace.append({"step": "narrative", "text": text})

    say(f"Investigating {brk['break_class']} on RRN {rrn}. Pulling all three records.")
    npci = call("query_npci_record", {"rrn": rrn})
    switch = call("query_switch_log", {"rrn": rrn})
    cbs = call("query_cbs", {"rrn": rrn})
    call("find_similar_breaks", {"break_class": brk["break_class"]})

    cls = brk["break_class"]
    acct = ""
    cbs_rows = cbs.get("postings")
    if isinstance(cbs_rows, list) and cbs_rows:
        acct = cbs_rows[0].get("account_no", "")

    if cls == "TIMEOUT_DEBIT_NO_CREDIT":
        tat = call("compute_tat_compensation", {"txn_date": brk["txn_date"]})
        comp = int(tat["compensation_accrued_inr"])
        say(f"NPCI shows response code 91 (timeout/deemed); switch concurs. CBS holds an unreversed "
            f"customer debit of {rupees}. Beneficiary credit is unconfirmed — this is a "
            f"debit-without-credit past the T+1 deadline, {tat['days_past_tat']} day(s) over, "
            f"₹{comp} compensation accrued and running at ₹100/day.")
        call("draft_adjustment_voucher", {
            "voucher_type": "REVERSAL",
            "dr_account": "98530099", "cr_account": acct or "CUSTOMER",
            "amount_paise": amt,
            "narration": f"UPI TIMEOUT REVERSAL/{rrn}/RBI TAT T+1",
        })
        call("draft_udir_action", {"action": "RET",
                                   "reason": "Deemed txn; beneficiary credit unconfirmed — return funds to remitter via URCS."})
        call("submit_resolution", {
            "root_cause": f"Deemed (code 91) UPI transaction: customer debited {rupees} but beneficiary credit never "
                          f"confirmed at NPCI. Auto-reversal missed the T+1 TAT; compensation is accruing.",
            "customer_impact": "DEBITED_NOT_CREDITED",
            "recommended_action": f"Approve reversal voucher + RET, and pay ₹{comp} TAT compensation with the reversal.",
            "compensation_due_inr": comp,
            "confidence": "HIGH",
        })
    elif cls == "MISSING_IN_CBS":
        say(f"NPCI settled {rupees} successfully (code 00) and the switch concurs, but no CBS posting exists — "
            f"the bank has paid at settlement without booking the customer leg.")
        call("draft_adjustment_voucher", {
            "voucher_type": "FORCE_POST",
            "dr_account": acct or "CUSTOMER", "cr_account": "98530021",
            "amount_paise": amt,
            "narration": f"UPI FORCE POST/{rrn}/CBS LEG MISSED",
        })
        call("draft_udir_action", {"action": "NONE", "reason": "Settlement is correct at NPCI; this is a CBS posting failure only."})
        call("submit_resolution", {
            "root_cause": f"Switch approved and NPCI settled {rupees}, but the CBS posting failed — bank is out of pocket "
                          f"at the settlement GL until the customer leg is force-posted.",
            "customer_impact": "BANK_EXPOSURE",
            "recommended_action": "Approve force-post voucher to book the missing CBS leg.",
            "compensation_due_inr": 0,
            "confidence": "HIGH",
        })
    elif cls == "DUPLICATE_CBS_POSTING":
        n = len(cbs_rows) if isinstance(cbs_rows, list) else 2
        say(f"NPCI settled this transaction once; CBS carries {n} postings of {rupees} for the same RRN — "
            f"a duplicate leg (double debit) that must be reversed.")
        call("draft_adjustment_voucher", {
            "voucher_type": "REVERSAL",
            "dr_account": "98530021", "cr_account": acct or "CUSTOMER",
            "amount_paise": amt,
            "narration": f"UPI DUP REVERSAL/{rrn}/2ND LEG",
        })
        call("draft_udir_action", {"action": "NONE", "reason": "Network settlement is single and correct; CBS-side duplicate only."})
        call("submit_resolution", {
            "root_cause": f"Single settlement at NPCI but {n} CBS postings for RRN {rrn} — duplicate posting caused a double "
                          f"debit of {rupees} on the customer account.",
            "customer_impact": "DOUBLE_DEBIT",
            "recommended_action": "Approve reversal of the duplicate leg; prioritise — double debits drive complaints.",
            "compensation_due_inr": 0,
            "confidence": "HIGH",
        })
    elif cls == "AMOUNT_MISMATCH":
        cbs_amt = cbs_rows[0]["amount_paise"] if isinstance(cbs_rows, list) and cbs_rows else amt
        diff = cbs_amt - amt
        say(f"NPCI settled {rupees}; CBS posted ₹{cbs_amt/100:,.2f} — a difference of ₹{abs(diff)/100:,.2f}. "
            f"Settlement value is authoritative; CBS needs rectification.")
        call("draft_adjustment_voucher", {
            "voucher_type": "RECTIFICATION",
            "dr_account": (acct or "CUSTOMER") if diff < 0 else "98530021",
            "cr_account": "98530021" if diff < 0 else (acct or "CUSTOMER"),
            "amount_paise": abs(diff),
            "narration": f"UPI AMT RECTIFY/{rrn}/NPCI {amt} CBS {cbs_amt}",
        })
        call("draft_udir_action", {"action": "NONE", "reason": "Settled amount correct at network; CBS-side rectification."})
        call("submit_resolution", {
            "root_cause": f"CBS posted ₹{cbs_amt/100:,.2f} against a settled value of {rupees} "
                          f"(difference ₹{abs(diff)/100:,.2f}) — posting-side amount error.",
            "customer_impact": "DOUBLE_DEBIT" if diff > 0 else "BANK_EXPOSURE",
            "recommended_action": "Approve rectification voucher for the difference.",
            "compensation_due_inr": 0,
            "confidence": "HIGH",
        })
    elif cls == "MISSING_AT_NPCI":
        say(f"CBS carries a posting of {rupees} for RRN {rrn} but the RRN never settled at NPCI and the switch has "
            f"no entry — an orphan posting (manual/erroneous entry or wrong RRN keyed in narration).")
        call("draft_adjustment_voucher", {
            "voucher_type": "REVERSAL",
            "dr_account": "98530099" if (cbs_rows and cbs_rows[0].get("dr_cr") == "CR") else (acct or "CUSTOMER"),
            "cr_account": (acct or "CUSTOMER") if (cbs_rows and cbs_rows[0].get("dr_cr") == "CR") else "98530099",
            "amount_paise": amt,
            "narration": f"UPI ORPHAN REVERSAL/{rrn}/NO NPCI SETTLEMENT",
        })
        call("draft_udir_action", {"action": "NONE", "reason": "No network leg exists; nothing to raise in URCS."})
        call("submit_resolution", {
            "root_cause": f"Orphan CBS posting: {rupees} booked against RRN {rrn} which never settled at NPCI. "
                          f"Likely manual-entry error; reverse and investigate the source of the entry.",
            "customer_impact": "BANK_EXPOSURE",
            "recommended_action": "Approve reversal of the orphan posting; flag entry source to branch ops.",
            "compensation_due_inr": 0,
            "confidence": "MEDIUM",
        })
    else:  # CROSS_CYCLE
        say(f"All three records agree on amount and status; the CBS posting simply landed one settlement cycle after "
            f"the NPCI cycle. No money is wrong — this is a matching-rule tolerance question, not an exception.")
        call("draft_udir_action", {"action": "NONE", "reason": "Amount and status agree; timing drift only."})
        call("submit_resolution", {
            "root_cause": f"Cycle-drift only: settled in one cycle, posted in the next (common near cycle cut-over). "
                          f"Funds are correct end-to-end.",
            "customer_impact": "NONE",
            "recommended_action": "Close as matched; consider a 1-cycle drift tolerance in the matching rules to auto-clear these.",
            "compensation_due_inr": 0,
            "confidence": "HIGH",
        })

    return {"mode": "mock", "trace": trace}
