<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0 (MAJOR — initial ratification)

Added principles:
  1. End-to-End Reliability (new)
  2. API-First Architecture (new)
  3. Test-Driven Stability (new)
  4. AI Integration Standard (new)
  5. Observability and Error Handling (new)
  6. Documentation First (new)
  7. Security and Secrets (new)
  8. Reproducible Development Environment (new)
  9. Bug Resolution Policy (new)
  10. Continuous Verification (new)

Added sections:
  - Quality Gates (new)
  - Development Workflow (new)
  - Governance (filled from template)

Removed sections: none (template placeholders replaced)

Templates requiring updates:
  - .specify/templates/plan-template.md — ✅ compatible (Constitution Check
    gate reads principles dynamically)
  - .specify/templates/spec-template.md — ✅ compatible (no constitution
    references to update)
  - .specify/templates/tasks-template.md — ✅ compatible (task categories
    align with principles)

Follow-up TODOs: none
-->

# Physical AI Textbook Platform Constitution

## Core Principles

### I. End-to-End Reliability

All features MUST be testable end-to-end. Backend APIs, frontend UI, and
AI services MUST work together as a complete system. Every feature MUST
include automated tests where possible.

- No feature is considered complete until it works across the full stack.
- Integration points between services (backend ↔ Qdrant, backend ↔ Gemini,
  frontend ↔ backend) MUST be verified with real or mocked connections.
- Failures at any layer MUST produce clear, actionable diagnostics.

### II. API-First Architecture

The FastAPI backend is the source of truth. All frontend interactions MUST
go through clearly defined API endpoints with documented request and
response schemas.

- Every endpoint MUST have a Pydantic request and response schema.
- The frontend MUST NOT embed business logic; it delegates to the API.
- API contracts (OpenAPI/Swagger) MUST stay current with implementation.

### III. Test-Driven Stability

Every endpoint and critical user flow MUST be covered by tests. This
includes pytest tests for backend APIs and Playwright tests for browser
interactions.

- Backend: `pytest` with `httpx.AsyncClient` for all FastAPI endpoints.
- Frontend: Playwright browser tests for critical user journeys.
- Playwright tests MUST run in non-headless mode during debugging to allow
  visual verification.
- Tests MUST pass before any feature branch is merged.

### IV. AI Integration Standard

All AI features MUST use the OpenAI SDK interface. Gemini models MUST be
accessed using OpenAI-compatible `chat.completions` APIs to maintain
provider portability.

- The `openai` Python package is the standard client for LLM calls.
- Model configuration (model name, temperature, max_tokens) MUST be
  driven by environment variables, not hardcoded.
- Embedding model and dimensions MUST be configurable to support model
  upgrades without code changes.

### V. Observability and Error Handling

All services MUST return clear error messages and MUST NOT expose raw
stack traces to the user. Failures from external services (Gemini API,
Qdrant, or database) MUST degrade gracefully.

- HTTP error responses MUST use standard status codes (400, 401, 404, 422,
  500) with a human-readable `detail` message.
- Rate-limit errors (429) from AI providers MUST return a user-friendly
  fallback message, not an exception.
- Server logs MUST include error type and context for debugging.

### VI. Documentation First

All major features MUST have clear documentation in the repository,
including endpoint descriptions, environment variables, and system
architecture.

- `README.md` MUST document setup, architecture, API reference, and
  deployment instructions.
- Every environment variable MUST be listed in `.env.example` with a
  description.
- API endpoints MUST be documented in the OpenAPI spec (`/docs`).

### VII. Security and Secrets

API keys, database URLs, and secrets MUST NOT be committed to the
repository. All secrets MUST be loaded through environment variables.

- `.env` files MUST be in `.gitignore`.
- `.env.example` MUST contain placeholder values, never real credentials.
- Auth tokens MUST be transmitted via `Authorization: Bearer` headers.
- No secret or credential MAY appear in logs, error messages, or
  client-facing responses.

### VIII. Reproducible Development Environment

The application MUST be runnable locally with clear setup instructions.
Developers MUST be able to start backend, frontend, and tests with
minimal setup.

- Backend: `cd backend && uv sync && uv run uvicorn src.main:app`
- Frontend: `cd frontend && npm install && npm start`
- Tests: `cd backend && uv run pytest tests/ -v`
- All external service dependencies (Neon, Qdrant, Gemini) MUST be
  documented with account setup steps.

### IX. Bug Resolution Policy

Any bug discovered during testing MUST be documented with root cause and
verified fix before closing.

- Every bug fix MUST include a re-test confirming the fix.
- Bugs that affect multiple components MUST be traced to the root cause,
  not patched at the symptom level.
- The full test suite MUST pass after every bug fix.

### X. Continuous Verification

Before any feature is considered complete, the backend test suite,
Playwright E2E tests, and frontend build MUST pass successfully.

- `uv run pytest tests/ -v` — all backend tests MUST pass.
- `npm run build` — frontend MUST build with zero errors.
- Playwright E2E tests (when present) MUST pass for critical user flows.
- These checks MUST be run before creating a pull request.

## Quality Gates

Every feature MUST pass through these gates in order:

1. **Spec Gate**: Feature specification written and checklist approved.
2. **Plan Gate**: Architecture plan reviewed; constitution check passed.
3. **Test Gate**: Tests written for all endpoints and critical flows.
4. **Implementation Gate**: Code implemented; all tests pass.
5. **Integration Gate**: Full-stack verification; frontend build clean;
   Playwright tests pass in non-headless mode.
6. **Documentation Gate**: README, API docs, and env vars updated.

## Development Workflow

1. **Branch**: Create a numbered feature branch (`NNN-short-name`).
2. **Specify**: Write a feature spec (`/sp.specify`).
3. **Plan**: Create an architecture plan (`/sp.plan`).
4. **Tasks**: Break down into testable tasks (`/sp.tasks`).
5. **Implement**: Follow TDD where applicable; commit after each phase.
6. **Verify**: Run full test suite + frontend build + E2E tests.
7. **Document**: Update README and API docs as needed.
8. **Review**: Create PR; verify constitution compliance.

## Governance

This constitution is the highest-authority document for the Physical AI
Textbook Platform. All specs, plans, tasks, and implementations MUST
comply with these principles.

- **Amendments**: Any change to this constitution MUST be documented with
  rationale, versioned, and recorded in a PHR. Principle removals or
  redefinitions require a MAJOR version bump.
- **Compliance**: Every `/sp.plan` execution includes a Constitution Check
  gate. Non-compliant plans MUST NOT proceed to implementation.
- **Conflict resolution**: If a spec or plan conflicts with a principle,
  the constitution takes precedence. Exceptions require an ADR with
  explicit justification.
- **Versioning**: MAJOR.MINOR.PATCH — MAJOR for principle changes, MINOR
  for new sections or material expansions, PATCH for clarifications.

**Version**: 1.0.0 | **Ratified**: 2026-03-09 | **Last Amended**: 2026-03-09
