# Quickstart Guide
## Feature: Full-Stack Todo Web Application

**Branch**: `002-fullstack-web-app`
**Date**: 2026-02-03

---

## Prerequisites

- **Node.js**: 18+ (for Next.js frontend)
- **Python**: 3.13+ (for FastAPI backend)
- **UV**: Python package manager
- **Git**: Version control
- **Neon Account**: Free tier PostgreSQL database
- **Code Editor**: VS Code recommended

---

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
git checkout 002-fullstack-web-app
```

### 2. Database Setup (Neon)

1. Create account at https://neon.tech
2. Create new project: "todo-app"
3. Copy connection string (format: `postgresql://user:pass@host/dbname`)
4. Save for environment configuration

### 3. Generate Shared Secret

```bash
# Generate a secure random secret for JWT signing
openssl rand -base64 32
```

Save this secret - it will be used in both frontend and backend.

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Environment File

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host/dbname

# Authentication (MUST match frontend)
BETTER_AUTH_SECRET=<your-generated-secret>

# CORS (add production URL after deployment)
CORS_ORIGINS=http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

### 3. Install Dependencies

```bash
# Using UV package manager
uv pip install -r requirements.txt

# Or create requirements.txt with:
# fastapi==0.110.0
# sqlmodel==0.0.14
# pydantic==2.6.0
# python-jose[cryptography]==3.3.0
# passlib[bcrypt]==1.7.4
# psycopg2-binary==2.9.9
# uvicorn[standard]==0.27.0
# python-dotenv==1.0.0
```

### 4. Initialize Database

```bash
# Run migrations (creates tables and indexes)
python -m alembic upgrade head

# Or if using SQLModel directly:
python -m src.database init
```

### 5. Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify**: Visit http://localhost:8000/docs for API documentation

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Create Environment File

Create `frontend/.env.local`:

```env
# Authentication (MUST match backend)
BETTER_AUTH_SECRET=<your-generated-secret>
BETTER_AUTH_URL=http://localhost:3000

# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (Better Auth needs direct access)
DATABASE_URL=postgresql://user:pass@host/dbname
```

### 3. Install Dependencies

```bash
npm install
# or
pnpm install
```

**Key Dependencies**:
- next@15+
- react@18+
- typescript@5+
- tailwindcss@3+
- better-auth
- swr
- react-hook-form
- zod

### 4. Start Development Server

```bash
npm run dev
# or
pnpm dev
```

**Verify**: Visit http://localhost:3000

---

## Verification Checklist

### Backend Health Check

```bash
# Test backend is running
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "database": "connected"}
```

### Frontend Health Check

1. Open http://localhost:3000
2. Should see signup/signin page
3. No console errors

### Database Connection

```bash
# From backend directory
python -c "from src.database import engine; print('Connected!' if engine else 'Failed')"
```

### JWT Secret Verification

```bash
# Verify secrets match
grep BETTER_AUTH_SECRET backend/.env
grep BETTER_AUTH_SECRET frontend/.env.local

# Both should show the same value
```

---

## First-Time User Flow

### 1. Create Account

1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Enter email and password (min 8 characters)
4. Submit form
5. Should redirect to tasks page with empty state

### 2. Add First Task

1. Click "Add Task" button
2. Enter title: "Test Task"
3. Enter description: "Verify application works"
4. Enter category: "Testing"
5. Submit form
6. Task should appear in list immediately

### 3. Test Task Operations

- **Mark Complete**: Click checkbox next to task
- **Edit Task**: Click "Edit" button, modify fields, save
- **Delete Task**: Click "Delete" button, confirm deletion
- **Search**: Type keyword in search box
- **Filter**: Select status or category from dropdowns

### 4. Test User Isolation

1. Sign out
2. Create second account with different email
3. Add tasks to second account
4. Sign out and sign back in to first account
5. Verify first account only sees its own tasks

---

## Common Issues & Solutions

### Issue: "Database connection failed"

**Solution**:
- Verify DATABASE_URL is correct in both .env files
- Check Neon dashboard - database should be active
- Ensure IP is whitelisted in Neon (or use "Allow all" for development)

### Issue: "JWT verification failed"

**Solution**:
- Verify BETTER_AUTH_SECRET matches in both .env files
- Restart both frontend and backend servers
- Clear browser cookies and try again

### Issue: "CORS error in browser console"

**Solution**:
- Verify CORS_ORIGINS in backend/.env includes http://localhost:3000
- Restart backend server
- Check browser network tab for actual origin being sent

### Issue: "Port already in use"

**Solution**:
```bash
# Find process using port 8000 (backend)
lsof -i :8000
kill -9 <PID>

# Find process using port 3000 (frontend)
lsof -i :3000
kill -9 <PID>
```

### Issue: "Module not found" errors

**Solution**:
```bash
# Backend
cd backend
uv pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Development Workflow

### Making Changes

1. **Spec-Driven Development**: All changes start with spec updates
2. **Feature Branches**: Create branch from `002-fullstack-web-app`
3. **Implementation**: Use Claude Code for all code changes
4. **Testing**: Verify changes work locally
5. **Commit**: Use descriptive commit messages

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### Database Migrations

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy automatically on push to main

**Environment Variables**:
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL` (production URL)
- `NEXT_PUBLIC_API_URL` (backend production URL)
- `DATABASE_URL`

### Backend (Railway or Render)

1. Push code to GitHub
2. Connect repository to Railway/Render
3. Configure environment variables
4. Deploy automatically on push to main

**Environment Variables**:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `CORS_ORIGINS` (production frontend URL)
- `HOST=0.0.0.0`
- `PORT=8000`

### Database (Neon)

- Already hosted, no deployment needed
- Update connection string if changing projects
- Monitor usage in Neon dashboard

---

## Monitoring & Debugging

### Backend Logs

```bash
# Development
uvicorn src.main:app --reload --log-level debug

# Production (Railway/Render)
# View logs in platform dashboard
```

### Frontend Logs

```bash
# Development
# Check browser console and terminal

# Production (Vercel)
# View logs in Vercel dashboard
```

### Database Queries

```bash
# Connect to Neon database
psql $DATABASE_URL

# View all users
SELECT id, email, created_at FROM users;

# View all tasks
SELECT id, user_id, title, completed FROM tasks;

# Check indexes
\di
```

---

## Performance Optimization

### Backend

- Database connection pooling (handled by Neon)
- Query optimization with indexes
- Response compression (gzip)
- Async/await for all I/O

### Frontend

- Code splitting (automatic with Next.js)
- Image optimization (next/image)
- Font optimization (next/font)
- SWR caching

---

## Security Checklist

- [ ] BETTER_AUTH_SECRET is strong (32+ characters)
- [ ] .env files are in .gitignore
- [ ] HTTPS enabled in production
- [ ] CORS configured for production origin only
- [ ] Database connection uses SSL in production
- [ ] JWT tokens expire after 7 days
- [ ] Passwords hashed with bcrypt
- [ ] Input validation on frontend and backend
- [ ] User isolation tested and verified

---

## Next Steps

1. **Complete MVP**: Implement all P1 user stories
2. **Testing**: Write integration tests for critical flows
3. **Documentation**: Update README with deployment instructions
4. **Deployment**: Deploy to production environments
5. **Phase III**: Plan AI chatbot integration

---

## Support & Resources

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Implementation Plan**: `specs/002-fullstack-web-app/plan.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contracts**: `specs/002-fullstack-web-app/contracts/`
- **Constitution**: `.specify/memory/constitution.md`

---

**Last Updated**: 2026-02-03
