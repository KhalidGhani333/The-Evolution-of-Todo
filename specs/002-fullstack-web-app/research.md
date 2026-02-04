# Research & Technical Decisions
## Feature: Full-Stack Todo Web Application

**Branch**: `002-fullstack-web-app`
**Date**: 2026-02-03
**Phase**: 0 - Research & Outline

---

## Research Questions Resolved

### 1. Authentication Architecture

**Decision**: Better Auth with JWT tokens (7-day expiration)

**Rationale**:
- Better Auth provides production-ready authentication with minimal configuration
- JWT tokens enable stateless authentication suitable for API architecture
- Shared secret between frontend and backend ensures token verification
- 7-day expiration balances security with user convenience

**Alternatives Considered**:
- NextAuth.js: Rejected because Better Auth has better FastAPI integration patterns
- Custom JWT implementation: Rejected due to security risks and maintenance overhead
- Session-based auth: Rejected because it requires server-side session storage and doesn't scale well with API architecture

**Implementation Pattern**:
1. Better Auth runs in Next.js frontend, issues JWT tokens
2. Frontend stores token securely (httpOnly cookies or secure storage)
3. Frontend includes token in Authorization header for API requests
4. FastAPI backend verifies JWT signature using shared BETTER_AUTH_SECRET
5. Backend extracts user_id from verified token
6. Backend filters all queries by authenticated user_id

---

### 2. Database Choice & Schema Design

**Decision**: Neon Serverless PostgreSQL with SQLModel ORM

**Rationale**:
- Neon provides serverless PostgreSQL with generous free tier (0.5 GB storage)
- SQLModel combines Pydantic validation with SQLAlchemy ORM
- Type-safe models prevent runtime errors
- Automatic migration support via Alembic
- Connection pooling handled by Neon

**Schema Design**:

**Users Table** (managed by Better Auth):
- `id` (text, primary key) - Better Auth generates UUIDs
- `email` (text, unique, not null) - User's email address
- `name` (text, nullable) - Optional display name
- `email_verified` (boolean, default false)
- `created_at`, `updated_at` (timestamp with timezone)

**Tasks Table**:
- `id` (integer, primary key, auto-increment)
- `user_id` (text, foreign key → users.id, not null, indexed)
- `title` (varchar 200, not null)
- `description` (text, nullable)
- `category` (varchar 50, nullable, indexed)
- `completed` (boolean, default false, indexed)
- `created_at`, `updated_at` (timestamp with timezone)

**Indexes**:
- `idx_tasks_user_id` on tasks(user_id) - Critical for user isolation queries
- `idx_tasks_completed` on tasks(completed) - For filtering by status
- `idx_tasks_category` on tasks(category) - For category filtering
- Composite index on (user_id, completed) for common query pattern

**Constraints**:
- Foreign key: tasks.user_id → users.id with ON DELETE CASCADE
- Check constraint: title length between 1 and 200 characters
- Check constraint: description length <= 1000 characters
- Check constraint: category length <= 50 characters

**Alternatives Considered**:
- SQLite: Rejected for production (Phase II requires multi-user with concurrent access)
- MongoDB: Rejected because relational data model is simpler for this use case
- Supabase: Rejected because Neon has better FastAPI integration examples

---

### 3. Monorepo Structure

**Decision**: Separate frontend/ and backend/ directories in single repository

**Rationale**:
- Clear separation of concerns between Next.js and FastAPI
- Independent deployment pipelines (Vercel for frontend, Railway/Render for backend)
- Shared types can be defined in both codebases (TypeScript interfaces match Pydantic models)
- Single repository simplifies version control and feature branches

**Directory Structure**:
```
/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and API client
│   │   └── types/           # TypeScript types
│   ├── public/              # Static assets
│   ├── .env.local           # Frontend environment variables
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── src/
│   │   ├── models/          # SQLModel entities
│   │   ├── api/             # Route handlers
│   │   ├── services/        # Business logic
│   │   ├── auth/            # JWT verification
│   │   └── database.py      # Database connection
│   ├── tests/               # Backend tests
│   ├── .env                 # Backend environment variables
│   └── pyproject.toml       # Python dependencies
│
├── specs/                    # Feature specifications
├── history/                  # PHRs and ADRs
└── README.md
```

**Alternatives Considered**:
- Turborepo/Nx monorepo: Rejected as overkill for 2-project structure
- Separate repositories: Rejected because it complicates feature branch workflow
- Single codebase (Next.js API routes): Rejected because FastAPI provides better Python ecosystem integration

---

### 4. API Design Pattern

**Decision**: RESTful API with user_id in URL path

**Rationale**:
- REST is well-understood and has excellent tooling support
- user_id in URL makes authorization explicit and auditable
- Standard HTTP methods (GET, POST, PUT, DELETE, PATCH) map to CRUD operations
- JSON request/response bodies are universal

**Endpoint Pattern**:
```
/api/{user_id}/tasks          # List/Create tasks
/api/{user_id}/tasks/{id}     # Get/Update/Delete specific task
/api/{user_id}/tasks/{id}/complete  # Toggle completion
```

**Authorization Flow**:
1. Extract user_id from URL path parameter
2. Verify JWT token from Authorization header
3. Extract authenticated_user_id from JWT payload
4. Compare: if user_id != authenticated_user_id, return 403 Forbidden
5. Proceed with operation, filtering by user_id

**Alternatives Considered**:
- GraphQL: Rejected due to added complexity for simple CRUD operations
- user_id in query parameter: Rejected because it's less RESTful and harder to audit
- No user_id in URL (infer from token): Rejected because explicit is better than implicit

---

### 5. Frontend State Management

**Decision**: SWR (stale-while-revalidate) for data fetching

**Rationale**:
- SWR provides automatic caching, revalidation, and optimistic updates
- Built-in support for loading and error states
- Minimal boilerplate compared to Redux or Zustand
- Perfect for CRUD operations with server as source of truth

**Data Flow**:
1. Component calls useSWR hook with API endpoint
2. SWR returns cached data immediately (if available)
3. SWR revalidates in background
4. Component re-renders with fresh data
5. Mutations use mutate() for optimistic updates

**Alternatives Considered**:
- TanStack Query (React Query): Also excellent, but SWR is lighter weight
- Redux Toolkit: Rejected as overkill for simple CRUD operations
- Context API: Rejected because it doesn't handle caching or revalidation

---

### 6. Form Validation Strategy

**Decision**: React Hook Form + Zod schemas

**Rationale**:
- React Hook Form minimizes re-renders (uncontrolled inputs)
- Zod provides type-safe schema validation
- Schemas can be shared between frontend and backend validation
- Excellent error handling and user feedback

**Validation Rules** (from spec FR-006):
- Title: required, 1-200 characters, non-empty after trim
- Description: optional, max 1000 characters
- Category: optional, max 50 characters

**Alternatives Considered**:
- Formik: Rejected due to performance issues with large forms
- Yup: Rejected because Zod has better TypeScript integration
- Manual validation: Rejected due to maintenance burden

---

### 7. Security Implementation

**Decision**: Defense-in-depth with multiple layers

**Security Layers**:

1. **Authentication** (FR-002, FR-003):
   - Passwords hashed with bcrypt (cost factor 12)
   - JWT tokens signed with HS256 algorithm
   - Tokens expire after 7 days
   - Refresh token rotation (optional for MVP)

2. **Authorization** (FR-013):
   - Every API request validates JWT token
   - user_id in URL must match authenticated user_id from token
   - Return 403 Forbidden for unauthorized access attempts

3. **Input Validation** (FR-007, FR-026, FR-027):
   - Frontend: Zod schemas validate before submission
   - Backend: Pydantic models validate all inputs
   - SQL injection prevented by SQLModel parameterized queries
   - XSS prevented by React's automatic escaping + input sanitization

4. **CORS Configuration** (FR-025):
   - Backend allows only frontend origin
   - Credentials included in CORS policy
   - Preflight requests handled correctly

5. **HTTPS** (FR-029):
   - Production deployment requires HTTPS
   - Vercel and Railway/Render provide automatic HTTPS

6. **Environment Security** (FR-030):
   - .env files in .gitignore
   - .env.example with placeholders for documentation
   - Secrets never committed to version control

**Alternatives Considered**:
- OAuth2 with social providers: Deferred to future phase (out of scope per spec)
- 2FA: Deferred to future phase (out of scope per spec)
- Rate limiting: Should be added but not in MVP requirements

---

### 8. Deployment Strategy

**Decision**: Vercel (frontend) + Railway or Render (backend) + Neon (database)

**Rationale**:
- All platforms offer generous free tiers
- Automatic HTTPS and CDN (Vercel)
- Easy environment variable management
- Git-based deployment workflows
- Zero-downtime deployments

**Deployment Flow**:
1. Push to feature branch triggers preview deployments
2. Merge to main triggers production deployment
3. Frontend deployed to Vercel (automatic)
4. Backend deployed to Railway/Render (automatic)
5. Database migrations run automatically on backend startup

**Environment Variables**:

Frontend (.env.local):
```
BETTER_AUTH_SECRET=<shared-secret>
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=<neon-connection-string>
```

Backend (.env):
```
DATABASE_URL=<neon-connection-string>
BETTER_AUTH_SECRET=<shared-secret>
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
HOST=0.0.0.0
PORT=8000
```

**Alternatives Considered**:
- Netlify: Rejected because Vercel has better Next.js integration
- Heroku: Rejected due to removal of free tier
- Self-hosted VPS: Rejected due to maintenance overhead

---

## Technology Stack Summary

### Frontend
- **Framework**: Next.js 15+ with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **Authentication**: Better Auth
- **Data Fetching**: SWR
- **Form Handling**: React Hook Form + Zod
- **HTTP Client**: Fetch API (native)

### Backend
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.13+
- **ORM**: SQLModel 0.0.14+
- **Validation**: Pydantic 2+
- **Authentication**: python-jose (JWT), passlib (bcrypt)
- **Database Driver**: psycopg2-binary
- **Server**: Uvicorn

### Database
- **Provider**: Neon Serverless PostgreSQL
- **Version**: PostgreSQL 16+
- **Free Tier**: 0.5 GB storage, 1 project

### Development Tools
- **Package Manager (Frontend)**: npm or pnpm
- **Package Manager (Backend)**: UV
- **Version Control**: Git
- **AI Development**: Claude Code + Spec-Kit Plus

---

## Performance Considerations

### Frontend Performance (SC-003, SC-004)
- Code splitting via Next.js App Router (automatic)
- Image optimization via next/image
- Font optimization via next/font
- Static generation for public pages
- Client-side caching via SWR

### Backend Performance (SC-004, SC-005)
- Database connection pooling (Neon handles this)
- Indexed queries on user_id, completed, category
- Pagination for large result sets (future enhancement)
- Response compression (gzip)
- Async/await for all I/O operations

### Database Performance
- Composite indexes for common query patterns
- Efficient foreign key relationships
- Minimal N+1 query issues (SQLModel eager loading)

---

## Risk Mitigation

### Risk 1: JWT Secret Mismatch
**Mitigation**: Document shared secret requirement prominently in setup guide. Add startup validation that tests JWT signing/verification.

### Risk 2: CORS Configuration Errors
**Mitigation**: Provide exact CORS configuration in quickstart.md. Test with both localhost and production URLs.

### Risk 3: Database Connection Issues
**Mitigation**: Implement connection retry logic. Provide clear error messages for connection failures.

### Risk 4: User Data Leakage
**Mitigation**: Comprehensive integration tests for user isolation. Security audit checklist in tasks.md.

### Risk 5: Free Tier Limitations
**Mitigation**: Document free tier limits. Monitor usage. Provide upgrade path documentation.

---

## Open Questions

None - all technical decisions resolved based on comprehensive specification.

---

**Research Complete**: All technical unknowns resolved. Ready for Phase 1 (Design & Contracts).
