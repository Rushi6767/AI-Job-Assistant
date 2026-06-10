"""
Vector store for storing and retrieving past applications using ChromaDB
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import json
from config import CHROMA_DIR, COLLECTION_NAME


class VectorStore:
    """Manages vector storage for past applications"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Job applications history"}
        )
    
    def add_application(self, app_id: str, job_title: str, company: str, 
                       resume: str, cover_letter: str, metadata: Dict):
        """Store an application in the vector database"""
        try:
            document = f"Job: {job_title} at {company}\n\nResume:\n{resume}\n\nCover Letter:\n{cover_letter}"
            
            self.collection.add(
                documents=[document],
                ids=[app_id],
                metadatas=[{
                    "job_title": job_title,
                    "company": company,
                    **metadata
                }]
            )
            return True
        except Exception as e:
            print(f"Error adding to vector store: {e}")
            return False
    
    def search_similar_applications(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for similar past applications"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results['documents']:
                return [{
                    'document': doc,
                    'metadata': meta
                } for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
            return []
        
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def get_successful_applications(self) -> List[Dict]:
        """Retrieve all successful past applications"""
        try:
            results = self.collection.get()
            return results
        except Exception as e:
            print(f"Error retrieving applications: {e}")
            return []


# Singleton instance
vector_store = VectorStore()

