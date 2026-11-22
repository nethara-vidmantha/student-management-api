# Student Management API

A RESTful Student Management API built with **FastAPI**, **Python**, and **PostgreSQL**. This project demonstrates CRUD operations, authentication, authorization, database relationships, migrations, and automated testing.

## Features

- Student CRUD operations (Create, Read, Update, Delete)
- User registration and login
- Secure password hashing
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Student filtering, sorting, and pagination
- SQLAlchemy database integration
- PostgreSQL database
- Alembic database migrations
- Pydantic data validation
- Custom exception handling
- CORS configuration
- Request processing-time middleware
- Automated testing with Pytest
- Test coverage reporting

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- Passlib / bcrypt
- Pytest
- HTTPX

## Project Structure

```text
student-management-api/
│
├── migrations/
│   └── versions/
│
├── routes/
│   ├── students.py
│   ├── users.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   └── test_main.py
│
├── .gitignore
├── alembic.ini
├── database.py
├── db_models.py
├── dependencies.py
├── main.py
├── models.py
└── security.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nethara-vidmantha/student-management-api.git
cd student-management-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install "fastapi[standard]" sqlalchemy "psycopg[binary]" alembic python-dotenv "passlib[bcrypt]" "bcrypt==4.0.1" "PyJWT[crypto]" python-multipart pytest httpx pytest-cov email-validator
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_management

TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_management_test

JWT_SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholders with your own credentials and secrets.

**Never upload your `.env` file to GitHub.**

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

API URL: http://127.0.0.1:8000

Interactive API documentation: http://127.0.0.1:8000/docs

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

- Register an account using `/register`.
- Log in using `/login`.
- Use the returned access token to access protected endpoints.
- Admin-only operations are protected using Role-Based Access Control.

## Testing

Run all automated tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov
```

Generate an HTML coverage report:

```bash
python -m pytest --cov --cov-report=html
```

**Test Results:**
- 49 automated tests passed.
- 100% coverage across application modules.
- 99% overall project coverage.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/app-info` | Application information |
| POST | `/register` | Register a user |
| POST | `/login` | User login |
| GET | `/students` | Retrieve students |
| POST | `/students` | Create a student (Admin) |
| GET | `/students/{student_id}` | Retrieve a student |
| PATCH | `/students/{student_id}` | Partially update a student (Admin) |
| PUT | `/students/{student_id}` | Update a student (Admin) |
| DELETE | `/students/{student_id}` | Delete a student (Admin) |
| GET | `/students-with-owners` | Retrieve students with their owners |

Additional endpoints support filtering, sorting, limiting, offsetting, and pagination.

## Author

**Nethara Vidmantha**<br>
Undergraduate – BICT (Hons) in Software Technology<br>
University of Sri Jayewardenepura

