Skill Name: FunctionCallingSkill
Purpose:
Configure and handle AI function calling (tools) for Gemini API.

Capabilities:
Define function schemas in Gemini format
Map MCP tools to Gemini function definitions
Execute function calls from AI responses
Return function results to AI for continuation
Handle multi-step tool execution
Manage tool call errors and retries

Usage Rules:
Used by AI-Agent-Builder agent
Required for Gemini tool integration
Must validate function arguments before execution
Always return results in expected format
Handle cases where AI doesn't call any tools
