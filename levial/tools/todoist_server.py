import os
import logging
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from todoist_api_python.api import TodoistAPI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todoist_server")

# Initialize FastMCP
mcp = FastMCP("Todoist")

def get_api():
    """Get the Todoist API client."""
    api_token = os.environ.get("TODOIST_API_TOKEN")
    if not api_token:
        raise ValueError("TODOIST_API_TOKEN environment variable not set.")
    return TodoistAPI(api_token)

@mcp.tool()
def get_tasks(filter: str = "today") -> str:
    """
    Get tasks from Todoist matching a filter (default: 'today').
    """
    try:
        api = get_api()
        tasks = api.get_tasks(filter=filter)
        
        if not tasks:
            return f"No tasks found for filter '{filter}'."
            
        result = f"Tasks ({filter}):\n"
        for task in tasks:
            result += f"- {task.content} (Due: {task.due.date if task.due else 'No date'})\n"
        return result
    except Exception as e:
        return f"Error fetching tasks: {str(e)}"

@mcp.tool()
def add_task(content: str, due_string: str = "today", priority: int = 1) -> str:
    """
    Add a new task to Todoist.
    Args:
        content: The task description.
        due_string: Natural language due date (e.g., 'tomorrow at 10am').
        priority: Priority level (1-4).
    """
    try:
        api = get_api()
        task = api.add_task(content=content, due_string=due_string, priority=priority)
        return f"Task created: {task.content} (ID: {task.id})"
    except Exception as e:
        return f"Error creating task: {str(e)}"

if __name__ == "__main__":
    mcp.run()
