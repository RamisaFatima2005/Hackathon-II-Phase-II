---
ID: "034"
TITLE: "Fix Backend AttributeError in /auth/current_user endpoint"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "gemini-1.5-flash-latest"
FEATURE: "fullstack-todo-app"
BRANCH: "main" # Assuming the user is on the main branch, update if known otherwise
USER: "user" # Replace with actual username if available
COMMAND: "now i am facing network error while doing signup and signin solve all the errors"
LABELS: ["bugfix", "backend", "authentication", "attribute-error"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - backend/src/dependencies.py
  - backend/src/api/auth.py
TESTS_YAML: [] # No tests were explicitly run or added in this interaction
---

## Prompt Text

now i am facing network error while doing signup and signin solve all the errors
(followed by backend log showing AttributeError: 'int' object has no attribute 'email')

## Response Text

The user reported a "Network Error" during signup and signin, accompanied by a backend `AttributeError: 'int' object has no attribute 'email'`. This error occurred in `backend/src/api/auth.py` at line 169, within the `get_current_user` *endpoint*.

The root cause was a conflict with a previous fix: the `get_current_user` *dependency* in `backend/src/dependencies.py` was modified to return an `int` (user ID) to resolve a `ProgrammingError`. However, the `get_current_user` *endpoint* was still expecting a full `User` object, leading to the `AttributeError`. Additionally, the endpoint was recursively calling itself due to a name collision.

The following changes were made:

- **`backend/src/dependencies.py`**:
    - Renamed the existing `get_current_user` dependency to `get_authenticated_user_id`. This dependency now exclusively returns the integer ID of the authenticated user.
    - Added a new dependency `get_current_active_user`, which takes the `user_id` from `get_authenticated_user_id` and fetches the complete `User` object from the database, returning it.
- **`backend/src/api/auth.py`**:
    - Updated import statements to reflect the new dependency names.
    - Renamed the `get_current_user` *endpoint* to `get_current_user_endpoint` to avoid name collision.
    - Modified the `get_current_user_endpoint` to use `Depends(get_current_active_user)`, ensuring it receives a `User` object, thus resolving the `AttributeError`.

These changes correctly separate the responsibility of providing a user ID versus a full user object, resolving the `AttributeError` and the cascading frontend "Network Error".
