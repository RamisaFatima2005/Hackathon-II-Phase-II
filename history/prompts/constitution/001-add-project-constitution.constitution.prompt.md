---
id: 001
title: Add project constitution
stage: constitution
date: 2025-12-11
surface: agent
model: gemini-1.5-flash-latest
feature: none
branch: N/A
user: user
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

/sp.constitution

Project Name: Hackathon Phase 2 - Multi-User Full-Stack Todo Web App

Core Objective: Transform Phase 1's in-memory console todo app into a modern full-stack web app with persistent storage, user authentication, and responsive UI. Support multi-user tasks (each user's tasks isolated). Implement exactly 5 features: Add Task, Delete Task, Update Task, View Task List, Mark as Complete. No additional features.

Mandatory Technology Stack (NO CHANGES ALLOWED):
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS for responsive UI.
- Backend: Python FastAPI for REST API.
- Database: Neon Serverless PostgreSQL with SQLModel ORM for models and queries.
- Authentication: Better Auth for email/password signup/signin with JWT tokens.
- Deployment: Vercel for frontend/backend.

Key Constraints:
- Spec-Driven Development ONLY: All code generated via Claude Code + Spec-Kit Plus. No manual coding.
- Security: JWT tokens for API auth (Bearer header), user_id based task isolation.
- API Endpoints Exact (use these paths):
  - GET /api/{user_id}/tasks - List all tasks
  - POST /api/{user_id}/tasks - Add task (body: {title: str, description: str})
  - GET /api/{user_id}/tasks/{id} - Get single task
  - PUT /api/{user_id}/tasks/{id} - Update task
  - DELETE /api/{user_id}/tasks/{id} - Delete task
  - PATCH /api/{user_id}/tasks/{id}/complete - Toggle complete status
- Auth Endpoints: POST /auth/signup, POST /auth/signin (return JWT).
- Frontend: Pages for signup, signin, dashboard (task list + CRUD forms). Use localStorage for JWT.
- Database Models: User (id, email, password_hash), Todo (id, user_id, title, description, completed: bool, created_at).
- Responsive: Mobile-first UI with Tailwind.
- Phase 1 Carryover: Reuse basic todo logic (e.g., task structure) but make persistent and web-based.
- Output Format: Always Markdown. Generate clean, error-free code with comments.
- Evaluation Focus: Working demo, spec history, no bugs.

Generate the full constitution.md file now.

## Response snapshot

The project constitution has been successfully generated and saved to `.specify/memory/constitution.md`.

**Summary:**
*   **New Version:** `1.0.0`
*   **Version Rationale:** This is a major version bump, as it represents the initial creation of the project constitution based on a comprehensive specification.
*   **Files Flagged for Manual Follow-up:**
    *   `.specify/templates/plan-template.md`
    *   `.specify/templates/spec-template.md`
    *   `.specify/templates/tasks-template.md`
    *   All `.toml` files in `.gemini/commands/`
*   **Suggested Commit Message:** `docs: add project constitution v1.0.0`

## Outcome

- ✅ Impact: Project constitution created successfully.
- 🧪 Tests: No tests run for constitution creation.
- 📁 Files: 1 file created: .specify/memory/constitution.md
- 🔁 Next prompts: Address template updates flagged in Sync Impact Report.
- 🧠 Reflection: The shell script for PHR creation failed. Used agent-native file writing instead.

## Evaluation notes (flywheel)

- Failure modes observed: Shell script for PHR creation failed to execute.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Investigate shell script execution for PHR creation on Windows.
