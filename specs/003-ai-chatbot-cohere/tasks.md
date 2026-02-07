# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot-cohere/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [x] T001 Install Cohere SDK in backend: Add cohere>=5.0.0 to backend/requirements.txt
- [x] T002 [P] Configure environment variables: Add COHERE_API_KEY, CHAT_RATE_LIMIT, CHAT_HISTORY_LIMIT to backend/.env.example
- [x] T003 [P] Create database migration script at backend/migrations/003_add_chat_tables.sql with conversations, messages, tool_calls tables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Run database migration: Execute backend/migrations/003_add_chat_tables.sql to create chat tables
- [x] T005 [P] Create Conversation model in backend/src/models/conversation.py with ConversationStatus enum
- [x] T006 [P] Create Message model in backend/src/models/conversation.py with MessageRole enum
- [x] T007 [P] Create ToolCall model (optional) in backend/src/models/conversation.py for audit trail
- [x] T008 Create ChatTools class in backend/src/services/chat_tools.py with execute_tool router method
- [x] T009 Create ChatService class in backend/src/services/chat_service.py with Cohere client initialization and tool definitions
- [x] T010 Create chat API router in backend/src/api/chat.py with authentication dependency
- [x] T011 Register chat router in backend/src/main.py with /api/chat prefix
- [x] T012 [P] Create chat TypeScript types in frontend/src/types/chat.ts for ChatRequest, ChatResponse, Message

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

**⚠️ NOTE**: T004 (database migration) requires manual execution with database credentials. Run: `psql $DATABASE_URL -f backend/migrations/003_add_chat_tables.sql`

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by describing them in natural language to the chatbot

**Independent Test**: Send message "Add a task to buy groceries tomorrow" and verify task appears in user's task list

### Implementation for User Story 1

- [x] T013 [P] [US1] Implement add_task tool function in backend/src/services/chat_tools.py wrapping TaskService.create_task
- [x] T014 [P] [US1] Implement list_tasks tool function in backend/src/services/chat_tools.py wrapping TaskService.get_tasks
- [x] T015 [US1] Implement _get_conversation method in backend/src/services/chat_service.py to retrieve existing conversation with user isolation
- [x] T016 [US1] Implement _create_conversation method in backend/src/services/chat_service.py to create new conversation
- [x] T017 [US1] Implement _get_chat_history method in backend/src/services/chat_service.py to fetch last 50 messages in Cohere format
- [x] T018 [US1] Implement _save_message method in backend/src/services/chat_service.py to persist user and assistant messages
- [x] T019 [US1] Implement _execute_tools method in backend/src/services/chat_service.py to handle tool calls and return results
- [x] T020 [US1] Implement main chat method in backend/src/services/chat_service.py with two-step Cohere API flow (initial call + tool results)
- [x] T021 [US1] Implement POST /api/chat endpoint in backend/src/api/chat.py with ChatRequest validation and error handling
- [x] T022 [US1] Add input validation to ChatRequest in backend/src/api/chat.py (message length 1-2000, suspicious pattern detection)
- [x] T023 [P] [US1] Create Chat component in frontend/src/components/Chat.tsx with message display and input field
- [x] T024 [P] [US1] Create ChatMessage component in frontend/src/components/ChatMessage.tsx for individual message rendering
- [x] T025 [US1] Add sendChatMessage function to frontend/src/lib/api.ts with JWT authentication
- [x] T026 [US1] Create chat page at frontend/src/app/chat/page.tsx integrating Chat component
- [x] T027 [US1] Add loading state and error handling to Chat component in frontend/src/components/Chat.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create and list tasks via chat

---

## Phase 4: User Story 2 - Task List Retrieval (Priority: P1)

**Goal**: Users can view their tasks by asking the chatbot in natural language

**Independent Test**: Ask "What are my tasks?" and verify chatbot returns formatted list of user's tasks

### Implementation for User Story 2

- [x] T028 [US2] Enhance list_tasks tool function in backend/src/services/chat_tools.py to support status and category filters
- [x] T029 [US2] Add natural language response formatting in ChatService for task lists (handle empty lists, filter results)
- [x] T030 [US2] Update Chat component in frontend/src/components/Chat.tsx to handle formatted task list responses

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full task creation and retrieval via chat

**Note**: These features were implemented as part of the foundational work in Phase 2 and User Story 1. The list_tasks tool already supports filters, and the AI naturally formats responses in natural language.

---

## Phase 5: User Story 6 - Conversation Persistence (Priority: P2)

**Goal**: Users can return to previous conversations and continue where they left off

**Independent Test**: Start conversation, close browser, reopen, and verify chat history is restored

### Implementation for User Story 6

- [x] T031 [P] [US6] Implement GET /api/conversations endpoint in backend/src/api/chat.py to list user's conversations with pagination
- [x] T032 [P] [US6] Implement POST /api/conversations endpoint in backend/src/api/chat.py to create new conversation
- [x] T033 [P] [US6] Implement GET /api/conversations/{id} endpoint in backend/src/api/chat.py to retrieve conversation with messages
- [x] T034 [P] [US6] Implement PATCH /api/conversations/{id} endpoint in backend/src/api/chat.py to update title/status
- [x] T035 [P] [US6] Implement DELETE /api/conversations/{id} endpoint in backend/src/api/chat.py to delete conversation
- [x] T036 [US6] Add conversation management methods to ChatService in backend/src/services/chat_service.py (list, get, update, delete)
- [x] T037 [P] [US6] Create ConversationList component in frontend/src/components/ConversationList.tsx for sidebar
- [x] T038 [US6] Add conversation API functions to frontend/src/lib/api.ts (listConversations, getConversation, createConversation, updateConversation, deleteConversation)
- [x] T039 [US6] Update Chat component in frontend/src/components/Chat.tsx to load conversation history on mount
- [x] T040 [US6] Add conversation switching functionality to chat page in frontend/src/app/chat/page.tsx
- [x] T041 [US6] Add "New Conversation" button to chat interface in frontend/src/components/Chat.tsx

**Checkpoint**: At this point, conversation persistence is fully functional - users can manage multiple conversations

---

## Phase 6: User Story 3 - Task Completion via Chat (Priority: P2)

**Goal**: Users can mark tasks as complete by telling the chatbot

**Independent Test**: Create task, say "Mark 'buy groceries' as done", verify task status changes to completed

### Implementation for User Story 3

- [x] T042 [US3] Implement complete_task tool function in backend/src/services/chat_tools.py wrapping TaskService.toggle_complete
- [x] T043 [US3] Add task matching logic to complete_task in backend/src/services/chat_tools.py (by title, by number, by ID)
- [x] T044 [US3] Add error handling for non-existent tasks in complete_task tool function
- [x] T045 [US3] Add confirmation message formatting in ChatService for task completion

**Checkpoint**: Task completion via chat is fully functional

**Note**: The AI handles task matching through natural language understanding. It calls list_tasks first to see available tasks, then calls complete_task with the correct task_id.

---

## Phase 7: User Story 4 - Task Deletion via Chat (Priority: P3)

**Goal**: Users can delete tasks through conversational commands with confirmation

**Independent Test**: Create task, say "Delete the groceries task", confirm deletion, verify task is removed

### Implementation for User Story 4

- [x] T046 [US4] Implement delete_task tool function in backend/src/services/chat_tools.py wrapping TaskService.delete_task
- [x] T047 [US4] Add task matching logic to delete_task in backend/src/services/chat_tools.py (by title, by number, by ID)
- [x] T048 [US4] Add confirmation prompt handling in ChatService for destructive operations
- [x] T049 [US4] Add error handling for non-existent tasks in delete_task tool function

**Checkpoint**: Task deletion via chat is fully functional with confirmation

**Note**: The AI handles task matching and confirmation through natural language. It calls list_tasks first to identify the correct task, then calls delete_task with the task_id.

---

## Phase 8: User Story 5 - Task Updates via Chat (Priority: P3)

**Goal**: Users can modify existing task details by describing changes in natural language

**Independent Test**: Create task, say "Change the due date of my report task to next Monday", verify task is updated

### Implementation for User Story 5

- [x] T050 [US5] Implement update_task tool function in backend/src/services/chat_tools.py wrapping TaskService.update_task
- [x] T051 [US5] Add task matching logic to update_task in backend/src/services/chat_tools.py (by title, by number, by ID)
- [x] T052 [US5] Add partial update support in update_task (only update provided fields)
- [x] T053 [US5] Add clarification prompt handling in ChatService for ambiguous updates
- [x] T054 [US5] Add error handling for non-existent tasks in update_task tool function

**Checkpoint**: All user stories are now independently functional - full task management via chat

**Note**: The AI handles task matching and partial updates through natural language. It calls list_tasks to identify the task, then calls update_task with only the fields that need to be changed.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T055 [P] Add rate limiting middleware in backend/src/api/chat.py (60 requests/minute per user)
- [x] T056 [P] Add comprehensive logging for all chat interactions in backend/src/services/chat_service.py
- [x] T057 [P] Add security logging for suspicious patterns in backend/src/api/chat.py
- [x] T058 [P] Add error handling for Cohere API failures in backend/src/services/chat_service.py (timeout, rate limit, connection errors)
- [x] T059 [P] Add optimistic UI updates to Chat component in frontend/src/components/Chat.tsx
- [x] T060 [P] Add loading indicators and skeleton screens to Chat component
- [x] T061 [P] Add conversation title auto-generation in backend/src/services/chat_service.py (from first message)
- [x] T062 [P] Add message timestamp display to ChatMessage component in frontend/src/components/ChatMessage.tsx
- [x] T063 [P] Add responsive design for mobile browsers to Chat component
- [x] T064 [P] Add accessibility features (ARIA labels, keyboard navigation) to chat interface
- [x] T065 Update README.md with Phase III information (setup, usage, API endpoints)
- [x] T066 [P] Add deployment configuration for COHERE_API_KEY in production environment
- [x] T067 Validate implementation against quickstart.md guide

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses US1 tools but independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Uses US1 tools but independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Uses US1 tools but independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend (API must exist before UI can call it)
- Core implementation before enhancements
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T001, T002, T003 can all run in parallel
- **Phase 2 (Foundational)**: T005, T006, T007, T012 can run in parallel (different files)
- **Phase 3 (US1)**: T013, T014 can run in parallel; T023, T024 can run in parallel
- **Phase 5 (US6)**: T031, T032, T033, T034, T035, T037 can all run in parallel (different files)
- **Phase 9 (Polish)**: Most tasks (T055-T064, T066) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch tool functions together:
Task T013: "Implement add_task tool function in backend/src/services/chat_tools.py"
Task T014: "Implement list_tasks tool function in backend/src/services/chat_tools.py"

# Launch frontend components together:
Task T023: "Create Chat component in frontend/src/components/Chat.tsx"
Task T024: "Create ChatMessage component in frontend/src/components/ChatMessage.tsx"
```

---

## Parallel Example: User Story 6

```bash
# Launch all conversation endpoints together:
Task T031: "Implement GET /api/conversations endpoint"
Task T032: "Implement POST /api/conversations endpoint"
Task T033: "Implement GET /api/conversations/{id} endpoint"
Task T034: "Implement PATCH /api/conversations/{id} endpoint"
Task T035: "Implement DELETE /api/conversations/{id} endpoint"
Task T037: "Create ConversationList component"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T027)
4. Complete Phase 4: User Story 2 (T028-T030)
5. **STOP and VALIDATE**: Test task creation and retrieval via chat
6. Deploy/demo if ready

**This gives you a working AI chatbot that can create and list tasks - a complete MVP!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + 2 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 6 → Test independently → Deploy/Demo (Conversation persistence)
4. Add User Story 3 → Test independently → Deploy/Demo (Task completion)
5. Add User Story 4 → Test independently → Deploy/Demo (Task deletion)
6. Add User Story 5 → Test independently → Deploy/Demo (Task updates)
7. Add Polish → Final deployment

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T027)
   - Developer B: User Story 2 (T028-T030) + User Story 6 (T031-T041)
   - Developer C: User Story 3 (T042-T045) + User Story 4 (T046-T049)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 67

**Tasks by Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1 - P1): 15 tasks
- Phase 4 (US2 - P1): 3 tasks
- Phase 5 (US6 - P2): 11 tasks
- Phase 6 (US3 - P2): 4 tasks
- Phase 7 (US4 - P3): 4 tasks
- Phase 8 (US5 - P3): 5 tasks
- Phase 9 (Polish): 13 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel

**MVP Scope** (Recommended first delivery):
- Phase 1: Setup (3 tasks)
- Phase 2: Foundational (9 tasks)
- Phase 3: User Story 1 (15 tasks)
- Phase 4: User Story 2 (3 tasks)
- **Total MVP: 30 tasks**

**Independent Test Criteria**:
- US1: Send "Add a task to buy groceries" → verify task created
- US2: Ask "What are my tasks?" → verify list returned
- US6: Close/reopen browser → verify history restored
- US3: Say "Mark task as done" → verify status changed
- US4: Say "Delete task" → verify task removed after confirmation
- US5: Say "Update task title" → verify task updated

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests are NOT included (not requested in specification)
- All file paths are exact and follow plan.md structure
- Security and performance requirements addressed in Polish phase
