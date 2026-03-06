# ADR-002: Cross-Language Session Validation (better-auth + FastAPI)

**Status**: Accepted  
**Date**: 2026-03-05

## Context
`better-auth` is used on the Docusaurus frontend (TypeScript), while the backend is FastAPI (Python). The backend needs to validate sessions to protect personalization and translation features.

## Decision
We will use a **Shared Database Pattern**. FastAPI will directly query the `session` table managed by `better-auth` in the Neon Postgres database.

## Rationale
- `better-auth` is primarily a TypeScript library. There is no mature Python client.
- Both services use the same Neon Postgres database.
- Direct database validation is stateless (from the app's perspective) and highly efficient.
- Avoids the complexity of a Node.js sidecar service.

## Consequences
- The FastAPI application must have read access to the `session` table.
- Authorization header in FastAPI will expect the better-auth bearer token.
- Validation logic in Python must check the `expires_at` column.
