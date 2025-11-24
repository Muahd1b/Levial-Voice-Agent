Business & Productivity for Levial
Date: November 24, 2025 Topic: Calendar/Task management via MCP and Email drafting/summarization.

1. Executive Summary
   Calendar & Tasks: Use MCP Servers for both Google Calendar and Todoist. This allows the LLM to naturally query and manipulate schedule/tasks.
   Orchestration: Implement a "Daily Planner" agent that can read from Calendar and write to Todoist (e.g., "Block time for deep work").
   Email:
   Reading: Use imaplib for broad compatibility or simplegmail for a cleaner Gmail-specific experience.
   Summarization: Run a local Llama 3.2 model via Ollama and LangChain. Use "Map-Reduce" chains for long threads.
   Drafting: Use the Gmail API (users.drafts.create) to create drafts for user review. Never send automatically.
2. Calendar & Task Management (MCP)
   Google Calendar MCP
   Architecture: A local Python MCP server.
   Tools:
   list_events(start_date, end_date)
   create_event(summary, start_time, end_time)
   find_free_slots(duration_minutes)
   Auth: OAuth 2.0 "Desktop App" flow. Credentials stored locally (credentials.json).
   Todoist MCP
   Architecture: A local Python MCP server.
   Tools:
   add_task(content, due_date, project_id)
   get_tasks(filter)
   Auth: API Token (easier than OAuth for personal use).
   Linking Strategy
   Workflow: "Plan my day"
   Agent calls Calendar.list_events() to see hard commitments.
   Agent calls Todoist.get_tasks(filter="today") to see to-dos.
   Agent proposes a schedule: "You have a gap at 2 PM. Shall I block it for 'Write Report'?"
   If yes, Agent calls Calendar.create_event(summary="Focus: Write Report", ...)
3. Email Workflow (Local & Private)
   Accessing Emails
   Protocol: IMAP is universal.
   Library: imaplib (built-in) or imap_tools (easier API).
   Privacy: All processing happens locally. No email data leaves the machine.
   Summarization Pipeline
   Fetch: Get unread emails from the last 24 hours.
   Clean: Strip HTML tags using BeautifulSoup.
   Summarize:
   Short (<4k tokens): "Stuff" chain (Direct prompt).
   Long (>4k tokens): "Map-Reduce" chain (Summarize chunks, then summarize summaries).
   Model: Llama 3.2 (3B) is sufficient for summarization and fast on local hardware.
   Drafting
   Tool: create_draft(to, subject, body)
   Safety: The agent only creates drafts. The user must hit "Send" in their email client.
4. Recommended Stack
   Calendar: google-api-python-client, mcp (Python SDK).
   Tasks: todoist-api-python, mcp.
   Email: imap_tools, beautifulsoup4.
   AI/Logic: langchain, langchain-ollama.
5. Implementation Plan
   Auth Setup: Generate Google OAuth credentials and Todoist API token.
   MCP Servers: Create mcp-server-calendar and mcp-server-todoist.
   Email Tool: Create a standalone Python script email_manager.py for fetching/summarizing.
   Integration: Add these tools to the Levial Orchestrator.
