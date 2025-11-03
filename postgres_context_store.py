"""
PostgreSQL-based Unlimited Context Store for Multi-Agent System

This module provides unlimited context window for agents by storing all
communications in PostgreSQL and retrieving relevant context on-demand.

Key Features:
- Unlimited message history storage
- Semantic context retrieval (relevance-based, not just recent)
- Per-agent context views
- Cross-session persistence
- Efficient querying with indexes
- Optional vector embeddings for semantic search
"""

import psycopg2
from psycopg2.extras import RealDictCursor, Json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    REQUEST = "REQUEST"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    DEBATE = "DEBATE"
    APPROVAL = "APPROVAL"
    UPDATE = "UPDATE"
    RESPONSE = "RESPONSE"


@dataclass
class StoredMessage:
    """Message stored in PostgreSQL"""
    id: str
    project_id: str
    sender: str
    recipient: Optional[str]
    message_type: str
    content: str
    context: Dict[str, Any]
    timestamp: datetime
    requires_response: bool = False
    response_to: Optional[str] = None
    importance: float = 0.5  # 0.0 to 1.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class PostgresContextStore:
    """
    Manages unlimited context storage in PostgreSQL
    
    Each agent can retrieve relevant context without context window limits.
    Uses semantic relevance scoring to fetch most pertinent messages.
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize connection to PostgreSQL
        
        Args:
            connection_string: PostgreSQL connection string
                Example: "dbname=destiny_team user=artur password=xxx host=localhost"
        """
        self.conn_string = connection_string
        self.conn = None
        self._connect()
        self._ensure_schema()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.conn_string)
            self.conn.autocommit = False
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")
    
    def _ensure_schema(self):
        """Create tables if they don't exist"""
        schema_sql = """
        -- Main messages table
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(255) PRIMARY KEY,
            project_id VARCHAR(255) NOT NULL,
            sender VARCHAR(255) NOT NULL,
            recipient VARCHAR(255),
            message_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            context JSONB,
            timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
            requires_response BOOLEAN DEFAULT FALSE,
            response_to VARCHAR(255),
            importance FLOAT DEFAULT 0.5,
            tags TEXT[],
            
            -- Indexes for fast queries
            CONSTRAINT fk_response_to FOREIGN KEY (response_to) REFERENCES messages(id) ON DELETE SET NULL
        );
        
        CREATE INDEX IF NOT EXISTS idx_messages_project ON messages(project_id);
        CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender);
        CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient);
        CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp DESC);
        CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(message_type);
        CREATE INDEX IF NOT EXISTS idx_messages_tags ON messages USING GIN(tags);
        CREATE INDEX IF NOT EXISTS idx_messages_context ON messages USING GIN(context);
        
        -- Agent context table (each agent's personal knowledge)
        CREATE TABLE IF NOT EXISTS agent_contexts (
            agent_name VARCHAR(255) NOT NULL,
            project_id VARCHAR(255) NOT NULL,
            context_key VARCHAR(255) NOT NULL,
            context_value JSONB NOT NULL,
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            importance FLOAT DEFAULT 0.5,
            
            PRIMARY KEY (agent_name, project_id, context_key)
        );
        
        CREATE INDEX IF NOT EXISTS idx_agent_contexts_agent ON agent_contexts(agent_name);
        CREATE INDEX IF NOT EXISTS idx_agent_contexts_project ON agent_contexts(project_id);
        CREATE INDEX IF NOT EXISTS idx_agent_contexts_updated ON agent_contexts(updated_at DESC);
        
        -- Project state table
        CREATE TABLE IF NOT EXISTS projects (
            project_id VARCHAR(255) PRIMARY KEY,
            project_name VARCHAR(500) NOT NULL,
            description TEXT,
            current_phase VARCHAR(100),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            metadata JSONB
        );
        
        -- Agent work queue
        CREATE TABLE IF NOT EXISTS agent_work_queue (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(255) NOT NULL,
            project_id VARCHAR(255) NOT NULL,
            task TEXT NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            priority INTEGER DEFAULT 5,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_work_queue_agent ON agent_work_queue(agent_name);
        CREATE INDEX IF NOT EXISTS idx_work_queue_status ON agent_work_queue(status);
        
        -- Decisions log
        CREATE TABLE IF NOT EXISTS decisions (
            id SERIAL PRIMARY KEY,
            project_id VARCHAR(255) NOT NULL,
            decision_text TEXT NOT NULL,
            decision_type VARCHAR(100),
            made_by VARCHAR(255) NOT NULL,
            approved_by TEXT[],
            timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
            context JSONB
        );
        
        -- Optional: Vector embeddings for semantic search
        -- Requires pgvector extension: CREATE EXTENSION IF NOT EXISTS vector;
        -- CREATE TABLE IF NOT EXISTS message_embeddings (
        --     message_id VARCHAR(255) PRIMARY KEY,
        --     embedding vector(1536),  -- OpenAI ada-002 dimension
        --     FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
        -- );
        """
        
        with self.conn.cursor() as cur:
            cur.execute(schema_sql)
            self.conn.commit()
    
    # ==================== MESSAGE STORAGE ====================
    
    def store_message(self, message: StoredMessage) -> bool:
        """
        Store a message in PostgreSQL
        
        Args:
            message: StoredMessage object
            
        Returns:
            True if successful
        """
        sql = """
        INSERT INTO messages (
            id, project_id, sender, recipient, message_type, content,
            context, timestamp, requires_response, response_to, importance, tags
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            content = EXCLUDED.content,
            context = EXCLUDED.context,
            importance = EXCLUDED.importance
        """
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (
                    message.id,
                    message.project_id,
                    message.sender,
                    message.recipient,
                    message.message_type,
                    message.content,
                    Json(message.context),
                    message.timestamp,
                    message.requires_response,
                    message.response_to,
                    message.importance,
                    message.tags
                ))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error storing message: {e}")
            return False
    
    def get_message(self, message_id: str) -> Optional[StoredMessage]:
        """Retrieve a specific message by ID"""
        sql = "SELECT * FROM messages WHERE id = %s"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (message_id,))
            row = cur.fetchone()
            
            if row:
                return StoredMessage(**row)
            return None
    
    # ==================== CONTEXT RETRIEVAL ====================
    
    def get_relevant_context_for_agent(
        self,
        agent_name: str,
        project_id: str,
        query: str,
        max_messages: int = 20,
        time_window_days: Optional[int] = None,
        min_importance: float = 0.0
    ) -> List[StoredMessage]:
        """
        Retrieve relevant context for an agent based on current query.
        
        This is the KEY method - it gives agents unlimited context by retrieving
        only the most relevant messages, not all messages.
        
        Args:
            agent_name: Name of the agent requesting context
            project_id: Current project ID
            query: Current question/topic (used for relevance scoring)
            max_messages: Maximum number of messages to return
            time_window_days: Only retrieve messages from last N days (None = all time)
            min_importance: Minimum importance score (0.0 to 1.0)
            
        Returns:
            List of relevant messages, sorted by relevance score
        """
        # Build query with relevance scoring
        time_filter = ""
        if time_window_days:
            time_filter = f"AND timestamp > NOW() - INTERVAL '{time_window_days} days'"
        
        # Keyword extraction for simple relevance
        query_keywords = self._extract_keywords(query)
        
        sql = f"""
        WITH relevance_scored AS (
            SELECT 
                *,
                -- Relevance scoring algorithm
                (
                    -- Factor 1: Keyword overlap (0-1)
                    (SELECT COUNT(*)::FLOAT FROM unnest(tags) tag WHERE tag = ANY(%s)) 
                    / GREATEST(array_length(tags, 1), 1)
                    * 0.3
                    
                    -- Factor 2: Recency (0-1, exponential decay)
                    + (
                        CASE 
                            WHEN EXTRACT(EPOCH FROM (NOW() - timestamp)) < 3600 THEN 1.0
                            WHEN EXTRACT(EPOCH FROM (NOW() - timestamp)) < 86400 THEN 0.7
                            WHEN EXTRACT(EPOCH FROM (NOW() - timestamp)) < 604800 THEN 0.4
                            ELSE 0.2
                        END
                    ) * 0.2
                    
                    -- Factor 3: Importance (stored in message)
                    + importance * 0.3
                    
                    -- Factor 4: Agent involvement (higher if agent sent/received)
                    + (
                        CASE 
                            WHEN sender = %s THEN 0.1
                            WHEN recipient = %s THEN 0.1
                            ELSE 0.0
                        END
                    ) * 0.2
                    
                ) as relevance_score
            FROM messages
            WHERE project_id = %s
                AND importance >= %s
                {time_filter}
        )
        SELECT * FROM relevance_scored
        WHERE relevance_score > 0.1
        ORDER BY relevance_score DESC, timestamp DESC
        LIMIT %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (
                query_keywords,
                agent_name,
                agent_name,
                project_id,
                min_importance,
                max_messages
            ))
            
            rows = cur.fetchall()
            return [StoredMessage(**row) for row in rows]
    
    def get_conversation_thread(
        self,
        message_id: str,
        include_context: bool = True
    ) -> List[StoredMessage]:
        """
        Get entire conversation thread for a message.
        
        Follows response_to chain to reconstruct conversation.
        """
        sql = """
        WITH RECURSIVE thread AS (
            -- Base case: the message itself
            SELECT * FROM messages WHERE id = %s
            
            UNION ALL
            
            -- Recursive case: messages that respond to this thread
            SELECT m.* 
            FROM messages m
            INNER JOIN thread t ON m.response_to = t.id
        )
        SELECT * FROM thread
        ORDER BY timestamp ASC
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (message_id,))
            rows = cur.fetchall()
            return [StoredMessage(**row) for row in rows]
    
    def get_agent_conversation_history(
        self,
        agent_name: str,
        project_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[StoredMessage]:
        """
        Get an agent's conversation history (sent or received).
        """
        sql = """
        SELECT * FROM messages
        WHERE project_id = %s
            AND (sender = %s OR recipient = %s)
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (project_id, agent_name, agent_name, limit, offset))
            rows = cur.fetchall()
            return [StoredMessage(**row) for row in rows]
    
    def get_messages_by_type(
        self,
        project_id: str,
        message_type: str,
        limit: int = 50
    ) -> List[StoredMessage]:
        """Get all messages of a specific type (e.g., all APPROVALS, all DEBATES)"""
        sql = """
        SELECT * FROM messages
        WHERE project_id = %s AND message_type = %s
        ORDER BY timestamp DESC
        LIMIT %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (project_id, message_type, limit))
            rows = cur.fetchall()
            return [StoredMessage(**row) for row in rows]
    
    # ==================== AGENT CONTEXT MANAGEMENT ====================
    
    def store_agent_context(
        self,
        agent_name: str,
        project_id: str,
        context_key: str,
        context_value: Any,
        importance: float = 0.5
    ) -> bool:
        """
        Store agent-specific context (personal knowledge, not messages).
        
        Example: Sarah (Architect) stores her architecture decisions,
                 Marcus (Developer) stores code patterns he's used.
        """
        sql = """
        INSERT INTO agent_contexts (agent_name, project_id, context_key, context_value, importance, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        ON CONFLICT (agent_name, project_id, context_key) 
        DO UPDATE SET 
            context_value = EXCLUDED.context_value,
            importance = EXCLUDED.importance,
            updated_at = NOW()
        """
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (
                    agent_name,
                    project_id,
                    context_key,
                    Json(context_value),
                    importance
                ))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error storing agent context: {e}")
            return False
    
    def get_agent_context(
        self,
        agent_name: str,
        project_id: str,
        context_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve agent's personal context.
        
        If context_key is None, returns all context for the agent.
        """
        if context_key:
            sql = """
            SELECT context_key, context_value, importance, updated_at
            FROM agent_contexts
            WHERE agent_name = %s AND project_id = %s AND context_key = %s
            """
            params = (agent_name, project_id, context_key)
        else:
            sql = """
            SELECT context_key, context_value, importance, updated_at
            FROM agent_contexts
            WHERE agent_name = %s AND project_id = %s
            ORDER BY importance DESC, updated_at DESC
            """
            params = (agent_name, project_id)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            
            if context_key:
                return rows[0]['context_value'] if rows else {}
            else:
                return {
                    row['context_key']: {
                        'value': row['context_value'],
                        'importance': row['importance'],
                        'updated_at': row['updated_at']
                    }
                    for row in rows
                }
    
    # ==================== PROJECT MANAGEMENT ====================
    
    def create_project(
        self,
        project_id: str,
        project_name: str,
        description: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Create a new project"""
        sql = """
        INSERT INTO projects (project_id, project_name, description, metadata, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
        """
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (
                    project_id,
                    project_name,
                    description,
                    Json(metadata or {})
                ))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating project: {e}")
            return False
    
    def update_project_phase(self, project_id: str, new_phase: str) -> bool:
        """Update project phase"""
        sql = """
        UPDATE projects 
        SET current_phase = %s, updated_at = NOW()
        WHERE project_id = %s
        """
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (new_phase, project_id))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating project phase: {e}")
            return False
    
    # ==================== ANALYTICS & INSIGHTS ====================
    
    def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive project statistics"""
        sql = """
        SELECT 
            COUNT(*) as total_messages,
            COUNT(DISTINCT sender) as active_agents,
            COUNT(CASE WHEN message_type = 'DEBATE' THEN 1 END) as debates,
            COUNT(CASE WHEN message_type = 'APPROVAL' THEN 1 END) as approvals,
            COUNT(CASE WHEN requires_response AND response_to IS NULL THEN 1 END) as pending_responses,
            MIN(timestamp) as project_start,
            MAX(timestamp) as last_activity
        FROM messages
        WHERE project_id = %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (project_id,))
            return dict(cur.fetchone())
    
    def get_agent_activity_summary(
        self,
        project_id: str,
        agent_name: str
    ) -> Dict[str, Any]:
        """Get summary of agent's activity in project"""
        sql = """
        SELECT 
            COUNT(*) as messages_sent,
            COUNT(DISTINCT recipient) as agents_contacted,
            AVG(importance) as avg_importance,
            COUNT(CASE WHEN message_type = 'DEBATE' THEN 1 END) as debates_initiated,
            COUNT(CASE WHEN message_type = 'APPROVAL' THEN 1 END) as approvals_requested
        FROM messages
        WHERE project_id = %s AND sender = %s
        """
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (project_id, agent_name))
            return dict(cur.fetchone())
    
    # ==================== UTILITY METHODS ====================
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Simple keyword extraction from text.
        
        In production, use NLP library like spaCy or NLTK for better extraction.
        """
        # Simple implementation: lowercase, split, remove common words
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        words = text.lower().split()
        keywords = [
            w.strip('.,!?;:')
            for w in words
            if len(w) > 3 and w.lower() not in common_words
        ]
        
        # Return unique keywords, limited to max_keywords
        return list(set(keywords))[:max_keywords]
    
    def search_messages(
        self,
        project_id: str,
        search_query: str,
        limit: int = 50
    ) -> List[StoredMessage]:
        """Full-text search across message content"""
        keywords = self._extract_keywords(search_query)
        
        sql = """
        SELECT * FROM messages
        WHERE project_id = %s
            AND (
                content ILIKE ANY(%s)
                OR tags && %s
            )
        ORDER BY timestamp DESC
        LIMIT %s
        """
        
        like_patterns = [f"%{kw}%" for kw in keywords]
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (project_id, like_patterns, keywords, limit))
            rows = cur.fetchall()
            return [StoredMessage(**row) for row in rows]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# ==================== INTEGRATION HELPER ====================

class AgentWithUnlimitedContext:
    """
    Wrapper class showing how to integrate PostgresContextStore with existing agents.
    
    This gives any agent access to unlimited context via PostgreSQL.
    """
    
    def __init__(
        self,
        agent_name: str,
        role: str,
        project_id: str,
        context_store: PostgresContextStore
    ):
        self.agent_name = agent_name
        self.role = role
        self.project_id = project_id
        self.context_store = context_store
    
    def think(self, prompt: str, max_context_messages: int = 20) -> str:
        """
        Agent thinking with unlimited context access.
        
        Instead of maintaining context in memory (limited by token windows),
        agent retrieves relevant context from PostgreSQL on-demand.
        """
        # Step 1: Retrieve relevant context from unlimited history
        relevant_messages = self.context_store.get_relevant_context_for_agent(
            agent_name=self.agent_name,
            project_id=self.project_id,
            query=prompt,
            max_messages=max_context_messages
        )
        
        # Step 2: Get agent's personal context (their accumulated knowledge)
        personal_context = self.context_store.get_agent_context(
            agent_name=self.agent_name,
            project_id=self.project_id
        )
        
        # Step 3: Build context prompt from retrieved data
        context_prompt = self._build_context_prompt(
            prompt,
            relevant_messages,
            personal_context
        )
        
        # Step 4: Call AI model with context (Cursor AI, or external API)
        # response = call_ai_model(context_prompt)
        response = f"[{self.agent_name} would respond with full context access]"
        
        return response
    
    def _build_context_prompt(
        self,
        current_prompt: str,
        relevant_messages: List[StoredMessage],
        personal_context: Dict[str, Any]
    ) -> str:
        """Build prompt with relevant context"""
        parts = []
        
        parts.append(f"You are {self.agent_name}, a {self.role}.")
        parts.append("\n--- YOUR PERSONAL KNOWLEDGE ---")
        
        for key, data in personal_context.items():
            parts.append(f"{key}: {data['value']}")
        
        parts.append("\n--- RELEVANT TEAM COMMUNICATIONS ---")
        
        for msg in relevant_messages:
            parts.append(
                f"[{msg.timestamp}] {msg.sender} → {msg.recipient or 'ALL'}: {msg.content}"
            )
        
        parts.append(f"\n--- CURRENT QUESTION ---")
        parts.append(current_prompt)
        
        return "\n".join(parts)
    
    def send_message(
        self,
        recipient: Optional[str],
        message_type: str,
        content: str,
        importance: float = 0.5,
        tags: Optional[List[str]] = None
    ) -> str:
        """Send message and store in PostgreSQL"""
        import uuid
        
        message = StoredMessage(
            id=str(uuid.uuid4()),
            project_id=self.project_id,
            sender=self.agent_name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            context={},
            timestamp=datetime.now(),
            importance=importance,
            tags=tags or []
        )
        
        self.context_store.store_message(message)
        return message.id
    
    def update_personal_context(self, key: str, value: Any, importance: float = 0.5):
        """Update agent's personal knowledge base"""
        self.context_store.store_agent_context(
            agent_name=self.agent_name,
            project_id=self.project_id,
            context_key=key,
            context_value=value,
            importance=importance
        )


if __name__ == "__main__":
    # Example usage
    print("PostgreSQL Unlimited Context Store for Multi-Agent System")
    print("=" * 60)
    print("\nTo use:")
    print("1. Install PostgreSQL: brew install postgresql")
    print("2. Create database: createdb destiny_team")
    print("3. Update connection string in code")
    print("4. Run this script to create tables")
    print("\nConnection string format:")
    print('  "dbname=destiny_team user=artur host=localhost"')
