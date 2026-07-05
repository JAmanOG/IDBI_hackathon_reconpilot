"""3-way matcher: NPCI vs switch vs CBS, grouped on RRN.

Deterministic pass covers ~99%+ of legs. Whatever survives is classified
into the break taxonomy and lands in the break register for the agentic
exceptions desk. Matching behaviour is driven by a rules JSON that the
NL rule-authoring endpoint can rewrite (e.g. "tolerate 1-cycle drift").
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.recon.schemas import BreakClass, CanonicalTxn, ReconStats, SEVERITY
from app.recon.tat import tat_status


def run_recon(
    npci: list[CanonicalTxn],
    switch: list[CanonicalTxn],
    cbs: list[CanonicalTxn],
    rules: dict,
    as_of: date | None = None,
) -> tuple[ReconStats, list[dict]]:
    as_of = as_of or date.today()
    amount_tol = int(rules.get("amount_tolerance_paise", 0))
    cycle_tol = int(rules.get("cycle_drift_tolerance", 0))

    by_rrn: dict[str, dict[str, list[CanonicalTxn]]] = defaultdict(lambda: {"NPCI": [], "SWITCH": [], "CBS": []})
    for t in npci:
        by_rrn[t.rrn]["NPCI"].append(t)
    for t in switch:
        by_rrn[t.rrn]["SWITCH"].append(t)
    for t in cbs:
        if t.rrn:
            by_rrn[t.rrn]["CBS"].append(t)

    stats = ReconStats(total_rrns=len(by_rrn))
    breaks: list[dict] = []

    def add_break(cls: BreakClass, rrn: str, legs: dict, note: str, amount: int, txn_date: str):
        b = {
            "rrn": rrn,
            "break_class": cls.value,
            "severity": SEVERITY[cls],
            "amount_paise": amount,
            "txn_date": txn_date,
            "age_days": (as_of - date.fromisoformat(txn_date)).days,
            "note": note,
            "legs": {k: [t.as_dict() for t in v] for k, v in legs.items()},
        }
        if cls == BreakClass.TIMEOUT_DEBIT_NO_CREDIT:
            b["tat"] = tat_status(txn_date, as_of)
        breaks.append(b)
        stats.by_class[cls.value] = stats.by_class.get(cls.value, 0) + 1

    for rrn, legs in by_rrn.items():
        n, s, c = legs["NPCI"], legs["SWITCH"], legs["CBS"]
        ref = (n or s or c)[0]
        amount, txn_date = ref.amount_paise, ref.txn_date

        # Orphan CBS posting: nothing at the network
        if c and not n and not s:
            add_break(BreakClass.MISSING_AT_NPCI, rrn, legs,
                      "CBS posting exists but RRN never settled at NPCI (orphan entry).",
                      amount, txn_date)
            continue

        npci_status = n[0].status if n else None

        # Failed at network, consistently failed at switch, nothing posted → clean
        if npci_status == "FAILED":
            if not c:
                stats.matched_failed_consistent += 1
            else:
                add_break(BreakClass.MISSING_AT_NPCI, rrn, legs,
                          "Txn failed at NPCI but a CBS posting exists — erroneous posting.",
                          amount, txn_date)
            continue

        # Timeout / deemed: customer debited, credit unconfirmed
        if npci_status == "TIMEOUT":
            has_unreversed_debit = any(x.dr_cr == "DR" for x in c) and len(c) == 1
            if has_unreversed_debit or c:
                add_break(BreakClass.TIMEOUT_DEBIT_NO_CREDIT, rrn, legs,
                          "Deemed/timeout txn: customer debit in CBS with no reversal; "
                          "beneficiary credit unconfirmed at NPCI. RBI T+1 clock applies.",
                          amount, txn_date)
            else:
                stats.matched_failed_consistent += 1  # timed out, nothing posted
            continue

        # Success at network from here on
        if not c:
            add_break(BreakClass.MISSING_IN_CBS, rrn, legs,
                      "Settled successfully at NPCI (switch concurs) but no CBS posting found.",
                      amount, txn_date)
            continue

        if len(c) > 1:
            add_break(BreakClass.DUPLICATE_CBS_POSTING, rrn, legs,
                      f"{len(c)} CBS postings for one settled txn — duplicate leg needs reversal.",
                      amount, txn_date)
            continue

        cbs_leg = c[0]
        if abs(cbs_leg.amount_paise - amount) > amount_tol:
            add_break(BreakClass.AMOUNT_MISMATCH, rrn, legs,
                      f"CBS posted {cbs_leg.amount_paise} paise vs NPCI settled {amount} paise "
                      f"(diff {cbs_leg.amount_paise - amount:+d}).",
                      amount, txn_date)
            continue

        # Logical drift across the day boundary: cycle 4 on day D and cycle 1
        # on day D+1 are adjacent settlement cycles (drift 1), not drift 3.
        def abs_cycle(t: CanonicalTxn) -> int:
            return date.fromisoformat(t.txn_date).toordinal() * 4 + (t.cycle - 1)

        npci_leg = n[0] if n else cbs_leg
        drift = abs(abs_cycle(cbs_leg) - abs_cycle(npci_leg))
        drifted_day = cbs_leg.txn_date != txn_date
        if drift > cycle_tol:
            add_break(BreakClass.CROSS_CYCLE, rrn, legs,
                      f"Settled in cycle {npci_leg.cycle} on {txn_date}, posted in cycle "
                      f"{cbs_leg.cycle} on {cbs_leg.txn_date}. Within policy? Adjust drift tolerance.",
                      amount, txn_date)
            continue
        if drift > 0 or drifted_day:
            stats.matched_with_cycle_drift += 1
            continue

        stats.matched += 1

    stats.breaks = len(breaks)
    return stats, breaks
