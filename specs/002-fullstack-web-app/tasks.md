# Implementation Tasks: Full-Stack Todo Web Application

**Feature Branch**: `002-fullstack-web-app`
**Generated**: 2026-02-03
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Task Summary

- **Total Tasks**: 45
- **Setup & Foundation**: 10 tasks
- **User Story 1 (P1)**: 8 tasks - Authentication
- **User Story 2 (P1)**: 7 tasks - Add/View Tasks
- **User Story 6 (P1)**: 4 tasks - Security
- **User Story 3 (P2)**: 3 tasks - Mark Complete
- **User Story 4 (P2)**: 5 tasks - Update/Delete
- **User Story 5 (P3)**: 5 tasks - Search/Filter
- **Polish**: 3 tasks

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize monorepo structure, configure dependencies, and establish database connection.

### Tasks

- [x] T001 Create monorepo directory structure (frontend/, backend/)
- [x] T002 [P] Initialize Next.js frontend with TypeScript and App Router in frontend/
- [x] T003 [P] Initialize FastAPI backend with UV package manager in backend/
- [x] T004 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [x] T005 [P] Create environment templates (.env.example) for frontend and backend
- [x] T006 Install frontend dependencies (Next.js, React, Better Auth, SWR, Zod, React Hook Form)
- [x] T007 Install backend dependencies (FastAPI, SQLModel, python-jose, passlib, psycopg2-binary, uvicorn)
- [x] T008 Configure Neon PostgreSQL connection in backend/src/database.py
- [x] T009 Create database schema (users and tasks tables) with indexes
- [x] T010 Generate and configure shared BETTER_AUTH_SECRET for both frontend and backend

**Completion Criteria**: Project structure exists, dependencies installed, database connected.

---

## Phase 2: Foundational Layer

**Goal**: Implement core infrastructure needed by all user stories.

### Tasks

- [x] T011 [P] Create User model in backend/src/models/user.py (Better Auth schema)
- [x] T012 [P] Create Task model in backend/src/models/task.py with validation
- [x] T013 [P] Implement JWT verification middleware in backend/src/auth/jwt.py
- [x] T014 [P] Create API client with auth headers in frontend/src/lib/api.ts
- [x] T015 [P] Create TypeScript types in frontend/src/types/index.ts (User, Task)
- [x] T016 Implement database connection pooling in backend/src/database.py
- [x] T017 Configure CORS in backend/src/main.py for frontend origin
- [x] T018 Create root layout with auth provider in frontend/src/app/layout.tsx

**Completion Criteria**: Models defined, JWT middleware ready, API client configured, CORS enabled.

---

## Phase 3: User Story 1 - Authentication (P1)

**Story**: As a new user, I want to sign up with email and password, so that I can have my own private todo list.

**Independent Test**: Create account → Sign in → Sign out → Verify JWT token issuance and redirection.

### Tasks

- [x] T019 [US1] Configure Better Auth in frontend/src/lib/auth.ts with email/password provider
- [x] T020 [P] [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx
- [x] T021 [P] [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx
- [x] T022 [P] [US1] Create signup form component in frontend/src/components/auth/SignupForm.tsx with Zod validation
- [x] T023 [P] [US1] Create signin form component in frontend/src/components/auth/SigninForm.tsx with Zod validation
- [x] T024 [US1] Implement auth state management with SWR in frontend/src/lib/auth.ts
- [x] T025 [US1] Create protected route middleware in frontend/src/middleware.ts
- [x] T026 [US1] Implement signout functionality and token invalidation

**Acceptance Criteria**:
- ✅ Valid signup redirects to tasks page with JWT token
- ✅ Valid signin returns JWT token and accesses tasks
- ✅ Signout invalidates token and redirects to login
- ✅ Duplicate email shows "Email already registered"
- ✅ Invalid credentials show "Invalid email or password"

---

## Phase 4: User Story 2 - Add and View Tasks (P1)

**Story**: As an authenticated user, I want to add new tasks and view my task list, so that I can track things I need to do.

**Independent Test**: Add tasks with title/description/category → View in list → Verify database persistence.

### Tasks

- [x] T027 [US2] Create tasks page in frontend/src/app/(dashboard)/tasks/page.tsx
- [x] T028 [P] [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [x] T029 [P] [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [x] T030 [P] [US2] Create TaskService for CRUD operations in backend/src/services/task_service.py
- [x] T031 [P] [US2] Create AddTaskForm component in frontend/src/components/tasks/AddTaskForm.tsx with validation
- [x] T032 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx
- [x] T033 [US2] Implement user_id filtering and authorization checks in TaskService

**Acceptance Criteria**:
- ✅ Task with title/description/category appears in list immediately
- ✅ Empty state message shown when no tasks exist
- ✅ Multiple tasks sorted by created date (newest first)
- ✅ Validation error shown for missing title
- ✅ Task saved to database with user_id

---

## Phase 5: User Story 6 - Secure Task Management (P1)

**Story**: As an authenticated user, I want my tasks to be private and secure, so that only I can access them.

**Independent Test**: Create two users → Add tasks to each → Verify neither can access other's tasks.

### Tasks

- [x] T034 [US6] Implement user_id validation in JWT middleware (backend/src/auth/jwt.py)
- [x] T035 [US6] Add 403 Forbidden checks for cross-user access in TaskService
- [x] T036 [US6] Implement token expiration handling in frontend/src/lib/api.ts
- [x] T037 [US6] Add redirect to login on 401/403 errors in frontend middleware

**Acceptance Criteria**:
- ✅ User A sees only their own tasks
- ✅ Expired JWT redirects to login page
- ✅ Unauthenticated access redirects to login
- ✅ API request without token returns 401
- ✅ API request with invalid token returns 401

---

## Phase 6: User Story 3 - Mark Tasks Complete (P2)

**Story**: As an authenticated user, I want to toggle task completion status, so that I can track my progress.

**Independent Test**: Mark task complete → Verify visual distinction → Mark incomplete → Verify persistence.

### Tasks

- [x] T038 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/tasks.py
- [x] T039 [P] [US3] Create TaskItem component with checkbox in frontend/src/components/tasks/TaskItem.tsx
- [x] T040 [US3] Implement optimistic UI updates for completion toggle with SWR mutate

**Acceptance Criteria**:
- ✅ Checkbox marks task complete with visual distinction
- ✅ Clicking again marks task incomplete
- ✅ Completion status persists after page refresh
- ✅ Cross-user toggle attempt returns 403

---

## Phase 7: User Story 4 - Update and Delete Tasks (P2)

**Story**: As an authenticated user, I want to edit or delete tasks, so that I can correct mistakes and remove tasks I no longer need.

**Independent Test**: Edit task details → Verify update → Delete task with confirmation → Verify removal.

### Tasks

- [x] T041 [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T042 [US4] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T043 [P] [US4] Create EditTaskForm component in frontend/src/components/tasks/EditTaskForm.tsx
- [x] T044 [P] [US4] Create DeleteConfirmDialog component in frontend/src/components/tasks/DeleteConfirmDialog.tsx
- [x] T045 [US4] Implement optimistic updates for edit/delete operations with SWR

**Acceptance Criteria**:
- ✅ Edit updates task immediately in UI
- ✅ Cancel discards changes
- ✅ Delete shows confirmation dialog
- ✅ Confirm removes task from list and database
- ✅ Cross-user edit/delete returns 403

---

## Phase 8: User Story 5 - Search and Filter Tasks (P3)

**Story**: As an authenticated user, I want to search and filter my tasks, so that I can quickly find specific items.

**Independent Test**: Search by keyword → Filter by status → Filter by category → Combine filters.

### Tasks

- [x] T046 [US5] Add search query parameter support to GET /api/{user_id}/tasks endpoint
- [x] T047 [US5] Add status and category filter parameters to GET /api/{user_id}/tasks endpoint
- [x] T048 [P] [US5] Create SearchBar component in frontend/src/components/tasks/SearchBar.tsx
- [x] T049 [P] [US5] Create FilterControls component in frontend/src/components/tasks/FilterControls.tsx
- [x] T050 [US5] Implement combined search and filter logic with SWR query params

**Acceptance Criteria**:
- ✅ Search shows only tasks matching keyword in title/description
- ✅ Status filter shows only completed or pending tasks
- ✅ Category filter shows only tasks in selected category
- ✅ Clear filters button resets to show all tasks
- ✅ Combined filters show tasks matching all criteria

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Add loading states, error handling, and responsive design.

### Tasks

- [x] T051 [P] Add loading skeletons to TaskList component
- [x] T052 [P] Implement error boundaries and user-friendly error messages
- [x] T053 [P] Add responsive design breakpoints for mobile/tablet/desktop

**Completion Criteria**: Loading states visible, errors handled gracefully, responsive on all devices.

---

## Dependency Graph

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1 Auth)
                                       ↓
                                    Phase 4 (US2 Add/View) → Phase 5 (US6 Security)
                                       ↓
                                    Phase 6 (US3 Complete)
                                       ↓
                                    Phase 7 (US4 Update/Delete)
                                       ↓
                                    Phase 8 (US5 Search/Filter)
                                       ↓
                                    Phase 9 (Polish)
```

**Critical Path**: Setup → Foundation → Auth → Add/View → Security

**Parallel Opportunities**:
- Within Setup: T002-T005 can run in parallel
- Within Foundation: T011-T015 can run in parallel
- Within US1: T020-T023 can run in parallel
- Within US2: T028-T032 can run in parallel
- Within US4: T043-T044 can run in parallel
- Within US5: T048-T049 can run in parallel
- Within Polish: T051-T053 can run in parallel

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
**Phases 1-5**: Setup + Foundation + US1 (Auth) + US2 (Add/View) + US6 (Security)
- **Tasks**: T001-T037 (37 tasks)
- **Delivers**: Working authentication + basic task management + security
- **Independent Test**: User can sign up, add tasks, view tasks, with full data isolation

### Incremental Delivery
1. **Sprint 1**: Phases 1-3 (Setup + Foundation + Auth) - T001-T026
2. **Sprint 2**: Phases 4-5 (Add/View + Security) - T027-T037
3. **Sprint 3**: Phases 6-7 (Complete + Update/Delete) - T038-T045
4. **Sprint 4**: Phases 8-9 (Search/Filter + Polish) - T046-T053

### Execution Notes
- Each user story phase is independently testable
- Mark tasks complete only when acceptance criteria are met
- Use [P] marker to identify parallelizable tasks
- Follow file paths exactly as specified
- Validate user isolation at every API endpoint

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] T### [P] [US#] Description with file path`
✅ Task IDs sequential (T001-T053)
✅ [P] markers on parallelizable tasks
✅ [US#] labels on user story tasks
✅ File paths specified for implementation tasks
✅ Acceptance criteria per user story
✅ Independent test criteria per user story

---

**Status**: Ready for implementation with `/sp.implement`
**Last Updated**: 2026-02-03
