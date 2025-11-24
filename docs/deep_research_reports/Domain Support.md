Research Report: Domain Support - Research Assistant for Levial
Date: November 24, 2025 Topic: Architectural patterns for an Automated Research Assistant in a local-first AI agent.

1. Executive Summary
   Iterative over Linear: For deep research, an Iterative "Agentic" Workflow (Plan -> Execute -> Reflect -> Refine) is superior to a simple linear chain. It allows the agent to self-correct when search results are poor.
   Scraping Stack: Use Firecrawl (or a local equivalent like crawl4ai) for LLM-ready markdown extraction. If strictly local, Trafilatura is the best Python library for extracting main content without overhead.
   Citation is Lineage: Track citations by maintaining a Source Registry. Every fact extracted must carry a source_id. Use a "Map-Reduce" approach where the "Map" step extracts facts+sources, and the "Reduce" step synthesizes them while preserving the [source_id] tags.
   Context Management: Use Map-Reduce Summarization for reading many documents. Don't stuff 20 pages into the context. Summarize each page with a focus on the research question, then synthesize the summaries.
   Report Structure: Follow a standard academic or business report format: Executive Summary -> Key Findings -> Detailed Analysis -> References.
   Existing Models: GPT-Researcher (Planner-Executor) and Stanford STORM (Multi-perspective) are the gold standards. Levial should adopt a simplified GPT-Researcher pattern (Planner + Parallel Workers).
2. Foundations & Definitions
   Autonomous Agent: An AI system that can break a high-level goal ("Research X") into sub-tasks and execute them without human intervention.
   Map-Reduce: A pattern where a large task is split into smaller chunks ("Map"), processed in parallel, and then combined ("Reduce").
   Scraping vs. Parsing: Scraping is fetching the HTML (often needing a browser). Parsing is extracting the useful text from that HTML.
   Citation Graph: A data structure linking specific claims in the final text back to the original source URL and snippet.
3. Conceptual Map / Framework
   The "Research Loop" Architecture:

Planner Agent:
Input: User Topic ("Future of Electric Aviation").
Action: Generates a list of 3-5 specific research questions.
Execution Agents (Parallel Workers):
Input: One specific question.
Action:
Search: Query Brave Search.
Scrape: Visit top 3 URLs (using Trafilatura or Firecrawl).
Read: Summarize content relevant to the question.
Extract: Pull key facts with citations.
Writer Agent:
Input: Aggregated summaries and facts from all workers.
Action: Synthesizes a coherent report, ensuring [Source ID] tags are preserved.
Reviewer Agent (Optional):
Action: Checks for hallucinations or missing citations. Loops back to Planner if gaps are found. 4. Current State of the Field
GPT-Researcher: The most popular open-source implementation. Uses a "Planner" to generate sub-questions and "Execution Agents" to scrape/summarize. Highly effective.
Stanford STORM: Uses "simulated conversations" between agents to explore a topic from multiple angles before writing. Produces Wikipedia-style depth.
Local Tools: ScrapeGraphAI and Crawl4AI are emerging as local-first, LLM-friendly scraping pipelines. 5. Approaches, Methods, and Tools
Workflow Architecture
Approach Best For Pros Cons
Linear Chain Simple fact-checking. Fast, predictable, easy to debug. Can't handle dead ends or complex topics.
Iterative (ReAct) Complex problem solving. Adaptable, self-correcting. Can get stuck in loops, slower.
Planner-Executor Deep Research. Parallelizable, structured, comprehensive. More complex state management.
Local Scraping Stack
Trafilatura: Best for pure text extraction. Fast, Python-native, no browser required.
Playwright + BeautifulSoup: Needed for dynamic JS sites. Heavier but more robust.
Crawl4AI: A new tool specifically designed to output LLM-friendly markdown. 6. Risks, Limitations, and Failure Modes
Rabbit Holes: The agent keeps searching for obscure details. Mitigation: Set a strict "Max Iterations" or "Max Depth" limit.
Hallucinated Citations: The LLM invents a source. Mitigation: Force the LLM to use [Source ID] from a provided list, never generate URLs.
Context Overflow: Trying to read too many sites. Mitigation: Strict Map-Reduce. Summarize before aggregating. 7. Actionable Recommendations for Levial
Recommended Stack
Orchestrator: Levial's existing State Machine (expanded to support sub-loops).
Search: mcp-server-brave-search.
Scraping: Trafilatura (start simple, add Playwright later if needed).
LLM: Ollama (Mistral/Llama 3).
Implementation Steps
Build the "Read" Tool: Create a Python function (or MCP tool) that takes a URL, downloads it with Trafilatura, and returns clean Markdown.
Implement "Planner" Prompt: Create a system prompt that takes a topic and outputs a JSON list of research questions.
Implement the Loop:
User: "Research X".
Levial: Calls Planner -> Gets Questions.
Levial: Loops through Questions -> Search -> Read -> Summarize.
Levial: Aggregates Summaries -> Writes Report.
Citation Tracking: In the "Read" step, assign an ID to the URL (e.g., [1]). Instruct the Summarizer to append [1] to any fact it extracts. 8. Assumptions & Uncertainties
Assumption: Local LLMs (8B size) are capable enough to follow the strict "Planner" and "Summarizer" instructions without losing track of the task.
Uncertainty: Handling paywalls and anti-bot protections locally might be flaky without a commercial proxy service.
