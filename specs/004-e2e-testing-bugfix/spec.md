# Feature Specification: End-to-End Application Testing & Bug Resolution

**Feature Branch**: `004-e2e-testing-bugfix`
**Created**: 2026-03-09
**Status**: Draft
**Input**: User description: "Run the whole application and test each API endpoint of FastAPI, test everything using Playwright MCP server (non-headless browser), resolve all issues/errors/bugs found, use OpenAI SDK for agent building with Gemini models (OpenAI SDK compatible chat.completion), use Context7 for fetching latest documentation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend API Endpoint Validation (Priority: P1)

A developer starts the FastAPI backend server and systematically tests every API endpoint to ensure they respond correctly, handle errors gracefully, and return the expected data formats. This covers the health check, user management, RAG chat, content personalization, and Urdu translation endpoints.

**Why this priority**: The backend API is the foundation of the entire platform. If endpoints don't work, no frontend feature can function. This is the most critical validation.

**Independent Test**: Can be fully tested by starting the backend server and issuing HTTP requests to each endpoint. Delivers confidence that all 6 API routes are functional.

**Acceptance Scenarios**:

1. **Given** the backend server is running, **When** a GET request is sent to `/health`, **Then** the response returns status "ok" with database and vector store connection status
2. **Given** the backend server is running, **When** a POST request is sent to `/users/` with valid user data, **Then** a new user is created and returned with an ID
3. **Given** a user exists in the database, **When** a GET request is sent to `/users/{id}`, **Then** the user profile is returned with all fields
4. **Given** the backend server is running, **When** a POST request is sent to `/chat/` with a question, **Then** a RAG-powered response is returned with sources and session tracking
5. **Given** a logged-in user, **When** a POST request is sent to `/personalize/` with chapter content, **Then** the content is rewritten based on the user's hardware and software background
6. **Given** the backend server is running, **When** a POST request is sent to `/translate/` with English content, **Then** the content is translated to Urdu
7. **Given** the backend server is running, **When** a GET request is sent to `/users/lookup?email=...`, **Then** the matching user is returned or a 404 error for missing users
8. **Given** a request is missing required fields, **When** sent to any endpoint, **Then** a 422 validation error is returned with clear error details

---

### User Story 2 - Frontend Browser Testing with Playwright (Priority: P1)

A tester opens the Docusaurus textbook site in a real browser (non-headless mode) and verifies the complete user journey: page navigation across all chapters, the floating chat widget interaction, the authentication modal (sign up/sign in), and the per-chapter action buttons (Personalize and Translate to Urdu).

**Why this priority**: Frontend is the user-facing layer. Browser-based testing catches rendering issues, JavaScript errors, and interaction bugs that unit tests miss. Non-headless mode provides visual confirmation.

**Independent Test**: Can be fully tested by launching Playwright against the running Docusaurus dev server. Delivers confidence that users can navigate, chat, and interact with all features.

**Acceptance Scenarios**:

1. **Given** the Docusaurus site is running, **When** the homepage loads, **Then** all module links are visible and clickable
2. **Given** a chapter page is open, **When** the user scrolls to the bottom, **Then** the floating chat widget is visible and functional
3. **Given** the chat widget is open, **When** the user types a question and presses Enter, **Then** the question is sent to the backend and a response appears in the chat window
4. **Given** the user is not logged in, **When** they click "Sign In", **Then** the authentication modal opens with Sign In and Sign Up tabs
5. **Given** the auth modal is open, **When** the user fills in the Sign Up form and submits, **Then** a new account is created and the user is logged in
6. **Given** the user is logged in on a chapter page, **When** they click "Personalize", **Then** the chapter content is transformed based on their background
7. **Given** the user is logged in on a chapter page, **When** they click "Translate to Urdu", **Then** the chapter content is translated to Urdu
8. **Given** personalized/translated content is shown, **When** the user clicks "Revert to Original", **Then** the original content is restored

---

### User Story 3 - Bug Resolution and Application Stability (Priority: P1)

During testing, any errors, exceptions, broken endpoints, UI glitches, or integration failures discovered are immediately diagnosed and fixed. The application is brought to a fully working state where all features operate end-to-end without errors.

**Why this priority**: Testing without fixing is incomplete. The primary goal is a stable, working application. Every bug found must be resolved before the testing phase is considered complete.

**Independent Test**: Can be tested by re-running the full test suite after each fix. Delivers a stable application with zero known critical bugs.

**Acceptance Scenarios**:

1. **Given** a bug is found during API testing, **When** the root cause is identified, **Then** the code is fixed and the endpoint is re-tested to confirm the fix
2. **Given** a bug is found during browser testing, **When** the root cause is identified, **Then** the frontend or backend code is fixed and the browser test is re-run
3. **Given** all fixes are applied, **When** the full backend test suite runs, **Then** all tests pass with zero failures
4. **Given** all fixes are applied, **When** the frontend builds, **Then** the build completes with zero errors

---

### User Story 4 - OpenAI SDK Integration with Gemini Models (Priority: P2)

The backend's AI service layer uses the OpenAI SDK in a manner compatible with Gemini models via the OpenAI-compatible chat.completions endpoint. This ensures the RAG chat, personalization, and translation features all work through a standardized interface.

**Why this priority**: The AI integration is already partially implemented. This story ensures it follows best practices using the OpenAI SDK's chat.completion interface with Gemini models, verified through actual endpoint testing.

**Independent Test**: Can be tested by sending a chat message through the `/chat/` endpoint and confirming the response is generated by Gemini through the OpenAI SDK. Delivers a verified, standards-compliant AI integration.

**Acceptance Scenarios**:

1. **Given** the backend uses the OpenAI SDK, **When** a chat request is sent, **Then** the response is generated by the configured Gemini model via the OpenAI-compatible endpoint
2. **Given** a personalization request is sent, **When** processed by the AI service, **Then** the content is personalized using the Gemini model through chat.completions
3. **Given** a translation request is sent, **When** processed by the AI service, **Then** the content is translated using the Gemini model through chat.completions
4. **Given** the Gemini API rate limit is hit, **When** a request is made, **Then** a user-friendly error message is returned instead of a raw exception

---

### Edge Cases

- What happens when the backend server is not running but the frontend tries to send a chat message? (Expected: user-friendly error in chat widget)
- What happens when a user tries to sign up with an email that already exists? (Expected: clear error message, not a server crash)
- What happens when the Qdrant vector store is unreachable? (Expected: health endpoint reports vector_store as disconnected; chat returns graceful fallback)
- What happens when Gemini API quota is exhausted? (Expected: "AI service temporarily unavailable" message)
- What happens when extremely long text (>10,000 chars) is sent for personalization or translation? (Expected: handled gracefully, possibly truncated)
- What happens when an invalid or expired auth token is sent? (Expected: endpoint falls back to anonymous user or returns 401 as appropriate)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All 6 backend API endpoints MUST return correct HTTP status codes and response schemas when tested with valid inputs
- **FR-002**: All backend API endpoints MUST return appropriate error responses (422, 404, 401, 500) for invalid inputs, missing resources, and server errors
- **FR-003**: The backend MUST start successfully, connect to Neon Postgres and Qdrant Cloud, and serve requests on the configured port
- **FR-004**: The Docusaurus frontend MUST build without errors and serve all 13 chapter pages across 4 modules
- **FR-005**: The floating chat widget MUST send messages to the backend and display responses in the browser
- **FR-006**: The authentication modal MUST allow users to sign up with name, email, password, hardware background, and software background
- **FR-007**: The authentication modal MUST allow users to sign in with email and password
- **FR-008**: Per-chapter action buttons (Personalize, Translate to Urdu) MUST be visible only to logged-in users
- **FR-009**: The Personalize button MUST send chapter content to `/personalize/` and display transformed content inline
- **FR-010**: The Translate to Urdu button MUST send chapter content to `/translate/` and display translated content inline
- **FR-011**: A "Revert to Original" option MUST restore the original chapter content after personalization or translation
- **FR-012**: The backend AI service MUST use the OpenAI SDK with Gemini models through the chat.completions interface
- **FR-013**: Browser-based tests MUST run in non-headless (visible) mode using Playwright
- **FR-014**: Every bug discovered during testing MUST be diagnosed, fixed, and verified before the testing session is complete
- **FR-015**: The existing backend test suite (pytest) MUST continue to pass after all fixes are applied

### Key Entities

- **API Endpoint**: A backend route that accepts requests and returns responses (path, method, request schema, response schema, auth requirement)
- **Test Case**: A specific scenario being validated (endpoint or UI flow, input data, expected outcome, actual outcome, pass/fail status)
- **Bug Report**: An issue discovered during testing (description, root cause, affected file(s), fix applied, verification result)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of backend API endpoints (health, users CRUD, user lookup, chat, personalize, translate) respond with correct status codes and data formats
- **SC-002**: All 15+ existing backend unit tests pass after bug fixes are applied
- **SC-003**: The Docusaurus frontend builds successfully and all 13 chapter pages render without JavaScript errors
- **SC-004**: Browser-based Playwright tests cover the complete user journey: homepage → chapter navigation → chat interaction → sign up → sign in → personalize → translate → revert
- **SC-005**: Zero critical bugs remain after the testing and fix cycle is complete
- **SC-006**: Every discovered bug has a documented root cause and verified fix
- **SC-007**: The AI service (RAG chat, personalization, translation) successfully generates responses when the Gemini API quota is available
- **SC-008**: Graceful degradation is confirmed — users receive friendly error messages when external services (Gemini, Qdrant) are unavailable

## Assumptions

- The Gemini API key is valid and has available quota (free tier limits may apply; rate-limited responses are acceptable)
- Neon Postgres and Qdrant Cloud services are accessible from the development environment (WSL2)
- The Playwright MCP server is available in the development environment for browser-based testing
- Non-headless browser testing requires a display environment (WSL2 with GUI support or X server forwarding)
- Context7 MCP tools are available for fetching up-to-date library documentation when needed during implementation
- The OpenAI SDK is already installed and configured to connect to Gemini's OpenAI-compatible endpoint

## Scope

### In Scope

- Testing all FastAPI backend endpoints with real HTTP requests
- Testing the Docusaurus frontend in a real browser using Playwright (non-headless)
- Fixing all bugs discovered during testing
- Verifying the OpenAI SDK integration with Gemini models
- Running and verifying the existing pytest test suite
- Verifying frontend build success

### Out of Scope

- Load testing or performance benchmarking
- Security penetration testing
- Deployment to production (Render, GitHub Pages)
- Adding new features beyond what already exists
- Mobile responsiveness testing
- Cross-browser testing (Playwright will use its default browser)
