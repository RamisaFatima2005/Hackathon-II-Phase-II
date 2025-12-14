---
ID: "030"
TITLE: "Fix 404 Not Found for Tasks API and Backend Rollback"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "gemini-1.5-flash-latest"
FEATURE: "fullstack-todo-app"
BRANCH: "main" # Assuming the user is on the main branch, update if known otherwise
USER: "user" # Replace with actual username if available
COMMAND: "when i sugnup on the dashboard page when i add new task it shows me error and after going on dashboard page backend shows this error WHERE "user".id = %(pk_1)s ..."
LABELS: ["bugfix", "frontend", "backend", "api"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - frontend/src/components/TaskList.tsx
  - frontend/src/components/AddTaskForm.tsx
TESTS_YAML: [] # No tests were explicitly run or added in this interaction
---

## Prompt Text

when i sugnup on the dashboard page when i add new task it shows me error and after going on dashboard page backend shows this error WHERE "user".id = %(pk_1)s
2025-12-14 10:36:49,430 INFO sqlalchemy.engine.Engine [generated in 0.00068s] {'pk_1': 1}
2025-12-14 10:36:49,430 - INFO - [generated in 0.00068s] {'pk_1': 1}
2025-12-14 10:36:49,945 - INFO - Fetching current user: ramisafatima67@gmail.com (ID: 1)
2025-12-14 10:36:49,945 INFO sqlalchemy.engine.Engine ROLLBACK
2025-12-14 10:36:49,945 - INFO - ROLLBACK
INFO:     127.0.0.1:52992 - "GET /auth/current_user HTTP/1.1" 200 OK
INFO:     127.0.0.1:52992 - "OPTIONS /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:53008 - "OPTIONS /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:53008 - "GET /tasks/ HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53008 - "GET /tasks/ HTTP/1.1" 404 Not Found, solve all the errors and make it error free

## Response Text

The user reported a `404 Not Found` error when trying to access `/tasks/` and a `ROLLBACK` in the backend logs.

Investigation revealed that the backend's tasks API endpoints are prefixed with `/api/{user_id}/`, but the frontend component `TaskList.tsx` was incorrectly calling `/tasks/` directly. `AddTaskForm.tsx` was correctly building the URL but lacked a explicit check for `userId`.

The following changes were made:

- **`frontend/src/components/TaskList.tsx`**: Modified to use the `useAuth` hook to retrieve `userId` and construct the correct API endpoint `/api/${userId}/tasks`. A check for `userId` presence was also added.
- **`frontend/src/components/AddTaskForm.tsx`**: An explicit check for `userId` presence was added before making the API call to prevent issues if `userId` is `null`.

These changes are expected to resolve the `404 Not Found` error by ensuring the frontend calls the correct API endpoint. The `ROLLBACK` error is likely a secondary effect of the incorrect API call and should also be resolved.
