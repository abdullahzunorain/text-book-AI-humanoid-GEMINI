---
id: "0013"
title: Refresh Architecture Plan Properly
stage: plan
date: 2026-03-08
surface: agent
model: claude-sonnet-4-6
feature: 003-physical-ai-robotics-textbook
branch: 003-physical-ai-robotics-textbook
user: abdullahzunorain
command: "/sp.plan refresh the architecture plan properly"
labels: ["plan","architecture","better-auth","subagents","rag","fastapi","refresh"]
links:
  spec: specs/003-physical-ai-robotics-textbook/spec.md
  ticket: null
  adr: specs/003-physical-ai-robotics-textbook/adrs/ADR-002-better-auth-fastapi.md
  pr: null
files:
  - specs/003-physical-ai-robotics-textbook/plan.md
  - specs/003-physical-ai-robotics-textbook/research.md
tests:
  - (none run)
---

## Prompt

/sp.plan refresh the architecture plan properly

## Response snapshot

Ran setup-plan.sh to initialize fresh plan template. Read all existing artifacts (spec.md, research.md, data-model.md, quickstart.md, openapi.yaml, actual backend/frontend source). Identified critical gaps in current MVP:

1. Chat/personalize/translate routes are NOT wired into main.py (only health endpoint is)
2. rag.py has broken relative imports (from crud_vectors import... instead of from src.db.crud_vectors import...)
3. better-auth integration missing from frontend
4. Per-chapter Personalize/Translate buttons not in Docusaurus
5. Claude Code Subagents/Skills not implemented (FR-010)

Wrote comprehensive plan.md covering:
- Current state table (✅ Done / ⚠️ Partial / ❌ Missing)
- Technical Context (full stack decisions)
- Constitution Check (all 10 gates)
- Actual project structure (realistic, not template placeholder)
- Phase 2A: Fix backend wiring + import paths
- Phase 2B: better-auth integration (frontend + FastAPI middleware)
- Phase 2C: Per-chapter action buttons in Docusaurus
- Phase 2D: Claude Code Subagents + Skills
- Phase 2E: TDD endpoint tests
- API contract summary, ADR register, risks

Updated research.md with FR-010 Subagents decision rationale.
Ran update-agent-context.sh claude successfully.

## Outcome

- ✅ Impact: Plan now accurately reflects actual codebase state and remaining work for all 4 bonus features
- 🧪 Tests: None run
- 📁 Files: plan.md (full rewrite), research.md (added FR-010 decision)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task breakdown, then `/sp.implement` to execute
- 🧠 Reflection: The critical gap (chat routes not wired into main.py) was discovered by reading actual source — confirms the value of plan refresh against real code

## Evaluation notes (flywheel)

- Failure modes observed: setup-plan.sh overwrites existing plan.md — ensured git history preserved old content before rewriting
- Graders run and results (PASS/FAIL): Constitution check: all 10 gates PASS
- Prompt variant (if applicable): sp.plan with explicit "refresh" instruction
- Next experiment (smallest change to try): run /sp.tasks to confirm task list aligns with phases 2A-2E
