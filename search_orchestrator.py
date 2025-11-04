#!/usr/bin/env python3
"""
SearchOrchestrator - Unified Search Interface

Provides unified access to all search layers in Destiny framework:
- Elasticsearch: full-text search, aggregations, time-series
- Qdrant: semantic/vector search
- PostgreSQL: structured queries, metadata
- Neo4j: graph queries, relationships

Usage:
    orchestrator = SearchOrchestrator()
    
    # Full-text search
    results = orchestrator.full_text_search("revenue trends 2020")
    
    # Semantic search
    results = orchestrator.semantic_search("sustainability initiatives")
    
    # Hybrid search (combines ES + Qdrant)
    results = orchestrator.hybrid_search("debt analysis", sources=['es', 'qdrant'])
"""
import json
import subprocess
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, asdict
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor


@dataclass
class SearchResult:
    """Unified search result format"""
    source: str  # 'elasticsearch', 'qdrant', 'postgres', 'neo4j'
    score: float
    content: str
    metadata: Dict[str, Any]
    id: str
    timestamp: Optional[str] = None


class SearchOrchestrator:
    """
    Unified search interface across all Destiny data layers.
    
    Orchestrates queries across Elasticsearch, Qdrant, PostgreSQL, and Neo4j,
    providing a consistent API for all search operations.
    """
    
    def __init__(
        self,
        es_url: str = "http://localhost:9200",
        es_user: str = "elastic",
        es_password: str = "changeme123",
        qdrant_url: str = "http://localhost:6333",
        postgres_conn: str = "dbname=destiny_team user=user password=password host=localhost port=5432",
        neo4j_container: str = "sms-neo4j",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password",
        lmstudio_url: str = "http://localhost:1234/v1",
    ):
        """Initialize SearchOrchestrator with connection parameters."""
        self.es_url = es_url
        self.es_user = es_user
        self.es_password = es_password
        self.qdrant_url = qdrant_url
        self.postgres_conn = postgres_conn
        self.neo4j_container = neo4j_container
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.lmstudio_url = lmstudio_url
    
    # ========================================================================
    # ELASTICSEARCH METHODS
    # ========================================================================
    
    def _log_document_access(
        self,
        es_doc_id: str,
        accessed_by: str,
        query_used: str,
        access_purpose: str = "search",
        results_count: int = 0,
        response_time_ms: float = 0.0
    ):
        """Log document access to PostgreSQL for audit trail"""
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO es_document_usage_log 
                (es_doc_id, accessed_by, query_used, access_purpose, results_count, response_time_ms)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (es_doc_id, accessed_by, query_used, access_purpose, results_count, response_time_ms))
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            # Don't fail search if logging fails
            print(f"⚠️  Usage logging failed: {e}")
    
    def full_text_search(
        self,
        query: str,
        index: str = "osint_reports_pdf",
        size: int = 10,
        highlight: bool = True,
        filters: Optional[Dict[str, Any]] = None,
        accessed_by: str = "system",
    ) -> List[SearchResult]:
        """
        Full-text search in Elasticsearch.
        
        Args:
            query: Search query string
            index: Elasticsearch index name
            size: Number of results to return
            highlight: Enable highlighting of matched terms
            filters: Optional filters (e.g., {"issuer": "Grupa Azoty"})
            accessed_by: Agent/user name for audit trail
            
        Returns:
            List of SearchResult objects
        """
        import time
        start_time = time.time()
        
        try:
            # Build ES query
            es_query = {
                "query": {
                    "bool": {
                        "must": [
                            {"multi_match": {
                                "query": query,
                                "fields": ["content^2", "filename", "issuer"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }}
                        ]
                    }
                },
                "size": size,
                "_source": ["issuer", "report_url", "filename", "file_size", "downloaded_at", "content_length"]
            }
            
            # Add filters
            if filters:
                filter_clauses = []
                for field, value in filters.items():
                    filter_clauses.append({"term": {field: value}})
                es_query["query"]["bool"]["filter"] = filter_clauses
            
            # Add highlighting
            if highlight:
                es_query["highlight"] = {
                    "fields": {"content": {"fragment_size": 150, "number_of_fragments": 3}},
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"]
                }
            
            # Execute search
            cmd = [
                "curl", "-s", "-u", f"{self.es_user}:{self.es_password}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(es_query),
                f"{self.es_url}/{index}/_search"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return []
            
            response = json.loads(result.stdout)
            hits = response.get("hits", {}).get("hits", [])
            
            # Convert to SearchResult objects
            results = []
            for hit in hits:
                source = hit.get("_source", {})
                highlight_text = ""
                if highlight and "highlight" in hit:
                    highlight_text = " ... ".join(hit["highlight"].get("content", []))
                
                content = highlight_text if highlight_text else source.get("filename", "")
                
                result = SearchResult(
                    source="elasticsearch",
                    score=hit.get("_score", 0.0),
                    content=content,
                    metadata=source,
                    id=hit.get("_id", ""),
                    timestamp=source.get("downloaded_at")
                )
                results.append(result)
                
                # Log access for audit trail
                response_time_ms = (time.time() - start_time) * 1000
                self._log_document_access(
                    es_doc_id=result.id,
                    accessed_by=accessed_by,
                    query_used=query,
                    access_purpose="full_text_search",
                    results_count=len(hits),
                    response_time_ms=response_time_ms
                )
            
            return results
            
        except Exception as e:
            print(f"❌ Elasticsearch search error: {e}")
            return []
    
    def aggregate_query(
        self,
        index: str = "osint_reports_pdf",
        agg_field: str = "issuer",
        agg_name: str = "by_issuer",
        agg_type: str = "terms",
        size: int = 10,
    ) -> Dict[str, Any]:
        """
        Execute aggregation query in Elasticsearch.
        
        Args:
            index: Index name
            agg_field: Field to aggregate on
            agg_name: Name for the aggregation
            agg_type: Aggregation type (terms, date_histogram, etc.)
            size: Number of buckets
            
        Returns:
            Aggregation results dictionary
        """
        try:
            es_query = {
                "size": 0,
                "aggs": {
                    agg_name: {
                        agg_type: {
                            "field": agg_field,
                            "size": size
                        }
                    }
                }
            }
            
            cmd = [
                "curl", "-s", "-u", f"{self.es_user}:{self.es_password}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(es_query),
                f"{self.es_url}/{index}/_search"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return {}
            
            response = json.loads(result.stdout)
            return response.get("aggregations", {})
            
        except Exception as e:
            print(f"❌ Elasticsearch aggregation error: {e}")
            return {}
    
    # ========================================================================
    # QDRANT METHODS
    # ========================================================================
    
    def semantic_search(
        self,
        query: str,
        collection: str = "destiny-team-framework-master",
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Semantic/vector search in Qdrant.
        
        Args:
            query: Search query (will be embedded)
            collection: Qdrant collection name
            limit: Number of results
            
        Returns:
            List of SearchResult objects
        """
        try:
            # Generate embedding for query
            embed_result = subprocess.run([
                'curl', '-s', '-X', 'POST', f"{self.lmstudio_url}/embeddings",
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "input": query,
                    "model": "text-embedding-intfloat-multilingual-e5-large-instruct"
                })
            ], capture_output=True, text=True, timeout=30)
            
            if embed_result.returncode != 0:
                return []
            
            embedding_response = json.loads(embed_result.stdout)
            embedding = embedding_response.get('data', [{}])[0].get('embedding')
            
            if not embedding:
                return []
            
            # Search in Qdrant
            search_query = {
                "vector": embedding,
                "limit": limit,
                "with_payload": True
            }
            
            search_result = subprocess.run([
                'curl', '-s', '-X', 'POST',
                f'{self.qdrant_url}/collections/{collection}/points/search',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(search_query)
            ], capture_output=True, text=True, timeout=30)
            
            if search_result.returncode != 0:
                return []
            
            response = json.loads(search_result.stdout)
            points = response.get('result', [])
            
            # Convert to SearchResult objects
            results = []
            for point in points:
                payload = point.get('payload', {})
                content = payload.get('content', payload.get('text', ''))[:500]
                
                results.append(SearchResult(
                    source="qdrant",
                    score=point.get('score', 0.0),
                    content=content,
                    metadata=payload,
                    id=str(point.get('id', '')),
                    timestamp=payload.get('timestamp')
                ))
            
            return results
            
        except Exception as e:
            print(f"❌ Qdrant search error: {e}")
            return []
    
    # ========================================================================
    # POSTGRESQL METHODS
    # ========================================================================
    
    def structured_query(
        self,
        sql: str,
        params: Optional[tuple] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute structured SQL query in PostgreSQL.
        
        Args:
            sql: SQL query string
            params: Optional query parameters
            
        Returns:
            List of result dictionaries
        """
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute(sql, params or ())
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            print(f"❌ PostgreSQL query error: {e}")
            return []
    
    def get_context_for_agent(
        self,
        agent_name: str,
        project_id: str = "destiny-team-framework-master",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get recent context for a specific agent from PostgreSQL.
        
        Args:
            agent_name: Agent name
            project_id: Project ID
            limit: Number of context items
            
        Returns:
            List of context dictionaries
        """
        sql = """
            SELECT context_key, context_value, updated_at, importance
            FROM agent_contexts
            WHERE agent_name = %s AND project_id = %s
            ORDER BY updated_at DESC
            LIMIT %s
        """
        return self.structured_query(sql, (agent_name, project_id, limit))
    
    # ========================================================================
    # NEO4J METHODS
    # ========================================================================
    
    def graph_query(
        self,
        cypher: str,
    ) -> List[Dict[str, Any]]:
        """
        Execute Cypher query in Neo4j.
        
        Args:
            cypher: Cypher query string
            
        Returns:
            List of result dictionaries (parsed from Neo4j output)
        """
        try:
            result = subprocess.run([
                'docker', 'exec', self.neo4j_container,
                'cypher-shell', '-u', self.neo4j_user, '-p', self.neo4j_password,
                '--format', 'plain',
                cypher
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return []
            
            # Parse Neo4j output (simplified)
            # Note: For production, use py2neo or neo4j Python driver
            lines = result.stdout.strip().split('\n')
            results = []
            
            for line in lines:
                if line and not line.startswith('+') and not line.startswith('|'):
                    results.append({"raw": line})
            
            return results
            
        except Exception as e:
            print(f"❌ Neo4j query error: {e}")
            return []
    
    def get_decision_chain(
        self,
        decision_keyword: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get decision chain from Neo4j knowledge graph.
        
        Args:
            decision_keyword: Keyword to search for in decisions
            limit: Number of decisions
            
        Returns:
            List of decision nodes
        """
        cypher = f"""
            MATCH (d:Decision)
            WHERE toLower(d.text) CONTAINS toLower('{decision_keyword}')
            RETURN d.text AS decision, d.timestamp AS timestamp, d.made_by AS made_by
            ORDER BY d.timestamp DESC
            LIMIT {limit}
        """
        return self.graph_query(cypher)
    
    # ========================================================================
    # HYBRID SEARCH
    # ========================================================================
    
    def hybrid_search(
        self,
        query: str,
        sources: List[Literal['es', 'qdrant', 'pg']] = ['es', 'qdrant'],
        es_index: str = "osint_reports_pdf",
        qdrant_collection: str = "destiny-team-framework-master",
        limit: int = 10,
        rerank: bool = True,
    ) -> List[SearchResult]:
        """
        Hybrid search combining multiple sources.
        
        Args:
            query: Search query
            sources: List of sources to query ('es', 'qdrant', 'pg')
            es_index: Elasticsearch index
            qdrant_collection: Qdrant collection
            limit: Results per source
            rerank: Re-rank combined results by score
            
        Returns:
            Combined and optionally re-ranked SearchResult list
        """
        all_results = []
        
        # Execute searches in parallel (conceptually)
        if 'es' in sources:
            es_results = self.full_text_search(query, index=es_index, size=limit)
            all_results.extend(es_results)
        
        if 'qdrant' in sources:
            qdrant_results = self.semantic_search(query, collection=qdrant_collection, limit=limit)
            all_results.extend(qdrant_results)
        
        if 'pg' in sources:
            # Search in PostgreSQL messages
            sql = """
                SELECT id, sender, content, timestamp, importance
                FROM messages
                WHERE content ILIKE %s
                ORDER BY importance DESC, timestamp DESC
                LIMIT %s
            """
            pg_results = self.structured_query(sql, (f"%{query}%", limit))
            
            for row in pg_results:
                all_results.append(SearchResult(
                    source="postgres",
                    score=row.get('importance', 0.5),
                    content=row.get('content', '')[:500],
                    metadata=dict(row),
                    id=row.get('id', ''),
                    timestamp=row.get('timestamp', '').isoformat() if row.get('timestamp') else None
                ))
        
        # Re-rank by score if requested
        if rerank and all_results:
            all_results.sort(key=lambda x: x.score, reverse=True)
        
        return all_results[:limit * len(sources)]
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def health_check(self) -> Dict[str, bool]:
        """
        Check health of all search backends.
        
        Returns:
            Dictionary with health status for each backend
        """
        health = {}
        
        # Elasticsearch
        try:
            result = subprocess.run([
                'curl', '-s', '-u', f"{self.es_user}:{self.es_password}",
                f"{self.es_url}/_cluster/health"
            ], capture_output=True, text=True, timeout=10)
            health['elasticsearch'] = result.returncode == 0
        except Exception:
            health['elasticsearch'] = False
        
        # Qdrant
        try:
            result = subprocess.run([
                'curl', '-s', f"{self.qdrant_url}/collections"
            ], capture_output=True, text=True, timeout=10)
            health['qdrant'] = result.returncode == 0
        except Exception:
            health['qdrant'] = False
        
        # PostgreSQL
        try:
            conn = psycopg2.connect(self.postgres_conn)
            conn.close()
            health['postgres'] = True
        except Exception:
            health['postgres'] = False
        
        # Neo4j
        try:
            result = subprocess.run([
                'docker', 'exec', self.neo4j_container,
                'cypher-shell', '-u', self.neo4j_user, '-p', self.neo4j_password,
                'RETURN 1'
            ], capture_output=True, text=True, timeout=10)
            health['neo4j'] = result.returncode == 0
        except Exception:
            health['neo4j'] = False
        
        return health
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics from all backends.
        
        Returns:
            Dictionary with counts and stats
        """
        stats = {}
        
        # Elasticsearch
        try:
            result = subprocess.run([
                'curl', '-s', '-u', f"{self.es_user}:{self.es_password}",
                f"{self.es_url}/osint_reports_pdf/_count"
            ], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                stats['elasticsearch_docs'] = data.get('count', 0)
        except Exception:
            stats['elasticsearch_docs'] = -1
        
        # Qdrant
        try:
            result = subprocess.run([
                'curl', '-s',
                f"{self.qdrant_url}/collections/destiny-team-framework-master"
            ], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                stats['qdrant_points'] = data.get('result', {}).get('points_count', 0)
        except Exception:
            stats['qdrant_points'] = -1
        
        # PostgreSQL
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM messages")
            stats['postgres_messages'] = cur.fetchone()[0]
            cur.close()
            conn.close()
        except Exception:
            stats['postgres_messages'] = -1
        
        return stats


def main():
    """Demo usage of SearchOrchestrator."""
    print("=" * 80)
    print("🔍 SearchOrchestrator - Demo")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Health check
    print("🏥 Health Check:")
    health = orchestrator.health_check()
    for backend, status in health.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {backend}")
    print()
    
    # Stats
    print("📊 Statistics:")
    stats = orchestrator.get_stats()
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    print()
    
    # Full-text search
    print("🔍 Full-text search (Elasticsearch):")
    query = "sprawozdanie finansowe"
    results = orchestrator.full_text_search(query, size=3)
    print(f"   Query: '{query}'")
    print(f"   Results: {len(results)}")
    for i, result in enumerate(results, 1):
        print(f"   {i}. [{result.score:.2f}] {result.metadata.get('filename', 'N/A')}")
    print()
    
    # Semantic search
    print("🧠 Semantic search (Qdrant):")
    query = "system architecture design"
    results = orchestrator.semantic_search(query, limit=3)
    print(f"   Query: '{query}'")
    print(f"   Results: {len(results)}")
    for i, result in enumerate(results, 1):
        print(f"   {i}. [{result.score:.2f}] {result.content[:80]}...")
    print()
    
    # Hybrid search
    print("🔄 Hybrid search (ES + Qdrant):")
    query = "financial analysis"
    results = orchestrator.hybrid_search(query, sources=['es', 'qdrant'], limit=5)
    print(f"   Query: '{query}'")
    print(f"   Results: {len(results)}")
    for i, result in enumerate(results, 1):
        print(f"   {i}. [{result.source}] [{result.score:.2f}] {result.content[:60]}...")
    print()
    
    print("=" * 80)
    print("✅ Demo completed")
    print("=" * 80)


if __name__ == "__main__":
    main()
