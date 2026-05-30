from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ChromaService:
    """
    Service for interacting with ChromaDB vector database.
    Note: This is a mock implementation. 
    Real implementation requires chromadb package.
    """

    def __init__(self):
        self.collections = {}
        self.initialized = False

    async def initialize(self):
        """Initialize ChromaDB connection."""
        try:
            # In production: import chromadb; client = chromadb.HttpClient(host="chromadb", port=8000)
            self.initialized = True
            self.collections = {
                "disaster_knowledge": {
                    "id": "disaster_knowledge",
                    "documents": [],
                    "embeddings": [],
                }
            }
            logger.info("ChromaDB service initialized")
        except Exception as e:
            logger.error(f"ChromaDB initialization failed: {e}")
            self.initialized = False

    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> bool:
        """
        Add documents to a collection.
        """
        try:
            if collection_name not in self.collections:
                self.collections[collection_name] = {
                    "id": collection_name,
                    "documents": [],
                    "embeddings": [],
                    "metadatas": [],
                }

            collection = self.collections[collection_name]
            
            for i, doc in enumerate(documents):
                doc_id = ids[i] if ids else f"doc-{len(collection['documents'])}"
                metadata = metadatas[i] if metadatas else {}
                
                collection["documents"].append({
                    "id": doc_id,
                    "text": doc,
                    "metadata": metadata,
                })

            logger.info(f"Added {len(documents)} documents to {collection_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False

    async def search(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        Returns list of {id, text, metadata, distance}.
        """
        try:
            if collection_name not in self.collections:
                return []

            collection = self.collections[collection_name]
            documents = collection.get("documents", [])

            # Mock search - return documents with simulated relevance
            results = []
            for doc in documents[:n_results]:
                # Simple keyword matching for mock
                relevance = 0.5
                if any(word in doc["text"].lower() for word in query.lower().split()):
                    relevance = 0.9

                results.append({
                    "id": doc["id"],
                    "text": doc["text"],
                    "metadata": doc.get("metadata", {}),
                    "distance": 1 - relevance,
                })

            # Sort by relevance (lower distance = more relevant)
            results.sort(key=lambda x: x["distance"])

            return results[:n_results]

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""
        try:
            if collection_name in self.collections:
                del self.collections[collection_name]
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return False

    async def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a collection."""
        if collection_name not in self.collections:
            return None

        collection = self.collections[collection_name]
        return {
            "id": collection["id"],
            "count": len(collection.get("documents", [])),
        }


chroma_service = ChromaService()
