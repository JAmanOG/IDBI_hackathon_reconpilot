"""ReconPilot API — FastAPI app.

Run:  uvicorn app.api.main:app --reload --port 8000
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import (ASSISTED_MINUTES_PER_BREAK, BOOTSTRAP_CLEAN, DATA_DIR,
                        DEFAULT_MATCH_RULES, IS_SERVERLESS,
                        MANUAL_MINUTES_PER_BREAK, RULES_PATH,
                        TAT_COMPENSATION_PER_DAY_INR)
from app.agent.agent import investigate
from app.datagen.generate import generate
from app.recon.matcher import run_recon
from app.recon.normalize import load_cbs, load_npci, load_switch
from app.store import db as store

app = FastAPI(title="ReconPilot", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_conn = store.connect()
_legs_cache: dict = {}


@app.on_event("startup")
def bootstrap_if_empty():
    """Serverless instances start with an empty /tmp — self-initialize.

    The generator is seeded, so every cold instance deterministically
    reproduces the same book and the same 75 breaks.
    """
    if not IS_SERVERLESS:
        return
    if (DATA_DIR / "npci_settlement.csv").exists() and store.latest_run(_conn):
        return
    generate(DATA_DIR, n_clean=BOOTSTRAP_CLEAN, seed=2026)
    npci, switch, cbs = _load_legs()
    rules = get_rules()
    stats, breaks = run_recon(npci, switch, cbs, rules)
    store.save_run(_conn, {**stats.__dict__, "elapsed_ms": 0,
                           "auto_match_rate": stats.auto_match_rate}, rules, breaks)


def get_rules() -> dict:
    if RULES_PATH.exists():
        return json.loads(RULES_PATH.read_text())
    return dict(DEFAULT_MATCH_RULES)


def save_rules(rules: dict) -> None:
    RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
    RULES_PATH.write_text(json.dumps(rules, indent=2))


def _load_legs():
    files = {
        "npci": DATA_DIR / "npci_settlement.csv",
        "switch": DATA_DIR / "switch_log.csv",
        "cbs": DATA_DIR / "cbs_gl_dump.csv",
    }
    missing = [k for k, p in files.items() if not p.exists()]
    if missing:
        raise HTTPException(400, f"Settlement files missing ({', '.join(missing)}). Run POST /api/generate-data first.")
    mtime = max(p.stat().st_mtime for p in files.values())
    if _legs_cache.get("mtime") != mtime:
        _legs_cache.update(
            mtime=mtime,
            npci=load_npci(files["npci"]),
            switch=load_switch(files["switch"]),
            cbs=load_cbs(files["cbs"]),
        )
    return _legs_cache["npci"], _legs_cache["switch"], _legs_cache["cbs"]


# ---------------------------------------------------------------- data & recon

class GenerateReq(BaseModel):
    clean: int = 50_000
    seed: int = 2026


@app.post("/api/generate-data")
def generate_data(req: GenerateReq):
    manifest = generate(DATA_DIR, n_clean=req.clean, seed=req.seed)
    _legs_cache.clear()
    return {"generated": manifest["files"], "seeded_breaks": manifest["seeded_counts"]}


@app.post("/api/recon/run")
def recon_run():
    npci, switch, cbs = _load_legs()
    rules = get_rules()
    t0 = time.perf_counter()
    stats, breaks = run_recon(npci, switch, cbs, rules)
    elapsed_ms = round((time.perf_counter() - t0) * 1000)
    run_id = store.save_run(_conn, {**stats.__dict__, "elapsed_ms": elapsed_ms,
                                    "auto_match_rate": stats.auto_match_rate}, rules, breaks)
    return {"run_id": run_id, "elapsed_ms": elapsed_ms,
            "auto_match_rate": stats.auto_match_rate,
            "stats": stats.__dict__, "breaks": len(breaks)}


@app.get("/api/summary")
def summary():
    run = store.latest_run(_conn)
    if not run:
        return {"run": None}
    open_breaks = store.list_breaks(_conn, run["id"], status="OPEN") + \
        store.list_breaks(_conn, run["id"], status="PROPOSED")
    resolved = store.list_breaks(_conn, run["id"], status="APPROVED")
    penalty_exposure = sum((b["tat"] or {}).get("compensation_accrued_inr", 0)
                           for b in open_breaks if b["tat"])
    accruing = sum(TAT_COMPENSATION_PER_DAY_INR for b in open_breaks
                   if b["tat"] and b["tat"].get("breached"))
    amount_at_risk = sum(b["amount_paise"] for b in open_breaks) / 100
    minutes_saved = len(resolved) * (MANUAL_MINUTES_PER_BREAK - ASSISTED_MINUTES_PER_BREAK)
    by_status: dict = {}
    for row in _conn.execute("SELECT status, COUNT(*) n FROM breaks WHERE run_id=? GROUP BY status", (run["id"],)):
        by_status[row["status"]] = row["n"]
    return {
        "run": run,
        "kpis": {
            "auto_match_rate": run["stats"].get("auto_match_rate"),
            "total_rrns": run["stats"].get("total_rrns"),
            "elapsed_ms": run["stats"].get("elapsed_ms"),
            "open_breaks": len(open_breaks),
            "penalty_exposure_inr": penalty_exposure,
            "penalty_accruing_per_day_inr": accruing,
            "amount_at_risk_inr": round(amount_at_risk, 2),
            "minutes_saved": minutes_saved,
            "fte_saved": round(minutes_saved / (8 * 60), 2),
        },
        "by_class": run["stats"].get("by_class", {}),
        "by_status": by_status,
    }


# ---------------------------------------------------------------- breaks

@app.get("/api/breaks")
def breaks(status: str | None = None, break_class: str | None = None):
    run = store.latest_run(_conn)
    if not run:
        return []
    return store.list_breaks(_conn, run["id"], status=status, break_class=break_class)


@app.get("/api/breaks/{break_id}")
def break_detail(break_id: int):
    brk = store.get_break(_conn, break_id)
    if not brk:
        raise HTTPException(404, "break not found")
    brk["audit"] = store.audit_for_break(_conn, break_id)
    return brk


@app.post("/api/breaks/{break_id}/investigate")
def break_investigate(break_id: int):
    brk = store.get_break(_conn, break_id)
    if not brk:
        raise HTTPException(404, "break not found")
    if brk["status"] in ("APPROVED", "REJECTED"):
        raise HTTPException(400, f"break already {brk['status']}")
    store.set_break_state(_conn, break_id, "INVESTIGATING")
    result = investigate(_conn, brk)
    return {"break_id": break_id, **result}


class DecisionReq(BaseModel):
    decision: str  # "approve" | "reject"
    reason: str = ""
    supervisor: str = "supervisor"


@app.post("/api/breaks/{break_id}/decision")
def break_decision(break_id: int, req: DecisionReq):
    brk = store.get_break(_conn, break_id)
    if not brk:
        raise HTTPException(404, "break not found")
    if brk["status"] != "PROPOSED":
        raise HTTPException(400, "no pending proposal on this break")
    status = "APPROVED" if req.decision == "approve" else "REJECTED"
    store.set_break_state(_conn, break_id, status, resolved_by=req.supervisor)
    store.audit(_conn, "supervisor", f"proposal_{req.decision}d", break_id,
                {"reason": req.reason, "by": req.supervisor})
    return {"break_id": break_id, "status": status}


# ---------------------------------------------------------------- rules

@app.get("/api/rules")
def rules_get():
    return get_rules()


class NLRuleReq(BaseModel):
    instruction: str


@app.post("/api/rules/nl")
def rules_nl(req: NLRuleReq):
    from app.api.rules_nl import author_rules

    current = get_rules()
    proposed = author_rules(req.instruction, current)

    npci, switch, cbs = _load_legs()
    stats_now, _ = run_recon(npci, switch, cbs, current)
    stats_new, _ = run_recon(npci, switch, cbs, proposed)
    return {
        "current_rules": current,
        "proposed_rules": {k: v for k, v in proposed.items() if k not in ("explanation", "mode")},
        "explanation": proposed.get("explanation"),
        "mode": proposed.get("mode"),
        "dry_run": {
            "breaks_before": stats_now.breaks,
            "breaks_after": stats_new.breaks,
            "by_class_before": stats_now.by_class,
            "by_class_after": stats_new.by_class,
        },
    }


class PromoteReq(BaseModel):
    rules: dict


@app.post("/api/rules/promote")
def rules_promote(req: PromoteReq):
    allowed = {"version", "match_keys", "amount_tolerance_paise",
               "cycle_drift_tolerance", "route_timeouts_to", "notes"}
    rules = {k: v for k, v in req.rules.items() if k in allowed}
    rules["version"] = int(get_rules().get("version", 1)) + 1
    save_rules(rules)
    store.audit(_conn, "supervisor", "rules_promoted", detail=rules)
    return {"promoted": rules}


# ---------------------------------------------------------------- static frontend

_dist = Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "dist"
if _dist.exists():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="frontend")
