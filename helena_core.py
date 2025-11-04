#!/usr/bin/env python3
"""
Helena's Core Functions - Knowledge Manager Implementation
Dr. Helena Kowalczyk's operational code

This module implements Helena's three core functions:
1. save_to_all_layers() - Save data to all 4 database layers
2. load_context() - Retrieve context via search and queries
3. generate_briefing() - Create role-specific briefings

Pattern: Paired with Aleksander (Orchestrator)
Trigger: Aleksander's actions
Role: Chief of Staff ensuring quality and documentation
"""

import psycopg2
import subprocess
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any


class HelenaCore:
    """
    Dr. Helena Kowalczyk - Knowledge Manager Core Functions
    
    Responsibilities:
    - Save important events to all 4 layers (PostgreSQL, Neo4j, Qdrant, Redis)
    - Load context for agents (search + queries)
    - Generate role-specific briefings
    - Ensure data persistence and quality
    
    Pattern: Always paired with Aleksander (Orchestrator)
    """
    
    def __init__(
        self,
        postgres_conn: str = "dbname=destiny_team user=user password=password host=localhost port=5432",
        neo4j_container: str = "sms-neo4j",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password",
        qdrant_url: str = "http://localhost:6333",
        redis_container: str = "kg-redis",
        lmstudio_url: str = "http://localhost:1234/v1/embeddings",
        project_id: str = "destiny-team-framework-master"
    ):
        """Initialize Helena with all database connections"""
        self.postgres_conn = postgres_conn
        self.neo4j_container = neo4j_container
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.qdrant_url = qdrant_url
        self.redis_container = redis_container
        self.lmstudio_url = lmstudio_url
        self.project_id = project_id
        self.collection_name = project_id
        
    # ========================================================================
    # CORE FUNCTION 1: SAVE TO ALL LAYERS
    # ========================================================================
    
    def save_to_all_layers(
        self,
        event_type: str,
        content: str,
        importance: float,
        made_by: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save important event to ALL 4 database layers
        
        This is Helena's PRIMARY function - ensuring nothing important is lost.
        Follows the principle: "If it's not saved, it didn't happen"
        
        Args:
            event_type: Type of event (decision, milestone, message, task, etc.)
            content: Main content/description
            importance: 0.0-1.0 scale (>0.8 recommended for saving)
            made_by: Who created/made this
            additional_data: Extra metadata (dict)
            
        Returns:
            Dict with save status for each layer:
            {
                "success": bool,
                "layers": {
                    "postgresql": {"status": "success/failed", "details": ...},
                    "neo4j": {"status": "success/failed", "details": ...},
                    "qdrant": {"status": "success/failed", "details": ...},
                    "redis": {"status": "success/failed", "details": ...}
                },
                "event_id": str (uuid),
                "timestamp": datetime
            }
        """
        print(f"\n{'='*80}")
        print(f"💾 HELENA: Saving to all layers")
        print(f"   Type: {event_type}")
        print(f"   Importance: {importance}")
        print(f"   By: {made_by}")
        print(f"{'='*80}\n")
        
        event_id = str(uuid.uuid4())
        timestamp = datetime.now()
        results = {
            "success": True,
            "layers": {},
            "event_id": event_id,
            "timestamp": timestamp.isoformat()
        }
        
        additional_data = additional_data or {}
        
        # Layer 1: PostgreSQL (structured data)
        pg_result = self._save_to_postgresql(
            event_type, content, importance, made_by, 
            event_id, timestamp, additional_data
        )
        results["layers"]["postgresql"] = pg_result
        if pg_result["status"] == "failed":
            results["success"] = False
            
        # Layer 2: Neo4j (if it's a decision, create knowledge chain)
        if event_type == "decision":
            neo4j_result = self._save_to_neo4j(
                content, made_by, event_id, additional_data
            )
            results["layers"]["neo4j"] = neo4j_result
            if neo4j_result["status"] == "failed":
                results["success"] = False
        else:
            results["layers"]["neo4j"] = {"status": "skipped", "reason": "not a decision"}
            
        # Layer 3: Qdrant (semantic search)
        if importance >= 0.75:  # Only embed important events
            qdrant_result = self._save_to_qdrant(
                event_type, content, importance, made_by, 
                event_id, timestamp, additional_data
            )
            results["layers"]["qdrant"] = qdrant_result
            if qdrant_result["status"] == "failed":
                results["success"] = False
        else:
            results["layers"]["qdrant"] = {"status": "skipped", "reason": f"importance {importance} < 0.75"}
            
        # Layer 4: Redis (hot cache)
        redis_result = self._save_to_redis(
            event_type, content, importance, made_by, 
            event_id, timestamp
        )
        results["layers"]["redis"] = redis_result
        if redis_result["status"] == "failed":
            results["success"] = False
            
        # Print summary
        self._print_save_summary(results)
        
        return results
    
    def _save_to_postgresql(
        self, event_type: str, content: str, importance: float,
        made_by: str, event_id: str, timestamp: datetime,
        additional_data: Dict
    ) -> Dict:
        """Save to PostgreSQL based on event type"""
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            if event_type == "decision":
                cur.execute("""
                    INSERT INTO decisions 
                    (project_id, decision_text, decision_type, made_by, 
                     approved_by, timestamp, context)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.project_id,
                    content,
                    additional_data.get("decision_type", "general"),
                    made_by,
                    additional_data.get("approved_by", [made_by]),
                    timestamp,
                    json.dumps(additional_data)
                ))
                
            elif event_type == "message":
                cur.execute("""
                    INSERT INTO messages 
                    (id, project_id, sender, recipient, message_type, 
                     content, context, timestamp, requires_response, response_to, importance, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    event_id,
                    self.project_id,
                    made_by,
                    additional_data.get("recipient", "Team"),
                    additional_data.get("message_type", "NOTIFICATION"),
                    content,
                    json.dumps(additional_data),
                    timestamp,
                    bool(additional_data.get("requires_response", False)),
                    additional_data.get("response_to"),
                    importance,
                    additional_data.get("tags", [])
                ))
                
            elif event_type == "agent_context":
                agent_name = additional_data.get("agent_name", made_by)
                context_key = additional_data.get("context_key", "general_update")
                cur.execute("""
                    INSERT INTO agent_contexts 
                    (agent_name, project_id, context_key, context_value, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (agent_name, project_id, context_key)
                    DO UPDATE SET context_value = EXCLUDED.context_value, 
                                  updated_at = EXCLUDED.updated_at
                """, (
                    agent_name,
                    self.project_id,
                    context_key,
                    json.dumps({"content": content, **additional_data}),
                    timestamp
                ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return {"status": "success", "table": event_type}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _save_to_neo4j(
        self, content: str, made_by: str, event_id: str, 
        additional_data: Dict
    ) -> Dict:
        """Save decision chain to Neo4j"""
        try:
            # Create decision node and relationship chain
            reasons = additional_data.get("reasons", [])
            
            # Escape single quotes for Cypher query
            content_escaped = content.replace("'", "\\'")
            
            cypher = f"""
            MATCH (p:Project {{id: '{self.project_id}'}})
            CREATE (decision:Decision {{
              id: '{event_id}',
              text: '{content_escaped}',
              made_by: '{made_by}',
              project_id: '{self.project_id}',
              timestamp: datetime(),
              importance: {additional_data.get('importance', 0.8)}
            }})
            CREATE (decision)-[:IN_PROJECT]->(p)
            """
            
            # Add reason chains
            for i, reason in enumerate(reasons):
                reason_escaped = reason.replace("'", "\\'")
                cypher += f"""
                CREATE (reason{i}:Reason {{text: '{reason_escaped}'}})
                CREATE (decision)-[:BECAUSE]->(reason{i})
                """
            
            cypher += "RETURN decision"
            
            result = subprocess.run([
                'docker', 'exec', self.neo4j_container,
                'cypher-shell', '-u', self.neo4j_user, '-p', self.neo4j_password,
                cypher
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"status": "success", "nodes": 1 + len(reasons)}
            else:
                return {"status": "failed", "error": result.stderr}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _save_to_qdrant(
        self, event_type: str, content: str, importance: float,
        made_by: str, event_id: str, timestamp: datetime,
        additional_data: Dict
    ) -> Dict:
        """Generate embedding and save to Qdrant"""
        try:
            # Generate embedding
            embed_text = f"{event_type}: {content}"
            
            result = subprocess.run([
                'curl', '-s', '-X', 'POST', self.lmstudio_url,
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "input": embed_text,
                    "model": "text-embedding-intfloat-multilingual-e5-large-instruct"
                })
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"status": "failed", "error": "embedding generation failed"}
            
            embedding_response = json.loads(result.stdout)
            embedding = embedding_response['data'][0]['embedding']
            
            # Get next ID
            result = subprocess.run([
                'curl', '-s', f'{self.qdrant_url}/collections/{self.collection_name}'
            ], capture_output=True, text=True)
            
            coll_raw = result.stdout.strip()
            coll_data = {}
            if coll_raw:
                try:
                    coll_data = json.loads(coll_raw)
                except Exception:
                    coll_data = {}

            # Ensure collection exists; create if missing
            if not coll_data or 'result' not in coll_data:
                create_payload = {
                    "vectors": {"size": 1024, "distance": "Cosine"}
                }
                create_res = subprocess.run([
                    'curl', '-s', '-X', 'PUT',
                    f'{self.qdrant_url}/collections/{self.collection_name}',
                    '-H', 'Content-Type: application/json',
                    '-d', json.dumps(create_payload)
                ], capture_output=True, text=True)
                if create_res.returncode != 0:
                    return {"status": "failed", "error": "failed to create Qdrant collection"}
                next_id = 1
            else:
                points_count = coll_data.get('result', {}).get('points_count', 0)
                try:
                    next_id = int(points_count) + 1
                except Exception:
                    next_id = 1
            
            # Save to Qdrant
            payload = {
                "type": event_type,
                "content": content,
                "importance": importance,
                "made_by": made_by,
                "timestamp": timestamp.isoformat(),
                "event_id": event_id,
                **additional_data
            }
            
            point_data = {
                "points": [{
                    "id": next_id,
                    "vector": embedding,
                    "payload": payload
                }]
            }
            
            result = subprocess.run([
                'curl', '-s', '-X', 'PUT',
                f'{self.qdrant_url}/collections/{self.collection_name}/points',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(point_data)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"status": "success", "point_id": next_id}
            else:
                return {"status": "failed", "error": "upload failed"}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _save_to_redis(
        self, event_type: str, content: str, importance: float,
        made_by: str, event_id: str, timestamp: datetime
    ) -> Dict:
        """Save to Redis hot cache"""
        try:
            event_json = json.dumps({
                "type": event_type,
                "content": content[:200],  # Truncate for cache
                "importance": importance,
                "made_by": made_by,
                "event_id": event_id,
                "timestamp": timestamp.isoformat()
            })
            
            key = f"destiny:hot_memory:{self.project_id}"
            
            # Add to list (LPUSH)
            result = subprocess.run([
                'docker', 'exec', self.redis_container,
                'redis-cli', 'LPUSH', key, event_json
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Trim to last 10 events
                subprocess.run([
                    'docker', 'exec', self.redis_container,
                    'redis-cli', 'LTRIM', key, '0', '9'
                ], capture_output=True, text=True)
                
                return {"status": "success", "cached": True}
            else:
                return {"status": "failed", "error": result.stderr}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _print_save_summary(self, results: Dict):
        """Print summary of save operation"""
        print(f"\n{'─'*80}")
        print(f"💾 SAVE SUMMARY:")
        print(f"{'─'*80}")
        
        for layer, result in results["layers"].items():
            status = result["status"]
            if status == "success":
                emoji = "✅"
            elif status == "skipped":
                emoji = "⏭️"
            else:
                emoji = "❌"
            
            print(f"{emoji} {layer.upper()}: {status}")
            if "reason" in result:
                print(f"     Reason: {result['reason']}")
            if "error" in result:
                print(f"     Error: {result['error']}")
        
        print(f"{'─'*80}")
        if results["success"]:
            print(f"✅ Overall: SUCCESS - Event saved")
        else:
            print(f"⚠️  Overall: PARTIAL - Some layers failed")
        print(f"Event ID: {results['event_id']}")
        print(f"{'='*80}\n")
    
    # ========================================================================
    # CORE FUNCTION 2: LOAD CONTEXT
    # ========================================================================
    
    def load_context(
        self,
        query: str,
        limit: int = 5,
        search_postgresql: bool = True,
        search_qdrant: bool = True
    ) -> Dict[str, Any]:
        """
        Load relevant context via semantic search + PostgreSQL queries
        
        Args:
            query: Natural language query
            limit: Maximum results to return
            search_postgresql: Whether to query PostgreSQL directly
            search_qdrant: Whether to do semantic search
            
        Returns:
            Dict with results from each source:
            {
                "query": str,
                "qdrant_results": List[Dict],
                "postgresql_results": List[Dict],
                "combined_summary": str
            }
        """
        print(f"\n{'='*80}")
        print(f"🔍 HELENA: Loading context")
        print(f"   Query: {query}")
        print(f"{'='*80}\n")
        
        results = {
            "query": query,
            "qdrant_results": [],
            "postgresql_results": [],
            "combined_summary": ""
        }
        
        # Search Qdrant (semantic)
        if search_qdrant:
            qdrant_results = self._search_qdrant(query, limit)
            results["qdrant_results"] = qdrant_results
            print(f"✅ Found {len(qdrant_results)} results from Qdrant")
        
        # Search PostgreSQL (structured)
        if search_postgresql:
            pg_results = self._query_postgresql(query, limit)
            results["postgresql_results"] = pg_results
            print(f"✅ Found {len(pg_results)} results from PostgreSQL")
        
        # Combine results
        results["combined_summary"] = self._combine_results(results)
        
        print(f"\n{'='*80}\n")
        return results
    
    def _search_qdrant(self, query: str, limit: int) -> List[Dict]:
        """Semantic search in Qdrant"""
        try:
            # Generate embedding for query
            result = subprocess.run([
                'curl', '-s', '-X', 'POST', self.lmstudio_url,
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "input": query,
                    "model": "text-embedding-intfloat-multilingual-e5-large-instruct"
                })
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return []
            
            embedding_response = json.loads(result.stdout)
            embedding = embedding_response['data'][0]['embedding']
            
            # Search Qdrant
            result = subprocess.run([
                'curl', '-s', '-X', 'POST',
                f'{self.qdrant_url}/collections/{self.collection_name}/points/search',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "vector": embedding,
                    "limit": limit,
                    "with_payload": True
                })
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                search_response = json.loads(result.stdout)
                return search_response['result']
            else:
                return []
                
        except Exception as e:
            print(f"⚠️  Qdrant search error: {e}")
            return []
    
    def _query_postgresql(self, query: str, limit: int) -> List[Dict]:
        """Query PostgreSQL for relevant records"""
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            # Get recent decisions
            cur.execute("""
                SELECT decision_text, decision_type, made_by, timestamp, context
                FROM decisions
                WHERE project_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """, (self.project_id, limit))
            
            rows = cur.fetchall()
            results = []
            
            for row in rows:
                results.append({
                    "type": "decision",
                    "text": row[0],
                    "decision_type": row[1],
                    "made_by": row[2],
                    "timestamp": row[3].isoformat() if row[3] else None,
                    "context": row[4]
                })
            
            cur.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"⚠️  PostgreSQL query error: {e}")
            return []
    
    def _combine_results(self, results: Dict) -> str:
        """Combine and summarize results"""
        summary_parts = []
        
        if results["qdrant_results"]:
            summary_parts.append("Semantic search found:")
            for i, r in enumerate(results["qdrant_results"][:3], 1):
                payload = r.get('payload', {})
                title = payload.get('title', payload.get('content', '')[:60])
                summary_parts.append(f"  {i}. {title}")
        
        if results["postgresql_results"]:
            summary_parts.append("\nRecent decisions:")
            for i, r in enumerate(results["postgresql_results"][:3], 1):
                summary_parts.append(f"  {i}. {r['text'][:60]}...")
        
        return "\n".join(summary_parts)
    
    # ========================================================================
    # CORE FUNCTION 3: GENERATE BRIEFING
    # ========================================================================
    
    def generate_briefing(
        self,
        agent_name: str,
        briefing_type: str = "morning"
    ) -> str:
        """
        Generate role-specific briefing for an agent
        
        Args:
            agent_name: Name of agent (e.g., "Tomasz Zieliński")
            briefing_type: "morning", "quick", "full"
            
        Returns:
            Formatted briefing string
        """
        print(f"\n{'='*80}")
        print(f"📋 HELENA: Generating {briefing_type} briefing for {agent_name}")
        print(f"{'='*80}\n")
        
        # Find agent's role
        role_info = self._get_agent_role(agent_name)
        
        # Get agent's recent context
        agent_context = self._get_agent_context(agent_name)
        
        # Get project status
        project_status = self._get_project_status()
        
        # Get relevant recent decisions
        recent_decisions = self._get_recent_decisions(limit=3)
        
        # Compose briefing
        briefing = self._compose_briefing(
            agent_name, role_info, agent_context,
            project_status, recent_decisions, briefing_type
        )
        
        print(f"✅ Briefing generated ({len(briefing)} chars)\n")
        print(f"{'='*80}\n")
        
        return briefing
    
    def _get_agent_role(self, agent_name: str) -> Dict:
        """Get agent's role information from search"""
        query = f"What is {agent_name}'s role and responsibilities?"
        results = self._search_qdrant(query, limit=1)
        
        if results:
            return results[0].get('payload', {})
        return {"role": "Unknown", "content": "Role information not found"}
    
    def _get_agent_context(self, agent_name: str) -> Dict:
        """Get agent's personal context from PostgreSQL"""
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT context_key, context_value, updated_at
                FROM agent_contexts
                WHERE agent_name = %s AND project_id = %s
                ORDER BY updated_at DESC
                LIMIT 5
            """, (agent_name, self.project_id))
            
            rows = cur.fetchall()
            context = {}
            
            for row in rows:
                context[row[0]] = json.loads(row[1]) if row[1] else {}
            
            cur.close()
            conn.close()
            
            return context
            
        except Exception as e:
            print(f"⚠️  Error getting agent context: {e}")
            return {}
    
    def _get_project_status(self) -> Dict:
        """Get current project status"""
        results = self._search_qdrant("current project status and priorities", limit=2)
        
        if results:
            return {
                "status": results[0].get('payload', {}).get('content', 'Status unknown'),
                "phase": "Framework Development"
            }
        return {"status": "Unknown", "phase": "Unknown"}
    
    def _get_recent_decisions(self, limit: int = 3) -> List[Dict]:
        """Get recent decisions from PostgreSQL"""
        return self._query_postgresql("recent decisions", limit)
    
    def _compose_briefing(
        self, agent_name: str, role_info: Dict, agent_context: Dict,
        project_status: Dict, recent_decisions: List[Dict],
        briefing_type: str
    ) -> str:
        """Compose formatted briefing"""
        
        lines = [
            f"═══════════════════════════════════════════════════════════════",
            f"BRIEFING FOR: {agent_name}",
            f"Type: {briefing_type.upper()}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"═══════════════════════════════════════════════════════════════",
            f"",
            f"YOUR ROLE:",
            f"  {role_info.get('content', 'Role information not found')[:200]}",
            f"",
            f"PROJECT STATUS:",
            f"  {project_status.get('status', 'Unknown')[:200]}",
            f"  Phase: {project_status.get('phase', 'Unknown')}",
            f"",
        ]
        
        if agent_context:
            lines.append(f"YOUR RECENT CONTEXT:")
            for key, value in list(agent_context.items())[:2]:
                content = value.get('content', str(value))[:100]
                lines.append(f"  • {key}: {content}...")
            lines.append(f"")
        
        if recent_decisions:
            lines.append(f"RECENT DECISIONS:")
            for i, dec in enumerate(recent_decisions[:3], 1):
                lines.append(f"  {i}. {dec['text'][:80]}...")
                lines.append(f"     By: {dec['made_by']} ({dec.get('timestamp', 'N/A')})")
            lines.append(f"")
        
        lines.extend([
            f"═══════════════════════════════════════════════════════════════",
            f"Need more details? Ask Helena to load specific context.",
            f"═══════════════════════════════════════════════════════════════",
        ])
        
        return "\n".join(lines)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                ║")
    print("║            HELENA CORE FUNCTIONS - Test Suite                 ║")
    print("║                                                                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    helena = HelenaCore()
    
    print("Test 1: Save a decision to all layers")
    print("─" * 80)
    
    result = helena.save_to_all_layers(
        event_type="decision",
        content="Phase 2 Implementation: Build Helena's core functions",
        importance=0.90,
        made_by="Aleksander Nowak",
        additional_data={
            "decision_type": "implementation",
            "approved_by": ["Artur"],
            "reasons": [
                "Phase 1 pilot test successful",
                "Architecture validated",
                "User approved full implementation"
            ]
        }
    )
    
    print("\n" + "="*80)
    print("Test 2: Load context with search")
    print("─" * 80)
    
    context = helena.load_context("What are the next priorities?", limit=3)
    print(f"\nResults summary:\n{context['combined_summary']}")
    
    print("\n" + "="*80)
    print("Test 3: Generate briefing for agent")
    print("─" * 80)
    
    briefing = helena.generate_briefing("Tomasz Zieliński", "morning")
    print(briefing)
    
    print("\n" + "="*80)
    print("✅ HELENA CORE FUNCTIONS: Operational!")
    print("="*80)
