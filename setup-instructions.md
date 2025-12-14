# Setup Instructions for Full-Stack Todo Application

This document outlines the steps to set up the necessary environment and configuration for the Full-Stack Todo Application.

## 1. Create a Neon Account and Database

The backend uses Neon for serverless PostgreSQL.

1.  **Sign up for Neon**: Go to [Neon.tech](https://neon.tech/) and sign up for a free account.
2.  **Create a new project**: Follow the on-screen instructions to create a new project.
3.  **Get your connection string**: Once your project is created, navigate to its dashboard. You should find a connection string (usually starting with `postgresql://`). It will look something like:
    `postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]?sslmode=require`
    *Keep this connection string handy, as you'll need it for your `.env` file.*

## 2. Backend Environment Setup

1.  **Navigate to the `backend` directory**:
    ```bash
    cd backend
    ```
2.  **Create your `.env` file**:
    Copy the provided `.env.example` file and rename it to `.env`.
    ```bash
    cp .env.example .env
    ```
    *(On Windows, you might use `copy .env.example .env`)*
3.  **Configure your `.env` file**:
    Open the newly created `.env` file and update the following variables:
    *   `DATABASE_URL`: Paste the connection string you obtained from Neon.
    *   `SECRET_KEY`: Generate a strong, random string for your JWT secret key (e.g., using an online generator or Python's `secrets` module).
    *   `ALGORITHM`: Keep as `HS256` unless you have a specific reason to change it.
    *   `ACCESS_TOKEN_EXPIRE_MINUTES`: Keep as `1440` (24 hours) or adjust as needed.

    Your `.env` file should look something like this:
    ```
    DATABASE_URL="postgresql://[YOUR_NEON_USER]:[YOUR_NEON_PASSWORD]@[YOUR_NEON_HOST]:[YOUR_NEON_PORT]/[YOUR_NEON_DB_NAME]?sslmode=require"
    SECRET_KEY="your_actual_strong_random_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=1440
    ```
    *Make sure the `SECRET_KEY` is not the placeholder string!*

4.  **Install Python dependencies**:
    Ensure you have Python 3.10+ installed. It's highly recommended to use a virtual environment.
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

## 3. Frontend Environment Setup (Once `frontend/` directory is created)

*(This section will be expanded once the frontend project is initialized as part of task T005.)*

1.  **Navigate to the `frontend` directory**:
    ```bash
    cd frontend
    ```
2.  **Create your `.env.local` file**:
    Copy the provided `.env.local.example` file and rename it to `.env.local`.
    ```bash
    cp .env.local.example .env.local
    ```
    *(On Windows, you might use `copy .env.local.example .env.local`)*
3.  **Configure your `.env.local` file**:
    Open the newly created `.env.local` file and update the `NEXT_PUBLIC_BACKEND_URL` to point to your running backend.
    ```
    NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
    ```
    *(Adjust the port if your backend runs on a different port)*

4.  **Install Node.js dependencies**:
    Ensure you have Node.js 18+ and npm/yarn installed.
    ```bash
    npm install
    # or yarn install
    ```
