---
ID: "033"
TITLE: "Fix Backend SQLAlchemy ProgrammingError: can't adapt type 'User'"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "gemini-1.5-flash-latest"
FEATURE: "fullstack-todo-app"
BRANCH: "main" # Assuming the user is on the main branch, update if known otherwise
USER: "user" # Replace with actual username if available
COMMAND: "now i am facing this error on frontend "Request failed with status code 500" and this on backend "  File "C:\Users\karakurom traders\Desktop\Phase-II\backend\venv312\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute ... ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'User' ..."
LABELS: ["bugfix", "backend", "sqlalchemy", "psycopg2"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - backend/src/dependencies.py
TESTS_YAML: [] # No tests were explicitly run or added in this interaction
---

## Prompt Text

now i am facing this error on frontend "Request failed with status code 500" and this on backend "  File "C:\Users\karakurom traders\Desktop\Phase-II\backend\venv312\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'User'
[SQL: INSERT INTO todo (user_id, title, description, completed, created_at) VALUES (%(user_id)s, %(title)s, %(description)s, %(completed)s, %(created_at)s) RETURNING todo.id]
[parameters: {'user_id': <User at 0x27dbf6dd810>, 'title': 'jhsdaidhkjdnm', 'description': 'jdghsuajzx', 'completed': False, 'created_at': datetime.datetime(2025, 12, 14, 5, 58, 22, 930777, tzinfo=datetime.timezone.utc)}]
(Background on this error at: https://sqlalche.me/e/20/f405)

INFO:     127.0.0.1:62892 - "POST /api/1/tasks HTTP/1.1" 500 Internal Server Error" while adding new task

## Response Text

The user reported a `500 Internal Server Error` on the frontend and a `sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'User'` on the backend when adding a new task.

The backend traceback clearly indicated that a `User` object was being passed for the `user_id` column during the `INSERT` operation into the `todo` table, whereas an integer was expected. This issue stemmed from the `get_current_user` dependency.

The following change was made:

- **`backend/src/dependencies.py`**: The `get_current_user` function was modified to return `user.id` (an integer) instead of the full `User` object. This ensures that the correct data type is passed to the database for the `user_id` column.

This fix directly addresses the `ProgrammingError` and consequently resolves the `500 Internal Server Error` on the frontend.
