"""
Master Orchestrator - Multi-Layer Memory System

Intelligently routes queries across 4 storage layers:
- Redis:      Hot cache (sub-ms)
- Qdrant:     Semantic search (10-50ms)
- PostgreSQL: Structured data (50-100ms)
- Neo4j:      Knowledge graph (100-500ms)

Plus LM Studio for local embeddings (FREE!)
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from postgres_context_store import PostgresContextStore
from neo4j_integration import Neo4jKnowledgeGraph, PostgresNeo4jBridge
from qdrant_integration import QdrantSemanticStore
from redis_cache import RedisCache
from lmstudio_embeddings import LMStudioEmbeddings


class MasterOrchestrator:
    """
    Master orchestrator for multi-layer memory system.
    
    Provides intelligent routing, caching, and result fusion
    across all 4 storage layers.
    """
    
    def __init__(
        self,
        # PostgreSQL
        postgres_conn: str,
        
        # Neo4j
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password",
        
        # Qdrant
        qdrant_url: str = "http://localhost:6333",
        
        # Redis
        redis_host: str = "localhost",
        redis_port: int = 6379,
        
        # LM Studio
        lmstudio_url: str = "http://localhost:1234/v1"
    ):
        """
        Initialize all storage layers.
        
        Args:
            postgres_conn: PostgreSQL connection string
            neo4j_uri: Neo4j Bolt URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            qdrant_url: Qdrant HTTP endpoint
            redis_host: Redis host
            redis_port: Redis port
            lmstudio_url: LM Studio API endpoint
        """
        print("🚀 Initializing Master Orchestrator...")
        print()
        
        # Layer 1: Hot Cache (Redis)
        print("  [1/4] Redis cache...")
        self.cache = RedisCache(host=redis_host, port=redis_port)
        
        # Layer 2: Structured Data (PostgreSQL)
        print("  [2/4] PostgreSQL store...")
        self.postgres = PostgresContextStore(postgres_conn)
        
        # Layer 3: Semantic Search (Qdrant + LM Studio)
        print("  [3/4] Qdrant + LM Studio...")
        self.qdrant = QdrantSemanticStore(
            qdrant_url=qdrant_url,
            lmstudio_url=lmstudio_url
        )
        
        # Layer 4: Knowledge Graph (Neo4j)
        print("  [4/4] Neo4j graph...")
        self.neo4j = Neo4jKnowledgeGraph(
            uri=neo4j_uri,
            user=neo4j_user,
            password=neo4j_password
        )
        
        # Bridge (auto-sync postgres -> neo4j)
        self.bridge = PostgresNeo4jBridge(self.postgres, self.neo4j)
        
        print()
        print("✅ All layers initialized!")
        print()
    
    # ==================== PROJECT MANAGEMENT ====================
    
    def create_project(
        self,
        project_id: str,
        name: str,
        description: str
    ) -> bool:
        """
        Create project across all layers.
        
        Returns:
            True if successful
        """
        try:
            # PostgreSQL
            self.postgres.create_project(project_id, name, description)
            
            # Neo4j
            self.neo4j.create_project_node(project_id, name, description)
            
            # Qdrant (create collection)
            self.qdrant.create_collection(project_id)
            
            # Redis (mark active)
            self.cache.mark_project_active(project_id)
            
            print(f"✅ Project '{name}' created across all layers")
            return True
            
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return False
    
    # ==================== MESSAGE STORAGE ====================
    
    def store_message(
        self,
        project_id: str,
        sender: str,
        recipient: Optional[str],
        message_type: str,
        content: str,
        importance: float = 0.5,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Store message across all layers.
        
        Returns:
            Message ID
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        tags = tags or []
        
        # Layer 1: Hot cache (instant access)
        self.cache.add_to_hot_memory(project_id, {
            "id": message_id,
            "sender": sender,
            "content": content,
            "timestamp": timestamp.isoformat()
        })
        
        # Layer 2: PostgreSQL (structured storage)
        from postgres_context_store import StoredMessage
        postgres_msg = StoredMessage(
            id=message_id,
            project_id=project_id,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            content=content,
            context={},
            timestamp=timestamp,
            importance=importance,
            tags=tags
        )
        self.postgres.store_message(postgres_msg)
        
        # Layer 3: Qdrant (semantic search)
        self.qdrant.store_message(
            project_id=project_id,
            message_id=message_id,
            content=content,
            sender=sender,
            timestamp=timestamp,
            message_type=message_type,
            importance=importance,
            tags=tags
        )
        
        # Layer 4: Neo4j (knowledge graph)
        self.neo4j.add_message_to_graph(
            message_id=message_id,
            project_id=project_id,
            sender=sender,
            content=content,
            timestamp=timestamp,
            message_type=message_type
        )
        
        return message_id
    
    # ==================== INTELLIGENT SEARCH ====================
    
    def search(
        self,
        project_id: str,
        query: str,
        search_type: str = "hybrid",  # hot, semantic, keyword, graph, hybrid
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Intelligent multi-layer search.
        
        Args:
            project_id: Project ID
            query: Search query
            search_type: Type of search
                - hot: Redis hot memory only (fastest)
                - semantic: Qdrant semantic search
                - keyword: PostgreSQL keyword search
                - graph: Neo4j graph traversal
                - hybrid: All layers (best results)
            limit: Max results
            
        Returns:
            Ranked results from appropriate layer(s)
        """
        # Check cache first
        cached = self.cache.get_cached_search(query, project_id)
        if cached:
            print("  ⚡ Cache hit!")
            return cached[:limit]
        
        results = []
        
        if search_type == "hot":
            # Layer 1: Hot memory (Redis)
            results = self._search_hot(project_id, query)
            
        elif search_type == "semantic":
            # Layer 3: Semantic search (Qdrant)
            results = self._search_semantic(project_id, query, limit)
            
        elif search_type == "keyword":
            # Layer 2: Keyword search (PostgreSQL)
            results = self._search_keyword(project_id, query, limit)
            
        elif search_type == "graph":
            # Layer 4: Graph traversal (Neo4j)
            results = self._search_graph(project_id, query)
            
        elif search_type == "hybrid":
            # ALL LAYERS: Hybrid search
            results = self._search_hybrid(project_id, query, limit)
        
        # Cache results
        self.cache.cache_search_results(query, project_id, results, ttl=300)
        
        return results
    
    def _search_hot(
        self,
        project_id: str,
        query: str
    ) -> List[Dict[str, Any]]:
        """Search hot memory (recent messages)"""
        hot_messages = self.cache.get_hot_memory(project_id)
        
        # Simple keyword filter
        query_lower = query.lower()
        return [
            msg for msg in hot_messages
            if query_lower in msg.get('content', '').lower()
        ]
    
    def _search_semantic(
        self,
        project_id: str,
        query: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Semantic search via Qdrant"""
        results = self.qdrant.search(
            project_id=project_id,
            query=query,
            limit=limit,
            score_threshold=0.6
        )
        
        # Add source
        for r in results:
            r['source'] = 'qdrant'
            r['search_type'] = 'semantic'
        
        return results
    
    def _search_keyword(
        self,
        project_id: str,
        query: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Keyword search via PostgreSQL"""
        results = self.postgres.search_messages(
            project_id=project_id,
            search_query=query,
            limit=limit
        )
        
        # Format results
        formatted = []
        for msg in results:
            formatted.append({
                "id": msg.id,
                "content": msg.content,
                "sender": msg.sender,
                "timestamp": msg.timestamp.isoformat(),
                "importance": msg.importance,
                "source": "postgres",
                "search_type": "keyword"
            })
        
        return formatted
    
    def _search_graph(
        self,
        project_id: str,
        query: str
    ) -> List[Dict[str, Any]]:
        """Graph-based search via Neo4j"""
        # Use Neo4j's "why" question answering
        result = self.neo4j.why_question(query, project_id)
        
        if "error" in result:
            return []
        
        # Format as list
        return [{
            "concept": result.get("concept"),
            "decision_chain": result.get("decision_chain"),
            "related_concepts": result.get("related_concepts"),
            "source": "neo4j",
            "search_type": "graph"
        }]
    
    def _search_hybrid(
        self,
        project_id: str,
        query: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search: combine semantic + keyword + graph.
        
        Uses Reciprocal Rank Fusion (RRF) for merging.
        """
        # Search all layers in parallel (conceptually)
        semantic_results = self._search_semantic(project_id, query, limit * 2)
        keyword_results = self._search_keyword(project_id, query, limit * 2)
        
        # Merge using RRF
        merged = self._reciprocal_rank_fusion(
            [semantic_results, keyword_results],
            k=60
        )
        
        return merged[:limit]
    
    def _reciprocal_rank_fusion(
        self,
        result_lists: List[List[Dict]],
        k: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Reciprocal Rank Fusion algorithm.
        
        Combines multiple ranked lists into one.
        Formula: RRF(d) = Σ(1 / (k + rank(d)))
        """
        # Track scores per document ID
        scores = {}
        docs = {}
        
        for result_list in result_lists:
            for rank, doc in enumerate(result_list, start=1):
                doc_id = doc.get('id', str(doc))
                
                # RRF score
                score = 1.0 / (k + rank)
                
                if doc_id in scores:
                    scores[doc_id] += score
                else:
                    scores[doc_id] = score
                    docs[doc_id] = doc
        
        # Sort by score
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        
        # Return sorted documents with RRF scores
        results = []
        for doc_id in sorted_ids:
            doc = docs[doc_id].copy()
            doc['rrf_score'] = scores[doc_id]
            results.append(doc)
        
        return results
    
    # ==================== ADVANCED QUERIES ====================
    
    def why_question(
        self,
        project_id: str,
        question: str
    ) -> Dict[str, Any]:
        """
        Answer "why" questions using graph traversal.
        
        Example: "Why did we choose PostgreSQL?"
        """
        return self.neo4j.why_question(question, project_id)
    
    def find_related(
        self,
        project_id: str,
        concept: str,
        max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """Find concepts related to a given concept"""
        return self.neo4j.find_related_concepts(concept, max_depth)
    
    def get_decision_chain(
        self,
        project_id: str,
        concept: str
    ) -> List[Dict[str, Any]]:
        """Get full decision chain for a concept"""
        return self.neo4j.find_decision_chain(concept, project_id)
    
    # ==================== STATISTICS ====================
    
    def get_system_status(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "cache": {
                "stats": self.cache.get_cache_stats(),
                "hot_memory_size": len(self.cache.get_hot_memory(project_id))
            },
            "postgres": self.postgres.get_project_statistics(project_id),
            "qdrant": self.qdrant.get_collection_stats(project_id),
            "neo4j": self.neo4j.get_project_statistics(project_id)
        }
    
    # ==================== CLEANUP ====================
    
    def close(self):
        """Close all connections"""
        print("Closing connections...")
        self.cache.close()
        self.postgres.close()
        self.neo4j.close()
        print("✅ All connections closed")


# ==================== EXAMPLE ====================

def example_usage():
    """Example of using the master orchestrator"""
    print("=" * 70)
    print("  🚀 MASTER ORCHESTRATOR - Full System Demo")
    print("=" * 70)
    print()
    
    # Initialize
    orchestrator = MasterOrchestrator(
        postgres_conn="dbname=destiny_team user=user password=password host=localhost port=5432",
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password",
        qdrant_url="http://localhost:6333",
        redis_host="localhost",
        redis_port=6379,
        lmstudio_url="http://localhost:1234/v1"
    )
    
    # Create project
    project_id = "demo-" + str(uuid.uuid4())[:8]
    orchestrator.create_project(
        project_id=project_id,
        name="E-commerce Platform",
        description="Building a scalable online store"
    )
    
    print("\n" + "="*70)
    print("  📨 Storing Messages Across All Layers")
    print("="*70)
    
    # Store messages
    messages = [
        ("Architect", "Wybraliśmy PostgreSQL dla ACID compliance"),
        ("Developer", "MongoDB odrzuciliśmy bo potrzebujemy transakcji"),
        ("Security", "OAuth 2.0 będzie używany do autentykacji"),
        ("DevOps", "Redis użyjemy do cache'owania sesji")
    ]
    
    for sender, content in messages:
        orchestrator.store_message(
            project_id=project_id,
            sender=sender,
            recipient=None,
            message_type="ANNOUNCEMENT",
            content=content,
            importance=0.8
        )
        print(f"  ✓ {sender}: {content[:50]}...")
    
    print("\n" + "="*70)
    print("  🔍 Hybrid Search (All Layers)")
    print("="*70)
    
    query = "Dlaczego wybraliśmy bazę danych?"
    print(f"\nQuery: {query}\n")
    
    results = orchestrator.search(
        project_id=project_id,
        query=query,
        search_type="hybrid",
        limit=5
    )
    
    print("Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result.get('source', 'unknown')}]")
        print(f"   Score: {result.get('rrf_score', result.get('score', 'N/A'))}")
        print(f"   Content: {result.get('content', 'N/A')[:80]}...")
    
    print("\n" + "="*70)
    print("  📊 System Status")
    print("="*70)
    
    status = orchestrator.get_system_status(project_id)
    print(f"\nRedis Cache:")
    print(f"  Used memory: {status['cache']['stats']['used_memory']}")
    print(f"  Hot memory messages: {status['cache']['hot_memory_size']}")
    
    print(f"\nPostgreSQL:")
    print(f"  Total messages: {status['postgres']['total_messages']}")
    
    print(f"\nQdrant:")
    print(f"  Vectors: {status['qdrant'].get('vectors_count', 'N/A')}")
    
    print(f"\nNeo4j:")
    print(f"  Total concepts: {status['neo4j'].get('total_concepts', 'N/A')}")
    
    print("\n" + "="*70)
    print("  ✅ Demo Complete!")
    print("="*70)
    
    orchestrator.close()


if __name__ == "__main__":
    example_usage()
