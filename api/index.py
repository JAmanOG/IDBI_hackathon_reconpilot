"""Vercel Python function entrypoint.

Vercel's Python runtime serves any ASGI app exported as `app`. The whole
FastAPI backend rides in one function; the React build is served by
Vercel's CDN (see vercel.json rewrites).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.api.main import app  # noqa: E402,F401
