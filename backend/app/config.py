"""Central configuration for ReconPilot."""
from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("RECONPILOT_DATA_DIR", BASE_DIR / "data"))
DB_PATH = Path(os.environ.get("RECONPILOT_DB", DATA_DIR / "reconpilot.db"))
RULES_PATH = DATA_DIR / "match_rules.json"

# LLM settings — agent falls back to deterministic mock mode when no key is set.
# Google Gemini via the google-genai SDK; client reads GEMINI_API_KEY / GOOGLE_API_KEY.
GEMINI_MODEL = os.environ.get("RECONPILOT_MODEL", "gemini-2.5-flash")
AGENT_MAX_TOOL_TURNS = 12

# Ops-economics assumptions (shown as editable chips in the UI)
MANUAL_MINUTES_PER_BREAK = 25
ASSISTED_MINUTES_PER_BREAK = 4
TAT_COMPENSATION_PER_DAY_INR = 100  # RBI DPSS.CO.PD No.629 (20 Sep 2019): UPI auto-reversal T+1, then Rs.100/day
UPI_REVERSAL_TAT_DAYS = 1  # T+1

DEFAULT_MATCH_RULES = {
    "version": 1,
    "match_keys": ["rrn"],
    "amount_tolerance_paise": 0,
    "cycle_drift_tolerance": 0,
    "route_timeouts_to": "exceptions-desk",
    "notes": "Baseline rules. Edit via the NL rule-authoring endpoint.",
}
