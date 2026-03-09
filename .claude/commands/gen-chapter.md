# Generate Textbook Chapter

Autonomous skill to generate a Docusaurus MDX chapter following the existing textbook structure.

## Input

Provide module name and week number as arguments, e.g., `/gen-chapter "Module 1: ROS 2" week-4`

## Steps

1. Read existing chapter files in `frontend/docs/` to understand the content structure:
   - Module landing page (`_category_.json`)
   - Weekly chapter files (e.g., `week-1-*.md`)
2. Analyze the writing style, heading structure, and section pattern:
   - Introduction / Overview
   - Core Concepts (with subheadings)
   - Hands-On Exercise / Lab
   - Key Takeaways
   - Exercises / Review Questions
3. Generate a new chapter file in the correct module directory:
   - File: `frontend/docs/<module-dir>/week-<N>-<slug>.md`
   - Front matter: `sidebar_position`, `title`, `description`
   - Content: Follow the detected pattern with relevant technical content
4. Update `_category_.json` if the new week changes the sidebar order
5. Run `cd frontend && npm run build` to verify the new chapter builds without errors

## Content Guidelines

- Write at university textbook level
- Include code examples in Python/ROS 2/relevant language
- Add Mermaid diagrams for architecture concepts
- Include 3-5 review questions at the end
- Reference related chapters with relative links
- Keep each section focused and scannable

## Output

Report: file path, chapter title, section count, build pass/fail status.
