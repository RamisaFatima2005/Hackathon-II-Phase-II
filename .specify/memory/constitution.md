<!--
Sync Impact Report:
Version change: 0.0.0 -> 1.0.0 (Initial creation based on detailed user specification)
List of modified principles: All principles are new.
Added sections: All sections are new.
Removed sections: None.
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .gemini/commands/sp.adr.toml: ⚠ pending
  - .gemini/commands/sp.analyze.toml: ⚠ pending
  - .gemini/commands/sp.checklist.toml: ⚠ pending
  - .gemini/commands/sp.clarify.toml: ⚠ pending
  - .gemini/commands/sp.constitution.toml: ⚠ pending
  - .gemini/commands/sp.git.commit_pr.toml: ⚠ pending
  - .gemini/commands/sp.implement.toml: ⚠ pending
  - .gemini/commands/sp.phr.toml: ⚠ pending
  - .gemini/commands/sp.plan.toml: ⚠ pending
  - .gemini/commands/sp.specify.toml: ⚠ pending
  - .gemini/commands/sp.tasks.toml: ⚠ pending
Follow-up TODOs: None.
-->
# Hackathon Phase 2 - Multi-User Full-Stack Todo Web App Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All development (code generation, architectural decisions, task breakdowns) MUST strictly adhere to the Spec-Driven Development (SDD) methodology using Gemini Code + Spec-Kit Plus. Manual coding is PROHIBITED.

### II. Mandatory Technology Stack
The project MUST utilize the following technology stack without any deviations:
*   Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS for responsive UI.
*   Backend: Python FastAPI for REST API.
*   Database: Neon Serverless PostgreSQL with SQLModel ORM for models and queries.
*   Authentication: Better Auth for email/password signup/signin with JWT tokens.
*   Deployment: Vercel for frontend/backend.

### III. Security and Data Isolation
All API interactions MUST be secured using JWT tokens (Bearer header). User-specific data, particularly tasks, MUST be strictly isolated such that each user can only access and modify their own tasks.

### IV. API Contract Adherence
The backend API MUST strictly implement the defined endpoints, methods, and request/response structures. No deviations in paths, methods, or required parameters are permitted.
*   GET /api/{user_id}/tasks - List all tasks
*   POST /api/{user_id}/tasks - Add task (body: {title: str, description: str})
*   GET /api/{user_id}/tasks/{id} - Get single task
*   PUT /api/{user_id}/tasks/{id} - Update task
*   DELETE /api/{user_id}/tasks/{id} - Delete task
*   PATCH /api/{user_id}/tasks/{id}/complete - Toggle complete status
*   Auth Endpoints: POST /auth/signup, POST /auth/signin (return JWT).

### V. Core Feature Set (5 Features)
The application MUST implement exactly five core features for task management: Add Task, Delete Task, Update Task, View Task List, and Mark as Complete. No additional task management features are permitted in this phase.

### VI. Data Model Consistency
The database models MUST be implemented exactly as specified:
*   User: `id`, `email`, `password_hash`
*   Todo: `id`, `user_id`, `title`, `description`, `completed: bool`, `created_at`
Rationale: Ensures data integrity and compatibility across the full stack.

## Design and UI/UX Requirements

*   Frontend: MUST include dedicated pages for signup, signin, and a dashboard displaying the task list with CRUD forms.
*   Authentication Token Management: JWT tokens retrieved from authentication MUST be stored in `localStorage` on the frontend.
*   Responsive UI: The user interface MUST be built with a mobile-first approach using Tailwind CSS to ensure responsiveness across devices.

## Project Deliverables and Quality Assurance

*   Output Format: All generated documentation and code MUST be in Markdown format, clean, and error-free with appropriate comments.
*   Evaluation Focus: The primary focus for evaluation is a working demo, a complete and accurate spec history, and the absence of bugs.
*   Phase 1 Carryover: Core todo logic and structure from Phase 1 MUST be adapted and reused, transitioning from in-memory to persistent web-based implementation.

## Governance

This constitution defines the fundamental principles and constraints for the project.
Amendments to this constitution require a clear rationale, documentation in an ADR, and approval by project leadership.
Compliance with these principles MUST be verified during code reviews and testing phases.
Any proposed changes to the mandatory technology stack or core feature set require a MAJOR version bump.
Additions or material expansions of guidance require a MINOR version bump.
Clarifications, wording, or typo fixes require a PATCH version bump.

**Version**: 1.0.0 | **Ratified**: 2025-12-11 | **Last Amended**: 2025-12-11