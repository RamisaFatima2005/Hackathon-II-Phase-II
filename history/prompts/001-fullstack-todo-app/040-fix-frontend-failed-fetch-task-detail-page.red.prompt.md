---
ID: "040"
TITLE: "Fix Frontend 'failed to fetch task' on Task Detail Page"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "gemini-1.5-flash-latest"
FEATURE: "fullstack-todo-app"
BRANCH: "main" # Assuming the user is on the main branch, update if known otherwise
USER: "user" # Replace with actual username if available
COMMAND: "in edit task so on this path "http://localhost:3000/task/1/edit" it shows failed to fetch task. Solve it aslo and make error free"
LABELS: ["bugfix", "frontend", "api-calls"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - frontend/src/app/task/[id]/page.tsx
TESTS_YAML: [] # No tests were explicitly run or added in this interaction
---

## Prompt Text

in edit task so on this path "http://localhost:3000/task/3" it shows failed to fetch task. Solve it aslo and make error free

## Response Text

The user reported that after editing a task and being redirected to the task detail page (`http://localhost:3000/task/[id]`), a "failed to fetch task" error was displayed. This indicated an issue with how the task details were being fetched on that specific page.

The root cause was that the API call on the task detail page (`frontend/src/app/task/[id]/page.tsx`) was not including the `user_id` in the URL prefix, similar to previous frontend issues.

The following changes were made:

-   **`frontend/src/app/task/[id]/page.tsx`**:
    -   Imported `useAuth` hook and retrieved `userId`.
    -   Updated the `apiClient.get` call within `fetchTask` to use `/api/${userId}/tasks/${id}`.
    -   Added a check for `userId` presence before making the API call.
    -   Added `console.error(err)` inside the `catch` block for debugging purposes.

These changes ensure that the task detail page correctly fetches task information using the authenticated user's ID, resolving the "failed to fetch task" error upon redirection after editing.
