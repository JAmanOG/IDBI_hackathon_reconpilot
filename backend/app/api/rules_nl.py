"""Natural-language rule authoring: ops-manager prose → matching-rule JSON.

Live mode asks Google Gemini for a schema-constrained JSON edit of the
current rules; offline mode falls back to a deterministic phrase parser.
Every generated ruleset is dry-run against the current files before it
can be promoted.
"""
from __future__ import annotations

import json
import re

from app.config import GEMINI_MODEL

# OpenAPI-subset schema (Gemini response_schema does not take additionalProperties)
RULE_SCHEMA = {
    "type": "object",
    "properties": {
        "amount_tolerance_paise": {"type": "integer"},
        "cycle_drift_tolerance": {"type": "integer"},
        "route_timeouts_to": {"type": "string"},
        "explanation": {"type": "string", "description": "One sentence describing the change made"},
    },
    "required": ["amount_tolerance_paise", "cycle_drift_tolerance", "route_timeouts_to", "explanation"],
}


def author_rules(prompt: str, current: dict) -> dict:
    try:
        return _author_live(prompt, current)
    except Exception:
        return _author_mock(prompt, current)


def _author_live(prompt: str, current: dict) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY from env
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"CURRENT RULES:\n{json.dumps(current)}\n\nINSTRUCTION:\n{prompt}",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You translate a bank recon ops-manager's instruction into an updated matching-rule "
                "configuration for a 3-way UPI reconciliation engine. Start from the CURRENT rules and "
                "change only what the instruction asks. amount_tolerance_paise: allowed paise difference "
                "between legs. cycle_drift_tolerance: how many adjacent settlement cycles apart the CBS "
                "posting may be from the NPCI cycle and still auto-match. route_timeouts_to: queue name "
                "for deemed/timeout transactions."
            ),
            response_mime_type="application/json",
            response_schema=RULE_SCHEMA,
        ),
    )
    parsed = json.loads(response.text)
    return {**current, **parsed, "mode": "live"}


def _author_mock(prompt: str, current: dict) -> dict:
    """Deterministic phrase parser for the common demo instructions."""
    rules = dict(current)
    p = prompt.lower()
    explanations = []

    m = re.search(r"(?:tolerate|allow|permit)\s+(?:up to\s+)?(\d+)[- ]cycle", p)
    if m or "cycle drift" in p or "next cycle" in p:
        n = int(m.group(1)) if m else 1
        rules["cycle_drift_tolerance"] = n
        explanations.append(f"cycle drift tolerance set to {n}")
    m = re.search(r"(?:amount|paise)\s+tolerance\s+(?:of\s+)?(?:₹|rs\.?\s*)?(\d+)", p)
    if m:
        rules["amount_tolerance_paise"] = int(m.group(1))
        explanations.append(f"amount tolerance set to {m.group(1)} paise")
    if "strict" in p or "no drift" in p or "zero drift" in p:
        rules["cycle_drift_tolerance"] = 0
        explanations.append("cycle drift tolerance reset to 0")
    m = re.search(r"route\s+timeouts?\s+to\s+([\w -]+)", p)
    if m:
        rules["route_timeouts_to"] = m.group(1).strip()
        explanations.append(f"timeouts routed to '{m.group(1).strip()}'")

    rules["explanation"] = "; ".join(explanations) if explanations else \
        "No recognised instruction — rules unchanged (offline parser understands cycle-drift, amount-tolerance and timeout-routing phrases)."
    rules["mode"] = "mock"
    return rules
