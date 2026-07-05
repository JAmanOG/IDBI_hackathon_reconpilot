"""Per-source adapters → canonical transaction legs.

Each adapter maps one raw file into CanonicalTxn records. When IDBI's
sandbox APIs replace the mock files, only this module changes — the
matcher, break register, agent and UI are source-agnostic.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from app.recon.schemas import CanonicalTxn, Source

_NARRATION_RRN = re.compile(r"UPI/(?:DR|CR)/(\d{12})/")


def load_npci(path: Path) -> list[CanonicalTxn]:
    df = pd.read_csv(path, dtype={"RRN": str})
    out = []
    for i, r in df.iterrows():
        resp = str(r["RESP_CODE"])
        status = "SUCCESS" if resp == "00" else ("TIMEOUT" if resp == "91" else "FAILED")
        out.append(CanonicalTxn(
            source=Source.NPCI.value,
            rrn=r["RRN"], txn_id=r["TXN_ID"],
            amount_paise=int(r["AMOUNT_PAISE"]),
            direction="OUTWARD" if r["DR_CR"] == "DR" else "INWARD",
            dr_cr=r["DR_CR"], resp_code=resp, status=status,
            cycle=int(r["SETTLEMENT_CYCLE"]), txn_date=r["TXN_DATE"],
            payer_vpa=r["PAYER_VPA"], payee_vpa=r["PAYEE_VPA"],
            raw_ref=f"npci:{i}",
        ))
    return out


def load_switch(path: Path) -> list[CanonicalTxn]:
    df = pd.read_csv(path, dtype={"RRN": str})
    out = []
    for i, r in df.iterrows():
        out.append(CanonicalTxn(
            source=Source.SWITCH.value,
            rrn=r["RRN"], txn_id=r["UPI_TXN_ID"],
            amount_paise=int(r["AMOUNT_PAISE"]),
            direction=r["DIRECTION"],
            dr_cr="DR" if r["DIRECTION"] == "OUTWARD" else "CR",
            resp_code=str(r["RESP_CODE"]), status=r["STATUS"],
            cycle=int(r["CYCLE"]), txn_date=str(r["LOCAL_TIMESTAMP"])[:10],
            payer_vpa=r["PAYER_VPA"], payee_vpa=r["PAYEE_VPA"],
            raw_ref=f"switch:{i}",
        ))
    return out


def load_cbs(path: Path) -> list[CanonicalTxn]:
    df = pd.read_csv(path, dtype=str)
    out = []
    for i, r in df.iterrows():
        m = _NARRATION_RRN.search(r["NARRATION"] or "")
        rrn = m.group(1) if m else ""
        out.append(CanonicalTxn(
            source=Source.CBS.value,
            rrn=rrn, txn_id=r["TRAN_ID"],
            amount_paise=int(r["AMOUNT_PAISE"]),
            direction="OUTWARD" if r["DR_CR"] == "DR" else "INWARD",
            dr_cr=r["DR_CR"], resp_code="", status="POSTED",
            cycle=int(r["CYCLE_POSTED"]), txn_date=r["TRAN_DATE"],
            account_no=r["ACCOUNT_NO"], narration=r["NARRATION"],
            raw_ref=f"cbs:{r['CBS_ENTRY_ID']}",
        ))
    return out
