import logging
import trafilatura
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web_scraper")

mcp = FastMCP("Web Scraper")

@mcp.tool()
def scrape_url(url: str) -> str:
    """
    Scrape the main text content from a URL using Trafilatura.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return f"Error: Could not fetch URL {url}"
            
        text = trafilatura.extract(downloaded)
        if not text:
            return f"Error: Could not extract text from {url}"
            
        return text
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

if __name__ == "__main__":
    mcp.run()
