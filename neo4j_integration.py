"""
Neo4j Knowledge Graph Integration for Destiny Team

This module creates a knowledge graph from agent communications,
enabling graph-based reasoning and decision chain tracking.
"""

from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re
from dataclasses import dataclass


@dataclass
class Concept:
    """A concept/entity in the knowledge graph"""
    name: str
    type: str  # technology, requirement, decision, person, etc.
    properties: Dict[str, Any]


@dataclass
class Relationship:
    """A relationship between concepts"""
    from_concept: str
    to_concept: str
    rel_type: str  # chosen_for, rejected_because, related_to, etc.
    properties: Dict[str, Any]


class Neo4jKnowledgeGraph:
    """
    Knowledge Graph for Destiny Team using Neo4j.
    
    Creates a graph of concepts, decisions, and relationships from
    agent communications for advanced reasoning.
    """
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (bolt://localhost:7687)
            user: Neo4j username
            password: Neo4j password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._ensure_schema()
    
    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
    
    def _ensure_schema(self):
        """Create indexes and constraints"""
        with self.driver.session() as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT decision_id IF NOT EXISTS FOR (d:Decision) REQUIRE d.id IS UNIQUE",
                "CREATE CONSTRAINT message_id IF NOT EXISTS FOR (m:Message) REQUIRE m.id IS UNIQUE",
                "CREATE CONSTRAINT project_id IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE",
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception:
                    pass  # Constraint already exists
            
            # Indexes
            indexes = [
                "CREATE INDEX concept_type IF NOT EXISTS FOR (c:Concept) ON (c.type)",
                "CREATE INDEX message_timestamp IF NOT EXISTS FOR (m:Message) ON (m.timestamp)",
                "CREATE INDEX decision_timestamp IF NOT EXISTS FOR (d:Decision) ON (m.timestamp)",
            ]
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception:
                    pass
    
    # ==================== PROJECT MANAGEMENT ====================
    
    def create_project_node(self, project_id: str, name: str, description: str) -> bool:
        """Create a project node in the graph"""
        with self.driver.session() as session:
            result = session.run("""
                MERGE (p:Project {id: $project_id})
                SET p.name = $name,
                    p.description = $description,
                    p.created_at = datetime()
                RETURN p
            """, project_id=project_id, name=name, description=description)
            
            return result.single() is not None
    
    # ==================== MESSAGE & AGENT TRACKING ====================
    
    def add_message_to_graph(
        self,
        message_id: str,
        project_id: str,
        sender: str,
        content: str,
        timestamp: datetime,
        message_type: str
    ) -> bool:
        """Add a message and its sender to the graph"""
        with self.driver.session() as session:
            session.run("""
                // Create or merge project
                MERGE (proj:Project {id: $project_id})
                
                // Create or merge agent
                MERGE (agent:Agent {name: $sender})
                ON CREATE SET agent.role = 'Unknown'
                
                // Create message
                MERGE (msg:Message {id: $message_id})
                SET msg.content = $content,
                    msg.timestamp = datetime($timestamp),
                    msg.type = $message_type,
                    msg.project_id = $project_id
                
                // Create relationships
                MERGE (agent)-[:SENT]->(msg)
                MERGE (msg)-[:IN_PROJECT]->(proj)
                
                // Extract and link concepts
                WITH msg
                UNWIND $concepts AS concept_name
                MERGE (c:Concept {name: concept_name})
                MERGE (msg)-[:MENTIONS]->(c)
                MERGE (c)-[:MENTIONED_IN]->(msg)
            """, 
                message_id=message_id,
                project_id=project_id,
                sender=sender,
                content=content,
                timestamp=timestamp.isoformat(),
                message_type=message_type,
                concepts=self._extract_concepts_simple(content)
            )
            
            return True
    
    # ==================== CONCEPT EXTRACTION ====================
    
    def _extract_concepts_simple(self, text: str) -> List[str]:
        """
        Simple concept extraction (keywords).
        
        In production, use NLP (spaCy, etc.) for better extraction.
        """
        # Common tech concepts
        tech_concepts = [
            'postgresql', 'mongodb', 'mysql', 'redis', 'neo4j', 'qdrant',
            'microservices', 'monolith', 'api', 'rest', 'graphql',
            'react', 'vue', 'angular', 'node', 'python', 'typescript',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'security', 'authentication', 'authorization', 'oauth',
            'testing', 'deployment', 'ci/cd', 'monitoring'
        ]
        
        text_lower = text.lower()
        found_concepts = []
        
        for concept in tech_concepts:
            if concept in text_lower:
                found_concepts.append(concept.title())
        
        return found_concepts
    
    def add_concept(
        self,
        name: str,
        concept_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add or update a concept in the graph"""
        props = properties or {}
        
        with self.driver.session() as session:
            session.run("""
                MERGE (c:Concept {name: $name})
                SET c.type = $type,
                    c += $props,
                    c.updated_at = datetime()
                RETURN c
            """, name=name, type=concept_type, props=props)
            
            return True
    
    # ==================== DECISION TRACKING ====================
    
    def add_decision(
        self,
        decision_id: str,
        project_id: str,
        decision_text: str,
        decided_by: str,
        chosen: List[str],
        rejected: List[str],
        reasons: List[str],
        timestamp: datetime
    ) -> bool:
        """
        Add a decision to the graph with relationships.
        
        Example:
            chosen = ["PostgreSQL"]
            rejected = ["MongoDB", "MySQL"]
            reasons = ["ACID compliance", "transactions"]
        """
        with self.driver.session() as session:
            session.run("""
                // Create decision node
                MERGE (d:Decision {id: $decision_id})
                SET d.text = $decision_text,
                    d.timestamp = datetime($timestamp),
                    d.decided_by = $decided_by,
                    d.project_id = $project_id
                
                // Link to project
                MERGE (proj:Project {id: $project_id})
                MERGE (d)-[:IN_PROJECT]->(proj)
                
                // Link to decider (agent)
                MERGE (agent:Agent {name: $decided_by})
                MERGE (agent)-[:MADE_DECISION]->(d)
                
                // Link chosen concepts
                WITH d
                UNWIND $chosen AS chosen_name
                MERGE (c:Concept {name: chosen_name})
                MERGE (d)-[:CHOSE]->(c)
                
                // Link rejected concepts
                WITH d
                UNWIND $rejected AS rejected_name
                MERGE (c:Concept {name: rejected_name})
                MERGE (d)-[:REJECTED]->(c)
                
                // Link reasons
                WITH d
                UNWIND $reasons AS reason_text
                MERGE (r:Reason {text: reason_text})
                MERGE (d)-[:BECAUSE]->(r)
            """,
                decision_id=decision_id,
                project_id=project_id,
                decision_text=decision_text,
                decided_by=decided_by,
                chosen=chosen,
                rejected=rejected,
                reasons=reasons,
                timestamp=timestamp.isoformat()
            )
            
            return True
    
    # ==================== RELATIONSHIPS ====================
    
    def add_relationship(
        self,
        from_concept: str,
        to_concept: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a relationship between concepts"""
        props = properties or {}
        
        with self.driver.session() as session:
            session.run(f"""
                MERGE (c1:Concept {{name: $from_concept}})
                MERGE (c2:Concept {{name: $to_concept}})
                MERGE (c1)-[r:{rel_type}]->(c2)
                SET r += $props,
                    r.updated_at = datetime()
                RETURN r
            """, from_concept=from_concept, to_concept=to_concept, props=props)
            
            return True
    
    # ==================== QUERYING ====================
    
    def find_decision_chain(
        self,
        concept_name: str,
        project_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find the decision chain for a concept.
        
        Returns why a concept was chosen, who decided, what was rejected, etc.
        """
        project_filter = "WHERE d.project_id = $project_id" if project_id else ""
        
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (c:Concept {{name: $concept_name}})
                MATCH (d:Decision)-[:CHOSE]->(c)
                {project_filter}
                OPTIONAL MATCH (d)-[:REJECTED]->(rejected:Concept)
                OPTIONAL MATCH (d)-[:BECAUSE]->(reason:Reason)
                OPTIONAL MATCH (agent:Agent)-[:MADE_DECISION]->(d)
                RETURN d.text as decision,
                       d.timestamp as timestamp,
                       agent.name as decided_by,
                       collect(DISTINCT rejected.name) as alternatives_rejected,
                       collect(DISTINCT reason.text) as reasons
                ORDER BY d.timestamp DESC
            """, concept_name=concept_name, project_id=project_id)
            
            return [dict(record) for record in result]
    
    def find_related_concepts(
        self,
        concept_name: str,
        max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """Find concepts related to a given concept (up to max_depth hops)"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (c1:Concept {name: $concept_name})-[*1..%d]-(c2:Concept)
                WHERE c1 <> c2
                RETURN DISTINCT c2.name as concept,
                       c2.type as type,
                       length(path) as distance,
                       [r in relationships(path) | type(r)] as relationship_chain
                ORDER BY distance, concept
                LIMIT 50
            """ % max_depth, concept_name=concept_name)
            
            return [dict(record) for record in result]
    
    def why_question(
        self,
        question: str,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Answer "why" questions using graph traversal.
        
        Example: "Why did we choose PostgreSQL?"
        """
        # Extract concept from question (simple keyword matching)
        concepts = self._extract_concepts_simple(question)
        
        if not concepts:
            return {"error": "Could not identify concept in question"}
        
        # Get decision chain for first concept
        concept = concepts[0]
        chain = self.find_decision_chain(concept, project_id)
        
        if not chain:
            return {"error": f"No decision found for {concept}"}
        
        # Get related concepts
        related = self.find_related_concepts(concept, max_depth=2)
        
        return {
            "concept": concept,
            "decision_chain": chain,
            "related_concepts": related[:10]
        }
    
    def get_concept_graph(
        self,
        project_id: str,
        concept_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get the concept graph for a project.
        
        Returns nodes and edges for visualization.
        """
        type_filter = ""
        if concept_types:
            types_str = ", ".join([f"'{t}'" for t in concept_types])
            type_filter = f"WHERE c.type IN [{types_str}]"
        
        with self.driver.session() as session:
            # Get nodes
            nodes_result = session.run(f"""
                MATCH (c:Concept)-[:MENTIONED_IN|:CHOSE|:REJECTED]->(m:Message)
                      -[:IN_PROJECT]->(p:Project {{id: $project_id}})
                {type_filter}
                RETURN DISTINCT c.name as name,
                       c.type as type,
                       count(m) as mention_count
                ORDER BY mention_count DESC
                LIMIT 100
            """, project_id=project_id)
            
            nodes = [dict(record) for record in nodes_result]
            
            # Get edges
            edges_result = session.run("""
                MATCH (c1:Concept)-[r]-(c2:Concept)
                WHERE c1.name IN $concept_names AND c2.name IN $concept_names
                RETURN DISTINCT c1.name as source,
                       c2.name as target,
                       type(r) as relationship
                LIMIT 500
            """, concept_names=[n['name'] for n in nodes])
            
            edges = [dict(record) for record in edges_result]
            
            return {
                "nodes": nodes,
                "edges": edges,
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            }
    
    # ==================== ANALYTICS ====================
    
    def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        """Get graph statistics for a project"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Project {id: $project_id})
                OPTIONAL MATCH (m:Message)-[:IN_PROJECT]->(p)
                OPTIONAL MATCH (d:Decision)-[:IN_PROJECT]->(p)
                OPTIONAL MATCH (c:Concept)-[:MENTIONED_IN]->(m)
                OPTIONAL MATCH (a:Agent)-[:SENT]->(m)
                RETURN count(DISTINCT m) as total_messages,
                       count(DISTINCT d) as total_decisions,
                       count(DISTINCT c) as total_concepts,
                       count(DISTINCT a) as total_agents
            """, project_id=project_id)
            
            return dict(result.single())
    
    def get_most_important_concepts(
        self,
        project_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get most mentioned/important concepts in a project"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Concept)-[:MENTIONS]-(m:Message)-[:IN_PROJECT]->
                      (p:Project {id: $project_id})
                WITH c, count(m) as mentions
                OPTIONAL MATCH (d:Decision)-[:CHOSE]->(c)
                WITH c, mentions, count(d) as chosen_in_decisions
                RETURN c.name as concept,
                       c.type as type,
                       mentions,
                       chosen_in_decisions,
                       (mentions + chosen_in_decisions * 10) as importance_score
                ORDER BY importance_score DESC
                LIMIT $limit
            """, project_id=project_id, limit=limit)
            
            return [dict(record) for record in result]
    
    # ==================== UTILITIES ====================
    
    def clear_project(self, project_id: str) -> bool:
        """Clear all data for a project (careful!)"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Project {id: $project_id})
                OPTIONAL MATCH (p)<-[:IN_PROJECT]-(node)
                DETACH DELETE node, p
            """, project_id=project_id)
            
            return True


# ==================== INTEGRATION HELPER ====================

class PostgresNeo4jBridge:
    """
    Bridge between PostgreSQL messages and Neo4j graph.
    
    Automatically populates Neo4j graph from PostgreSQL messages.
    """
    
    def __init__(self, postgres_store, neo4j_graph):
        self.postgres = postgres_store
        self.neo4j = neo4j_graph
    
    def sync_project_to_graph(self, project_id: str) -> Dict[str, int]:
        """
        Sync all messages from PostgreSQL to Neo4j graph.
        
        Returns stats: messages_synced, concepts_extracted, decisions_added
        """
        # Get all messages for project
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT id, sender, content, timestamp, message_type
                FROM messages
                WHERE project_id = %s
                ORDER BY timestamp ASC
            """, (project_id,))
            
            messages = cur.fetchall()
        
        stats = {
            "messages_synced": 0,
            "concepts_extracted": 0,
            "decisions_detected": 0
        }
        
        for msg_id, sender, content, timestamp, msg_type in messages:
            # Add message to graph
            self.neo4j.add_message_to_graph(
                message_id=msg_id,
                project_id=project_id,
                sender=sender,
                content=content,
                timestamp=timestamp,
                message_type=msg_type
            )
            stats["messages_synced"] += 1
            
            # Detect decisions (simple heuristic)
            if self._is_decision(content, msg_type):
                self._extract_and_add_decision(
                    msg_id, project_id, content, sender, timestamp
                )
                stats["decisions_detected"] += 1
        
        return stats
    
    def _is_decision(self, content: str, msg_type: str) -> bool:
        """Detect if message contains a decision"""
        decision_keywords = [
            'wybrali?my', 'decided', 'choose', 'wyb?r',
            'b?dziemy u?ywa?', 'we will use', 'going with'
        ]
        
        content_lower = content.lower()
        return (
            msg_type in ['DECISION', 'APPROVAL'] or
            any(kw in content_lower for kw in decision_keywords)
        )
    
    def _extract_and_add_decision(
        self,
        message_id: str,
        project_id: str,
        content: str,
        decided_by: str,
        timestamp: datetime
    ):
        """Extract decision details and add to graph"""
        # Simple extraction (in production, use NLP)
        chosen = []
        rejected = []
        reasons = []
        
        # Extract chosen (simple regex)
        chosen_patterns = [
            r'wybrali?my (\w+)',
            r'decided on (\w+)',
            r'going with (\w+)'
        ]
        
        for pattern in chosen_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            chosen.extend(matches)
        
        if chosen:
            self.neo4j.add_decision(
                decision_id=message_id,
                project_id=project_id,
                decision_text=content[:200],
                decided_by=decided_by,
                chosen=chosen,
                rejected=rejected,
                reasons=reasons,
                timestamp=timestamp
            )


if __name__ == "__main__":
    # Example usage
    print("Neo4j Knowledge Graph Integration for Destiny Team")
    print("=" * 60)
    print("\nConnection format:")
    print('  uri = "bolt://localhost:7687"')
    print('  user = "neo4j"')
    print('  password = "your_password"')
