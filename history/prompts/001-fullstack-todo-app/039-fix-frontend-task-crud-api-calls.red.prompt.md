---
ID: "039"
TITLE: "Fix Frontend Task CRUD API Calls"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "gemini-1.5-flash-latest"
FEATURE: "fullstack-todo-app"
BRANCH: "main" # Assuming the user is on the main branch, update if known otherwise
USER: "user" # Replace with actual username if available
COMMAND: "when i edit, mark as complete or click on delete button to delete, edit and mark as complete button it shows error"
LABELS: ["bugfix", "frontend", "api-calls"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - frontend/src/components/TaskItem.tsx
  - frontend/src/app/task/[id]/edit/page.tsx
TESTS_YAML: [] # No tests were explicitly run or added in this interaction
---

## Prompt Text

when i edit, mark as complete or click on delete button to delete, edit and mark as complete button it shows error faild to fetch task or failed to delete task solve it and make it run

## Response Text

The user reported frontend errors like "failed to fetch task" or "failed to delete task" when interacting with task management buttons (edit, mark as complete, delete). This indicated incorrect API call URLs from the frontend to the backend.

The issue was similar to a previous `404 Not Found` error, where API calls were missing the `/api/{user_id}/` prefix.

The following changes were made:

-   **`frontend/src/components/TaskItem.tsx`**:
    -   Imported `useAuth` hook and retrieved `userId`.
    -   Updated `handleDelete` to use `/api/${userId}/tasks/${task.id}`.
    -   Updated `handleToggleComplete` to use `/api/${userId}/tasks/${task.id}/complete`.
    -   Added `userId` presence checks before making API calls.
-   **`frontend/src/app/task/[id]/edit/page.tsx`**:
    -   Imported `useAuth` hook and retrieved `userId`.
    -   Updated `fetchTask` to use `/api/${userId}/tasks/${id}` for `apiClient.get`.
    -   Updated `handleSubmit` to use `/api/${userId}/tasks/${id}` for `apiClient.put`.
    -   Added `userId` presence checks before making API calls.

These changes ensure that all task-related API calls from the frontend include the necessary `user_id` in their URLs, resolving the "failed to fetch task", "failed to delete task", and similar errors.
