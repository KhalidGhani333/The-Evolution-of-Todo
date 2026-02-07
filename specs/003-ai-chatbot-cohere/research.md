# Technical Research: AI-Powered Todo Chatbot with Cohere API

**Feature**: Phase III - AI Chatbot Integration
**Created**: 2026-02-06
**Status**: Research Complete

## Executive Summary

This document provides comprehensive technical research for implementing an AI-powered conversational interface for the Todo application using Cohere's command-r-plus model. The research addresses the constitutional deviation (using Cohere instead of OpenAI), stateless architecture requirements, database schema design, tool calling implementation, security patterns, and performance optimization strategies.

---

## 1. Cohere API Integration (Constitution Deviation)

### Decision
Use **Cohere API with command-r-plus model** for natural language understanding and tool calling capabilities.

### Rationale
- **Practical Necessity**: Gemini free tier is not working for the user, while Cohere free tier is functional and accessible
- **Tool Calling Support**: Cohere's command-r-plus model provides robust tool calling capabilities similar to OpenAI's function calling
- **Production-Ready**: Cohere offers enterprise-grade APIs with good documentation and Python SDK support
- **Cost-Effective**: Free tier available for development and testing, with clear pricing for production scaling

### Alternatives Considered

1. **OpenAI Agents SDK (Constitutional Requirement)**
   - Pros: Officially specified in constitution, mature ecosystem, extensive documentation
   - Cons: Requires paid API access, user may not have access or budget
   - Verdict: Not viable due to access/cost constraints

2. **Google Gemini API**
   - Pros: Free tier available, good performance, Google backing
   - Cons: User reports free tier not working, unreliable for development
   - Verdict: Rejected due to technical issues

3. **Anthropic Claude API**
   - Pros: Excellent reasoning capabilities, tool use support
   - Cons: No free tier, requires paid access
   - Verdict: Not viable due to cost constraints

4. **Open Source Models (Llama, Mistral)**
   - Pros: Free to use, full control, no API limits
   - Cons: Requires infrastructure for hosting, complex setup, lower quality tool calling
   - Verdict: Too complex for hackathon timeline

### Implementation Notes

**Cohere Python SDK**: `pip install cohere>=5.0.0`

**Tool Calling Flow**: Two-step process - initial chat request with tools, then follow-up with tool results if AI invokes tools.

**Key Parameters**:
- model: "command-r-plus"
- temperature: 0.3 (deterministic responses)
- chat_history: List of previous messages for context
- tools: List of 5 tool definitions
- tool_results: Results from tool executions (second call only)

---

## 2. Stateless Conversation Architecture

### Decision
Implement **fully stateless backend** where each API request rebuilds conversation context from the database, with no server-side session storage.

### Rationale
- **Horizontal Scalability**: Any backend instance can handle any request
- **Reliability**: No session loss due to server restarts
- **Simplicity**: No session management, Redis, or sticky sessions needed
- **Cloud-Native**: Aligns with serverless and containerized deployment (Phase IV/V)
- **Consistency**: Extends Phase II's stateless JWT authentication pattern

### Alternatives Considered

1. **Server-Side Session Storage (Redis/Memcached)**
   - Rejected: Adds infrastructure complexity, requires sticky sessions

2. **Client-Side State Management**
   - Rejected: Security risk, large payloads, client manipulation possible

3. **Hybrid Approach (Cache + Database)**
   - Deferred: Future optimization if performance issues arise

### Implementation Strategy

**On Each Request**:
1. Extract user_id from JWT token
2. Extract conversation_id from request body
3. Query database for conversation messages (last 50)
4. Transform to Cohere chat_history format
5. Send to Cohere API with current message
6. Save user message and AI response to database
7. Return AI response to client

**Performance Mitigation**:
- Database indexing on (conversation_id, created_at)
- Limit to last 50 messages per conversation
- Connection pooling (already configured in Phase II)
- Query optimization with specific column selection

---

## 3. Database Schema Design

### Decision
Add **three new tables**: conversations, messages, and tool_calls (optional).

### Rationale
- **Separation of Concerns**: Chat data separate from task data
- **User Isolation**: Each table includes user_id foreign key
- **Audit Trail**: Full conversation history for debugging and analytics
- **Scalability**: Normalized schema supports efficient queries
- **Consistency**: Follows Phase II conventions (SQLModel, timestamps, user_id)

### Schema Definition

**Conversations Table**:
- id (UUID, primary key)
- user_id (foreign key to users, indexed)
- title (varchar 200, default "New Conversation")
- status (enum: active/archived, indexed)
- created_at (timestamp, indexed)
- updated_at (timestamp)

**Messages Table**:
- id (UUID, primary key)
- conversation_id (foreign key to conversations, indexed)
- role (enum: user/assistant, indexed)
- content (text, message content)
- tool_calls (JSON, optional metadata)
- tool_results (JSON, optional metadata)
- created_at (timestamp, indexed)

**Tool Calls Table** (Optional):
- id (UUID, primary key)
- message_id (foreign key to messages, indexed)
- tool_name (varchar 100, indexed)
- parameters (JSON)
- result (JSON)
- success (boolean, indexed)
- error_message (text, optional)
- execution_time_ms (integer, optional)
- created_at (timestamp, indexed)

### Critical Indexes
1. conversations.user_id - User isolation queries
2. conversations.created_at - List by recency
3. messages.conversation_id - Message retrieval
4. (messages.conversation_id, messages.created_at) - Composite for optimal performance

---

## 4. Tool Calling Implementation

### Decision
Implement **five tool functions** as thin wrappers around existing TaskService methods.

### Rationale
- **Reuse Existing Logic**: TaskService already implements CRUD with user isolation
- **Thin Wrapper Pattern**: Tools translate AI parameters to service calls
- **Consistent Security**: User isolation enforced at service layer
- **Error Handling**: Service errors propagate to AI for natural language responses
- **Testability**: Tool functions independently testable

### Tool Functions

1. **add_task**: Create new task (title, description, category)
2. **list_tasks**: Retrieve tasks with filters (status, category)
3. **complete_task**: Mark task as completed (task_id)
4. **delete_task**: Delete task permanently (task_id)
5. **update_task**: Update task properties (task_id, title, description, category)

### Tool Execution Pattern

**Router Function**: Maps tool names to functions, injects user_id and session, executes tool, returns structured result.

**Return Format**: All tools return `{"success": bool, "message": str, "data": dict}` or `{"success": false, "error": str}`

---

## 5. Security Patterns

### Decision
Implement **defense-in-depth security** with multiple layers.

### Rationale
- **Zero Trust**: Validate at every layer
- **User Isolation**: Enforce at database query level
- **Audit Trail**: Log all interactions
- **Prompt Injection Defense**: Treat user input as untrusted data
- **Compliance**: Prepare for security audits

### Security Layers

**1. Input Validation**:
- Pydantic schema validation
- Message length limits (1-2000 characters)
- Whitespace normalization
- Suspicious pattern detection

**2. Prompt Injection Prevention**:
- System prompt with security rules
- User input sandboxing
- Control character removal
- Instruction isolation

**3. User Isolation Enforcement**:
- user_id from JWT token (never from user input)
- user_id in all database WHERE clauses
- Ownership verification before operations
- 403 Forbidden for unauthorized access

**4. Comprehensive Logging**:
- Log all chat interactions (user_id, conversation_id, timestamps)
- Log tool invocations (tool name, parameters, results)
- Log security events (suspicious patterns, failed auth)
- Log performance metrics (response times, error rates)

**5. Rate Limiting**:
- Per-user rate limits (e.g., 60 requests/minute)
- Per-IP rate limits for abuse prevention
- Exponential backoff for repeated failures

---

## 6. Performance Optimization

### Decision
Implement **targeted optimizations** to meet performance targets (<3s chat, <500ms DB).

### Rationale
- **User Experience**: Fast responses critical for chat interface
- **Scalability**: Efficient queries support concurrent users
- **Cost Control**: Minimize API calls and database load

### Optimization Strategies

**1. Database Performance**:
- Composite indexes on (conversation_id, created_at)
- Connection pooling (already configured)
- Limit conversation history to 50 messages
- Async database operations where possible

**2. API Performance**:
- Cohere API timeout: 5 seconds
- Retry logic with exponential backoff
- Graceful degradation on API failures
- Cache tool definitions (static data)

**3. Frontend Performance**:
- Optimistic UI updates (show user message immediately)
- Loading indicators during AI processing
- Pagination for long conversation histories
- WebSocket consideration for future real-time updates

**4. Monitoring**:
- Track p95 latency for chat responses
- Track p95 latency for database queries
- Alert on performance degradation
- Dashboard for key metrics

---

## 7. Error Handling Strategy

### Decision
Implement **graceful error handling** with user-friendly messages.

### Error Categories

**1. AI Service Errors**:
- Cohere API down: "I'm temporarily unavailable. Please try again."
- Rate limit exceeded: "I'm receiving too many requests. Please wait a moment."
- Timeout: "That took too long. Please try again with a shorter message."

**2. Database Errors**:
- Connection failure: "I'm having trouble saving your message. Please try again."
- Query timeout: "That operation took too long. Please try again."
- Constraint violation: "That operation couldn't be completed. Please check your input."

**3. Tool Execution Errors**:
- Task not found: "I couldn't find that task. Can you be more specific?"
- Invalid parameters: "I didn't understand that request. Can you rephrase?"
- Permission denied: "You don't have permission to access that task."

**4. Validation Errors**:
- Empty message: "Please enter a message."
- Message too long: "That message is too long. Please keep it under 2000 characters."
- Suspicious content: "That message contains suspicious content. Please rephrase."

---

## 8. Testing Strategy

### Unit Testing
- Test each tool function with valid/invalid inputs
- Test conversation persistence and retrieval
- Test user isolation enforcement
- Test input validation and sanitization
- Test error handling for all scenarios

### Integration Testing
- Test end-to-end chat flow
- Test conversation state restoration
- Test JWT authentication integration
- Test concurrent operations
- Test AI service failure scenarios

### Performance Testing
- Load test with 100 concurrent users
- Measure response latency under load
- Test database query performance
- Measure UI rendering performance

### Security Testing
- Test user data isolation
- Test prompt injection attempts
- Test SQL injection and XSS
- Test authentication enforcement
- Test authorization checks

---

## 9. Deployment Considerations

### Environment Variables
- COHERE_API_KEY: Cohere API key (required)
- DATABASE_URL: PostgreSQL connection string (existing)
- JWT_SECRET: JWT signing secret (existing)
- CHAT_RATE_LIMIT: Requests per minute per user (default: 60)
- CHAT_HISTORY_LIMIT: Max messages per conversation (default: 50)

### Database Migration
- Run migration to create conversations, messages, tool_calls tables
- Create indexes for performance
- No data migration needed (new feature)

### Monitoring
- Set up alerts for API errors
- Monitor response latency
- Track tool usage analytics
- Monitor security events

---

## 10. Future Enhancements

**Phase III+** (Post-MVP):
- Conversation export to PDF/JSON
- Voice input/output integration
- Multi-language support (Urdu)
- Advanced AI features (task suggestions, prioritization)
- Real-time updates via WebSocket
- Conversation search and filtering
- Task templates via chat
- Calendar integration

**Performance Optimizations**:
- Redis caching for conversation history
- CDN for static assets
- Database read replicas
- Async task processing

---

## Constitutional Compliance Note

**Deviation**: Using Cohere API instead of OpenAI Agents SDK (Phase III requirement)

**Justification**:
- Gemini free tier not working (user-reported technical issue)
- Cohere free tier functional and accessible
- Cohere provides equivalent tool calling capabilities
- No architectural impact - tool calling pattern remains the same
- Can migrate to OpenAI in future if needed (tool definitions portable)

**Approval**: Documented in research.md for stakeholder review

---

## Conclusion

This research provides a comprehensive technical foundation for implementing Phase III AI chatbot with Cohere API. All key decisions are documented with rationale, alternatives considered, and implementation notes. The approach balances security, performance, and user experience while maintaining consistency with Phase II architecture.

**Next Steps**: Proceed to Phase 1 design (data-model.md, contracts/, quickstart.md)
