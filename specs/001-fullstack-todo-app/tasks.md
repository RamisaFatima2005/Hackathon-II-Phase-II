---
description: "Task list for feature implementation"
---

# Tasks: Full-Stack Todo Application

**Input**: Design documents from `/specs/001-fullstack-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with FastAPI and SQLModel dependencies in `backend/`
- [X] T003 Initialize Next.js project with TypeScript and Tailwind CSS in `frontend/`
- [X] T004 [P] Configure linting and formatting tools for both `backend/` and `frontend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T005 Setup database schema and migrations framework in `backend/src/database.py`
- [X] T006 [P] Implement authentication/authorization framework using Better Auth in `backend/src/services/auth_utils.py` and `backend/src/services/jwt_handler.py`
- [X] T007 [P] Setup API routing and middleware structure in `backend/src/main.py` and `backend/src/dependencies.py`
- [X] T008 Create base models for User and Todo in `backend/src/models/user.py` and `backend/src/models/todo.py`
- [X] T009 Configure error handling and logging infrastructure in `backend/src/main.py`
- [X] T010 Setup environment configuration management for `backend/` and `frontend/`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: As a new user, I want to sign up with my email and password so I can access the todo application. As an existing user, I want to sign in with my credentials to manage my tasks.

**Independent Test**: Can be fully tested by creating a new user, logging in, and verifying successful token acquisition and dashboard access, independent of todo list features.

### Implementation for User Story 1

- [X] T011 [P] [US1] Create `UserCreate` and `Token` schemas in `backend/src/schemas/auth.py`
- [X] T012 [P] [US1] Implement signup endpoint in `backend/src/api/auth.py`
- [X] T013 [US1] Implement signin endpoint in `backend/src/api/auth.py`
- [X] T014 [US1] Implement `/users/me` endpoint to get current user details in `backend/src/api/auth.py`
- [X] T015 [P] [US1] Create `AuthContext.tsx` to manage auth state in `frontend/src/contexts/`
- [X] T016 [P] [US1] Create signin page at `frontend/src/app/signin/page.tsx`
- [X] T017 [P] [US1] Create signup page at `frontend/src/app/signup/page.tsx`
- [X] T018 [US1] Create `ProtectedRoute.tsx` component in `frontend/src/components/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View My Todo List (Priority: P1)

**Goal**: As a logged-in user, I want to view a list of all my existing todo tasks, including their title, description, completion status, and creation timestamp, so I can see what I need to do.

**Independent Test**: Can be tested by logging in and verifying that existing tasks for that user are displayed correctly on the dashboard.

### Implementation for User Story 2

- [X] T030 [US2] Create protected route wrapper for dashboard in `frontend/src/app/dashboard/page.tsx`
- [X] T031 [US2] Create `TaskList.tsx` component to display tasks in `frontend/src/components/TaskList.tsx`
- [ ] T032 [P] [US2] In `TaskList.tsx`, fetch tasks on mount and handle loading state
- [ ] T033 [US2] In `TaskList.tsx`, display tasks in a responsive table/cards and handle empty state
- [ ] T034 [P] [US2] Create `TaskItem.tsx` component to display a single task with its details in `frontend/src/components/TaskItem.tsx`
- [ ] T035 [US2] In `TaskItem.tsx`, show completion status and action buttons (edit, delete, complete)
- [ ] T036 [US2] In `frontend/src/app/dashboard/page.tsx`, integrate the `TaskList.tsx` component.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Add a New Todo Task (Priority: P1)

**Goal**: As a logged-in user, I want to add a new todo task with a title and description so I can keep track of new items.

**Independent Test**: Can be tested by logging in, adding a task through the UI, and verifying its appearance in the list and persistence after refresh.

### Implementation for User Story 3

- [X] T040 [P] [US3] Create `AddTaskForm.tsx` component with title and description fields in `frontend/src/components/AddTaskForm.tsx`
- [X] T041 [US3] In `AddTaskForm.tsx`, implement form validation and submit handler.
- [X] T042 [US3] In `AddTaskForm.tsx`, auto-refresh the task list after adding a new task.
- [X] T043 [US3] In `frontend/src/app/dashboard/page.tsx`, integrate the `AddTaskForm.tsx` component.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T100 [P] Documentation updates in `README.md`
- [ ] T101 Code cleanup and refactoring across `frontend/` and `backend/`
- [ ] T102 [P] Add unit tests for key components
- [ ] T103 Security hardening of API endpoints
- [ ] T104 Run `quickstart.md` validation

---

## Dependencies & Execution Order

- **Setup (Phase 1)** must complete before **Foundational (Phase 2)**.
- **Foundational (Phase 2)** must complete before any User Story phase.
- User stories can be implemented in parallel after Phase 2 is complete.
- Within each user story, models should be created before services, and services before API endpoints.
- UI components can be developed in parallel with backend work for the same user story.
