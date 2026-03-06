# Implementation Plan: Physical AI & Humanoid Robotics Textbook (AI-Native)

**Branch**: `003-physical-ai-robotics-textbook` | **Date**: 2026-03-05 | **Spec**: `specs/003-physical-ai-robotics-textbook/spec.md`
**Status**: Ready for `/sp.tasks`

## Summary

Build a fully deployed, AI-native textbook platform for the "Physical AI & Humanoid Robotics" course. The platform consists of:
1. A **Docusaurus 3** static site (deployed to GitHub Pages) containing structured course content across 4 modules and 13 weekly chapters.
2. A **FastAPI** backend (deployed to Render.com) that powers a RAG chatbot, content personalization, and Urdu translation — all backed by **Qdrant Cloud** (vectors) and **Neon Serverless Postgres** (relational data).
3. A **better-auth** authentication layer integrated into the Docusaurus frontend, with session validation shared via the Neon database to FastAPI.
4. **Claude Code Subagents** automating content generation, RAG indexing, and test scaffolding for bonus points.

## Technical Context

| Concern | Decision |
|---|---|
| **Frontend** | Docusaurus 3 (React, TypeScript) |
| **Backend** | FastAPI (Python 3.13, managed by `uv`) |
| **Vector DB** | Qdrant Cloud Free Tier — collection size `768` (ADR-001) |
| **Embedding Model** | `gemini-embedding-001` — 768 dimensions (ADR-001) |
| **LLM** | `gemini-2.0-flash` via Google Generative AI SDK |
| **Relational DB** | Neon Serverless Postgres (SQLAlchemy async) |
| **Auth** | `better-auth` (frontend) + shared Neon session table (FastAPI) (ADR-002) |
| **Testing** | `pytest` + `httpx.AsyncClient` — TDD mandatory for all endpoints |
| **Package Manager** | `uv` for Python, `npm` for Node.js |
| **Dev Environment** | WSL2 (Ubuntu 22.04) |
| **Frontend Deploy** | GitHub Pages via `npm run deploy` + GitHub Actions |
| **Backend Deploy** | Render.com (free tier, Docker) |
| **Content Structure** | Module landing pages + weekly sub-pages (ADR-003) |

## Constitution Check

- [x] Spec-Driven: Plan originates from `spec.md`.
- [x] Docusaurus-First: Frontend is Docusaurus 3.
- [x] RAG-Native: Core feature using FastAPI/Neon/Qdrant.
- [x] TDD: Pytest before implementation.
- [x] `uv` Tooling: All Python commands via `uv`.
- [x] WSL2: Scripts documented for WSL2.
- [x] Knowledge Capture: PHRs required.
- [x] Mandated Auth: `better-auth` integration.

## Project Structure

### Documentation

```text
specs/003-physical-ai-robotics-textbook/
├── spec.md                  # Requirements
├── plan.md                  # This file
├── research.md              # Phase 0 output
├── data-model.md            # Phase 1 output
├── quickstart.md            # Phase 1 output
├── adrs/
│   ├── ADR-001-vector-dimensions.md
│   ├── ADR-002-better-auth-fastapi.md
│   └── ADR-003-content-structure.md
├── contracts/
│   └── openapi.yaml         # FastAPI contracts
└── tasks.md                 # Phase 2 output
```

### Source Code

```text
backend/
├── src/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   ├── services/
│   └── db/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── theme/
│   └── services/
└── docs/

scripts/                     # Claude Code Subagent scripts
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Two deployments | Docusaurus (static) vs FastAPI (dynamic) | Vercel serverless would require full FastAPI refactor. |
| Auth complexity | Cross-language (TS auth + Python backend) | Direct consequence of mandated stack. |
