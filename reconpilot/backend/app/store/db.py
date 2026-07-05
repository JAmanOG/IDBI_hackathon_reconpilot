"""SQLite break register + append-only audit log.

Break lifecycle: OPEN → INVESTIGATING → PROPOSED → APPROVED / REJECTED.
Every state change and every agent step is journaled to audit_log —
that append-only trail is the explainability artifact the demo shows.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS recon_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    stats_json TEXT NOT NULL,
    rules_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS breaks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    rrn TEXT NOT NULL,
    break_class TEXT NOT NULL,
    severity TEXT NOT NULL,
    amount_paise INTEGER NOT NULL,
    txn_date TEXT NOT NULL,
    age_days INTEGER NOT NULL,
    note TEXT NOT NULL,
    legs_json TEXT NOT NULL,
    tat_json TEXT,
    status TEXT NOT NULL DEFAULT 'OPEN',
    proposal_json TEXT,
    agent_trace_json TEXT,
    resolved_at TEXT,
    resolved_by TEXT
);
CREATE INDEX IF NOT EXISTS idx_breaks_run ON breaks(run_id);
CREATE INDEX IF NOT EXISTS idx_breaks_status ON breaks(status);
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    at TEXT NOT NULL,
    actor TEXT NOT NULL,          -- 'agent' | 'supervisor' | 'system'
    break_id INTEGER,
    action TEXT NOT NULL,
    detail_json TEXT
);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = Path(path or DB_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def audit(conn: sqlite3.Connection, actor: str, action: str,
          break_id: int | None = None, detail: dict | None = None) -> None:
    conn.execute(
        "INSERT INTO audit_log(at, actor, break_id, action, detail_json) VALUES(?,?,?,?,?)",
        (now(), actor, break_id, action, json.dumps(detail or {})),
    )
    conn.commit()


def save_run(conn: sqlite3.Connection, stats: dict, rules: dict, breaks: list[dict]) -> int:
    cur = conn.execute(
        "INSERT INTO recon_runs(started_at, stats_json, rules_json) VALUES(?,?,?)",
        (now(), json.dumps(stats), json.dumps(rules)),
    )
    run_id = cur.lastrowid
    for b in breaks:
        conn.execute(
            """INSERT INTO breaks(run_id, rrn, break_class, severity, amount_paise,
               txn_date, age_days, note, legs_json, tat_json)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (run_id, b["rrn"], b["break_class"], b["severity"], b["amount_paise"],
             b["txn_date"], b["age_days"], b["note"], json.dumps(b["legs"]),
             json.dumps(b.get("tat")) if b.get("tat") else None),
        )
    conn.commit()
    audit(conn, "system", "recon_run_completed", detail={"run_id": run_id, "breaks": len(breaks)})
    return run_id


def latest_run(conn: sqlite3.Connection) -> dict | None:
    r = conn.execute("SELECT * FROM recon_runs ORDER BY id DESC LIMIT 1").fetchone()
    if not r:
        return None
    return {"id": r["id"], "started_at": r["started_at"],
            "stats": json.loads(r["stats_json"]), "rules": json.loads(r["rules_json"])}


def _row_to_break(r: sqlite3.Row, include_legs: bool = False) -> dict:
    d = {
        "id": r["id"], "run_id": r["run_id"], "rrn": r["rrn"],
        "break_class": r["break_class"], "severity": r["severity"],
        "amount_paise": r["amount_paise"], "txn_date": r["txn_date"],
        "age_days": r["age_days"], "note": r["note"], "status": r["status"],
        "tat": json.loads(r["tat_json"]) if r["tat_json"] else None,
        "proposal": json.loads(r["proposal_json"]) if r["proposal_json"] else None,
        "resolved_at": r["resolved_at"], "resolved_by": r["resolved_by"],
    }
    if include_legs:
        d["legs"] = json.loads(r["legs_json"])
        d["agent_trace"] = json.loads(r["agent_trace_json"]) if r["agent_trace_json"] else None
    return d


def list_breaks(conn: sqlite3.Connection, run_id: int, status: str | None = None,
                break_class: str | None = None) -> list[dict]:
    q = "SELECT * FROM breaks WHERE run_id=?"
    args: list = [run_id]
    if status:
        q += " AND status=?"
        args.append(status)
    if break_class:
        q += " AND break_class=?"
        args.append(break_class)
    q += " ORDER BY CASE severity WHEN 'HIGH' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END, amount_paise DESC"
    return [_row_to_break(r) for r in conn.execute(q, args).fetchall()]


def get_break(conn: sqlite3.Connection, break_id: int) -> dict | None:
    r = conn.execute("SELECT * FROM breaks WHERE id=?", (break_id,)).fetchone()
    return _row_to_break(r, include_legs=True) if r else None


def set_break_state(conn: sqlite3.Connection, break_id: int, status: str,
                    proposal: dict | None = None, trace: list | None = None,
                    resolved_by: str | None = None) -> None:
    sets, args = ["status=?"], [status]
    if proposal is not None:
        sets.append("proposal_json=?")
        args.append(json.dumps(proposal))
    if trace is not None:
        sets.append("agent_trace_json=?")
        args.append(json.dumps(trace))
    if status in ("APPROVED", "REJECTED"):
        sets.append("resolved_at=?")
        args.append(now())
        sets.append("resolved_by=?")
        args.append(resolved_by or "supervisor")
    args.append(break_id)
    conn.execute(f"UPDATE breaks SET {', '.join(sets)} WHERE id=?", args)
    conn.commit()


def audit_for_break(conn: sqlite3.Connection, break_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT at, actor, action, detail_json FROM audit_log WHERE break_id=? ORDER BY id",
        (break_id,)).fetchall()
    return [{"at": r["at"], "actor": r["actor"], "action": r["action"],
             "detail": json.loads(r["detail_json"] or "{}")} for r in rows]
