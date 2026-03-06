# Data Model: Physical AI & Humanoid Robotics Textbook (AI-Native)

## Neon Postgres Tables

### `user` (Extends better-auth schema)
| Field | Type | Constraint | Notes |
|---|---|---|---|
| `id` | `VARCHAR` | PK | better-auth uses string IDs |
| `name` | `VARCHAR(255)` | NOT NULL | Display name |
| `email` | `VARCHAR(255)` | UNIQUE, NOT NULL | Login identifier |
| `email_verified` | `BOOLEAN` | DEFAULT FALSE | better-auth field |
| `hardware_background` | `VARCHAR(100)` | NOT NULL | Signup question (e.g. `RTX GPU`, `No GPU`) |
| `software_background` | `VARCHAR(100)` | NOT NULL | Signup question (e.g. `Intermediate Python`) |
| `learning_goal` | `VARCHAR(100)` | NULLABLE | Signup question (e.g. `Job transition`) |
| `created_at` | `TIMESTAMPTZ` | DEFAULT NOW() | |

### `session` (better-auth standard)
| Field | Type | Constraint | Notes |
|---|---|---|---|
| `id` | `VARCHAR` | PK | Session ID |
| `token` | `VARCHAR` | UNIQUE, NOT NULL | Bearer token sent in Authorization header |
| `user_id` | `VARCHAR` | FK → user.id | |
| `expires_at` | `TIMESTAMPTZ` | NOT NULL | FastAPI checks this before serving request |
| `created_at` | `TIMESTAMPTZ` | DEFAULT NOW() | |

### `message` (FastAPI managed)
| Field | Type | Constraint | Notes |
|---|---|---|---|
| `id` | `SERIAL` | PK | |
| `user_id` | `VARCHAR` | FK → user.id, NULLABLE | NULL for anonymous users |
| `session_id` | `VARCHAR(36)` | NOT NULL | UUID grouping messages per conversation |
| `role` | `VARCHAR(10)` | NOT NULL | `'user'` or `'assistant'` |
| `content` | `TEXT` | NOT NULL | Message body |
| `created_at` | `TIMESTAMPTZ` | DEFAULT NOW() | |

## Qdrant Collection: `textbook_chunks`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Auto-generated per chunk |
| **vector** | `float[768]` | `gemini-embedding-001` output |
| `text` | string (payload) | Raw chunk text (max ~500 tokens) |
| `module_name` | string (payload) | e.g. `"Module 1: ROS 2 Architecture"` |
| `chapter_title` | string (payload) | e.g. `"Week 3: Nodes, Topics & Services"` |
| `url` | string (payload) | Relative Docusaurus path |
| `chunk_index` | int (payload) | Position within the chapter |

## Relationships
- **User (1) → Message (N)**: A user can have many chat messages.
- **User (1) → Session (N)**: A user can have multiple chat sessions.
- **Message (N) → Session (1)**: Messages are grouped by session.
- **User Context**: `hardware_background` and `software_background` fields are mandatory for personalization to work.
