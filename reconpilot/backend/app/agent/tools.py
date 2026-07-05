"""Agent tools — every consequential lookup/draft is a typed tool.

The agent PROPOSES; it never posts. Vouchers and UDIR actions are drafts
that land in the approval queue. Each tool execution is journaled to the
audit log, which is the explainability artifact.
"""
from __future__ import annotations

import json
import sqlite3

from app.config import TAT_COMPENSATION_PER_DAY_INR
from app.recon.schemas import GL_UPI_SETTLEMENT, GL_UPI_SUSPENSE
from app.recon.tat import tat_status
from app.store import db as store

TOOL_DEFINITIONS = [
    {
        "name": "query_npci_record",
        "description": "Fetch the NPCI settlement-file record(s) for the RRN under investigation. Returns the network's view of the transaction: amount, response code, settlement cycle, remitter/beneficiary banks.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"rrn": {"type": "string", "description": "12-digit Retrieval Reference Number"}},
            "required": ["rrn"],
            "additionalProperties": False,
        },
    },
    {
        "name": "query_switch_log",
        "description": "Fetch the bank's UPI switch log entries for the RRN. Shows what the switch accepted/timed out and the local timestamps.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"rrn": {"type": "string"}},
            "required": ["rrn"],
            "additionalProperties": False,
        },
    },
    {
        "name": "query_cbs",
        "description": "Fetch Finacle CBS posting(s) for the RRN: entry ids, account, DR/CR, amount, narration, posting cycle/date. Multiple rows for the same RRN indicate duplicate postings.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"rrn": {"type": "string"}},
            "required": ["rrn"],
            "additionalProperties": False,
        },
    },
    {
        "name": "find_similar_breaks",
        "description": "Search the break register for previously APPROVED resolutions of the same break class — precedent for how this desk resolves this exception type.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"break_class": {"type": "string"}},
            "required": ["break_class"],
            "additionalProperties": False,
        },
    },
    {
        "name": "compute_tat_compensation",
        "description": "Compute the RBI TAT position for this transaction (circular DPSS.CO.PD No.629, 20 Sep 2019): days past the T+1 auto-reversal deadline and Rs.100/day compensation accrued to date.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"txn_date": {"type": "string", "description": "YYYY-MM-DD transaction date"}},
            "required": ["txn_date"],
            "additionalProperties": False,
        },
    },
    {
        "name": "draft_adjustment_voucher",
        "description": "Draft (NOT post) a Finacle adjustment voucher for supervisor approval. Use REVERSAL to undo an erroneous/duplicate leg, FORCE_POST to post a missing leg, RECTIFICATION for an amount difference.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "voucher_type": {"type": "string", "enum": ["REVERSAL", "FORCE_POST", "RECTIFICATION"]},
                "dr_account": {"type": "string", "description": "Account/GL to debit (customer a/c no. or GL code)"},
                "cr_account": {"type": "string", "description": "Account/GL to credit"},
                "amount_paise": {"type": "integer"},
                "narration": {"type": "string"},
            },
            "required": ["voucher_type", "dr_account", "cr_account", "amount_paise", "narration"],
            "additionalProperties": False,
        },
    },
    {
        "name": "draft_udir_action",
        "description": "Draft (NOT submit) the NPCI URCS/UDIR dispute action. TCC = Transaction Credit Confirmation (beneficiary was credited; confirm). RET = Return (funds returned to remitter). Use NONE when no network action is needed.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["TCC", "RET", "NONE"]},
                "reason": {"type": "string"},
            },
            "required": ["action", "reason"],
            "additionalProperties": False,
        },
    },
    {
        "name": "submit_resolution",
        "description": "Submit the final investigation result for supervisor approval. Call this exactly once, after gathering evidence and drafting the needed voucher/UDIR artefacts.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "root_cause": {"type": "string", "description": "Plain-English root cause, in recon-desk language"},
                "customer_impact": {"type": "string", "enum": ["DEBITED_NOT_CREDITED", "DOUBLE_DEBIT", "NONE", "BANK_EXPOSURE"]},
                "recommended_action": {"type": "string", "description": "One-line action for the supervisor"},
                "compensation_due_inr": {"type": "integer", "description": "RBI TAT compensation accrued (0 if not applicable)"},
                "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
            },
            "required": ["root_cause", "customer_impact", "recommended_action", "compensation_due_inr", "confidence"],
            "additionalProperties": False,
        },
    },
]


def gemini_function_declarations() -> list[dict]:
    """TOOL_DEFINITIONS → Gemini function declarations.

    Gemini's OpenAPI-subset schema rejects `additionalProperties` and has no
    `strict` flag, so both are stripped; everything else maps 1:1
    (input_schema → parameters).
    """
    def strip(node):
        if isinstance(node, dict):
            node.pop("additionalProperties", None)
            for v in node.values():
                strip(v)
        elif isinstance(node, list):
            for v in node:
                strip(v)

    decls = []
    for t in TOOL_DEFINITIONS:
        schema = json.loads(json.dumps(t["input_schema"]))
        strip(schema)
        decls.append({"name": t["name"], "description": t["description"], "parameters": schema})
    return decls


class ToolExecutor:
    """Executes agent tools against the break's evidence + the break register."""

    def __init__(self, conn: sqlite3.Connection, brk: dict):
        self.conn = conn
        self.brk = brk
        self.drafts: dict = {"voucher": None, "udir": None, "resolution": None}

    def execute(self, name: str, args: dict) -> str:
        fn = getattr(self, f"_t_{name}", None)
        if fn is None:
            return json.dumps({"error": f"unknown tool {name}"})
        result = fn(args)
        store.audit(self.conn, "agent", f"tool:{name}", self.brk["id"],
                    {"input": args, "output_preview": result[:400]})
        return result

    # -- evidence lookups (from the break's 3-way legs snapshot) ------------
    def _legs(self, source: str) -> list[dict]:
        return self.brk.get("legs", {}).get(source, [])

    def _t_query_npci_record(self, args: dict) -> str:
        rows = self._legs("NPCI")
        return json.dumps({"rrn": args["rrn"], "records": rows or "NO RECORD AT NPCI"})

    def _t_query_switch_log(self, args: dict) -> str:
        rows = self._legs("SWITCH")
        return json.dumps({"rrn": args["rrn"], "records": rows or "NO SWITCH ENTRY"})

    def _t_query_cbs(self, args: dict) -> str:
        rows = self._legs("CBS")
        return json.dumps({"rrn": args["rrn"], "postings": rows or "NO CBS POSTING"})

    def _t_find_similar_breaks(self, args: dict) -> str:
        rows = self.conn.execute(
            """SELECT rrn, note, proposal_json FROM breaks
               WHERE break_class=? AND status='APPROVED' AND id != ? LIMIT 3""",
            (args["break_class"], self.brk["id"])).fetchall()
        precedents = [{"rrn": r["rrn"],
                       "resolution": json.loads(r["proposal_json"] or "{}").get("resolution", {})}
                      for r in rows]
        return json.dumps({"precedents": precedents or "No approved precedents yet for this class."})

    def _t_compute_tat_compensation(self, args: dict) -> str:
        return json.dumps(tat_status(args["txn_date"]))

    # -- drafting tools ------------------------------------------------------
    def _t_draft_adjustment_voucher(self, args: dict) -> str:
        voucher = {
            **args,
            "status": "DRAFT — pending supervisor approval",
            "maker": "reconpilot-agent",
            "checker_required": True,
            "suspense_gl_hint": {"settlement": GL_UPI_SETTLEMENT, "suspense": GL_UPI_SUSPENSE},
        }
        self.drafts["voucher"] = voucher
        return json.dumps({"drafted": True, "voucher": voucher})

    def _t_draft_udir_action(self, args: dict) -> str:
        udir = {**args, "rrn": self.brk["rrn"], "status": "DRAFT — pending supervisor approval"}
        self.drafts["udir"] = udir
        return json.dumps({"drafted": True, "udir_action": udir})

    def _t_submit_resolution(self, args: dict) -> str:
        self.drafts["resolution"] = args
        return json.dumps({"accepted": True, "note": "Queued for supervisor approval."})
