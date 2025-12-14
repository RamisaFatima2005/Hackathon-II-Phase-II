# Data Model for Full-Stack Todo Application

## Entities

### User

Represents a registered user of the application.

*   **id**: Unique identifier (Primary Key).
    *   Type: UUID or Integer (auto-incrementing) - will be determined by SQLModel's default for Primary Key.
    *   Constraints: Unique, Not Null.
*   **email**: User's email address, used for login.
    *   Type: String.
    *   Constraints: Unique, Not Null, Valid Email Format.
*   **password_hash**: Hashed password for security.
    *   Type: String.
    *   Constraints: Not Null.

### Todo

Represents a single task created by a user.

*   **id**: Unique identifier for the task (Primary Key).
    *   Type: UUID or Integer (auto-incrementing).
    *   Constraints: Unique, Not Null.
*   **user_id**: Foreign key linking to the `User` entity, indicating task ownership.
    *   Type: UUID or Integer (matching `User.id` type).
    *   Constraints: Not Null, Foreign Key (references `User.id`).
*   **title**: Brief description/name of the task.
    *   Type: String.
    *   Constraints: Not Null, Min Length (e.g., 1 character), Max Length (e.g., 255 characters).
*   **description**: Optional, more detailed description of the task.
    *   Type: Optional String.
    *   Constraints: Max Length (e.g., 1000 characters).
*   **completed**: Status indicating whether the task is completed or not.
    *   Type: Boolean.
    *   Default: False.
    *   Constraints: Not Null.
*   **created_at**: Timestamp of when the task was created.
    *   Type: DateTime.
    *   Default: Current Timestamp.
    *   Constraints: Not Null.

## Relationships

*   **User to Todo**: One-to-Many.
    *   A `User` can have multiple `Todo` items.
    *   Each `Todo` item belongs to exactly one `User`.

## Validation Rules (derived from Functional Requirements and common sense)

*   **User Registration**:
    *   `email` must be unique and a valid email format.
    *   `password` must meet minimum complexity requirements (e.g., length, characters - handled by Better Auth).
*   **Task Creation/Update**:
    *   `title` cannot be empty.
    *   `title` and `description` should adhere to maximum length constraints.
    *   `user_id` for a task must correspond to an existing user.
    *   Access to `Todo` items is restricted to the `user_id` associated with the JWT token.
