"""RBI TAT-compensation clock.

RBI DPSS.CO.PD No.629/02.01.014/2019-20 (20 Sep 2019): for a UPI txn where
the customer's account is debited but the beneficiary is not credited, the
transaction must be auto-reversed by T+1; beyond that the bank owes the
customer Rs.100/day, automatically, without a complaint being filed.
"""
from __future__ import annotations

from datetime import date

from app.config import TAT_COMPENSATION_PER_DAY_INR, UPI_REVERSAL_TAT_DAYS


def tat_status(txn_date: str, as_of: date | None = None) -> dict:
    as_of = as_of or date.today()
    t0 = date.fromisoformat(txn_date)
    deadline_days = UPI_REVERSAL_TAT_DAYS
    days_elapsed = (as_of - t0).days
    days_past_tat = max(0, days_elapsed - deadline_days)
    return {
        "txn_date": txn_date,
        "as_of": as_of.isoformat(),
        "tat_deadline": f"T+{deadline_days}",
        "days_elapsed": days_elapsed,
        "days_past_tat": days_past_tat,
        "compensation_accrued_inr": days_past_tat * TAT_COMPENSATION_PER_DAY_INR,
        "accruing_per_day_inr": TAT_COMPENSATION_PER_DAY_INR if days_past_tat >= 0 and days_elapsed >= deadline_days else 0,
        "breached": days_past_tat > 0,
    }
