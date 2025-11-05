"""
PostgreSQL Client with pgvector Support
Paweł Kowalski
2025-11-05
"""

import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class SearchResult:
    """Semantic search result"""
    document_id: str
    chunk_id: int
    content: str
    similarity: float
    metadata: Dict[str, Any]


class PostgresClient:
    """
    PostgreSQL client with pgvector for embeddings
    
    Features:
    - Store document embeddings
    - Semantic search
    - Task tracking
    - Performance metrics
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "destiny_analytical",
        user: str = "destiny",
        password: str = "destiny_dev_2024"
    ):
        """
        Initialize PostgreSQL client
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
        """
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            # Enable autocommit for better performance
            self.conn.autocommit = False
            print("✅ PostgreSQL connected")
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ PostgreSQL disconnected")
    
    def health_check(self) -> bool:
        """
        Check database health
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result[0] == 1
        except:
            return False
    
    def store_embedding(
        self,
        case_id: str,
        document_id: str,
        chunk_id: int,
        content: str,
        embedding: List[float],
        model_used: str,
        text_hash: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store document embedding
        
        Args:
            case_id: Case identifier
            document_id: Document identifier
            chunk_id: Chunk number
            content: Text content
            embedding: Embedding vector
            model_used: Model name
            text_hash: Content hash
            metadata: Optional metadata
            
        Returns:
            UUID of inserted record
        """
        query = """
        INSERT INTO document_embeddings 
        (case_id, document_id, chunk_id, content, embedding, model_used, text_hash, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (document_id, chunk_id) DO UPDATE
        SET embedding = EXCLUDED.embedding,
            content = EXCLUDED.content,
            model_used = EXCLUDED.model_used,
            metadata = EXCLUDED.metadata
        RETURNING id
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (
                case_id,
                document_id,
                chunk_id,
                content,
                embedding,
                model_used,
                text_hash,
                json.dumps(metadata) if metadata else None
            ))
            result = cur.fetchone()
            self.conn.commit()
            return str(result[0])
    
    def batch_store_embeddings(self, records: List[Dict[str, Any]]) -> int:
        """
        Batch store embeddings
        
        Args:
            records: List of embedding records
            
        Returns:
            Number of records inserted
        """
        query = """
        INSERT INTO document_embeddings 
        (case_id, document_id, chunk_id, content, embedding, model_used, text_hash, metadata)
        VALUES %s
        ON CONFLICT (document_id, chunk_id) DO UPDATE
        SET embedding = EXCLUDED.embedding,
            content = EXCLUDED.content,
            model_used = EXCLUDED.model_used,
            metadata = EXCLUDED.metadata
        """
        
        values = [
            (
                rec['case_id'],
                rec['document_id'],
                rec['chunk_id'],
                rec['content'],
                rec['embedding'],
                rec['model_used'],
                rec['text_hash'],
                json.dumps(rec.get('metadata'))
            )
            for rec in records
        ]
        
        with self.conn.cursor() as cur:
            execute_values(cur, query, values)
            self.conn.commit()
            return len(values)
    
    def semantic_search(
        self,
        query_embedding: List[float],
        case_id: Optional[str] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[SearchResult]:
        """
        Semantic search using cosine similarity
        
        Args:
            query_embedding: Query vector
            case_id: Optional case filter
            limit: Max results
            similarity_threshold: Minimum similarity
            
        Returns:
            List of SearchResults
        """
        # Build query
        query = """
        SELECT 
            document_id,
            chunk_id,
            content,
            1 - (embedding <=> %s::vector) as similarity,
            metadata
        FROM document_embeddings
        """
        
        params = [query_embedding]
        
        if case_id:
            query += " WHERE case_id = %s"
            params.append(case_id)
        
        query += """
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """
        params.extend([query_embedding, limit])
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            
            return [
                SearchResult(
                    document_id=row['document_id'],
                    chunk_id=row['chunk_id'],
                    content=row['content'],
                    similarity=float(row['similarity']),
                    metadata=row['metadata'] or {}
                )
                for row in results
                if row['similarity'] >= similarity_threshold
            ]
    
    def store_agent_task(
        self,
        case_id: str,
        task_id: str,
        agent_name: str,
        agent_role: str,
        status: str,
        task_data: Dict[str, Any],
        result_data: Optional[Dict[str, Any]] = None,
        confidence_score: Optional[float] = None,
        tokens_used: Optional[int] = None,
        time_taken: Optional[float] = None
    ) -> str:
        """
        Store agent task
        
        Args:
            case_id: Case identifier
            task_id: Task identifier
            agent_name: Agent name
            agent_role: Agent role
            status: Task status
            task_data: Task data
            result_data: Optional result data
            confidence_score: Optional confidence
            tokens_used: Optional token count
            time_taken: Optional execution time
            
        Returns:
            UUID of inserted record
        """
        query = """
        INSERT INTO agent_tasks
        (case_id, task_id, agent_name, agent_role, status, task_data, 
         result_data, confidence_score, tokens_used, time_taken, completed_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (task_id) DO UPDATE
        SET status = EXCLUDED.status,
            result_data = EXCLUDED.result_data,
            confidence_score = EXCLUDED.confidence_score,
            tokens_used = EXCLUDED.tokens_used,
            time_taken = EXCLUDED.time_taken,
            completed_at = EXCLUDED.completed_at
        RETURNING id
        """
        
        completed_at = datetime.now() if status == 'completed' else None
        
        with self.conn.cursor() as cur:
            cur.execute(query, (
                case_id,
                task_id,
                agent_name,
                agent_role,
                status,
                json.dumps(task_data),
                json.dumps(result_data) if result_data else None,
                confidence_score,
                tokens_used,
                time_taken,
                completed_at
            ))
            result = cur.fetchone()
            self.conn.commit()
            return str(result[0])
    
    def get_case_tasks(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Get all tasks for a case
        
        Args:
            case_id: Case identifier
            
        Returns:
            List of task records
        """
        query = """
        SELECT * FROM agent_tasks
        WHERE case_id = %s
        ORDER BY created_at ASC
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (case_id,))
            return cur.fetchall()
    
    def create_case(
        self,
        case_id: str,
        title: str,
        description: str,
        case_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new case
        
        Args:
            case_id: Case identifier
            title: Case title
            description: Case description
            case_type: Type of case
            metadata: Optional metadata
            
        Returns:
            UUID of created case
        """
        query = """
        INSERT INTO cases (case_id, title, description, case_type, status, metadata)
        VALUES (%s, %s, %s, %s, 'active', %s)
        RETURNING id
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (
                case_id,
                title,
                description,
                case_type,
                json.dumps(metadata) if metadata else None
            ))
            result = cur.fetchone()
            self.conn.commit()
            return str(result[0])
    
    def store_quality_review(
        self,
        task_id: str,
        reviewer: str,
        grade: str,
        quality_score: float,
        strengths: List[str],
        gaps: List[str],
        suggestions: List[str],
        approved: bool,
        review_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store quality review (for Claude supervision)
        
        Args:
            task_id: Task being reviewed
            reviewer: Reviewer name
            grade: Grade (A-F)
            quality_score: Numeric score
            strengths: List of strengths
            gaps: List of gaps
            suggestions: List of suggestions
            approved: Whether approved
            review_data: Optional review data
            
        Returns:
            UUID of review record
        """
        query = """
        INSERT INTO quality_reviews
        (task_id, reviewer, grade, quality_score, strengths, gaps, 
         suggestions, approved, review_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (
                task_id,
                reviewer,
                grade,
                quality_score,
                strengths,
                gaps,
                suggestions,
                approved,
                json.dumps(review_data) if review_data else None
            ))
            result = cur.fetchone()
            self.conn.commit()
            return str(result[0])
    
    def get_performance_stats(self, case_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Args:
            case_id: Optional case filter
            
        Returns:
            Performance stats dict
        """
        query = """
        SELECT 
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
            AVG(confidence_score) as avg_confidence,
            AVG(time_taken) as avg_time,
            SUM(tokens_used) as total_tokens
        FROM agent_tasks
        """
        
        if case_id:
            query += " WHERE case_id = %s"
            params = (case_id,)
        else:
            params = None
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return dict(cur.fetchone())


def test_postgres_client():
    """Test PostgreSQL client"""
    print("🧪 Testing PostgreSQL Client...\n")
    
    try:
        # Initialize client
        print("1. Connecting to PostgreSQL...")
        client = PostgresClient()
        
        # Health check
        print("2. Health check...")
        healthy = client.health_check()
        print(f"   {'✅' if healthy else '❌'} Database: {'Healthy' if healthy else 'Down'}")
        
        if not healthy:
            return
        
        # Create test case
        print("\n3. Creating test case...")
        case_id = f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        client.create_case(
            case_id=case_id,
            title="Test Case - Database Integration",
            description="Testing PostgreSQL integration",
            case_type="test"
        )
        print(f"   ✅ Case created: {case_id}")
        
        # Store test embedding
        print("\n4. Storing test embedding...")
        test_embedding = [0.1] * 1024  # Dummy 1024-dim vector
        record_id = client.store_embedding(
            case_id=case_id,
            document_id="test_doc_001",
            chunk_id=0,
            content="Test document content for semantic search.",
            embedding=test_embedding,
            model_used="test-model",
            text_hash="abc123",
            metadata={"test": True}
        )
        print(f"   ✅ Embedding stored: {record_id}")
        
        # Semantic search
        print("\n5. Testing semantic search...")
        results = client.semantic_search(
            query_embedding=test_embedding,
            case_id=case_id,
            limit=5,
            similarity_threshold=0.5
        )
        print(f"   ✅ Found {len(results)} results")
        if results:
            print(f"   Top result: {results[0].content[:50]}... (similarity: {results[0].similarity:.3f})")
        
        # Store task
        print("\n6. Storing agent task...")
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        client.store_agent_task(
            case_id=case_id,
            task_id=task_id,
            agent_name="Test Agent",
            agent_role="test",
            status="completed",
            task_data={"test": "data"},
            result_data={"result": "success"},
            confidence_score=0.85,
            tokens_used=100,
            time_taken=1.5
        )
        print(f"   ✅ Task stored: {task_id}")
        
        # Get stats
        print("\n7. Getting performance stats...")
        stats = client.get_performance_stats(case_id)
        print(f"   Total tasks: {stats['total_tasks']}")
        print(f"   Completed: {stats['completed_tasks']}")
        print(f"   Avg confidence: {stats['avg_confidence']:.2f}")
        
        print("\n✅ All PostgreSQL tests passed!")
        
        # Cleanup
        client.disconnect()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_postgres_client()
