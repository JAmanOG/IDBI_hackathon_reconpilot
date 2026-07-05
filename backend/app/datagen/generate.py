"""Synthetic 3-way UPI settlement data generator.

Produces one settlement window (a few cycles across a few days) as three
files a recon desk would actually receive:

  npci_settlement.csv  — NPCI raw/settlement extract (network truth)
  switch_log.csv       — the bank's UPI switch log
  cbs_gl_dump.csv      — Finacle-style GL/transaction dump

plus ground_truth.json recording every seeded break so the demo can prove
detection is complete (nothing found that wasn't seeded, nothing seeded
that wasn't found).

Column semantics mirror the real artefacts (RRN join key, response codes,
settlement cycles, Finacle narration format `UPI/DR/{rrn}/{vpa}/{remark}`)
without reproducing any proprietary file layout.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

from app.config import DATA_DIR

BANKS = ["HDFC", "SBIN", "ICIC", "AXIS", "YESB", "PYTM", "KKBK", "BARB"]
HANDLES = ["okhdfcbank", "oksbi", "okicici", "ybl", "paytm", "axl", "ibl", "apl"]
FIRST = ["rahul", "priya", "amit", "sneha", "vikas", "kavita", "arjun", "meera",
         "sanjay", "pooja", "imran", "lakshmi", "ravi", "anita", "deepak", "fatima"]
MERCHANTS = [
    ("swiggy", "icici"), ("zomato", "hdfcbank"), ("bigbasket", "ybl"),
    ("jiomart", "axl"), ("irctc", "sbi"), ("bookmyshow", "icici"),
    ("dmart", "hdfcbank"), ("phonepemerchant", "ybl"), ("bharatpe", "ibl"),
    ("reliancetrends", "axl"), ("medplus", "okicici"), ("bpclpetrol", "sbi"),
]
REMARKS = ["Payment", "UPI", "Bill payment", "Order", "Transfer", "Recharge", "Groceries"]


def _rrn(day: date, serial: int) -> str:
    # 12-digit RRN: YYDDD (julian) + 7-digit serial — the shape desks recognise.
    return f"{day:%y}{day.timetuple().tm_yday:03d}{serial:07d}"


def _txn_id(day: date, serial: int) -> str:
    return f"IDB{day:%y%m%d}{serial:011d}"


def _vpa(rng: random.Random) -> str:
    style = rng.random()
    if style < 0.45:
        return f"{rng.choice(FIRST)}{rng.randint(1, 999)}@{rng.choice(HANDLES)}"
    if style < 0.8:
        return f"{rng.randint(70000_00000, 99999_99999)}@{rng.choice(HANDLES)}"
    return f"{rng.choice(FIRST)}.{rng.choice(FIRST)}@{rng.choice(HANDLES)}"


def _amount_paise(rng: random.Random, p2m: bool) -> int:
    if p2m:
        rupees = rng.choice([49, 99, 120, 149, 210, 349, 420, 550, 799, 1200, 1850, 2400])
        rupees += rng.randint(0, 400)
    else:
        rupees = rng.choice([100, 500, 1000, 2000, 5000, 10000, 15000]) + rng.randint(0, 2000)
    return rupees * 100 + rng.choice([0, 0, 0, 50])


def generate(
    out_dir: Path,
    n_clean: int = 50_000,
    n_timeout: int = 30,
    n_missing_cbs: int = 10,
    n_orphan_cbs: int = 5,
    n_amount_mismatch: int = 5,
    n_duplicate_cbs: int = 10,
    n_cross_cycle: int = 15,
    n_failed_clean: int = 400,
    seed: int = 2026,
) -> dict:
    rng = random.Random(seed)
    out_dir.mkdir(parents=True, exist_ok=True)

    today = date.today()
    # Settlement window: T-6 .. T-1 so TAT clocks show real accrual at demo time.
    days = [today - timedelta(days=d) for d in range(6, 0, -1)]

    npci_rows: list[dict] = []
    switch_rows: list[dict] = []
    cbs_rows: list[dict] = []
    truth: list[dict] = []
    serial = 0
    cbs_entry = 0

    def base_txn(day: date, force_outward: bool | None = None) -> dict:
        nonlocal serial
        serial += 1
        p2m = rng.random() < 0.62
        outward = force_outward if force_outward is not None else (rng.random() < 0.55)
        if p2m and outward:
            m, h = rng.choice(MERCHANTS)
            payee = f"{m}@{h}"
            payer = _vpa(rng)
        else:
            payer, payee = _vpa(rng), _vpa(rng)
        return {
            "rrn": _rrn(day, serial),
            "txn_id": _txn_id(day, serial),
            "day": day,
            "cycle": rng.randint(1, 4),
            "amount": _amount_paise(rng, p2m),
            "outward": outward,
            "payer": payer,
            "payee": payee,
            "hhmmss": f"{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:{rng.randint(0, 59):02d}",
            "acct": f"01{rng.randint(10**8, 10**9 - 1)}",
        }

    def push_npci(t: dict, resp: str) -> None:
        npci_rows.append({
            "RRN": t["rrn"], "TXN_ID": t["txn_id"],
            "TXN_DATE": t["day"].isoformat(), "TXN_TIME": t["hhmmss"],
            "AMOUNT_PAISE": t["amount"],
            "TXN_TYPE": "PAY",
            "DR_CR": "DR" if t["outward"] else "CR",
            "PAYER_VPA": t["payer"], "PAYEE_VPA": t["payee"],
            "REMITTER_BANK": "IDIB" if t["outward"] else rng.choice(BANKS),
            "BENEFICIARY_BANK": rng.choice(BANKS) if t["outward"] else "IDIB",
            "RESP_CODE": resp,
            "SETTLEMENT_CYCLE": t["cycle"],
        })

    def push_switch(t: dict, resp: str, status: str) -> None:
        switch_rows.append({
            "SWITCH_TXN_REF": f"SW{t['rrn']}",
            "RRN": t["rrn"], "UPI_TXN_ID": t["txn_id"],
            "LOCAL_TIMESTAMP": f"{t['day'].isoformat()} {t['hhmmss']}",
            "AMOUNT_PAISE": t["amount"],
            "DIRECTION": "OUTWARD" if t["outward"] else "INWARD",
            "PAYER_VPA": t["payer"], "PAYEE_VPA": t["payee"],
            "RESP_CODE": resp, "STATUS": status,
            "CYCLE": t["cycle"],
        })

    def push_cbs(t: dict, amount: int | None = None, cycle: int | None = None,
                 day: date | None = None) -> None:
        nonlocal cbs_entry
        cbs_entry += 1
        amt = amount if amount is not None else t["amount"]
        dr = t["outward"]
        cp = t["payee"] if dr else t["payer"]
        cbs_rows.append({
            "CBS_ENTRY_ID": f"FIN{cbs_entry:09d}",
            "ACCOUNT_NO": t["acct"],
            "TRAN_ID": f"S{rng.randint(10**7, 10**8 - 1)}",
            "TRAN_DATE": (day or t["day"]).isoformat(),
            "VALUE_DATE": (day or t["day"]).isoformat(),
            "DR_CR": "DR" if dr else "CR",
            "AMOUNT_PAISE": amt,
            "NARRATION": f"UPI/{'DR' if dr else 'CR'}/{t['rrn']}/{cp}/{rng.choice(REMARKS)}",
            "GL_CODE": "SB001",
            "CYCLE_POSTED": cycle if cycle is not None else t["cycle"],
        })

    # ---- clean, fully matched transactions -------------------------------
    for _ in range(n_clean):
        t = base_txn(rng.choice(days))
        push_npci(t, "00")
        push_switch(t, "00", "SUCCESS")
        push_cbs(t)

    # ---- clean failures (consistent everywhere; no CBS posting expected) --
    for _ in range(n_failed_clean):
        t = base_txn(rng.choice(days))
        push_npci(t, "U30")
        push_switch(t, "U30", "FAILED")

    def record(t: dict, cls: str) -> None:
        truth.append({"rrn": t["rrn"], "class": cls, "amount_paise": t["amount"],
                      "txn_date": t["day"].isoformat()})

    # ---- seeded breaks ----------------------------------------------------
    # 1) Timeout / deemed: customer debited, credit unconfirmed. Oldest days
    #    so the Rs.100/day clock shows accrual.
    for i in range(n_timeout):
        t = base_txn(days[i % 3], force_outward=True)  # T-6..T-4
        push_npci(t, "91")
        push_switch(t, "91", "TIMEOUT")
        push_cbs(t)  # debit sits in CBS, no reversal
        record(t, "TIMEOUT_DEBIT_NO_CREDIT")

    # 2) Success at NPCI+switch, CBS posting failed
    for _ in range(n_missing_cbs):
        t = base_txn(rng.choice(days))
        push_npci(t, "00")
        push_switch(t, "00", "SUCCESS")
        record(t, "MISSING_IN_CBS")

    # 3) Orphan CBS posting — nothing at NPCI/switch
    for _ in range(n_orphan_cbs):
        t = base_txn(rng.choice(days))
        push_cbs(t)
        record(t, "MISSING_AT_NPCI")

    # 4) Amount mismatch (fat-finger / truncation at CBS)
    for _ in range(n_amount_mismatch):
        t = base_txn(rng.choice(days))
        push_npci(t, "00")
        push_switch(t, "00", "SUCCESS")
        delta = rng.choice([100, 1000, 9000, -500])
        push_cbs(t, amount=max(100, t["amount"] + delta))
        record(t, "AMOUNT_MISMATCH")

    # 5) Duplicate CBS posting (double debit)
    for _ in range(n_duplicate_cbs):
        t = base_txn(rng.choice(days), force_outward=True)
        push_npci(t, "00")
        push_switch(t, "00", "SUCCESS")
        push_cbs(t)
        push_cbs(t)  # the duplicate leg
        record(t, "DUPLICATE_CBS_POSTING")

    # 6) Cross-cycle drift: settled cycle c, posted cycle c+1 (next day when c==4)
    for _ in range(n_cross_cycle):
        t = base_txn(rng.choice(days[:-1]))
        push_npci(t, "00")
        push_switch(t, "00", "SUCCESS")
        drift_day = t["day"] + timedelta(days=1) if t["cycle"] == 4 else t["day"]
        push_cbs(t, cycle=min(t["cycle"] + 1, 4) if t["cycle"] < 4 else 1, day=drift_day)
        record(t, "CROSS_CYCLE")

    rng.shuffle(npci_rows)
    rng.shuffle(switch_rows)
    rng.shuffle(cbs_rows)

    def dump(name: str, rows: list[dict]) -> None:
        with open(out_dir / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    dump("npci_settlement.csv", npci_rows)
    dump("switch_log.csv", switch_rows)
    dump("cbs_gl_dump.csv", cbs_rows)

    manifest = {
        "generated_for": today.isoformat(),
        "files": {"npci": len(npci_rows), "switch": len(switch_rows), "cbs": len(cbs_rows)},
        "seeded_breaks": truth,
        "seeded_counts": {
            "TIMEOUT_DEBIT_NO_CREDIT": n_timeout,
            "MISSING_IN_CBS": n_missing_cbs,
            "MISSING_AT_NPCI": n_orphan_cbs,
            "AMOUNT_MISMATCH": n_amount_mismatch,
            "DUPLICATE_CBS_POSTING": n_duplicate_cbs,
            "CROSS_CYCLE": n_cross_cycle,
        },
    }
    (out_dir / "ground_truth.json").write_text(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate synthetic 3-way UPI settlement files")
    ap.add_argument("--clean", type=int, default=50_000)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out", type=Path, default=DATA_DIR)
    args = ap.parse_args()
    m = generate(args.out, n_clean=args.clean, seed=args.seed)
    print(json.dumps({"files": m["files"], "seeded": m["seeded_counts"]}, indent=2))
