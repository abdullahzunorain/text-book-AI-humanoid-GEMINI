# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
Every feature, chapter, or component must originate from a formal specification (`specs/<feature>/spec.md`). Implementation only begins after a validated plan (`plan.md`) and task list (`tasks.md`) are approved. Vibe-coding is strictly prohibited.

### II. Docusaurus-First Documentation
The textbook is the primary artifact. All technical content must be authored in Markdown/MDX following Docusaurus conventions. The structure must align with the "Physical AI & Humanoid Robotics" course modules defined in the hackathon syllabus.

### III. RAG-Native Integration
The RAG chatbot is a core component, not an add-on. Every chapter must be "RAG-ready" (clear structure, relevant metadata). The chatbot must utilize FastAPI, Neon Serverless Postgres, and Qdrant Cloud to provide precise answers based ONLY on the textbook content.

### IV. Knowledge Capture (PHR)
Every user interaction must be recorded in a Prompt History Record (PHR). This ensures transparency, reproducibility, and a clear audit trail of the project's evolution.

### V. Test-First Implementation
For the RAG backend and interactive components, TDD is mandatory. For the textbook content, "tests" include link validation, linting, and RAG accuracy checks.

### VI. Modern AI Stack
We strictly adhere to the mandated stack: Docusaurus (Frontend), FastAPI (API), Neon (Database), Qdrant (Vector DB), and OpenAI Agents.

## Technical Constraints
- **Styling:** Prefer Vanilla CSS for Docusaurus customizations unless otherwise specified.
- **Authentication:** Use `better-auth` for the signup/signin feature.
- **Deployment:** The book must be deployable to GitHub Pages.

## Governance
- This constitution supersedes all other development practices in this project.
- Amendments require a formal ADR and update to this document.
- All PRs must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-03-03 | **Last Amended**: 2026-03-03
