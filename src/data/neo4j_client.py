"""
Neo4j Graph Database Client
Paweł Kowalski
2025-11-05
"""

import urllib.request
import urllib.error
import json
import base64
from typing import List, Dict, Any, Optional


class Neo4jClient:
    """
    Neo4j graph database client for relationship analysis
    
    Features:
    - Entity relationship mapping
    - Financial flow analysis
    - Timeline analysis
    - Graph traversal queries
    
    Use for:
    - Financial transaction networks
    - Entity connections
    - Fraud detection patterns
    - Temporal relationship analysis
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 7474,
        username: str = "neo4j",
        password: str = "destiny_dev_2024"
    ):
        """
        Initialize Neo4j client
        
        Args:
            host: Neo4j host
            port: Neo4j HTTP port
            username: Username
            password: Password
        """
        self.base_url = f"http://{host}:{port}"
        self.username = username
        self.password = password
        self.available = self._check_availability()
    
    def _get_auth_header(self) -> str:
        """Get basic auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    def _check_availability(self) -> bool:
        """Check if Neo4j is available"""
        try:
            req = urllib.request.Request(f"{self.base_url}/db/neo4j/tx/commit")
            req.add_header("Authorization", self._get_auth_header())
            req.add_header("Content-Type", "application/json")
            
            # Simple query
            data = {"statements": [{"statement": "RETURN 1"}]}
            req.data = json.dumps(data).encode('utf-8')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    def execute_cypher(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute Cypher query
        
        Args:
            query: Cypher query
            parameters: Optional query parameters
            
        Returns:
            Query results
        """
        if not self.available:
            raise Exception("Neo4j not available")
        
        req = urllib.request.Request(f"{self.base_url}/db/neo4j/tx/commit")
        req.add_header("Authorization", self._get_auth_header())
        req.add_header("Content-Type", "application/json")
        
        data = {
            "statements": [
                {
                    "statement": query,
                    "parameters": parameters or {}
                }
            ]
        }
        
        req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Parse results
            results = []
            for statement_result in result.get('results', []):
                for row in statement_result.get('data', []):
                    results.append(row.get('row', []))
            
            return results
    
    def create_entity(
        self,
        case_id: str,
        entity_id: str,
        entity_type: str,
        properties: Dict[str, Any]
    ):
        """
        Create entity node
        
        Args:
            case_id: Case identifier
            entity_id: Entity identifier
            entity_type: Entity type (Person, Company, Account, etc.)
            properties: Entity properties
        """
        query = f"""
        MERGE (e:{entity_type} {{entity_id: $entity_id}})
        SET e.case_id = $case_id
        SET e += $properties
        RETURN e
        """
        
        params = {
            "case_id": case_id,
            "entity_id": entity_id,
            "properties": properties
        }
        
        return self.execute_cypher(query, params)
    
    def create_relationship(
        self,
        from_entity_id: str,
        to_entity_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        """
        Create relationship between entities
        
        Args:
            from_entity_id: Source entity ID
            to_entity_id: Target entity ID
            relationship_type: Relationship type (TRANSFERRED_TO, OWNS, etc.)
            properties: Relationship properties
        """
        query = f"""
        MATCH (a {{entity_id: $from_id}})
        MATCH (b {{entity_id: $to_id}})
        MERGE (a)-[r:{relationship_type}]->(b)
        SET r += $properties
        RETURN r
        """
        
        params = {
            "from_id": from_entity_id,
            "to_id": to_entity_id,
            "properties": properties or {}
        }
        
        return self.execute_cypher(query, params)
    
    def find_paths(
        self,
        from_entity_id: str,
        to_entity_id: str,
        max_depth: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find paths between two entities
        
        Args:
            from_entity_id: Source entity
            to_entity_id: Target entity
            max_depth: Maximum path length
            
        Returns:
            List of paths
        """
        query = f"""
        MATCH path = (a {{entity_id: $from_id}})-[*1..{max_depth}]-(b {{entity_id: $to_id}})
        RETURN path
        LIMIT 10
        """
        
        params = {
            "from_id": from_entity_id,
            "to_id": to_entity_id
        }
        
        return self.execute_cypher(query, params)
    
    def analyze_financial_flows(
        self,
        case_id: str,
        min_amount: float = 0
    ) -> List[Dict[str, Any]]:
        """
        Analyze financial transaction flows
        
        Args:
            case_id: Case identifier
            min_amount: Minimum transaction amount
            
        Returns:
            Financial flow analysis
        """
        query = """
        MATCH (a)-[t:TRANSFERRED_TO]->(b)
        WHERE a.case_id = $case_id 
        AND t.amount >= $min_amount
        RETURN a.entity_id as from_entity,
               b.entity_id as to_entity,
               t.amount as amount,
               t.date as date
        ORDER BY t.amount DESC
        """
        
        params = {
            "case_id": case_id,
            "min_amount": min_amount
        }
        
        return self.execute_cypher(query, params)
    
    def get_entity_connections(
        self,
        entity_id: str,
        depth: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get all connections for an entity
        
        Args:
            entity_id: Entity identifier
            depth: Relationship depth
            
        Returns:
            Connected entities
        """
        query = f"""
        MATCH (e {{entity_id: $entity_id}})-[r*1..{depth}]-(connected)
        RETURN DISTINCT connected.entity_id as connected_entity,
               type(r[0]) as relationship_type
        """
        
        params = {"entity_id": entity_id}
        
        return self.execute_cypher(query, params)
    
    def detect_cycles(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Detect circular relationships (potential fraud indicator)
        
        Args:
            case_id: Case identifier
            
        Returns:
            Detected cycles
        """
        query = """
        MATCH path = (a)-[*3..5]->(a)
        WHERE a.case_id = $case_id
        RETURN path
        LIMIT 10
        """
        
        params = {"case_id": case_id}
        
        return self.execute_cypher(query, params)
    
    def get_graph_stats(self, case_id: str) -> Dict[str, Any]:
        """
        Get graph statistics for a case
        
        Args:
            case_id: Case identifier
            
        Returns:
            Graph statistics
        """
        # Count nodes
        node_query = """
        MATCH (n {case_id: $case_id})
        RETURN count(n) as node_count
        """
        
        # Count relationships
        rel_query = """
        MATCH (a {case_id: $case_id})-[r]->()
        RETURN count(r) as rel_count
        """
        
        nodes = self.execute_cypher(node_query, {"case_id": case_id})
        rels = self.execute_cypher(rel_query, {"case_id": case_id})
        
        return {
            "nodes": nodes[0][0] if nodes else 0,
            "relationships": rels[0][0] if rels else 0
        }


def test_neo4j_client():
    """Test Neo4j client"""
    print("🧪 Testing Neo4j Client...\n")
    
    # Initialize
    print("1. Connecting to Neo4j...")
    client = Neo4jClient()
    
    if not client.available:
        print("   ⚠️  Neo4j not available - start with: docker-compose up -d neo4j")
        return
    
    print("   ✅ Neo4j connected")
    
    # Create test entities
    print("\n2. Creating test entities...")
    client.create_entity(
        case_id="test_case",
        entity_id="company_a",
        entity_type="Company",
        properties={"name": "Company A", "industry": "Tech"}
    )
    
    client.create_entity(
        case_id="test_case",
        entity_id="company_b",
        entity_type="Company",
        properties={"name": "Company B", "industry": "Finance"}
    )
    print("   ✅ Entities created")
    
    # Create relationship
    print("\n3. Creating relationship...")
    client.create_relationship(
        from_entity_id="company_a",
        to_entity_id="company_b",
        relationship_type="TRANSFERRED_TO",
        properties={"amount": 100000, "date": "2024-Q4"}
    )
    print("   ✅ Relationship created")
    
    # Get connections
    print("\n4. Getting entity connections...")
    connections = client.get_entity_connections("company_a")
    print(f"   ✅ Found {len(connections)} connections")
    
    # Get stats
    print("\n5. Graph statistics...")
    stats = client.get_graph_stats("test_case")
    print(f"   Nodes: {stats['nodes']}")
    print(f"   Relationships: {stats['relationships']}")
    
    print("\n✅ Neo4j tests complete!")


if __name__ == "__main__":
    test_neo4j_client()
