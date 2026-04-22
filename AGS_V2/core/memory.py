import chromadb
from chromadb.config import Settings
import os

class FailureMemoryEngine:
    """
    Handles the embedding and storage of failed executions to ensure the agent 
    never repeats the same hallucination/error twice forever.
    Uses 'all-MiniLM-L6-v2' implicitly via ChromaDB's default embedding function.
    """
    
    def __init__(self, persist_directory: str = "./memory_data"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize Persistent Client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Get or create the failures collection
        # default embedding function is all-MiniLM-L6-v2 for text
        self.collection = self.client.get_or_create_collection(
            name="failures",
            metadata={"hnsw:space": "cosine"}
        )
    
    def log_failure(self, task_id: str, error_message: str, stack_trace: str, resolution_note: str = ""):
        """
        Embed and save the error trace.
        """
        document = f"ERROR: {error_message}\n\nTRACE:\n{stack_trace}"
        
        # We use task_id + a hash/UUID as ID to easily index
        import uuid
        doc_id = f"{task_id}_{uuid.uuid4().hex[:8]}"
        
        self.collection.add(
            documents=[document],
            metadatas=[{"task_id": task_id, "resolution": resolution_note}],
            ids=[doc_id]
        )
    
    def check_for_similar_failure(self, current_error_message: str, current_stack_trace: str, threshold: float = 0.82) -> dict:
        """
        Query ChromaDB via cosine similarity to check if this exact error signature has been made before.
        Returns the resolution note if found, preventing the agent from looping.
        """
        query_text = f"ERROR: {current_error_message}\n\nTRACE:\n{current_stack_trace}"
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=1,
            # ChromaDB usually returns distances (1 - cosine_similarity for cosine space)
            # So a distance <= (1 - 0.82) is what we look for. 0.18 threshold.
        )
        
        if results['distances'] and results['distances'][0]:
            distance = results['distances'][0][0]
            similarity = 1.0 - distance
            
            if similarity >= threshold:
                metadata = results['metadatas'][0][0]
                return {
                    "matched": True,
                    "similarity": similarity,
                    "resolution_note": metadata.get("resolution", "No resolution previously recorded. Manually review.")
                }
                
        return {"matched": False}

# Singleton instance for the whole app
failure_memory = FailureMemoryEngine()
