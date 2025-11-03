"""
Qdrant Vector Store Integration with LM Studio Embeddings

Combines Qdrant vector database with local LM Studio embeddings
for semantic search with ZERO external API costs.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter, 
    FieldCondition, MatchValue, SearchRequest
)
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from lmstudio_embeddings import LMStudioEmbeddings


class QdrantSemanticStore:
    """
    Semantic search using Qdrant + LM Studio.
    
    Stores message embeddings in Qdrant for fast semantic search.
    Uses local multilingual E5-large model (1024 dimensions).
    """
    
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        lmstudio_url: str = "http://localhost:1234/v1",
        collection_prefix: str = "destiny-team"
    ):
        """
        Initialize Qdrant semantic store.
        
        Args:
            qdrant_url: Qdrant server URL
            lmstudio_url: LM Studio server URL
            collection_prefix: Prefix for collection names
        """
        self.qdrant = QdrantClient(url=qdrant_url)
        self.embedder = LMStudioEmbeddings(base_url=lmstudio_url)
        self.collection_prefix = collection_prefix
        self.dimension = 1024  # E5-large dimension
    
    # ==================== COLLECTION MANAGEMENT ====================
    
    def create_collection(self, project_id: str) -> bool:
        """
        Create a Qdrant collection for a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if created successfully
        """
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            # Check if exists
            collections = self.qdrant.get_collections().collections
            if any(c.name == collection_name for c in collections):
                print(f"Collection {collection_name} already exists")
                return True
            
            # Create collection
            self.qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE
                )
            )
            
            print(f"✅ Created collection: {collection_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating collection: {e}")
            return False
    
    def delete_collection(self, project_id: str) -> bool:
        """Delete a project's collection"""
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            self.qdrant.delete_collection(collection_name)
            print(f"✅ Deleted collection: {collection_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting collection: {e}")
            return False
    
    # ==================== MESSAGE STORAGE ====================
    
    def store_message(
        self,
        project_id: str,
        message_id: str,
        content: str,
        sender: str,
        timestamp: datetime,
        message_type: str,
        importance: float = 0.5,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Store a message with its embedding in Qdrant.
        
        Args:
            project_id: Project identifier
            message_id: Unique message ID
            content: Message content
            sender: Agent name
            timestamp: When message was sent
            message_type: Type of message
            importance: Importance score (0-1)
            tags: Optional tags
            
        Returns:
            True if stored successfully
        """
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            # Generate embedding
            embedding = self.embedder.embed(content)
            
            # Create point
            point = PointStruct(
                id=message_id,
                vector=embedding,
                payload={
                    "content": content,
                    "sender": sender,
                    "timestamp": timestamp.isoformat(),
                    "message_type": message_type,
                    "importance": importance,
                    "tags": tags or [],
                    "project_id": project_id
                }
            )
            
            # Upsert to Qdrant
            self.qdrant.upsert(
                collection_name=collection_name,
                points=[point]
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Error storing message: {e}")
            return False
    
    def store_messages_batch(
        self,
        project_id: str,
        messages: List[Dict[str, Any]],
        batch_size: int = 10
    ) -> Dict[str, int]:
        """
        Store multiple messages in batches.
        
        Args:
            project_id: Project identifier
            messages: List of message dicts
            batch_size: Batch size for embedding generation
            
        Returns:
            Stats: stored, failed
        """
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        stats = {"stored": 0, "failed": 0}
        
        # Process in batches
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i + batch_size]
            
            try:
                # Generate embeddings for batch
                contents = [msg['content'] for msg in batch]
                embeddings = self.embedder.embed(contents)
                
                # Create points
                points = []
                for msg, embedding in zip(batch, embeddings):
                    point = PointStruct(
                        id=msg['id'],
                        vector=embedding,
                        payload={
                            "content": msg['content'],
                            "sender": msg['sender'],
                            "timestamp": msg['timestamp'].isoformat(),
                            "message_type": msg.get('message_type', 'UNKNOWN'),
                            "importance": msg.get('importance', 0.5),
                            "tags": msg.get('tags', []),
                            "project_id": project_id
                        }
                    )
                    points.append(point)
                
                # Upsert batch
                self.qdrant.upsert(
                    collection_name=collection_name,
                    points=points
                )
                
                stats["stored"] += len(points)
                print(f"✅ Stored batch {i//batch_size + 1}: {len(points)} messages")
                
            except Exception as e:
                print(f"❌ Error in batch {i//batch_size + 1}: {e}")
                stats["failed"] += len(batch)
        
        return stats
    
    # ==================== SEMANTIC SEARCH ====================
    
    def search(
        self,
        project_id: str,
        query: str,
        limit: int = 20,
        score_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for messages.
        
        Args:
            project_id: Project identifier
            query: Search query (natural language)
            limit: Max results
            score_threshold: Minimum similarity score
            filters: Optional filters (sender, message_type, etc.)
            
        Returns:
            List of matching messages with scores
        """
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed(query)
            
            # Build filter
            filter_conditions = []
            if filters:
                for key, value in filters.items():
                    filter_conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
            
            query_filter = Filter(must=filter_conditions) if filter_conditions else None
            
            # Search
            results = self.qdrant.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter
            )
            
            # Format results
            formatted = []
            for result in results:
                formatted.append({
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload.get("content"),
                    "sender": result.payload.get("sender"),
                    "timestamp": result.payload.get("timestamp"),
                    "message_type": result.payload.get("message_type"),
                    "importance": result.payload.get("importance"),
                    "tags": result.payload.get("tags", [])
                })
            
            return formatted
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def find_similar(
        self,
        project_id: str,
        message_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find messages similar to a given message.
        
        Args:
            project_id: Project identifier
            message_id: Reference message ID
            limit: Max results
            
        Returns:
            List of similar messages
        """
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            # Get reference message
            result = self.qdrant.retrieve(
                collection_name=collection_name,
                ids=[message_id]
            )
            
            if not result:
                return []
            
            # Get its vector
            vector = result[0].vector
            
            # Search for similar
            results = self.qdrant.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit + 1  # +1 because it will include itself
            )
            
            # Format and exclude self
            formatted = []
            for r in results:
                if r.id != message_id:
                    formatted.append({
                        "id": r.id,
                        "score": r.score,
                        "content": r.payload.get("content"),
                        "sender": r.payload.get("sender")
                    })
            
            return formatted[:limit]
            
        except Exception as e:
            print(f"❌ Error finding similar: {e}")
            return []
    
    # ==================== STATISTICS ====================
    
    def get_collection_stats(self, project_id: str) -> Dict[str, Any]:
        """Get statistics for a collection"""
        collection_name = f"{self.collection_prefix}-{project_id}"
        
        try:
            info = self.qdrant.get_collection(collection_name)
            
            return {
                "collection_name": collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== UTILITIES ====================
    
    def test_connection(self) -> bool:
        """Test if Qdrant and LM Studio are reachable"""
        print("Testing connections...")
        
        # Test LM Studio
        print("\n1. LM Studio Embeddings:")
        lm_ok = self.embedder.test_connection()
        
        # Test Qdrant
        print("\n2. Qdrant Vector Store:")
        try:
            collections = self.qdrant.get_collections()
            print(f"✅ Qdrant connected!")
            print(f"Existing collections: {len(collections.collections)}")
            qdrant_ok = True
        except Exception as e:
            print(f"❌ Qdrant error: {e}")
            qdrant_ok = False
        
        return lm_ok and qdrant_ok


# ==================== EXAMPLE ====================

def example_usage():
    """Example of using Qdrant semantic store"""
    print("=" * 70)
    print("  Qdrant + LM Studio Semantic Search Example")
    print("=" * 70)
    print()
    
    # Initialize
    store = QdrantSemanticStore()
    
    # Test connections
    if not store.test_connection():
        print("\n❌ Connection test failed!")
        return
    
    print("\n" + "=" * 70)
    print("  ✅ Connections OK!")
    print("=" * 70)
    
    # Create collection
    project_id = "test-project-" + str(uuid.uuid4())[:8]
    print(f"\nCreating collection for project: {project_id}")
    store.create_collection(project_id)
    
    # Store sample messages
    print("\nStoring sample messages...")
    messages = [
        {
            "id": str(uuid.uuid4()),
            "content": "Wybraliśmy PostgreSQL dla ACID compliance",
            "sender": "Architect",
            "timestamp": datetime.now(),
            "importance": 0.9
        },
        {
            "id": str(uuid.uuid4()),
            "content": "MongoDB odrzuciliśmy bo potrzebujemy transakcji",
            "sender": "Developer",
            "timestamp": datetime.now(),
            "importance": 0.7
        },
        {
            "id": str(uuid.uuid4()),
            "content": "Redis użyjemy do cache'owania sesji",
            "sender": "DevOps",
            "timestamp": datetime.now(),
            "importance": 0.6
        }
    ]
    
    stats = store.store_messages_batch(project_id, messages)
    print(f"\n✅ Stored {stats['stored']} messages")
    
    # Semantic search
    print("\n" + "=" * 70)
    print("  Semantic Search Test")
    print("=" * 70)
    
    query = "Dlaczego wybraliśmy bazę danych?"
    print(f"\nQuery: {query}")
    print("\nResults:")
    
    results = store.search(project_id, query, limit=5, score_threshold=0.5)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Sender: {result['sender']}")
        print(f"   Content: {result['content']}")
    
    print("\n" + "=" * 70)
    print("  ✅ Example Complete!")
    print("=" * 70)


if __name__ == "__main__":
    example_usage()
