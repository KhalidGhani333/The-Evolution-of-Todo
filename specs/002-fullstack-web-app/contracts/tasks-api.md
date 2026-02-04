# API Contract: Tasks Endpoints
## Feature: Full-Stack Todo Web Application

**Version**: 1.0.0
**Base URL**: `/api/{user_id}/tasks`
**Managed By**: FastAPI backend

---

## Overview

Tasks endpoints provide CRUD operations for todo items. All endpoints require JWT authentication and enforce user isolation - users can only access their own tasks.

**Authorization Pattern**:
1. Extract `user_id` from URL path
2. Verify JWT token from Authorization header
3. Extract `authenticated_user_id` from JWT payload (`sub` claim)
4. Compare: if `user_id != authenticated_user_id`, return 403 Forbidden
5. Proceed with operation, filtering by `user_id`

---

## GET /api/{user_id}/tasks

**Purpose**: List all tasks for authenticated user with optional filters (FR-009, FR-014, FR-015, FR-016, FR-017)

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Query Parameters** (all optional):
- `status` (string): Filter by completion status
  - Values: `all`, `pending`, `completed`
  - Default: `all`
- `category` (string): Filter by category (exact match)
- `search` (string): Search keyword in title or description (case-insensitive)

**Examples**:
```
GET /api/user-123/tasks
GET /api/user-123/tasks?status=pending
GET /api/user-123/tasks?category=Work
GET /api/user-123/tasks?search=groceries
GET /api/user-123/tasks?status=pending&category=Personal&search=buy
```

### Response

**Success (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "userId": "user-123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "category": "Personal",
      "completed": false,
      "createdAt": "2026-02-03T10:00:00Z",
      "updatedAt": "2026-02-03T10:00:00Z"
    },
    {
      "id": 2,
      "userId": "user-123",
      "title": "Finish project report",
      "description": "Complete Q4 analysis",
      "category": "Work",
      "completed": true,
      "createdAt": "2026-02-02T14:30:00Z",
      "updatedAt": "2026-02-03T09:15:00Z"
    }
  ],
  "total": 2,
  "filters": {
    "status": "all",
    "category": null,
    "search": null
  }
}
```

**Success (200 OK)** - Empty list:
```json
{
  "tasks": [],
  "total": 0,
  "filters": {
    "status": "all",
    "category": null,
    "search": null
  }
}
```

**Error (401 Unauthorized)** - Missing or invalid token:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)** - user_id mismatch:
```json
{
  "error": "Forbidden: Cannot access another user's tasks",
  "code": "FORBIDDEN"
}
```

---

## POST /api/{user_id}/tasks

**Purpose**: Create a new task (FR-006, FR-007, FR-008)

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",  // optional
  "category": "Personal"               // optional
}
```

**Validation**:
- `title`: Required, 1-200 characters, non-empty after trim
- `description`: Optional, max 1000 characters
- `category`: Optional, max 50 characters

### Response

**Success (201 Created)**:
```json
{
  "id": 1,
  "userId": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "category": "Personal",
  "completed": false,
  "createdAt": "2026-02-03T10:00:00Z",
  "updatedAt": "2026-02-03T10:00:00Z"
}
```

**Error (400 Bad Request)** - Validation error:
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": [
    {
      "field": "title",
      "message": "Title is required and must be between 1-200 characters"
    }
  ]
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden: Cannot create task for another user",
  "code": "FORBIDDEN"
}
```

---

## GET /api/{user_id}/tasks/{id}

**Purpose**: Retrieve a specific task by ID

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)
- `id` (integer, required): Task ID

**Headers**:
```
Authorization: Bearer <jwt-token>
```

### Response

**Success (200 OK)**:
```json
{
  "id": 1,
  "userId": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "category": "Personal",
  "completed": false,
  "createdAt": "2026-02-03T10:00:00Z",
  "updatedAt": "2026-02-03T10:00:00Z"
}
```

**Error (404 Not Found)** - Task doesn't exist or belongs to another user:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden: Cannot access another user's task",
  "code": "FORBIDDEN"
}
```

---

## PUT /api/{user_id}/tasks/{id}

**Purpose**: Update a task's details (FR-010)

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)
- `id` (integer, required): Task ID

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Body** (all fields optional, only provided fields are updated):
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas",
  "category": "Shopping"
}
```

**Validation**:
- `title`: If provided, 1-200 characters, non-empty after trim
- `description`: If provided, max 1000 characters
- `category`: If provided, max 50 characters

### Response

**Success (200 OK)**:
```json
{
  "id": 1,
  "userId": "user-123",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas",
  "category": "Shopping",
  "completed": false,
  "createdAt": "2026-02-03T10:00:00Z",
  "updatedAt": "2026-02-03T11:30:00Z"
}
```

**Error (400 Bad Request)** - Validation error:
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": [
    {
      "field": "title",
      "message": "Title must be between 1-200 characters"
    }
  ]
}
```

**Error (404 Not Found)**:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden: Cannot update another user's task",
  "code": "FORBIDDEN"
}
```

---

## DELETE /api/{user_id}/tasks/{id}

**Purpose**: Delete a task permanently (FR-011)

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)
- `id` (integer, required): Task ID

**Headers**:
```
Authorization: Bearer <jwt-token>
```

### Response

**Success (204 No Content)**:
```
(empty body)
```

**Error (404 Not Found)**:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden: Cannot delete another user's task",
  "code": "FORBIDDEN"
}
```

---

## PATCH /api/{user_id}/tasks/{id}/complete

**Purpose**: Toggle task completion status (FR-012)

**Authentication**: Required (JWT token)

### Request

**Path Parameters**:
- `user_id` (string, required): User ID (must match authenticated user)
- `id` (integer, required): Task ID

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Body**:
```json
{
  "completed": true
}
```

### Response

**Success (200 OK)**:
```json
{
  "id": 1,
  "userId": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "category": "Personal",
  "completed": true,
  "createdAt": "2026-02-03T10:00:00Z",
  "updatedAt": "2026-02-03T12:00:00Z"
}
```

**Error (404 Not Found)**:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden: Cannot modify another user's task",
  "code": "FORBIDDEN"
}
```

---

## Common Response Headers

All successful responses include:
```
Content-Type: application/json
X-Request-ID: <unique-request-id>
```

All error responses include:
```
Content-Type: application/json
X-Request-ID: <unique-request-id>
```

---

## Rate Limiting (Future Enhancement)

Not implemented in MVP, but recommended for production:
- 100 requests per minute per user
- 429 Too Many Requests response when exceeded

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_TOKEN` | 401 | JWT token missing, invalid, or expired |
| `FORBIDDEN` | 403 | User attempting to access another user's data |
| `NOT_FOUND` | 404 | Task doesn't exist or belongs to another user |
| `VALIDATION_ERROR` | 400 | Request body validation failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Performance Expectations (SC-004)

- All endpoints must respond within 500ms under normal load
- Database queries optimized with indexes on user_id, completed, category
- Connection pooling handled by Neon

---

## Security Notes (FR-013)

1. **User Isolation**: All queries filtered by authenticated user_id
2. **Authorization**: user_id in URL must match JWT token's sub claim
3. **Input Validation**: All inputs validated on both frontend and backend
4. **SQL Injection Prevention**: SQLModel uses parameterized queries
5. **XSS Prevention**: Input sanitization + React automatic escaping
