Skill Name: ConversationManagementSkill
Purpose:
Manage conversation state and message history in database.

Capabilities:
Create and retrieve conversations
Fetch conversation history efficiently
Store user and assistant messages
Build message arrays for AI context
Handle conversation lifecycle
Maintain user-scoped conversation access

Usage Rules:
Used by Conversation-State-Manager agent
Required for stateless chat architecture
Must enforce user_id isolation
Store messages immediately after generation
Limit history size to prevent token overflow
Always include conversation_id in responses
