# Data Model: Interactive CLI Todo Application

**Date**: 2026-02-02
**Feature**: Interactive CLI Todo Application
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the data structures and entities for the Interactive CLI Todo Application. The data model is designed to support all functional requirements while maintaining simplicity and clarity for a single-file implementation.

## Core Entities

### 1. Todo Entity

The primary entity representing a single todo item.

**Attributes**:

| Field | Type | Required | Constraints | Default | Description |
|-------|------|----------|-------------|---------|-------------|
| `id` | string (UUID) | Yes | UUID4 format | Auto-generated | Unique identifier for the todo |
| `title` | string | Yes | 1-200 characters | None | Brief description of the task |
| `description` | string | No | 0-1000 characters | Empty string | Detailed description of the task |
| `category` | string | No | 0-50 characters | Empty string | Categorization tag for organization |
| `completed` | boolean | Yes | true/false | false | Completion status of the task |
| `created_at` | string (ISO 8601) | Yes | Valid datetime | Current timestamp | When the todo was created |
| `updated_at` | string (ISO 8601) | Yes | Valid datetime | Current timestamp | When the todo was last modified |

**Validation Rules**:
- `title`: Must not be empty or whitespace-only, maximum 200 characters
- `description`: Maximum 1000 characters, can be empty
- `category`: Maximum 50 characters, can be empty
- `completed`: Must be boolean value
- `id`: Must be valid UUID4 string
- `created_at`, `updated_at`: Must be valid ISO 8601 datetime strings

**Example JSON Representation**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and vegetables",
  "category": "shopping",
  "completed": false,
  "created_at": "2026-02-02T10:30:00Z",
  "updated_at": "2026-02-02T10:30:00Z"
}
```

### 2. Application State

The in-memory state of the application during runtime.

**Attributes**:

| Field | Type | Description |
|-------|------|-------------|
| `todos` | List[Todo] | Collection of all todo items |
| `undo_stack` | List[List[Todo]] | Stack of previous states for undo (max 10) |
| `current_menu` | string | Current menu context (main, add, list, etc.) |
| `selected_index` | integer | Currently selected menu item index |
| `filter_category` | string or None | Active category filter (None = no filter) |
| `search_query` | string or None | Active search query (None = no search) |

**State Transitions**:
- Application starts → Load todos from JSON → Initialize empty undo stack
- User performs action → Push current state to undo stack → Execute action → Update state
- User selects undo → Pop from undo stack → Restore previous state
- User exits → Save current todos to JSON → Terminate

### 3. Menu State

Represents the current menu and navigation state.

**Menu Types**:
- `MAIN_MENU`: Primary navigation menu
- `ADD_TODO`: Add new todo workflow
- `LIST_TODOS`: Display all todos
- `SEARCH_TODOS`: Search interface
- `FILTER_TODOS`: Filter by category interface
- `COMPLETE_TODO`: Mark todo complete interface
- `INCOMPLETE_TODO`: Mark todo incomplete interface
- `UPDATE_TODO`: Update todo interface
- `DELETE_TODO`: Delete todo interface
- `UNDO`: Undo last action
- `HELP`: Display help information
- `EXIT`: Exit application

**Navigation Flow**:
```
MAIN_MENU
├── ADD_TODO → (collect input) → MAIN_MENU
├── LIST_TODOS → (display) → MAIN_MENU
├── SEARCH_TODOS → (collect query) → (display results) → MAIN_MENU
├── FILTER_TODOS → (select category) → (display filtered) → MAIN_MENU
├── COMPLETE_TODO → (select todo) → (mark complete) → MAIN_MENU
├── INCOMPLETE_TODO → (select todo) → (mark incomplete) → MAIN_MENU
├── UPDATE_TODO → (select todo) → (collect updates) → MAIN_MENU
├── DELETE_TODO → (select todo) → (confirm) → MAIN_MENU
├── UNDO → (restore state) → MAIN_MENU
├── HELP → (display help) → MAIN_MENU
└── EXIT → (save) → Terminate
```

## Data Persistence

### Storage Format: JSON

**File**: `todos.json` (created in application directory)

**Structure**:
```json
{
  "version": "1.0",
  "todos": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string",
      "category": "string",
      "completed": boolean,
      "created_at": "ISO-8601-datetime",
      "updated_at": "ISO-8601-datetime"
    }
  ]
}
```

**Persistence Operations**:

1. **Load on Startup**:
   - Check if `todos.json` exists
   - If exists: Parse JSON and validate structure
   - If missing or invalid: Initialize with empty list
   - Handle corrupted files gracefully with error message

2. **Save on Exit**:
   - Serialize current todos to JSON
   - Write to temporary file first
   - Atomic rename to `todos.json`
   - Handle write errors with user notification

3. **Error Recovery**:
   - Corrupted JSON: Log error, start with empty list, backup corrupted file
   - Missing file: Create new file with empty list
   - Permission denied: Display error, continue with in-memory only
   - Disk full: Display error, attempt to save to alternative location

## Data Operations

### CRUD Operations

**Create (Add Todo)**:
```
Input: title (required), description (optional), category (optional)
Process:
  1. Validate title (not empty, ≤200 chars)
  2. Validate description (≤1000 chars)
  3. Validate category (≤50 chars)
  4. Generate UUID for id
  5. Set completed = false
  6. Set created_at = current timestamp
  7. Set updated_at = current timestamp
  8. Add to todos list
  9. Push previous state to undo stack
Output: Success message with todo ID
```

**Read (List/Search/Filter)**:
```
List All:
  - Return all todos sorted by created_at (newest first)
  - Display with completion status and category

Search:
  Input: search query (string)
  Process: Case-insensitive match in title or description
  Output: Filtered list of matching todos

Filter by Category:
  Input: category name
  Process: Exact match on category field
  Output: Filtered list of todos in category
```

**Update (Modify Todo)**:
```
Input: todo ID, new title (optional), new description (optional), new category (optional)
Process:
  1. Find todo by ID
  2. Validate new values if provided
  3. Update fields
  4. Set updated_at = current timestamp
  5. Push previous state to undo stack
Output: Success message
```

**Delete (Remove Todo)**:
```
Input: todo ID
Process:
  1. Find todo by ID
  2. Confirm deletion with user
  3. Remove from todos list
  4. Push previous state to undo stack
Output: Success message
```

**Toggle Completion**:
```
Input: todo ID
Process:
  1. Find todo by ID
  2. Toggle completed field
  3. Set updated_at = current timestamp
  4. Push previous state to undo stack
Output: Success message with new status
```

### Undo Operation

```
Process:
  1. Check if undo stack is not empty
  2. Pop previous state from stack
  3. Restore todos list to previous state
  4. Display message indicating what was undone
Output: Success message
```

## Data Integrity

### Validation Rules

**On Load**:
- Verify JSON structure matches expected schema
- Validate all required fields present
- Validate data types for all fields
- Validate constraints (string lengths, UUID format)
- Skip invalid todos with warning message

**On Save**:
- Ensure all todos have valid structure
- Use atomic write pattern (temp file + rename)
- Verify write succeeded before confirming to user

**On User Input**:
- Validate before creating/updating todos
- Provide clear error messages for validation failures
- Re-prompt user on validation errors

### Consistency Rules

1. **Unique IDs**: All todos must have unique UUID identifiers
2. **Timestamps**: created_at ≤ updated_at for all todos
3. **Completion Status**: Must be boolean (true/false)
4. **String Lengths**: Enforce maximum lengths on all string fields
5. **Undo Stack**: Maximum 10 levels, oldest removed when full

## Performance Considerations

### In-Memory Operations
- Use list for todos (maintains insertion order)
- Use dict for ID-based lookups (O(1) access)
- Cache search/filter results until next modification

### Persistence Operations
- Load once at startup (not on every operation)
- Save once at exit (not after every operation)
- Use atomic writes to prevent corruption

### Scalability
- Support up to 1000+ todos without performance degradation
- Implement pagination for display if list exceeds 100 items
- Use efficient search algorithms (case-insensitive string matching)

## Future Extensibility

This data model is designed to support future phases:

**Phase II (Web App)**:
- Add `user_id` field for multi-user support
- Add `priority` field for task prioritization
- Add `tags` field for multiple categorization

**Phase III (AI Chatbot)**:
- Add `conversation_id` for chat context
- Add `ai_generated` flag for AI-created todos

**Phase V (Advanced Features)**:
- Add `due_date` field for deadlines
- Add `recurrence_rule` for recurring tasks
- Add `reminder_time` for notifications

The current simple structure allows easy extension without breaking existing functionality.
