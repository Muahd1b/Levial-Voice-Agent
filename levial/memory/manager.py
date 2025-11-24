import logging
import time
from typing import Dict, Any, List
from pathlib import Path

from .vector_store import VectorStore
from .user_profile import UserProfile

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, base_dir: Path):
        """
        Initialize the Memory Manager.
        
        Args:
            base_dir: Base directory for storing memory artifacts.
        """
        self.memory_dir = base_dir / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.vector_store = VectorStore(str(self.memory_dir / "chroma_db"))
        self.user_profile = UserProfile(str(self.memory_dir / "user_profile.json"))

    def add_interaction(self, role: str, content: str):
        """
        Add a conversation turn to episodic memory.
        """
        timestamp = int(time.time())
        metadata = {
            "role": role,
            "timestamp": timestamp,
            "type": "conversation"
        }
        # Use a simple ID strategy for now
        mem_id = f"{timestamp}_{role}"
        self.vector_store.add_memory(content, metadata, mem_id)

    def get_relevant_context(self, query: str) -> str:
        """
        Retrieve relevant context from both Vector Store and User Profile.
        """
        # 1. Get explicit profile data
        profile = self.user_profile.get_profile()
        profile_str = f"User Profile: {profile}"
        
        # 2. Get episodic memories
        memories = self.vector_store.search_memory(query, n_results=3)
        memory_str = ""
        if memories:
            memory_str = "\nRelevant Past Conversations:\n"
            for mem in memories:
                memory_str += f"- {mem['metadata'].get('role', 'unknown')}: {mem['text']}\n"
        
        return f"{profile_str}\n{memory_str}"
