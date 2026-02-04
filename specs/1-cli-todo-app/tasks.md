# Implementation Tasks: Interactive CLI Todo Application

**Branch**: `1-cli-todo-app` | **Date**: 2026-02-02
**Feature**: Interactive CLI Todo Application (Phase I)
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## Overview

This document breaks down the Phase I Interactive CLI Todo Application into discrete, testable tasks organized by user story. Each task follows the Agentic Dev Stack workflow and is designed for implementation via Claude Code.

**Total Tasks**: 28
**Estimated Completion**: Sequential implementation with parallel opportunities

## Task Organization

Tasks are organized into phases:
1. **Setup**: Project initialization (4 tasks)
2. **Foundational**: Core infrastructure (5 tasks)
3. **User Story 1**: New User Experience - Add & View (5 tasks)
4. **User Story 2**: Daily Usage - Complete, Search, Filter (6 tasks)
5. **User Story 3**: Bulk Operations - Update, Delete, Undo (4 tasks)
6. **User Story 4**: Error Recovery - Validation & Error Handling (4 tasks)

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies

- [X] T001 Create project directory structure (src/, tests/)
- [X] T002 Initialize UV project with pyproject.toml (Python 3.13+, rich>=13.7.0, pytest>=7.4.0)
- [X] T003 Create README.md with setup instructions from quickstart.md
- [X] T004 Create .gitignore for Python project (venv, __pycache__, todos.json, .pytest_cache)

## Phase 2: Foundational

**Goal**: Build core infrastructure needed by all user stories

- [X] T005 [P] Implement Todo data class in src/main.py (id, title, description, category, completed, timestamps)
- [X] T006 [P] Implement JSON persistence functions in src/main.py (load_todos, save_todos with atomic writes)
- [X] T007 Implement application state management in src/main.py (todos list, undo_stack, current_menu)
- [X] T008 [P] Implement rich console setup in src/main.py (Console instance, color scheme, table formatting)
- [X] T009 Implement main menu display in src/main.py (11 options with arrow-key navigation using rich)

## Phase 3: User Story 1 - New User Experience

**Story Goal**: User can add first todo, view list, and persist data between sessions

**Independent Test Criteria**:
- [ ] User can start application and see main menu
- [ ] User can add todo with title and category
- [ ] User can view todo list showing completion status
- [ ] User can exit and data persists to todos.json
- [ ] User can restart and see previously added todos

**Tasks**:

- [X] T010 [P] [US1] Implement add_todo function in src/main.py (collect title, description, category; generate UUID; add to list)
- [X] T011 [P] [US1] Implement list_todos function in src/main.py (display todos in rich table with status indicators)
- [X] T012 [US1] Implement menu navigation loop in src/main.py (handle user selection, route to functions)
- [X] T013 [US1] Implement exit_application function in src/main.py (save todos, display goodbye message)
- [X] T014 [US1] Implement application startup in src/main.py (load todos, display welcome, show menu)

## Phase 4: User Story 2 - Daily Usage

**Story Goal**: User can mark todos complete, add multiple tasks, search, and filter by category

**Independent Test Criteria**:
- [ ] User can mark todos as complete/incomplete
- [ ] User can add multiple todos in one session
- [ ] User can search todos by keyword (case-insensitive)
- [ ] User can filter todos by category
- [ ] All operations complete within 2 seconds

**Tasks**:

- [X] T015 [P] [US2] Implement mark_complete function in src/main.py (select todo by ID, toggle completed status)
- [X] T016 [P] [US2] Implement mark_incomplete function in src/main.py (select todo by ID, set completed=false)
- [X] T017 [P] [US2] Implement search_todos function in src/main.py (case-insensitive keyword match in title/description)
- [X] T018 [P] [US2] Implement filter_by_category function in src/main.py (display categories, filter todos)
- [X] T019 [US2] Integrate completion functions into menu navigation in src/main.py
- [X] T020 [US2] Integrate search and filter into menu navigation in src/main.py

## Phase 5: User Story 3 - Bulk Operations

**Story Goal**: User can update todos, delete todos, and undo last action

**Independent Test Criteria**:
- [ ] User can update todo title, description, or category
- [ ] User can delete todo with confirmation
- [ ] User can undo last action (up to 10 levels)
- [ ] Undo restores previous state correctly

**Tasks**:

- [X] T021 [P] [US3] Implement update_todo function in src/main.py (select todo, update fields with validation)
- [X] T022 [P] [US3] Implement delete_todo function in src/main.py (select todo, confirm, remove from list)
- [X] T023 [US3] Implement undo_last_action function in src/main.py (pop from undo_stack, restore state)
- [X] T024 [US3] Implement state snapshot before mutations in src/main.py (push to undo_stack before add/update/delete)

## Phase 6: User Story 4 - Error Recovery

**Story Goal**: Application handles all invalid inputs gracefully without crashing

**Independent Test Criteria**:
- [ ] Empty title input shows error and re-prompts
- [ ] Exceeding length limits shows error and re-prompts
- [ ] Corrupted JSON file loads with safe defaults
- [ ] Invalid menu selections handled gracefully
- [ ] Application never crashes from user input

**Tasks**:

- [X] T025 [P] [US4] Implement input validation functions in src/main.py (validate_title, validate_description, validate_category)
- [X] T026 [P] [US4] Implement error display function in src/main.py (show error in rich panel, re-prompt user)
- [X] T027 [US4] Add try-except blocks to JSON operations in src/main.py (handle FileNotFoundError, JSONDecodeError)
- [X] T028 [US4] Add input validation to all user input collection in src/main.py (apply validators, show errors)

## Phase 7: Polish & Documentation

**Goal**: Final touches and help system

- [X] T029 [P] Implement help_display function in src/main.py (show usage instructions, keyboard shortcuts)
- [X] T030 [P] Add performance optimization in src/main.py (lazy loading for large lists, efficient search)
- [ ] T031 Create demo video showing all features (max 90 seconds)
- [X] T032 Final testing and validation against acceptance criteria

## Dependencies

### Story Completion Order

```
Setup (Phase 1)
  ↓
Foundational (Phase 2)
  ↓
├─→ US1: New User Experience (Phase 3) [BLOCKING for all others]
    ↓
    ├─→ US2: Daily Usage (Phase 4) [Can start after US1]
    ├─→ US3: Bulk Operations (Phase 5) [Can start after US1]
    └─→ US4: Error Recovery (Phase 6) [Can start after US1]
        ↓
        Polish (Phase 7)
```

**Critical Path**: Setup → Foundational → US1 → Polish
**Parallel Opportunities**: US2, US3, US4 can be implemented in parallel after US1

### Task Dependencies

**Blocking Tasks** (must complete before others):
- T001-T004: Setup (blocks all)
- T005-T009: Foundational (blocks all user stories)
- T010-T014: US1 (blocks US2, US3, US4)

**Parallel Tasks** (can execute simultaneously):
- T005, T006, T008 (different components)
- T010, T011 (different functions)
- T015, T016, T017, T018 (different functions)
- T021, T022 (different functions)
- T025, T026 (different functions)
- T029, T030 (different components)

## Parallel Execution Examples

### After Foundational Phase
```
Parallel Group 1 (US1):
- T010: Implement add_todo
- T011: Implement list_todos
Then: T012, T013, T014 (sequential)
```

### After US1 Complete
```
Parallel Group 2 (US2):
- T015: Implement mark_complete
- T016: Implement mark_incomplete
- T017: Implement search_todos
- T018: Implement filter_by_category

Parallel Group 3 (US3):
- T021: Implement update_todo
- T022: Implement delete_todo

Parallel Group 4 (US4):
- T025: Implement validation functions
- T026: Implement error display
```

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
**Recommended First Delivery**: User Story 1 only
- Tasks T001-T014
- Provides: Add todo, view list, persistence
- Testable: Complete new user experience
- Deliverable: Working console app with basic functionality

### Incremental Delivery
1. **MVP**: US1 (New User Experience)
2. **Iteration 2**: US2 (Daily Usage) - adds search, filter, completion
3. **Iteration 3**: US3 (Bulk Operations) - adds update, delete, undo
4. **Iteration 4**: US4 (Error Recovery) - adds robustness
5. **Final**: Polish - adds help, optimization

### Testing Strategy
- Unit tests not explicitly required by specification
- Integration testing via manual validation against acceptance criteria
- Each user story has independent test criteria for validation

## Task Format Validation

✅ All tasks follow required format:
- Checkbox: `- [ ]`
- Task ID: T001-T032 (sequential)
- [P] marker: Present on parallelizable tasks
- [US#] label: Present on user story tasks
- Description: Clear action with file path
- File paths: All tasks specify src/main.py (single-file implementation)

## Summary

- **Total Tasks**: 32
- **Setup Tasks**: 4
- **Foundational Tasks**: 5
- **US1 Tasks**: 5 (New User Experience)
- **US2 Tasks**: 6 (Daily Usage)
- **US3 Tasks**: 4 (Bulk Operations)
- **US4 Tasks**: 4 (Error Recovery)
- **Polish Tasks**: 4
- **Parallel Opportunities**: 15 tasks can run in parallel
- **MVP Scope**: 14 tasks (Setup + Foundational + US1)
- **Critical Path**: Setup → Foundational → US1 → Polish

## Next Steps

1. Review and approve task breakdown
2. Execute tasks using `/sp.implement` or manual implementation via Claude Code
3. Validate each user story against independent test criteria
4. Iterate through user stories incrementally
5. Complete polish phase for final delivery
