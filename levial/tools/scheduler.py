import logging
import datetime
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")

mcp = FastMCP("Scheduler")

@mcp.tool()
def backward_plan(goal: str, deadline: str, tasks: List[Dict[str, Any]]) -> str:
    """
    Generate a backward plan from a deadline.
    
    Args:
        goal: The main goal (e.g., "Pass Exam").
        deadline: ISO date string (YYYY-MM-DD).
        tasks: List of dicts with 'name', 'duration_days', 'dependencies' (list of names).
    """
    try:
        deadline_date = datetime.date.fromisoformat(deadline)
        
        # Simple topological sort or just reverse scheduling
        # For MVP, let's assume tasks are provided in dependency order or we just schedule backwards.
        # A real implementation would use networkx for DAG resolution.
        
        # Let's just schedule them backwards from deadline for now.
        current_date = deadline_date
        schedule = []
        
        # Reverse tasks to schedule last one first (if input is logical order)
        # Or just assume we need to fit them all.
        
        for task in reversed(tasks):
            duration = task.get('duration_days', 1)
            start_date = current_date - datetime.timedelta(days=duration)
            
            schedule.append({
                "task": task['name'],
                "start": start_date.isoformat(),
                "end": current_date.isoformat()
            })
            
            current_date = start_date
            
        # Check if start date is in the past
        today = datetime.date.today()
        if current_date < today:
            return f"Warning: Plan starts in the past ({current_date}). You are behind schedule!\n" + _format_schedule(schedule)
            
        return _format_schedule(schedule)
        
    except Exception as e:
        return f"Error generating plan: {str(e)}"

def _format_schedule(schedule: List[Dict[str, Any]]) -> str:
    # Sort by start date
    schedule.sort(key=lambda x: x['start'])
    result = "Backward Plan:\n"
    for item in schedule:
        result += f"- {item['start']} to {item['end']}: {item['task']}\n"
    return result

if __name__ == "__main__":
    mcp.run()
