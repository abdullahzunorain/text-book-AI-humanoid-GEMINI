---
id: "0014"
title: Generate Actionable Task Breakdown
stage: tasks
date: 2026-03-08
surface: agent
model: claude-sonnet-4-6
feature: 003-physical-ai-robotics-textbook
branch: 003-physical-ai-robotics-textbook
user: abdullahzunorain
command: "/sp.tasks generate the actionable task breakdown"
labels: ["tasks","tdd","better-auth","rag","subagents","fastapi","docusaurus"]
links:
  spec: specs/003-physical-ai-robotics-textbook/spec.md
  ticket: null
  adr: specs/003-physical-ai-robotics-textbook/adrs/ADR-002-better-auth-fastapi.md
  pr: null
files:
  - specs/003-physical-ai-robotics-textbook/tasks.md
tests:
  - (none run — tasks define the tests to write)
---

## Prompt

/sp.tasks generate the actionable task breakdown

## Response snapshot

Ran check-prerequisites.sh, loaded all design docs (plan.md, spec.md, data-model.md, contracts/openapi.yaml, research.md, quickstart.md). Read tasks-template.md for structure.

Generated comprehensive tasks.md with 65 tasks across 8 phases:

- Phase 1 (5 tasks): Verify existing setup (uv, npm, Docusaurus build)
- Phase 2 (17 tasks): Fix critical backend wiring gap — import paths, Pydantic schemas, TDD tests, API routes, wire into main.py
- Phase 3 (3 tasks): US1 verification (Docusaurus already complete)
- Phase 4 (6 tasks): US2+US3 — wire Chat.tsx to live backend, session_id, selected text
- Phase 5 (13 tasks): US4 — better-auth install, Neon migration, FastAPI auth middleware, AuthModal, useAuth hook, Layout auth state
- Phase 6 (6 tasks): US5 — ChapterActions component, contentApi service, DocItem override, content swap state
- Phase 7 (6 tasks): FR-010 — 3 Claude Code skills (ingest-content, gen-tests, gen-chapter)
- Phase 8 (9 tasks): Polish, error handling, deployment

Key decisions captured:
- Phase 2 (backend wiring) is the most critical gap — blocks everything
- TDD tasks marked [TEST] must fail before implementation
- 30 of 65 tasks are parallelizable [P]
- Max potential: 300 pts (100 base + 50 auth + 100 actions + 50 subagents)

## Outcome

- ✅ Impact: 65 specific, executable tasks covering all 6 hackathon deliverables
- 🧪 Tests: TDD test tasks defined (T012–T015, T035, T038)
- 📁 Files: specs/003-physical-ai-robotics-textbook/tasks.md
- 🔁 Next prompts: `/sp.implement` to start executing tasks, beginning with Phase 2
- 🧠 Reflection: Phase 2 (fix backend wiring) is the highest-priority gap — the RAG logic exists but is completely unexposed. All bonus features depend on this being fixed first.

## Evaluation notes (flywheel)

- Failure modes observed: tasks.md already had content (old version) — required Read before Write
- Graders run and results (PASS/FAIL): all 65 tasks follow checklist format (checkbox + ID + labels + file path)
- Prompt variant (if applicable): sp.tasks with "generate actionable" context
- Next experiment (smallest change to try): start with T006 (fix rag.py imports) — 15-minute task with high impact
