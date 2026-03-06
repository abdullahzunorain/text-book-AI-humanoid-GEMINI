# Feature Specification: Physical AI & Humanoid Robotics Textbook (AI-Native)

**Feature Branch**: `003-physical-ai-robotics-textbook`  
**Created**: 2026-03-04
**Status**: Draft  
**Input**: User description: "1 Automatic Zoom Hackathon I: Create a Textbook for Teaching Physical AI & Humanoid Robotics Course... use wsl for bash command and uv python manager for this project...use test-driven development must test each and everything you are building and also check the all the fast api end-points..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Textbook Navigation and Reading (Priority: P1)

As a student, I want to access a professionally structured online textbook covering Physical AI and Humanoid Robotics (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA) so that I can learn these cutting-edge technologies through an interactive platform.

**Why this priority**: This is the base functionality. Without the content and the site, there is no platform for AI features.

**Independent Test**: Can be fully tested by deploying to GitHub Pages and verifying all 4 modules (ROS 2, Digital Twin, NVIDIA Isaac, VLA) are navigable.

**Acceptance Scenarios**:

1. **Given** the user is on the homepage, **When** they navigate through the sidebar, **Then** they see content for all 4 required modules.
2. **Given** the site is built, **When** it is deployed to GitHub Pages, **Then** all internal links and images resolve correctly.

---

### User Story 2 - Integrated RAG Chatbot (Priority: P1)

As a student, I want an integrated AI chatbot that answers questions based *only* on the textbook content so that I have a reliable tutor that doesn't hallucinate outside information.

**Why this priority**: Core deliverable. RAG is the "AI-native" heart of the project.

**Independent Test**: Can be fully tested by asking the chatbot a specific question found in the text and a question NOT found in the text.

**Acceptance Scenarios**:

1. **Given** a question about ROS 2 nodes (present in text), **When** the user submits the query, **Then** the chatbot provides an answer cited from the textbook.
2. **Given** a question about baking a cake (not in text), **When** the user submits the query, **Then** the chatbot politely declines or states it only knows about the textbook.

---

### User Story 3 - Selected Text Contextual Query (Priority: P1)

As a student, I want to highlight a confusing paragraph and ask the chatbot to explain it so that I can get immediate clarification on specific text.

**Why this priority**: Explicit core requirement from the hackathon brief.

**Independent Test**: Can be fully tested by selecting text in the browser, opening the chat, and asking "Explain this".

**Acceptance Scenarios**:

1. **Given** the user has selected a sentence about "VLA models", **When** they ask "What does this mean?", **Then** the chatbot responds specifically using the selected text as primary context.

---

### User Story 4 - Better-Auth Signup/Signin with Background (Priority: P2)

As a new user, I want to sign up using a secure system and provide my hardware/software background so the system knows how to tailor the learning experience for me.

**Why this priority**: High-value bonus (50 points) and foundational for personalization. Uses mandated `better-auth`.

**Independent Test**: Can be fully tested by completing the signup flow and verifying the background data is stored in the Neon database.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they sign up, **Then** they are presented with mandatory questions about their hardware and software background.
2. **Given** a returning user, **When** they sign in via `better-auth`, **Then** they are successfully authenticated and their profile is loaded.

---

### User Story 5 - Content Personalization & Urdu Translation (Priority: P3)

As a logged-in user, I want to click buttons to "Personalize" or "Translate to Urdu" the current chapter so that the material is easier for me to understand.

**Why this priority**: Bonus features (50 points each). Enhances the "AI-native" experience.

**Independent Test**: Can be fully tested by clicking the action buttons and verifying the DOM updates with transformed text.

**Acceptance Scenarios**:

1. **Given** a user with "Software" background, **When** they click "Personalize", **Then** the content uses software analogies (e.g., comparing a robot joint to an API endpoint).
2. **Given** a user clicks "Translate to Urdu", **When** the process completes, **Then** the chapter content is displayed in Urdu while keeping technical terms in English where appropriate.

### Edge Cases

- What happens when the Gemini API or Qdrant Cloud reaches its free tier limit? (System must fail gracefully with a user-friendly message).
- How does the system handle very large text selections for contextual queries? (Must truncate or warn if context window is exceeded).
- What happens if a user skips the background questions during signup? (Registration should be blocked or defaults should be applied).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST be built with Docusaurus and deployed to GitHub Pages.
- **FR-002**: The system MUST implement a RAG chatbot using FastAPI, Neon Postgres, and Qdrant Cloud.
- **FR-003**: The chatbot MUST use the OpenAI SDK (configured for Gemini) for generating responses.
- **FR-004**: The system MUST support "Selected Text" queries where highlighted text is sent as context to the backend.
- **FR-005**: The system MUST implement User Authentication (Signup/Signin) using `better-auth`.
- **FR-006**: The system MUST collect and store "Software Background" and "Hardware Background" for every user.
- **FR-007**: The system MUST provide "Personalize" and "Translate" buttons at the start of each chapter.
- **FR-008**: The backend MUST be managed using `uv` and tested using TDD principles (FastAPI endpoint testing).
- **FR-009**: The system MUST record every user interaction in a Prompt History Record (PHR).

### Key Entities 

- **User Profile**: Managed by `better-auth` + custom fields (Hardware/Software background).
- **Textbook Content**: Markdown/MDX files chunked and embedded in Qdrant.
- **Chat Session**: Stored in Neon Postgres with link to User and Session ID.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of FastAPI endpoints have corresponding automated tests that pass.
- **SC-002**: RAG chatbot responses are generated in under 5 seconds (average).
- **SC-003**: Personalized content matches the user's background in 90% of test cases.
- **SC-004**: User registration successfully captures background data in 100% of completed signups.
- **SC-005**: The site builds and deploys to GitHub Pages without errors.
