Research Report: Personalization & Memory for Levial
Date: November 24, 2025 Topic: Architectural patterns for long-term memory and user profiling in a local-first AI assistant.

1. Executive Summary
   Hybrid Architecture is Key: The most robust solution for a local assistant like Levial is a hybrid memory architecture combining a Vector Database (for semantic similarity and episodic memory) and a Knowledge Graph (for structured facts and relationships).
   ChromaDB & SQLite are Top Local Contenders: For the vector store, ChromaDB is excellent for developer ease and Python integration, while SQLite with vector extensions offers a lightweight, single-file solution.
   Profile Implicitly, Verify Explicitly: Build user profiles primarily through implicit observation of interactions (topics discussed, tasks performed) but provide an explicit UI for the user to view, correct, and delete these inferred preferences.
   RAG needs "Smarts": Simple retrieval isn't enough. Implement Hybrid Search (keyword + vector) and Query Transformation (rewriting user queries) to improve context relevance.
   Proactive = Event-Driven: Proactive assistance requires an event loop that checks new data (e.g., weather, emails) against stored user interests (Memory) to trigger notifications.
   Privacy by Design: Keep all data local. Use local LLMs (Ollama) and ensure the memory store is just a file/directory on the user's disk, not a cloud service.
   Memory Lifecycle: Implement a "forgetting" mechanism or a relevance decay to prevent the memory from becoming cluttered and retrieving outdated info.
   Retrieval Agents: Move beyond simple RAG to "Retrieval Agents" that can actively decide what to search for and when, rather than just retrieving based on the immediate user prompt.
2. Foundations & Definitions
   Vector Database (Vector DB): A database that stores data as mathematical vectors (lists of numbers). It allows finding "semantically similar" items (e.g., "plane" is close to "aircraft").
   Technical: Uses algorithms like HNSW to perform Approximate Nearest Neighbor (ANN) search on high-dimensional embeddings.
   Knowledge Graph (KG): A structured database that stores data as entities (nodes) and relationships (edges). E.g.,

(Jonas)-[LIKES]->(Aviation)
.
Technical: Often implemented using graph databases like Neo4j or simply as structured triples in a relational DB. Good for reasoning and explicit facts.
Episodic Memory: Memory of specific past experiences or conversations. "We talked about the Cessna 172 last Tuesday."
Semantic Memory: General knowledge and facts, often distilled from experiences. "Jonas prefers high-wing aircraft."
RAG (Retrieval-Augmented Generation): The process of fetching relevant data from memory and feeding it to the LLM to ground its response. 3. Conceptual Map / Framework
The "Memory Wheel" Architecture:

Ingestion (The Senses):
User input (Voice/Text) -> Short-term Context.
Conversation completed -> Summarizer Agent extracts key facts & summary.
Storage (The Brain):
Episodic: Raw conversation logs & summaries -> Vector DB (ChromaDB).
Semantic: Extracted Facts (User Profile) -> Knowledge Graph (or Structured JSON/SQLite).
Retrieval (The Recall):
User Query -> Query Transformer (expands query).
Hybrid Search: Query Vector DB (semantic) + Knowledge Graph (exact facts).
Re-ranking: Filter results by relevance and recency.
Generation (The Speech):
LLM receives: System Prompt + Retrieved Context + User Query.
Generates response.
Proactive Trigger (The Intuition):
Background Event (e.g., Time, Webhook) -> Check Semantic Memory for relevance -> Trigger Notification. 4. Current State of the Field
State of the Art: Moving from simple "retrieve top-k chunks" to Agentic RAG, where the model actively queries its memory, critiques the results, and iterates.
Local-First: The rise of capable local LLMs (Llama 3, Mistral) and efficient local vector stores (Chroma, LanceDB) has made sophisticated local memory viable on consumer hardware.
Key Players:
Vector Stores: ChromaDB, LanceDB, Qdrant (local mode), SQLite-vec.
Frameworks: LangChain, LlamaIndex (heavy focus on RAG).
Graph: Neo4j (has a free community edition), MemGraph. 5. Approaches, Methods, and Tools
Memory Architecture Options
Approach Best For Pros Cons
Vector DB Only (ChromaDB) General conversation history, "fuzzy" recall. Easy to set up, handles unstructured text well. Bad at exact facts ("What is my wife's name?"), lacks reasoning.
Knowledge Graph Only Structured data, complex reasoning. Explicit relationships, high precision. Hard to build/maintain, brittle for casual conversation.
Hybrid (Vector + Graph) Levial's Goal. Best of both worlds. High recall (Vector) + High precision (Graph). Higher complexity to implement.
Simple JSON/SQLite MVP, strict user profiles. Zero overhead, human-readable. No semantic search, doesn't scale well.
User Profiling Strategy
Implicit: Analyze every conversation with a background "Profiler Agent" (a cheaper LLM call) to extract interests.
Example: User asks about "Cessna 172 specs" -> Agent tags interest: Aviation.
Explicit: Provide a profile.json or a UI where the user can see: "I think you like Aviation. Is this correct?" 6. Use Cases / Case Studies
MemGPT: An OS-like memory management system for LLMs. It manages a "working context" and swaps data in/out of long-term storage. Lesson: Managing the context window is crucial.
GraphRAG (Microsoft): Uses LLMs to build a knowledge graph from text, then uses the graph for retrieval. Lesson: Graphs provide better "global" understanding of a corpus than vector search alone.
Personal AI Assistants (Pi, Rewind): Rewind records everything (screen/audio) and makes it searchable. Lesson: Privacy and local-only processing are the biggest selling points. 7. Risks, Limitations, and Failure Modes
Context Poisoning: Retrieving too much or irrelevant old info can confuse the LLM, leading to hallucinations.
Stale Memories: "I'm flying to Paris" is relevant today, but not next month. Memory needs a "Time-to-Live" or decay factor.
Privacy Leaks: Even locally, if the assistant reads a sensitive file and stores it in clear text in the vector DB, it's a risk. Mitigation: Encrypt the DB storage.
Performance: Running an LLM + Vector Search + TTS locally can be slow. Mitigation: Use smaller embedding models (all-MiniLM) and efficient stores (SQLite/Chroma). 8. Actionable Recommendations for Levial
Phase 1: The Foundation (Immediate)
Storage: Implement ChromaDB (local persistence) for storing conversation history chunks.
Profile: Create a simple JSON-based User Profile (user_profile.json) for explicit facts (Name, Location, Core Interests).
Retrieval: Implement a basic RAG pipeline:
On user query, embed query.
Search ChromaDB for top-3 relevant past conversation chunks.
Load user_profile.json into System Prompt.
Generate response.
Phase 2: Intelligence (Next 1-2 Months)
Implicit Profiling: Add a post-conversation step where a small LLM (e.g., 8B param) summarizes the chat and updates the user_profile.json with new interests.
Hybrid Search: If the user asks a specific fact ("What is the V-speed for a C172?"), search a structured Aviation Knowledge Base (could be a simple SQLite table or JSON) in addition to the Vector DB.
Proactive Loop: Create a scheduled task (e.g., every morning) that:
Reads user_profile.json (Interest: Aviation).
Checks an external API (Weather/NOTAMs).
If a relevant alert is found, injects it into the "Start of Day" greeting.
Decision Criteria
Start with ChromaDB: It's Python-native, easy, and works well locally.
Start with JSON for Profile: Don't overengineer a Knowledge Graph yet. A structured JSON is a baby Knowledge Graph. 9. Assumptions & Uncertainties
Assumption: The user's local hardware can handle running an embedding model alongside the main LLM without significant latency.
Uncertainty: The quality of implicit profiling depends heavily on the LLM's reasoning capabilities. Smaller local models might miss nuances or hallucinate interests.
