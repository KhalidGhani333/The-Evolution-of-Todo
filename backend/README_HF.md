---
title: Todo API Backend
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo API Backend

FastAPI backend for The Evolution of Todo application with JWT authentication and PostgreSQL database.

## Features

- User authentication with JWT tokens
- Task CRUD operations with user isolation
- PostgreSQL database integration
- RESTful API with automatic documentation

## API Documentation

Once deployed, visit:
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation

## Environment Variables

Required secrets (configure in Space settings):
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT (min 32 characters)
- `FRONTEND_URL` - Frontend URL for CORS
