import logging
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persistence_path: str):
        """
        Initialize the Vector Store using ChromaDB.
        
        Args:
            persistence_path: Path to the directory where ChromaDB will store data.
        """
        self.client = chromadb.PersistentClient(path=persistence_path)
        
        # Create or get the collection for conversation history
        self.collection = self.client.get_or_create_collection(
            name="conversation_history",
            metadata={"hnsw:space": "cosine"}
        )

    def add_memory(self, text: str, metadata: Dict[str, Any], id: str):
        """
        Add a text chunk to the vector store.
        """
        try:
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[id]
            )
            logger.info(f"Added memory to vector store: {id}")
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")

    def search_memory(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant memories.
        
        Returns:
            List of dictionaries containing 'text' and 'metadata'.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            memories = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    memories.append({
                        "text": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return memories
            
        except Exception as e:
            logger.error(f"Failed to search memory: {e}")
            return []
