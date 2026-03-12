# Research: Physical AI & Humanoid Robotics Textbook (AI-Native)

**Updated**: 2026-03-08

## Phase 0 — Research (Resolved)

All unknowns are resolved via ADRs. No open questions remain before implementation.

### Decision: Vector Dimension Strategy (ADR-001)
- **Decision**: Set `VECTOR_SIZE = 768` in `vector_store.py` to match `gemini-embedding-001` output.
- **Rationale**: `gemini-embedding-001` produces 768-dimensional vectors. The previous `3072` setting in `vector_store.py` was a mismatch that would cause ingestion failures.
- **Alternatives**: Using `text-embedding-004` (3072-dim) was considered but `gemini-embedding-001` is standard for the Flash model family.

### Decision: Auth Integration (ADR-002)
- **Decision**: Share the Neon Postgres database between Docusaurus (Node.js) and FastAPI (Python). FastAPI will query the `session` table directly to validate bearer tokens.
- **Rationale**: `better-auth` is a TypeScript-first library. A pure Python implementation is not available. Direct database validation is the most efficient cross-language pattern.
- **Alternatives**: A Node.js sidecar service was considered but rejected to avoid deployment complexity.

### Decision: Content Structure for RAG (ADR-003)
- **Decision**: Implement a hierarchy of module landing pages + 13 weekly sub-pages (Option C).
- **Rationale**: This provides the best balance between UX navigation and granular context retrieval for the RAG chatbot.
- **Alternatives**: A flat structure was rejected as it would overwhelm the sidebar and reduce citation accuracy.

### Decision: Technology Choices
| Choice | Rationale | Alternatives |
|--------|-----------|--------------|
| Gemini 2.0 Flash | Fast, high context window (1M+ tokens), generous free tier. | GPT-4o-mini |
| Render.com | Easy Docker deployment for FastAPI. | Vercel Serverless |
| GitHub Pages | Native Docusaurus deployment. | Netlify |
| Qdrant Cloud | Purpose-built vector search with hybrid filtering. | Pinecone |
| Neon | Serverless Postgres with branching, perfect for TDD. | Supabase |

### Decision: Claude Code Subagents Pattern (FR-010)
- **Decision**: Implement reusable Agent Skills as `.claude/commands/*.md` files using the Claude Code custom commands format.
- **Rationale**: Custom commands in `.claude/commands/` are Claude Code's native mechanism for reusable subagent workflows. They can be invoked via `/skill-name` within any session.
- **Skills planned**: `ingest-content` (run RAG ingestion pipeline), `gen-tests` (scaffold TDD tests), `gen-chapter` (generate Docusaurus chapter from topic outline).
- **Alternatives**: Standalone Python scripts were considered but lack the agentic context awareness of Claude Code commands.
