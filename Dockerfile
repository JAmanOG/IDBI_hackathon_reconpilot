# ReconPilot — single-container deployment (Render / Railway / Fly.io / AWS App Runner).
# Vercel does NOT run Docker; for Vercel use vercel.json + api/index.py instead.

# --- stage 1: build the React frontend -------------------------------------
FROM node:22-slim AS webbuild
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- stage 2: python runtime ------------------------------------------------
FROM python:3.12-slim
WORKDIR /srv
ENV PYTHONUNBUFFERED=1 \
    RECONPILOT_DATA_DIR=/srv/data

COPY backend/pyproject.toml backend/
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pandas google-genai python-dotenv

COPY backend/app backend/app
# static mount in app.api.main resolves to <repo>/frontend/dist relative to backend/
COPY --from=webbuild /web/dist frontend/dist

WORKDIR /srv/backend
EXPOSE 8000
# $PORT is injected by Render/Railway/App Runner; default 8000 locally
CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
