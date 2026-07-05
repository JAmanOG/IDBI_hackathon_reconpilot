"""Canonical schema + break taxonomy.

Vocabulary follows what a UPI recon desk actually uses: RRN (Retrieval
Reference Number) is the primary 3-way join key; TCC/RET are the NPCI
adjustment actions raised through URCS/UDIR; the suspense GL parks
unresolved legs. Response codes are illustrative but mirror NPCI
conventions ("00" approved, "91" timeout/deemed, "U30" debit failed).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Source(str, Enum):
    NPCI = "NPCI"
    SWITCH = "SWITCH"
    CBS = "CBS"


class BreakClass(str, Enum):
    TIMEOUT_DEBIT_NO_CREDIT = "TIMEOUT_DEBIT_NO_CREDIT"   # deemed txn: customer debited, credit unconfirmed → TAT clock runs
    MISSING_IN_CBS = "MISSING_IN_CBS"                     # NPCI+switch success, CBS posting failed
    MISSING_AT_NPCI = "MISSING_AT_NPCI"                   # orphan CBS posting, nothing settled at NPCI
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"                   # legs disagree on amount
    DUPLICATE_CBS_POSTING = "DUPLICATE_CBS_POSTING"       # same RRN posted twice in CBS (double debit/credit)
    CROSS_CYCLE = "CROSS_CYCLE"                           # settled in cycle N, posted in cycle N+1 (rule-tunable)


SEVERITY = {
    BreakClass.TIMEOUT_DEBIT_NO_CREDIT: "HIGH",   # customer-impacting + RBI compensation accrues
    BreakClass.MISSING_IN_CBS: "HIGH",            # bank out-of-pocket at settlement
    BreakClass.DUPLICATE_CBS_POSTING: "HIGH",     # double debit = complaint + reversal urgency
    BreakClass.AMOUNT_MISMATCH: "MEDIUM",
    BreakClass.MISSING_AT_NPCI: "MEDIUM",
    BreakClass.CROSS_CYCLE: "LOW",
}

# Suspense/settlement GLs used in drafted vouchers (Finacle-style office accounts)
GL_UPI_SETTLEMENT = "98530021"
GL_UPI_SUSPENSE = "98530099"


@dataclass
class CanonicalTxn:
    """One leg of a transaction as seen by one source, normalized."""
    source: str
    rrn: str
    txn_id: str
    amount_paise: int
    direction: str          # OUTWARD = IDBI customer pays; INWARD = IDBI customer receives
    dr_cr: str              # from IDBI books' perspective
    resp_code: str          # 00 approved · 91 timeout/deemed · U30 debit failed
    status: str             # SUCCESS / FAILED / TIMEOUT
    cycle: int
    txn_date: str           # YYYY-MM-DD (settlement date at NPCI; posting date at CBS)
    payer_vpa: str = ""
    payee_vpa: str = ""
    account_no: str = ""
    narration: str = ""
    raw_ref: str = ""       # row id in the source file

    def as_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class ReconStats:
    total_rrns: int = 0
    matched: int = 0
    matched_failed_consistent: int = 0
    matched_with_cycle_drift: int = 0
    breaks: int = 0
    by_class: dict = field(default_factory=dict)

    @property
    def auto_match_rate(self) -> float:
        if not self.total_rrns:
            return 0.0
        ok = self.matched + self.matched_failed_consistent + self.matched_with_cycle_drift
        return round(100.0 * ok / self.total_rrns, 2)
