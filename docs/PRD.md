Product Requirements Document (PRD)

Product: Local Voice Chat Agent
Owner: Muahdib
Version: v2.0 (Expanded Orchestration & Domain Support)

---

1. Executive Summary

---

Vision

- Deliver a fully local, privacy-preserving voice assistant that runs entirely on a personal machine.
- Core loop: microphone → Whisper ASR → Ollama LLM (mistral:latest as default) “thinking” → Piper TTS → speakers.
- **New in v2.0:** Evolves from a simple chat loop to a capable **Agent** using the **Model Context Protocol (MCP)** to interact with the world (Calendar, Email, Web, Simulators).
- **New in v2.0:** Implements **Hybrid Memory** (Vector + Graph/Profile) for long-term personalization.
- Everything is driven by a configuration layer so the assistant’s behavior is data-driven rather than code-driven.

Success Criteria

- Natural voice chat with ≤ 2 s perceived latency for short utterances on “balanced” profile hardware.
- **Tool Use:** Successfully executes complex tasks (e.g., "Schedule a meeting", "Research this topic") via MCP.
- **Personalization:** Remembers user preferences and facts across sessions.
- **Domain Mastery:** Provides specialized support for Aviation, Education, and Productivity.

---

2. Goals & Non-Goals

---

2.1 Primary Goals (Phase 2)

- **Orchestration:** Implement a robust state machine that supports "Thinking -> Tool Call -> Observing -> Speaking".
- **Connectivity:** Use MCP to connect to local and remote tools standardly.
- **Memory:** Persist user context beyond a single session.
- **Domain Support:** Ship specialized modules for: - **Productivity:** Calendar, Tasks, Email. - **Research:** Deep web research and report writing. - **Aviation:** Weather, NOTAMs, and Flight Sim integration. - **Education:** Study scheduling and Flashcard generation.

  2.2 Strategic Goals

- Keep the architecture modular: ASR, wake word, LLM, TTS, memory, and config can evolve independently.
- Maintain "Local-First" privacy: No data leaves the device unless explicitly requested (e.g., sending an email).

  2.3 Out of Scope (for now)

- Multi-user support (voice fingerprinting).
- Home Automation (Home Assistant integration) - planned for Phase 3.
- GUI - Voice remains the primary interface.

---

3. Product Scope

---

In Scope (v2.0)

- **Core Voice Loop:** Wake word -> ASR -> LLM -> TTS.
- **Web Interface:** Visual frontend for interaction and status monitoring.
- **MCP Client:** Dynamic discovery and execution of tools.
- **Memory System:** ChromaDB (Vector) + JSON Profile (Structured).
- **Domain Modules:**
  - **Business:** Google Calendar (OAuth), Todoist, Local Email (IMAP/Drafting).
  - **Research:** Planner-Executor agent for web research.
  - **Aviation:** CheckWX API, X-Plane UDP Monitor.
  - **Education:** Backward Planning Scheduler, Anki Deck Generator.

Explicitly Out of Scope

- Server-side inference (Cloud LLMs).
- Mobile App companion.

---

4. Target User & Use Cases

---

Primary Persona

- A single power user (Jonas) on their laptop/desktop who values privacy, aviation, and productivity.

Core Use Cases

- **"Plan my day":** Check calendar, weather, and tasks to propose a schedule.
- **"Research X":** Conduct deep research on a topic and generate a markdown report.
- **"Flight Instructor":** Quiz on aviation knowledge or monitor a flight sim session.
- **"Study Buddy":** Generate flashcards from notes and schedule study sessions.

---

5. Experience Overview

---

5.1 Assistant States

- IDLE – waiting for wake word.
- LISTENING – capturing utterance.
- THINKING – LLM processing.
- **EXECUTING** – Calling an MCP tool (e.g., searching web).
- SPEAKING – TTS playback.

  5.2 Flows

- **Tool Use:** User: "What's the weather?" -> THINKING -> EXECUTING (Call Weather Tool) -> THINKING (Synthesize answer) -> SPEAKING.
- **Visual Feedback:** Web UI shows real-time state (Listening, Thinking, Speaking) and conversation history.

---

6. System Architecture

---

Component Overview

- **Orchestrator:** Central state machine. Now handles MCP Tool execution loops.
- **MCP Client:** Connects to local servers (Calendar, Filesystem, Brave Search).
- **Memory Manager:**
  - **Short-term:** In-memory conversation history.
  - **Long-term (Episodic):** ChromaDB vector store.
  - **User Profile:** JSON file for explicit preferences.
- **Domain Agents:** Specialized logic (e.g., Research Planner) that may override the default chat loop for specific tasks.
- **Web Interface:** Next.js application for visual interaction and control.
- **API Server:** FastAPI server providing WebSocket connection for the Web UI.

---

7. Functional Requirements

---

FR-1 to FR-10 (Core Voice Loop) - _Unchanged_
FR-11 **MCP Support:** The system MUST be able to connect to standard MCP servers and expose their tools to the LLM.
FR-12 **Long-term Memory:** The system MUST store and retrieve past conversation snippets based on semantic relevance.
FR-13 **Calendar Integration:** The system MUST be able to read/write Google Calendar events via local OAuth.
FR-14 **Web Research:** The system MUST be able to search the web, scrape content, and synthesize a report.
FR-15 **Aviation Data:** The system MUST be able to fetch METAR/TAF/NOTAMs.
FR-16 **Sim Integration:** The system MUST be able to read telemetry from X-Plane via UDP.

---

8. Non-Functional Requirements

---

NFR-1 **Privacy:** All memory and tool execution (where possible) must be local.
NFR-2 **Latency:** Tool execution should not block the main thread; provide audio feedback ("Checking that...") if > 2s.
NFR-3 **Safety:** Destructive actions (Delete Event, Send Email) MUST require explicit voice confirmation.

---

9. Release Plan

---

Phase 1 – Core MVP (Completed)

- Basic Voice Loop.

Phase 2 – Expanded Orchestration (Current)

- **Step 1:** Core MCP Integration & Refactoring.
- **Step 2:** Memory System (ChromaDB + Profile).
- **Step 3:** Business Domain (Calendar/Email).
- **Step 4:** Research Domain.
- **Step 5:** Aviation & Education Domains.

---

10. Open Questions & Risks

---

1. **Context Window:** Will the local LLM (Mistral) handle the context of multiple tools and memory chunks? _Mitigation: Strict context management and summarization._
2. **Tool Latency:** How slow will Python-based MCP servers be? _Mitigation: Keep servers running or optimize startup._
