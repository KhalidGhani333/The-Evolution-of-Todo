# Contracts Directory

**Feature**: Interactive CLI Todo Application (Phase I)
**Date**: 2026-02-02

## Why No API Contracts?

This directory is typically used for API contracts (OpenAPI/GraphQL schemas) when building web services or APIs. However, **Phase I is a console application** with no external API endpoints.

## Phase I Architecture

The Phase I application is:
- **Single-user console application**
- **Local-only execution** (no network communication)
- **Direct function calls** (no HTTP/REST endpoints)
- **JSON file persistence** (not an API)

Therefore, API contracts are not applicable for this phase.

## Future Phases

API contracts will be relevant in:

### Phase II: Full-Stack Web Application
- RESTful API endpoints for todo operations
- OpenAPI specification for backend API
- Frontend-backend contract definitions

### Phase III: AI Chatbot
- MCP (Model Context Protocol) tool definitions
- Chat API endpoint specifications
- Agent-to-service contracts

## Phase I Interface Documentation

Instead of API contracts, Phase I uses:

1. **Data Model**: See `data-model.md` for entity definitions
2. **Function Signatures**: Documented in source code docstrings
3. **CLI Interface**: Documented in `quickstart.md`

## Internal Function Contracts

While there are no external API contracts, the application does have internal function contracts defined in the code:

**Example**:
```python
def add_todo(title: str, description: str = "", category: str = "") -> dict:
    """
    Add a new todo item.

    Args:
        title: Todo title (required, 1-200 chars)
        description: Optional description (max 1000 chars)
        category: Optional category (max 50 chars)

    Returns:
        dict: Created todo with id, timestamps, and all fields

    Raises:
        ValueError: If title is empty or exceeds length limits
    """
```

These internal contracts are enforced through:
- Type hints (Python typing module)
- Input validation functions
- Unit tests verifying behavior
- Docstring documentation

## Summary

**Phase I**: No external API contracts needed (console application)
**Phase II+**: API contracts will be defined in this directory using OpenAPI/GraphQL schemas
