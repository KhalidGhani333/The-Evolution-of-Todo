# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot-cohere` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-cohere/spec.md`

## Summary

Implement an AI-powered conversational interface for the Todo application using Cohere's command-r-plus model. Users will manage tasks through natural language commands instead of traditional UI interactions. The system uses a stateless architecture where conversation context is rebuilt from the database on each request, with five tool functions (add_task, list_tasks, complete_task, delete_task, update_task) that wrap existing TaskService methods. Security is enforced through JWT authentication, user data isolation at every layer, and comprehensive input validation to prevent prompt injection attacks.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Node.js 18+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Cohere SDK (>=5.0.0), Better Auth JWT verification
- Frontend: Next.js 16 (App Router), React, TypeScript
**Storage**: Neon PostgreSQL (existing) + 3 new tables (conversations, messages, tool_calls)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (backend: Hugging Face Spaces, frontend: Vercel)
**Project Type**: Web application (existing backend + frontend structure)
**Performance Goals**:
- Chat response: <3 seconds (p95)
- Database queries: <500ms (p95)
- UI rendering: <100ms after API response
- Support 100 concurrent users
**Constraints**:
- Stateless architecture (no server-side sessions)
- User data isolation enforced at database level
- Cohere API free tier rate limits
- JWT token-based authentication (existing)
**Scale/Scope**:
- Multi-user web application
- Unlimited conversations per user
- 50 messages per conversation (context window limit)
- 5 tool functions for task management

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Passed Gates

1. **Spec-Driven Development**: All implementation follows spec → plan → tasks workflow
2. **Phase-Progressive Architecture**: Building on completed Phase II (Full-Stack Web App)
3. **AI-Agent First Development**: Using Claude Code and Spec-Kit Plus for implementation
4. **Quality Over Speed**: Comprehensive security, testing, and performance requirements defined
5. **Submission-Ready Continuity**: Proper version control, documentation, and submission readiness maintained

### ⚠️ Constitutional Deviation (Justified)

**Deviation**: Using Cohere API instead of OpenAI Agents SDK (Phase III requirement)

**Justification**:
- **Technical Necessity**: Gemini free tier not working (user-reported issue)
- **Practical Alternative**: Cohere free tier functional and accessible
- **Equivalent Capability**: Cohere provides tool calling capabilities similar to OpenAI
- **No Architectural Impact**: Tool calling pattern remains the same, tool definitions portable
- **Migration Path**: Can migrate to OpenAI in future if needed without architectural changes

**Approval**: Documented in research.md for stakeholder review. Deviation does not compromise core principles or quality standards.

### ✅ Re-check After Phase 1 Design

All constitutional principles maintained:
- Security requirements met (JWT auth, user isolation, input validation)
- Performance standards defined and achievable (<3s chat, <500ms DB)
- Technology stack adherence (FastAPI, SQLModel, Next.js, Neon DB) - only AI provider changed
- Quality standards maintained (80%+ test coverage, comprehensive error handling)

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-cohere/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 research output (completed)
├── data-model.md        # Phase 1 data model (completed)
├── quickstart.md        # Phase 1 quickstart guide (completed)
├── contracts/           # Phase 1 API contracts (completed)
│   └── chat-api.yaml    # OpenAPI specification for chat endpoints
├── checklist.md         # Requirements checklist (completed)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan - run /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py              # Existing (Phase II)
│   │   ├── user.py              # Existing (Phase II)
│   │   └── conversation.py      # NEW: Conversation, Message, ToolCall models
│   ├── services/
│   │   ├── task_service.py      # Existing (Phase II)
│   │   ├── chat_service.py      # NEW: Cohere integration, conversation management
│   │   └── chat_tools.py        # NEW: Tool function implementations
│   ├── api/
│   │   ├── tasks.py             # Existing (Phase II)
│   │   ├── auth.py              # Existing (Phase II)
│   │   └── chat.py              # NEW: Chat endpoints
│   ├── database.py              # Existing (Phase II) - no changes needed
│   ├── auth.py                  # Existing (Phase II) - no changes needed
│   └── main.py                  # Existing (Phase II) - add chat router
├── tests/
│   ├── unit/
│   │   ├── test_chat_service.py # NEW: Chat service unit tests
│   │   └── test_chat_tools.py   # NEW: Tool function unit tests
│   ├── integration/
│   │   └── test_chat_api.py     # NEW: Chat API integration tests
│   └── security/
│       └── test_chat_security.py # NEW: Security tests (prompt injection, etc.)
├── migrations/
│   └── 003_add_chat_tables.sql  # NEW: Database migration for chat tables
└── requirements.txt             # UPDATE: Add cohere>=5.0.0

frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.tsx         # Existing (Phase II)
│   │   ├── Chat.tsx             # NEW: Chat interface component
│   │   ├── ChatMessage.tsx      # NEW: Individual message component
│   │   └── ConversationList.tsx # NEW: Conversation sidebar component
│   ├── app/
│   │   ├── tasks/               # Existing (Phase II)
│   │   └── chat/                # NEW: Chat page
│   │       └── page.tsx         # NEW: Chat page component
│   ├── lib/
│   │   └── api.ts               # UPDATE: Add chat API functions
│   └── types/
│       └── chat.ts              # NEW: Chat-related TypeScript types
└── tests/
    └── chat.test.tsx            # NEW: Chat component tests
```

**Structure Decision**: Using existing web application structure (Option 2) with backend and frontend directories. New chat functionality integrates seamlessly with existing Phase II architecture. No structural changes needed - only adding new files to existing directories.

## Complexity Tracking

> **No violations requiring justification**

All complexity is justified by requirements:
- Three new tables (conversations, messages, tool_calls) are minimal for conversation management
- Five tool functions map directly to five user stories in spec
- Stateless architecture reduces complexity (no session management)
- Thin wrapper pattern for tools avoids code duplication

## Phase 0: Research Summary

**Status**: ✅ Completed

**Key Decisions Documented in research.md**:

1. **Cohere API Integration**: Using command-r-plus model with tool calling capabilities
2. **Stateless Architecture**: Rebuild conversation context from database on each request
3. **Database Schema**: Three new tables with strategic indexing for performance
4. **Tool Calling Pattern**: Five thin wrapper functions around existing TaskService
5. **Security Layers**: Input validation, prompt injection prevention, user isolation, logging
6. **Performance Strategy**: Database indexing, connection pooling, message limiting, async operations

**Research Artifacts**:
- research.md (comprehensive technical decisions with rationale)

## Phase 1: Design Summary

**Status**: ✅ Completed

**Design Artifacts Created**:

1. **data-model.md**: Complete entity definitions with validation rules, relationships, indexes, and SQLModel implementation
2. **contracts/chat-api.yaml**: OpenAPI 3.0 specification for all chat endpoints with request/response schemas
3. **quickstart.md**: Step-by-step implementation guide with code examples

**Key Design Decisions**:

### 1. Database Schema

**Conversations Table**:
- UUID primary key for global uniqueness
- user_id foreign key for data isolation
- status enum (active/archived) for lifecycle management
- Composite index on (user_id, created_at) for efficient listing

**Messages Table**:
- UUID primary key
- conversation_id foreign key with cascade delete
- role enum (user/assistant) for message type
- Optional JSON fields for tool metadata
- Composite index on (conversation_id, created_at) for chronological retrieval

**ToolCalls Table** (Optional):
- Detailed audit trail for debugging
- Tracks execution time and success/failure
- Enables analytics on tool usage

### 2. API Design

**POST /api/chat**:
- Primary endpoint for sending messages
- Accepts optional conversation_id (creates new if omitted)
- Returns conversation_id and AI response
- Includes tool_calls metadata for transparency

**GET /api/conversations**:
- List user's conversations with pagination
- Filter by status (active/archived)
- Ordered by updated_at DESC

**GET /api/conversations/{id}**:
- Retrieve conversation with message history
- Limit messages for performance (default 50)

**PATCH /api/conversations/{id}**:
- Update title or status
- User isolation enforced

**DELETE /api/conversations/{id}**:
- Cascade delete all messages
- Permanent deletion

### 3. Security Architecture

**Layer 1: Input Validation**:
- Pydantic schemas with length limits
- Whitespace normalization
- Suspicious pattern detection

**Layer 2: Authentication**:
- JWT token verification (existing Phase II mechanism)
- user_id extracted from token, never from user input

**Layer 3: Authorization**:
- User isolation enforced in all database queries
- Ownership verification before operations
- 403 Forbidden for unauthorized access

**Layer 4: Prompt Injection Prevention**:
- System prompt with security rules
- User input sandboxing
- Instruction isolation

**Layer 5: Audit Logging**:
- Log all chat interactions
- Log tool invocations
- Log security events

### 4. Performance Optimization

**Database**:
- Strategic indexing on high-traffic queries
- Connection pooling (already configured)
- Limit conversation history to 50 messages
- Composite indexes for multi-column queries

**API**:
- Cohere API timeout: 5 seconds
- Retry logic with exponential backoff
- Graceful degradation on failures

**Frontend**:
- Optimistic UI updates
- Loading indicators
- Pagination for long histories

### 5. Tool Calling Implementation

**Tool Definition Pattern**:
```python
{
    "name": "add_task",
    "description": "Create a new task for the user",
    "parameter_definitions": {
        "title": {"type": "str", "required": True},
        "description": {"type": "str", "required": False}
    }
}
```

**Execution Flow**:
1. User sends message
2. Cohere API analyzes intent
3. AI decides to invoke tool(s)
4. Backend executes tool with user_id injection
5. Tool result returned to AI
6. AI formats result into natural language
7. Response saved to database and returned to user

**Tool Functions**:
- add_task: Wraps TaskService.create_task
- list_tasks: Wraps TaskService.get_tasks
- complete_task: Wraps TaskService.toggle_complete
- delete_task: Wraps TaskService.delete_task
- update_task: Wraps TaskService.update_task

All tools enforce user isolation by injecting user_id from JWT token.

## Implementation Sequence

### Phase 2: Tasks Generation (Next Step)

Run `/sp.tasks` to generate actionable task list from this plan. Expected task categories:

1. **Database Setup** (1-2 tasks):
   - Create migration script
   - Run migration and verify

2. **Backend Models** (1 task):
   - Implement Conversation, Message, ToolCall models

3. **Backend Services** (3-4 tasks):
   - Implement ChatService with Cohere integration
   - Implement ChatTools with 5 tool functions
   - Implement conversation management service
   - Add error handling and logging

4. **Backend API** (2-3 tasks):
   - Implement chat endpoint
   - Implement conversation management endpoints
   - Add rate limiting middleware

5. **Frontend Components** (3-4 tasks):
   - Create Chat component
   - Create ChatMessage component
   - Create ConversationList component
   - Add chat page

6. **Frontend Integration** (1-2 tasks):
   - Add chat API functions
   - Add TypeScript types
   - Integrate with existing auth

7. **Testing** (4-5 tasks):
   - Write unit tests for ChatService
   - Write unit tests for ChatTools
   - Write integration tests for chat API
   - Write security tests
   - Write frontend component tests

8. **Documentation** (1 task):
   - Update README with Phase III information

9. **Deployment** (1-2 tasks):
   - Configure environment variables
   - Deploy backend and frontend

**Estimated Total**: 18-25 tasks

### Phase 3: Implementation (After /sp.tasks)

Execute tasks in dependency order using `/sp.implement` or manual execution.

### Phase 4: Testing & Validation

- Run all unit tests (target: 80%+ coverage)
- Run integration tests
- Run security tests (prompt injection, SQL injection, XSS)
- Performance testing (100 concurrent users)
- Manual testing with diverse natural language inputs

### Phase 5: Deployment

- Run database migrations on production
- Configure COHERE_API_KEY in production environment
- Deploy backend to Hugging Face Spaces
- Deploy frontend to Vercel
- Verify end-to-end functionality

## Risk Mitigation

### Risk 1: Cohere API Reliability
**Mitigation**: Graceful error handling, user-friendly messages, traditional UI remains functional

### Risk 2: Prompt Injection Attacks
**Mitigation**: Multi-layer security (input validation, system prompt rules, user isolation at DB level)

### Risk 3: Performance Degradation
**Mitigation**: Database indexing, message limiting, connection pooling, monitoring

### Risk 4: Poor Natural Language Understanding
**Mitigation**: Confirmation prompts for destructive operations, clear feedback, comprehensive testing

### Risk 5: Cost Overruns
**Mitigation**: Monitor API usage, implement rate limiting, set up billing alerts

## Success Criteria

Implementation is complete when:

1. ✅ All 35 functional requirements from spec.md are implemented
2. ✅ All 20 success criteria from spec.md are met
3. ✅ 80%+ unit test coverage achieved
4. ✅ Integration tests pass for all endpoints
5. ✅ Security tests pass (no vulnerabilities)
6. ✅ Performance targets met (<3s chat, <500ms DB)
7. ✅ Manual testing confirms natural language understanding works
8. ✅ Deployment successful on production environment
9. ✅ Documentation complete and accurate
10. ✅ Constitutional compliance maintained

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task list from this plan
2. **Review tasks** with stakeholders for approval
3. **Execute tasks** using `/sp.implement` or manual implementation
4. **Test thoroughly** at each stage
5. **Deploy incrementally** (database → backend → frontend)
6. **Monitor and iterate** based on user feedback

---

**Plan Status**: ✅ Complete and ready for task generation
**Constitutional Compliance**: ✅ Passed with justified deviation (Cohere vs OpenAI)
**Design Artifacts**: ✅ All Phase 1 artifacts created (research.md, data-model.md, contracts/, quickstart.md)
**Ready for**: `/sp.tasks` command to generate actionable task list
