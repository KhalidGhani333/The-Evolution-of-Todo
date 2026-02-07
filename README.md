# Full-Stack Todo Web Application with AI Assistant

A modern, multi-user todo application with secure authentication, RESTful API, responsive web interface, and AI-powered conversational task management. Built with Next.js frontend and FastAPI backend, featuring user isolation, persistent PostgreSQL storage, and natural language task operations via Cohere AI.

## Features

- 🔐 **User Authentication** - Secure signup/signin with JWT tokens and Better Auth
- 👥 **Multi-User Support** - Private task lists with complete data isolation
- 🤖 **AI Chat Assistant** - Natural language task management with Cohere AI (Phase III)
- 💬 **Conversation History** - Persistent chat sessions with context restoration
- ✅ **Task Management** - Create, read, update, delete tasks with rich metadata
- 🔍 **Search & Filter** - Find tasks by keyword, status, or category
- 📱 **Responsive Design** - Works seamlessly on mobile, tablet, and desktop
- 🚀 **RESTful API** - Clean FastAPI backend with automatic documentation
- 🗄️ **PostgreSQL Database** - Persistent storage with Neon Database
- 🔒 **Security First** - Password hashing, JWT validation, CORS protection, SQL injection prevention, rate limiting

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
- **AI Integration**: Cohere API (command-r-plus model)

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.13+
- **UV** package manager (for Python)
- **Neon Database** account (free tier)
- **Cohere API** account (for AI chat feature - free tier available)

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
# - COHERE_API_KEY (for AI chat feature - get from https://cohere.com)
# - CHAT_RATE_LIMIT (optional, default: 60 requests/minute)
# - CHAT_HISTORY_LIMIT (optional, default: 50 messages)

# Run database migrations
psql $DATABASE_URL -f migrations/001_create_tables.sql
psql $DATABASE_URL -f migrations/002_add_user_id.sql
psql $DATABASE_URL -f migrations/003_add_chat_tables.sql
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

#### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Authenticate user

#### Tasks (RESTful API)
- `GET /api/tasks` - List user's tasks (with optional filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

#### AI Chat (Phase III)
- `POST /api/chat` - Send message to AI assistant
- `GET /api/chat/conversations` - List user's conversations
- `POST /api/chat/conversations` - Create new conversation
- `GET /api/chat/conversations/{id}` - Get conversation with message history
- `PATCH /api/chat/conversations/{id}` - Update conversation (title, status)
- `DELETE /api/chat/conversations/{id}` - Delete conversation

All task and chat endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### AI Chat Features

The AI assistant can understand natural language commands for task management:

**Examples:**
- "Add a task to buy groceries tomorrow"
- "What are my tasks?"
- "Mark the groceries task as done"
- "Delete the old reminder"
- "Update my report task deadline to Friday"

**Tool Calling:**
The AI uses Cohere's function calling to execute task operations:
- `add_task` - Create new tasks
- `list_tasks` - Retrieve tasks with filters
- `complete_task` - Mark tasks as complete
- `delete_task` - Remove tasks
- `update_task` - Modify task properties

**Rate Limiting:**
- 60 requests per minute per user
- Automatic rate limit enforcement with 429 status code

## Project Structure

```
.
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   │   ├── chat/        # AI chat interface (Phase III)
│   │   │   ├── signin/      # Authentication pages
│   │   │   └── tasks/       # Task management pages
│   │   ├── components/      # React components
│   │   │   ├── Chat.tsx     # Main chat component
│   │   │   ├── ChatMessage.tsx  # Message display
│   │   │   └── ConversationList.tsx  # Conversation sidebar
│   │   ├── lib/             # Utilities and API client
│   │   ├── types/           # TypeScript type definitions
│   │   └── middleware.ts    # Auth middleware
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── src/
│   │   ├── models/          # SQLModel database models
│   │   │   ├── task.py      # Task model
│   │   │   ├── user.py      # User model
│   │   │   └── conversation.py  # Chat models (Phase III)
│   │   ├── api/             # API route handlers
│   │   │   ├── tasks.py     # Task endpoints
│   │   │   ├── auth.py      # Auth endpoints
│   │   │   └── chat.py      # Chat endpoints (Phase III)
│   │   ├── services/        # Business logic
│   │   │   ├── task_service.py
│   │   │   ├── chat_service.py   # Cohere integration
│   │   │   └── chat_tools.py     # AI tool functions
│   │   ├── auth.py          # Authentication logic
│   │   └── database.py      # Database connection
│   ├── migrations/          # Database migrations
│   │   ├── 001_create_tables.sql
│   │   ├── 002_add_user_id.sql
│   │   └── 003_add_chat_tables.sql  # Phase III
│   ├── tests/               # Backend tests
│   ├── main.py              # FastAPI entry point
│   └── pyproject.toml
│
├── specs/                    # Feature specifications
│   ├── 1-cli-todo-app/      # Phase I (CLI)
│   ├── 002-fullstack-web-app/  # Phase II (Web)
│   └── 003-ai-chatbot-cohere/  # Phase III (AI Chat)
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
# Database
DATABASE_URL=postgresql://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
FRONTEND_URL=http://localhost:3000

# AI Chat (Phase III)
COHERE_API_KEY=your-cohere-api-key
CHAT_RATE_LIMIT=60
CHAT_HISTORY_LIMIT=50
```

### Frontend (.env.local)
```env
# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@host/database

# API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Features

- Password hashing with bcrypt (cost factor 12)
- JWT tokens with 7-day expiration
- User data isolation via user_id filtering
- CORS protection (whitelist frontend origin)
- SQL injection prevention (ORM parameterized queries)
- XSS prevention (input sanitization)
- CSRF protection (SameSite cookies)
- Rate limiting (60 requests/minute per user for chat)
- Prompt injection detection (suspicious pattern filtering)
- Comprehensive security logging

## User Stories

### Phase I & II - Core Features
1. **User Registration & Authentication** - Sign up, sign in, secure session management
2. **Add and View Tasks** - Create tasks with title, description, category
3. **Mark Tasks Complete** - Toggle completion status with visual feedback
4. **Update and Delete Tasks** - Edit task details, remove tasks with confirmation
5. **Search and Filter** - Find tasks by keyword, status, or category
6. **Secure Task Management** - Private tasks, no cross-user access

### Phase III - AI-Powered Chat
1. **Natural Language Task Creation** - Create tasks by describing them in conversation
2. **Task List Retrieval** - Ask "What are my tasks?" in natural language
3. **Task Completion via Chat** - Mark tasks complete through conversation
4. **Task Deletion via Chat** - Delete tasks with natural language commands
5. **Task Updates via Chat** - Modify task details conversationally
6. **Conversation Persistence** - Return to previous conversations with full history

## License

Phase III - Hackathon Project (AI-Powered Todo Chatbot)

## Development Phases

- **Phase I**: CLI Todo Application (Python)
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI)
- **Phase III**: AI-Powered Conversational Interface (Cohere Integration)

## Contributing

This project follows Spec-Driven Development (SDD) workflow:
1. Specification (`/sp.spec`)
2. Planning (`/sp.plan`)
3. Task Breakdown (`/sp.tasks`)
4. Implementation (Red → Green → Refactor)

See specifications in `specs/` directory:
- `specs/1-cli-todo-app/` - Phase I specifications
- `specs/002-fullstack-web-app/` - Phase II specifications
- `specs/003-ai-chatbot-cohere/` - Phase III specifications

## Getting a Cohere API Key

1. Visit [https://cohere.com](https://cohere.com)
2. Sign up for a free account
3. Navigate to API Keys section in dashboard
4. Generate a new API key
5. Add to backend `.env` file as `COHERE_API_KEY`

Free tier includes:
- 100 API calls per minute
- Sufficient for development and testing
- Access to command-r-plus model

## Troubleshooting

### Chat not working
- Verify `COHERE_API_KEY` is set in backend `.env`
- Check backend logs for Cohere API errors
- Ensure database migrations have been run (003_add_chat_tables.sql)

### Rate limit errors
- Default is 60 requests/minute per user
- Adjust `CHAT_RATE_LIMIT` in backend `.env` if needed

### Conversation history not loading
- Verify JWT token is valid
- Check browser console for API errors
- Ensure user_id matches between requests
