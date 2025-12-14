# Feature Specification: Full-Stack Todo Application

**Feature Branch**: `001-fullstack-todo-app`
**Created**: 2025-12-11
**Status**: Draft
**Input**: Using the constitution.md from Hackathon Phase 2 Todo App. Specify the initial high-level spec for the entire full-stack app. Requirements: 1. User Authentication: Email/password signup and signin. On success, issue JWT token valid for 24 hours. Store in frontend localStorage. 2. Database Setup: PostgreSQL tables for User and Todo. Auto-migrate on startup. 3. Backend API: Implement all 6 exact endpoints with SQLModel CRUD operations. Verify JWT in middleware to extract user_id and restrict access. 4. Frontend Structure: Next.js app with routes: / (signin), /signup, /dashboard (protected, requires token). Dashboard shows user's task list, add form, edit/delete buttons per task. 5. Features Integration: - View List: Fetch and display tasks in a responsive table/card view (title, desc, completed status, timestamp). - Add: Form with title/desc, POST to API. - Update: Inline edit or modal, PUT to API. - Delete: Confirm button, DELETE to API. - Mark Complete: Checkbox toggle, PATCH to API. 6. Error Handling: 401 for unauth, 404 for not found, validation errors. 7. Persistence: All tasks saved/retrieved from Neon DB, not in-memory. Output: Markdown spec file named 'initial-spec.md' with sections: Overview, User Stories, API Specs, UI Components, Database Schema.

## Overview

This specification outlines the initial high-level requirements for the "Hackathon Phase 2 - Multi-User Full-Stack Todo Web App". The primary objective is to transform the Phase 1 in-memory console todo app into a modern full-stack web application. It will feature persistent storage, user authentication, a responsive UI, and support multi-user tasks with strict isolation of each user's data.

### Core Requirements

1.  **User Authentication**: Implement email/password signup and signin. Upon successful authentication, a JWT token valid for 24 hours will be issued and stored in the frontend's `localStorage`.
2.  **Database Setup**: Configure PostgreSQL with tables for `User` and `Todo` entities. The database schema must auto-migrate on application startup.
3.  **Backend API**: Develop a FastAPI backend implementing the six specified CRUD endpoints for todo tasks using SQLModel. JWT verification middleware will be used to extract `user_id` and enforce task access restrictions.
4.  **Frontend Structure**: A Next.js application with routes for `/` (signin), `/signup`, and `/dashboard`. The `/dashboard` route will be protected, requiring a valid JWT token. The dashboard will display the user's task list, provide a form for adding new tasks, and include edit/delete buttons for each task.
5.  **Features Integration (Todo CRUD)**:
    *   **View List**: Fetch and display tasks in a responsive table/card view, showing title, description, completed status, and creation timestamp.
    *   **Add**: A form allowing users to add new tasks with a title and description, sending a POST request to the API.
    *   **Update**: Functionality for inline editing or via a modal to modify a task's title or description, sending a PUT request to the API.
    *   **Delete**: A confirmation step before sending a DELETE request to the API to remove a task.
    *   **Mark Complete**: A checkbox or toggle to change a task's completion status, sending a PATCH request to the API.
6.  **Error Handling**: Implement robust error handling, returning appropriate HTTP status codes such as 401 for unauthorized access, 404 for not found resources, and specific validation errors (e.g., 400 Bad Request).
7.  **Persistence**: All task data and user information will be persistently stored and retrieved from the Neon PostgreSQL database, moving away from in-memory storage.

## User Scenarios & Testing

### User Story 1 - User Authentication (Priority: P1)

As a new user, I want to sign up with my email and password so I can access the todo application. As an existing user, I want to sign in with my credentials to manage my tasks.

**Why this priority**: Essential for multi-user functionality and security, it's the gateway to all other features.

**Independent Test**: Can be fully tested by creating a new user, logging in, and verifying successful token acquisition and dashboard access, independent of todo list features.

**Acceptance Scenarios**:

1.  **Given** I am on the signup page, **When** I enter a unique, valid email and password and submit, **Then** my account is created, I receive a JWT, and I am redirected to the dashboard.
2.  **Given** I am on the signin page, **When** I enter my registered email and password and submit, **Then** I receive a valid JWT, it's stored in `localStorage`, and I am redirected to my dashboard.
3.  **Given** I am on the signin page, **When** I enter invalid credentials, **Then** I see an error message (e.g., "Invalid credentials") and remain on the signin page.
4.  **Given** I am a logged-in user, **When** I try to access a protected route (e.g., `/dashboard`) without a valid or expired token, **Then** I am redirected to the signin page with an unauthorized message.

---

### User Story 2 - View My Todo List (Priority: P1)

As a logged-in user, I want to view a list of all my existing todo tasks, including their title, description, completion status, and creation timestamp, so I can see what I need to do.

**Why this priority**: Core functionality for any todo application, allowing users to see their data.

**Independent Test**: Can be tested by logging in and verifying that existing tasks for that user are displayed correctly on the dashboard.

**Acceptance Scenarios**:

1.  **Given** I am logged in and navigate to the dashboard, **When** the page loads, **Then** I see a responsive display of my tasks, showing title, description, completed status (e.g., checkbox), and creation timestamp for each.
2.  **Given** I am logged in and have no tasks, **When** I navigate to the dashboard, **Then** I see a message indicating no tasks are present (e.g., "No tasks yet. Add one!").

---

### User Story 3 - Add a New Todo Task (Priority: P1)

As a logged-in user, I want to add a new todo task with a title and description so I can keep track of new items.

**Why this priority**: Allows users to populate their task list, directly enabling the primary use case.

**Independent Test**: Can be tested by logging in, adding a task through the UI, and verifying its appearance in the list and persistence after refresh.

**Acceptance Scenarios**:

1.  **Given** I am logged in and on the dashboard, **When** I fill out the "Add Task" form with a title and description and submit, **Then** the new task appears at the top (or bottom, consistent) of my todo list, and the form fields are cleared.
2.  **Given** I am logged in and on the dashboard, **When** I try to add a task with an empty title, **Then** I see a validation error message (e.g., "Title cannot be empty").

---

### User Story 4 - Update an Existing Todo Task (Priority: P2)

As a logged-in user, I want to modify the title or description of an existing task so I can correct mistakes or update details.

**Why this priority**: Provides essential flexibility for task management, though less critical than viewing and adding.

**Independent Test**: Can be tested by modifying an existing task through the UI and verifying the changes are reflected in the list and persisted.

**Acceptance Scenarios**:

1.  **Given** I am logged in and on the dashboard, **When** I select an existing task to edit, modify its title or description, and save, **Then** the task updates in my list with the new details (e.g., via inline edit or a modal).
2.  **Given** I am logged in, and I try to update a task that does not belong to me (e.g., by manipulating the `task_id` in the request), **Then** I receive an unauthorized error (401 response) and the task remains unchanged.

---

### User Story 5 - Mark a Todo Task as Complete/Incomplete (Priority: P2)

As a logged-in user, I want to toggle the completion status of a task so I can track my progress.

**Why this priority**: Enhances task management by allowing users to track progress, a common todo app feature.

**Independent Test**: Can be tested by toggling a task's completion status and observing the visual change and persistence.

**Acceptance Scenarios**:

1.  **Given** I am logged in and on the dashboard, **When** I click the "Mark Complete" checkbox or button for a task, **Then** the task's status visually changes (e.g., text is struck through, or it moves to a "completed" section).
2.  **Given** I am logged in, and I try to mark a task as complete that does not belong to me, **Then** I receive an unauthorized error (401 response) and the task remains unchanged.

---

### User Story 6 - Delete a Todo Task (Priority: P2)

As a logged-in user, I want to remove a task from my list when it's no longer relevant so my list stays clean.

**Why this priority**: Allows users to manage their task list effectively by removing unwanted items.

**Independent Test**: Can be tested by deleting a task and verifying its removal from the list and database.

**Acceptance Scenarios**:

1.  **Given** I am logged in and on the dashboard, **When** I click the "Delete" button for a task and confirm the action, **Then** the task is immediately removed from my list.
2.  **Given** I am logged in, and I try to delete a task that does not belong to me, **Then** I receive an unauthorized error (401 response) and the task remains in the owner's list.

### Edge Cases

- What happens when a user's JWT expires? They should be redirected to the signin page.
- How does the system handle concurrent updates to the same task by the same user? The last valid update should prevail.
- What if a network error occurs during an API call? The UI should indicate failure and allow retry.

## Requirements

### Functional Requirements

-   **FR-001**: The system MUST allow users to register with a unique email and password.
-   **FR-002**: The system MUST allow registered users to log in with their email and password.
-   **FR-003**: Upon successful login, the system MUST issue a JWT token valid for 24 hours.
-   **FR-004**: The frontend MUST store the JWT token in `localStorage`.
-   **FR-005**: The backend API MUST validate JWT tokens for all protected endpoints.
-   **FR-006**: The backend API MUST restrict access to tasks based on the `user_id` extracted from the JWT token.
-   **FR-007**: The backend MUST expose the following API endpoints with SQLModel CRUD operations:
    *   GET `/api/{user_id}/tasks` - List all tasks for a specific user.
    *   POST `/api/{user_id}/tasks` - Add a new task (body: `{title: str, description: Optional[str]}`).
    *   GET `/api/{user_id}/tasks/{id}` - Get a single task by ID for a specific user.
    *   PUT `/api/{user_id}/tasks/{id}` - Update an existing task by ID for a specific user.
    *   DELETE `/api/{user_id}/tasks/{id}` - Delete a task by ID for a specific user.
    *   PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle the completion status of a task by ID for a specific user.
-   **FR-008**: The backend MUST expose authentication endpoints: `POST /auth/signup`, `POST /auth/signin`.
-   **FR-009**: The frontend MUST implement routes for `/` (signin), `/signup`, and `/dashboard`.
-   **FR-010**: The `/dashboard` route MUST be protected and require a valid JWT token.
-   **FR-011**: The dashboard MUST display a list of the logged-in user's tasks.
-   **FR-012**: The dashboard MUST include a form for adding new tasks.
-   **FR-013**: Each displayed task MUST have controls for editing and deleting.
-   **FR-014**: The API MUST return a 401 Unauthorized status for unauthorized access attempts to protected resources.
-   **FR-015**: The API MUST return a 404 Not Found status for requests to non-existent resources (e.g., task IDs not belonging to the user).
-   **FR-016**: The API MUST return appropriate validation errors (e.g., 400 Bad Request) for invalid input (e.g., empty task title).
-   **FR-017**: All tasks and user data MUST be persistently stored in a PostgreSQL database.
-   **FR-018**: The database schema MUST be automatically migrated on application startup.

### Non-Functional Requirements

*   **NFR-001**: The application UI MUST be responsive across various device sizes (mobile, tablet, desktop).
*   **NFR-002**: The application MUST use Tailwind CSS for styling.
*   **NFR-003**: All code and documentation MUST be generated using the specified SDD tools.
*   **NFR-004**: The application MUST be deployable to Vercel.
*   **NFR-005**: The system MUST be designed to support up to 1,000 users and a total of 10,000 tasks.
*   **NFR-006**: The application UI MUST adhere to WCAG 2.1 AA accessibility standards.
*   **NFR-007**: The backend API MUST implement basic access logs and error logging for operational monitoring and debugging.

### Key Entities

-   **User**: Represents a registered user of the application.
    *   Attributes: `id` (unique identifier), `email` (unique, for login), `password_hash` (hashed password for security).
-   **Todo**: Represents a single task created by a user.
    *   Attributes: `id` (unique identifier), `user_id` (foreign key linking to User), `title` (brief description of the task), `description` (optional, more detailed description), `completed` (boolean, true if task is done), `created_at` (timestamp of creation).

## Success Criteria

### Measurable Outcomes

-   **SC-001**: Users can successfully sign up, sign in, and access their personal dashboard within 10 seconds of clicking the signin button.
-   **SC-002**: A logged-in user can perform all CRUD operations (View, Add, Update, Mark Complete, Delete) on their own tasks with less than 500ms API response time.
-   **SC-003**: Tasks created by one user are not visible or modifiable by another user, verified by API-level authorization checks.
-   **SC-004**: The application UI is fully functional and presents correctly on mobile, tablet, and desktop browsers (screen widths 320px to 1920px).
-   **SC-005**: All API endpoints adhere to the specified paths, methods, and security requirements (JWT validation, user_id isolation) as per automated API contract tests.
-   **SC-006**: The application successfully connects to and persists data in the Neon PostgreSQL database, verified by data integrity checks after operations.

## Assumptions

-   The "Better Auth" library provides JWT generation and validation functionalities suitable for integration and adhering to security best practices.
-   The `user_id` path parameter in the API endpoints is consistently handled and validated against the authenticated user's ID for all protected task operations.
-   Basic, user-friendly error messages for API failures (e.g., "Task not found", "Unauthorized") are sufficient for this phase. Detailed custom error handling for every possible technical scenario is out of scope.
-   The `created_at` timestamp for `Todo` items will be automatically generated by the database/ORM (SQLModel) upon creation.
-   Password hashing, salting, and secure storage of user credentials are handled adequately by the chosen authentication library/framework (Better Auth).

## Clarifications

### Session 2025-12-11
- Q: What are the expected maximum number of users or tasks the application should support in this initial phase? → A: Up to 1,000 users, 10,000 tasks total.
- Q: Are there any specific accessibility standards (e.g., WCAG) that the application's frontend should adhere to? → A: WCAG 2.1 AA.
- Q: What level of logging is required for the backend API to support debugging and operational monitoring? → A: Basic access logs and errors only.