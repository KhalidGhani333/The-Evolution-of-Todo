# Full-Stack Todo Web Application

A modern, multi-user todo application with secure authentication, RESTful API, and responsive web interface. Built with Next.js frontend and FastAPI backend, featuring user isolation and persistent PostgreSQL storage.

## Features

- 🔐 **User Authentication** - Secure signup/signin with JWT tokens and Better Auth
- 👥 **Multi-User Support** - Private task lists with complete data isolation
- ✅ **Task Management** - Create, read, update, delete tasks with rich metadata
- 🔍 **Search & Filter** - Find tasks by keyword, status, or category
- 📱 **Responsive Design** - Works seamlessly on mobile, tablet, and desktop
- 🚀 **RESTful API** - Clean FastAPI backend with automatic documentation
- 🗄️ **PostgreSQL Database** - Persistent storage with Neon Database
- 🔒 **Security First** - Password hashing, JWT validation, CORS protection, SQL injection prevention

## Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Authentication**: Better Auth
- **Data Fetching**: SWR
- **Forms**: React Hook Form + Zod validation

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.13+
- **UV** package manager (for Python)
- **Neon Database** account (free tier)

## Installation

### 1. Install UV Package Manager

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env and add your configuration:
# - DATABASE_URL (Neon PostgreSQL connection string)
# - BETTER_AUTH_SECRET (shared secret with frontend)
# - FRONTEND_URL (for CORS)
```

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local and add:
# - BETTER_AUTH_SECRET (same as backend)
# - BETTER_AUTH_URL (backend API URL)
# - DATABASE_URL (Neon PostgreSQL connection string)
```

## Running the Application

### Start Backend Server

```bash
cd backend

# Activate virtual environment (if not already activated)
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Run FastAPI server
python main.py
```

Backend will run on `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend

# Run Next.js development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Authenticate user
- `GET /api/tasks` - List user's tasks (with optional filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

## Project Structure

```
.
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and API client
│   │   ├── types/           # TypeScript type definitions
│   │   └── middleware.ts    # Auth middleware
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── src/
│   │   ├── models/          # SQLModel database models
│   │   ├── routes/          # API route handlers
│   │   ├── auth/            # Authentication logic
│   │   └── database.py      # Database connection
│   ├── tests/               # Backend tests
│   ├── main.py              # FastAPI entry point
│   └── pyproject.toml
│
├── specs/                    # Feature specifications
│   ├── 1-cli-todo-app/      # Phase I (CLI)
│   └── 002-fullstack-web-app/ # Phase II (Web)
│
├── history/                  # Development history
│   ├── prompts/             # Prompt History Records
│   └── adr/                 # Architecture Decision Records
│
└── README.md                # This file
```

## Development

### Run Backend Tests

```bash
cd backend
pytest
pytest --cov=src --cov-report=html  # With coverage
```

### Run Frontend Linting

```bash
cd frontend
npm run lint
```

### Build for Production

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```env
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@host/database
```

## Security Features

- Password hashing with bcrypt (cost factor 12)
- JWT tokens with 7-day expiration
- User data isolation via user_id filtering
- CORS protection (whitelist frontend origin)
- SQL injection prevention (ORM parameterized queries)
- XSS prevention (input sanitization)
- CSRF protection (SameSite cookies)

## User Stories

1. **User Registration & Authentication** - Sign up, sign in, secure session management
2. **Add and View Tasks** - Create tasks with title, description, category
3. **Mark Tasks Complete** - Toggle completion status with visual feedback
4. **Update and Delete Tasks** - Edit task details, remove tasks with confirmation
5. **Search and Filter** - Find tasks by keyword, status, or category
6. **Secure Task Management** - Private tasks, no cross-user access

## License

Phase II - Hackathon Project

## Contributing

This project follows Spec-Driven Development (SDD) workflow:
1. Specification (`/sp.spec`)
2. Planning (`/sp.plan`)
3. Task Breakdown (`/sp.tasks`)
4. Implementation (Red → Green → Refactor)

See `specs/002-fullstack-web-app/` for detailed specifications.
