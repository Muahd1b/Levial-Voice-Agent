Deep Research Report: Expanded Orchestration for Levial
Date: November 24, 2025 Audience: Jonas (Founder/Developer of Levial) Goal: Design a robust, modular orchestration layer for Levial using the Model Context Protocol (MCP).

Executive Summary
MCP is the Standard: The Model Context Protocol (MCP) is the de-facto standard for connecting LLMs to external tools. The official mcp Python SDK is the recommended library.
Client-Server Architecture: Levial will act as an MCP Client, connecting to multiple local or remote MCP Servers (e.g., filesystem, brave-search, git).
Dynamic Discovery: Tools should be discovered dynamically at runtime. The mcp SDK handles the ListTools protocol, allowing Levial to query connected servers for their capabilities.
Orchestration Logic: The

ConversationOrchestrator
needs to be updated to:
Initialize connections to configured MCP servers.
Fetch available tools (ListTools).
Inject tool definitions into the LLM's system prompt.
Parse LLM responses for tool calls.
Execute tools via the MCP client (CallTool).
Feed results back to the LLM.
Security is Critical: Running a local filesystem server requires strict sandboxing (e.g., Docker or restricted user permissions) to prevent accidental data loss.
Recommended Stack:
Client: mcp (Python SDK).
Servers: mcp-server-filesystem (official), mcp-server-brave-search (official/community).
LLM: Mistral/Ollama (ensure model supports function calling or use a prompt engineering approach).
Foundations & Definitions
MCP (Model Context Protocol): An open standard for connecting AI models to data and tools.
MCP Client: The application (Levial) that talks to the LLM and manages tool execution.
MCP Server: A standalone process that exposes specific resources (files) or tools (functions) to the client.
Transport: The communication channel (usually stdio for local processes, or SSE for remote).
Conceptual Map
⚠️ Failed to render Mermaid diagram: Parse error on line 2
graph TD
User[User (Voice/Text)] --> Levial[Levial (MCP Client)]
Levial -->|Context + Tools| LLM[Ollama (Mistral)]
LLM -->|Tool Call| Levial
Levial -->|CallTool| Server1[Filesystem MCP Server]
Levial -->|CallTool| Server2[Brave Search MCP Server]
Server1 -->|Result| Levial
Server2 -->|Result| Levial
Levial -->|Final Response| TTS[Piper TTS]
Current State of the Field
Adoption: MCP is rapidly gaining traction, backed by Anthropic.
Ecosystem: A growing list of "Reference Servers" exists for common tasks (Git, Filesystem, Postgres, Brave Search).
Python SDK: The mcp library is mature enough for production use in a local assistant.
Approaches & Methods

1. MCP Client Implementation
   Library: Use mcp (pip install mcp).
   Connection: Use stdio transport for local servers. This means Levial will spawn the MCP server processes as subprocesses.
   Pattern:

# Pseudo-code for Client

async with StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]) as params:
async with mcp.ClientSession(params) as session:
tools = await session.list_tools() # ... expose tools to LLM ... 2. Tool Discovery & Registry
Dynamic Registry: Levial should maintain an internal registry of active MCP sessions.
Startup: Read config.json -> Start MCP Servers -> Query ListTools -> Aggregate all tools into a single list for the LLM. 3. Orchestration Logic (The Loop)
State Machine Update:
THINKING: Now involves a sub-loop:
Generate LLM response.
Check if response is a Tool Call.
If yes -> EXECUTING state -> Call Tool -> Add result to history -> Goto 1.
If no -> SPEAKING state. 4. Security & Sandboxing
Filesystem: Do NOT give root access. Configure the filesystem server to only access specific directories (e.g., /Users/jonas/levial_data).
Human-in-the-loop: For sensitive actions (delete file, send email), Levial should ask for voice confirmation ("I'm about to delete file X, proceed?").
Specific Integrations
Web Search
Provider: Brave Search is recommended for its privacy focus and robust API.
Workflow:
User: "What's the weather in Tokyo?"
Levial (LLM): Calls brave_search.search(query="weather Tokyo").
MCP Server: Returns search snippets.
Levial (LLM): Summarizes snippets into a spoken response.
File System
Schema: Standard read_file, write_file, list_directory tools.
Use Case: "Summarize the PDF in my downloads folder." -> list_directory -> read_file -> Summarize.
Risks & Mitigations
Latency: Spawning multiple MCP servers might slow down startup. Mitigation: Keep servers running in background or lazy-load them.
Context Window: Too many tools might overflow the LLM's context. Mitigation: Filter tools based on user intent or use a larger model context.
Hallucination: LLM might call non-existent tools. Mitigation: Strict prompt engineering and validation of tool calls.
Actionable Recommendations
Install SDK: pip install mcp.
Update Config: Add an mcp_servers section to

config/default.json
.
Refactor Orchestrator: Implement the "Tool Use" sub-loop in

levial/orchestrator.py
.
Start Simple: Begin with just the Time or Calculator tool to verify the pipeline before adding complex Web Search.
Further Reading
Model Context Protocol Documentation
Anthropic Python SDK
MCP Server List
