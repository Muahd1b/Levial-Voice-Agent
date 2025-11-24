import logging
import json
from typing import List, Dict, Any
from ..llm import OllamaLLM
from ..mcp_client import MCPClient

logger = logging.getLogger(__name__)

class ResearcherAgent:
    def __init__(self, llm: OllamaLLM, mcp_client: MCPClient):
        self.llm = llm
        self.mcp_client = mcp_client

    async def research(self, topic: str) -> str:
        """
        Conduct deep research on a topic.
        """
        logger.info(f"Starting research on: {topic}")
        
        # 1. Plan
        plan_prompt = (
            f"You are a Research Planner. The user wants to research: '{topic}'.\n"
            "Generate a list of 3 specific search queries to investigate this topic.\n"
            "Output ONLY a JSON list of strings, e.g. [\"query 1\", \"query 2\", \"query 3\"]."
        )
        plan_response = self.llm.query(plan_prompt)
        try:
            queries = json.loads(plan_response)
            if not isinstance(queries, list):
                raise ValueError("Output is not a list")
        except Exception as e:
            logger.error(f"Failed to parse plan: {e}")
            queries = [topic] # Fallback

        # 2. Execute (Search & Scrape)
        aggregated_info = ""
        for query in queries:
            logger.info(f"Executing query: {query}")
            # Call Brave Search (assuming it's available as 'brave_search' tool or similar)
            # Note: Tool names depend on the MCP server implementation. 
            # The official brave-search server exposes `brave_web_search`.
            try:
                search_results = await self.mcp_client.call_tool("brave-search", "brave_web_search", {"query": query, "count": 2})
                # Parse results (assuming JSON string or dict)
                # This part depends heavily on the specific MCP server output format.
                # For now, we append the raw result.
                aggregated_info += f"\n--- Search Results for '{query}' ---\n{search_results}\n"
                
                # Ideally, we would parse URLs and scrape them here using 'web_scraper' tool.
                # But for MVP, we might just rely on search snippets if scraping is too slow/complex to parse from here.
                # Let's try to scrape the first URL if possible? 
                # Parsing the search result to find URLs is tricky without knowing the exact schema.
                
            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")

        # 3. Write Report
        report_prompt = (
            f"You are a Research Writer. Write a concise markdown report on '{topic}' based on the following information:\n\n"
            f"{aggregated_info[:10000]}\n\n" # Truncate to avoid context overflow
            "Structure: Executive Summary, Key Findings, Conclusion."
        )
        report = self.llm.query(report_prompt)
        return report
