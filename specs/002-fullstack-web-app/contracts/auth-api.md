# API Contract: Authentication Endpoints
## Feature: Full-Stack Todo Web Application

**Version**: 1.0.0
**Base URL**: `/api/auth`
**Managed By**: Better Auth (Next.js frontend)

---

## Overview

Authentication endpoints are provided by Better Auth and handle user registration, sign-in, sign-out, and session management. These endpoints issue JWT tokens that the FastAPI backend verifies.

---

## POST /api/auth/signup

**Purpose**: Register a new user account

**Authentication**: None (public endpoint)

### Request

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"  // optional
}
```

**Validation**:
- `email`: Required, valid email format, unique
- `password`: Required, minimum 8 characters
- `name`: Optional, max 100 characters

### Response

**Success (201 Created)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-02-03T10:00:00Z",
    "updatedAt": "2026-02-03T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-02-10T10:00:00Z"
}
```

**Error (400 Bad Request)** - Email already exists:
```json
{
  "error": "Email already registered",
  "code": "EMAIL_EXISTS"
}
```

**Error (400 Bad Request)** - Invalid input:
```json
{
  "error": "Password must be at least 8 characters",
  "code": "INVALID_PASSWORD"
}
```

---

## POST /api/auth/signin

**Purpose**: Authenticate existing user and issue JWT token

**Authentication**: None (public endpoint)

### Request

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Response

**Success (200 OK)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-02-03T10:00:00Z",
    "updatedAt": "2026-02-03T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-02-10T10:00:00Z"
}
```

**Error (401 Unauthorized)** - Invalid credentials:
```json
{
  "error": "Invalid email or password",
  "code": "INVALID_CREDENTIALS"
}
```

---

## POST /api/auth/signout

**Purpose**: Invalidate user session and JWT token

**Authentication**: Required (JWT token)

### Request

**Headers**:
```
Authorization: Bearer <jwt-token>
```

### Response

**Success (200 OK)**:
```json
{
  "message": "Signed out successfully"
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "code": "INVALID_TOKEN"
}
```

---

## GET /api/auth/session

**Purpose**: Retrieve current user session information

**Authentication**: Required (JWT token)

### Request

**Headers**:
```
Authorization: Bearer <jwt-token>
```

### Response

**Success (200 OK)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-02-03T10:00:00Z",
    "updatedAt": "2026-02-03T10:00:00Z"
  },
  "expiresAt": "2026-02-10T10:00:00Z"
}
```

**Error (401 Unauthorized)** - Token expired:
```json
{
  "error": "Session expired. Please sign in again.",
  "code": "TOKEN_EXPIRED"
}
```

**Error (401 Unauthorized)** - Invalid token:
```json
{
  "error": "Invalid session",
  "code": "INVALID_TOKEN"
}
```

---

## JWT Token Structure

**Algorithm**: HS256 (HMAC with SHA-256)

**Payload**:
```json
{
  "sub": "uuid-string",  // user_id
  "email": "user@example.com",
  "iat": 1738579200,     // issued at (Unix timestamp)
  "exp": 1739184000      // expires at (Unix timestamp, +7 days)
}
```

**Verification**:
- Backend verifies signature using shared `BETTER_AUTH_SECRET`
- Backend extracts `sub` (user_id) from verified token
- Backend uses user_id for authorization checks

---

## Security Notes

1. **Password Storage**: Passwords hashed with bcrypt (cost factor 12)
2. **Token Expiration**: JWT tokens expire after 7 days
3. **HTTPS Required**: All auth endpoints must use HTTPS in production
4. **CORS**: Auth endpoints accessible only from allowed origins
5. **Rate Limiting**: Consider implementing rate limiting for signup/signin (future enhancement)

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `EMAIL_EXISTS` | 400 | Email already registered |
| `INVALID_PASSWORD` | 400 | Password doesn't meet requirements |
| `INVALID_CREDENTIALS` | 401 | Email or password incorrect |
| `INVALID_TOKEN` | 401 | JWT token invalid or malformed |
| `TOKEN_EXPIRED` | 401 | JWT token has expired |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
