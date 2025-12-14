# Quickstart Guide: Full-Stack Todo Application

This guide provides instructions to set up and run the Full-Stack Todo Application locally.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Python 3.10+**: For the FastAPI backend.
*   **Node.js 18+ & npm/yarn**: For the Next.js frontend.
*   **Docker** (Recommended): For easily running a local PostgreSQL database.
*   **PostgreSQL Client**: `psql` or a GUI client like DBeaver/PgAdmin for database interaction.

## 2. Setup Database (PostgreSQL)

The application requires a PostgreSQL database. You can use Neon Serverless PostgreSQL for deployment, but for local development, Docker is recommended.

### Using Docker (Recommended for local development)

1.  **Start PostgreSQL container**:
    ```bash
    docker run --name todo-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=todo_db -p 5432:5432 -d postgres:15
    ```
2.  **Verify connection**: You should be able to connect to `postgresql://user:password@localhost:5432/todo_db`.

### Using an existing PostgreSQL instance

Ensure you have a PostgreSQL database running and note down its connection details (host, port, user, password, database name).

## 3. Backend Setup (FastAPI)

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
2.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows
    # source venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt # (You will need to generate this first if not present)
    ```
3.  **Configure environment variables**:
    Create a `.env` file in the `backend/` directory with your database connection string and JWT secret.
    ```
    DATABASE_URL="postgresql://user:password@localhost:5432/todo_db"
    SECRET_KEY="your_super_secret_jwt_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 24 hours
    ```
    *Replace `your_super_secret_jwt_key` with a strong, random key.*

4.  **Run migrations (if applicable)**:
    *(Instructions for running SQLModel migrations will go here once defined, e.g., using Alembic)*

5.  **Start the backend server**:
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will be available at `http://localhost:8000`.

## 4. Frontend Setup (Next.js)

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
3.  **Configure environment variables**:
    Create a `.env.local` file in the `frontend/` directory with the backend API URL.
    ```
    NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
    ```
4.  **Start the frontend development server**:
    ```bash
    npm run dev
    # or yarn dev
    ```
    The frontend application will be available at `http://localhost:3000`.

## 5. Access the Application

Open your web browser and navigate to `http://localhost:3000` to access the Full-Stack Todo Application. You can then sign up, sign in, and manage your tasks.
