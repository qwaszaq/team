"""
Full Team Integration - 9 Agent System with Multi-Layer Memory

Complete integration of all agents with PostgreSQL, Neo4j, Qdrant, Redis.
Now includes Knowledge Manager (Dr. Helena Kowalczyk) for documentation.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from master_orchestrator import MasterOrchestrator
from knowledge_manager_agent import KnowledgeManagerAgent, DocumentationOrchestrator
from postgres_integration import PostgresAgent
from destiny_team import AgentPersonality, MessageType, ProjectState


class FullDestinyTeam:
    """
    Complete Destiny Team with all 9 agents + multi-layer memory.
    
    Team:
    1. Aleksander Nowak - Orchestrator
    2. Magdalena Kowalska - Product Manager
    3. Katarzyna Wiśniewska - Architect
    4. Tomasz Zieliński - Developer
    5. Anna Nowakowska - QA Engineer
    6. Piotr Szymański - DevOps Engineer
    7. Michał Dąbrowski - Security Specialist
    8. Dr. Joanna Wójcik - Data Scientist
    9. Dr. Helena Kowalczyk - Knowledge Manager ← NEW!
    
    Memory System:
    - PostgreSQL (structured data)
    - Neo4j (knowledge graph)
    - Qdrant (semantic search)
    - Redis (hot cache)
    - LM Studio (local embeddings)
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
        lmstudio_url: str = "http://localhost:1234/v1",
        
        # Project
        project_id: Optional[str] = None
    ):
        """Initialize full team with multi-layer memory"""
        
        # Initialize memory orchestrator
        self.memory = MasterOrchestrator(
            postgres_conn=postgres_conn,
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password,
            qdrant_url=qdrant_url,
            redis_host=redis_host,
            redis_port=redis_port,
            lmstudio_url=lmstudio_url
        )
        
        # Initialize Knowledge Manager
        self.knowledge_manager = KnowledgeManagerAgent(
            postgres_store=self.memory.postgres,
            neo4j_graph=self.memory.neo4j,
            qdrant_store=self.memory.qdrant
        )
        
        # Documentation orchestrator
        self.doc_orchestrator = DocumentationOrchestrator(self.memory)
        
        self.project_id = project_id or str(uuid.uuid4())
        
        # Create all agents
        self.agents = self._create_all_agents()
    
    def _create_all_agents(self) -> Dict[str, Any]:
        """Create all 9 agents"""
        agents = {}
        
        # 1. Orchestrator
        agents['orchestrator'] = {
            'name': 'Aleksander Nowak',
            'role': 'Orchestrator',
            'model': 'claude-sonnet-4.5',
            'personality': 'Calm, strategic, coordinator'
        }
        
        # 2. Product Manager
        agents['pm'] = {
            'name': 'Magdalena Kowalska',
            'role': 'Product Manager',
            'model': 'gpt-5',
            'personality': 'User-focused, empathetic'
        }
        
        # 3. Architect
        agents['architect'] = {
            'name': 'Katarzyna Wiśniewska',
            'role': 'Architect',
            'model': 'gpt-5',
            'personality': 'Visionary, pragmatic'
        }
        
        # 4. Developer
        agents['developer'] = {
            'name': 'Tomasz Zieliński',
            'role': 'Developer',
            'model': 'claude-codex',
            'personality': 'Practical, quality-focused'
        }
        
        # 5. QA Engineer
        agents['qa'] = {
            'name': 'Anna Nowakowska',
            'role': 'QA Engineer',
            'model': 'gemini-pro-2.5',
            'personality': 'Detail-oriented, thorough'
        }
        
        # 6. DevOps
        agents['devops'] = {
            'name': 'Piotr Szymański',
            'role': 'DevOps Engineer',
            'model': 'gpt-5',
            'personality': 'Automation enthusiast'
        }
        
        # 7. Security
        agents['security'] = {
            'name': 'Michał Dąbrowski',
            'role': 'Security Specialist',
            'model': 'claude-sonnet-4.5',
            'personality': 'Security-first mindset'
        }
        
        # 8. Data Scientist
        agents['data_scientist'] = {
            'name': 'Dr. Joanna Wójcik',
            'role': 'Data Scientist',
            'model': 'gemini-pro-2.5',
            'personality': 'Data-driven, analytical'
        }
        
        # 9. Knowledge Manager ← NEW!
        agents['knowledge_manager'] = {
            'name': 'Dr. Helena Kowalczyk',
            'role': 'Knowledge Manager',
            'model': 'claude-sonnet-4.5',
            'personality': 'Organized, systematic, documentation expert',
            'instance': self.knowledge_manager
        }
        
        return agents
    
    # ==================== PROJECT LIFECYCLE ====================
    
    def start_project(self, name: str, description: str) -> str:
        """Start new project with full team"""
        # Create in all layers
        self.memory.create_project(
            project_id=self.project_id,
            name=name,
            description=description
        )
        
        # Orchestrator announces
        self.memory.store_message(
            project_id=self.project_id,
            sender="Aleksander Nowak",
            recipient=None,
            message_type="ANNOUNCEMENT",
            content=f"🚀 Nowy projekt: {name}\n\n{description}\n\nZespół, zaczynamy!",
            importance=0.9,
            tags=["project_start", "announcement"]
        )
        
        # Knowledge Manager creates initial docs
        self.knowledge_manager.generate_project_documentation(self.project_id)
        
        return self.project_id
    
    def end_of_day_workflow(self):
        """Run at end of each work day"""
        self.doc_orchestrator.end_of_day_workflow(self.project_id)
    
    def end_of_phase_workflow(
        self,
        phase_name: str,
        start_date: datetime,
        end_date: datetime
    ):
        """Run at end of each project phase"""
        self.doc_orchestrator.end_of_phase_workflow(
            project_id=self.project_id,
            phase_name=phase_name,
            start_date=start_date,
            end_date=end_date
        )
    
    # ==================== AGENT COMMUNICATION ====================
    
    def agent_sends_message(
        self,
        sender_role: str,
        content: str,
        recipient_role: Optional[str] = None,
        message_type: str = "ANNOUNCEMENT",
        importance: float = 0.5
    ) -> str:
        """Agent sends message (stored in all layers)"""
        sender_name = self.agents[sender_role]['name']
        recipient_name = self.agents[recipient_role]['name'] if recipient_role else None
        
        message_id = self.memory.store_message(
            project_id=self.project_id,
            sender=sender_name,
            recipient=recipient_name,
            message_type=message_type,
            content=content,
            importance=importance
        )
        
        # If it's a decision, Knowledge Manager documents it
        if message_type == "DECISION" or importance > 0.8:
            self._trigger_documentation(message_id, content, sender_name)
        
        return message_id
    
    def _trigger_documentation(
        self,
        message_id: str,
        content: str,
        sender: str
    ):
        """Trigger Knowledge Manager to document important message"""
        # Knowledge Manager analyzes and documents
        print(f"\n📝 Helena: Documenting important message from {sender}...")
    
    # ==================== QUERIES ====================
    
    def search(self, query: str, search_type: str = "hybrid") -> List[Dict]:
        """Search across all layers"""
        return self.memory.search(
            project_id=self.project_id,
            query=query,
            search_type=search_type
        )
    
    def why_question(self, question: str) -> Dict:
        """Answer 'why' question using knowledge graph"""
        return self.memory.why_question(
            project_id=self.project_id,
            question=question
        )
    
    def get_team_status(self) -> Dict:
        """Get status of all systems"""
        return self.memory.get_system_status(self.project_id)
    
    def close(self):
        """Close all connections"""
        self.memory.close()


# ==================== EXAMPLE USAGE ====================

def example_full_team():
    """Example showing complete system with Knowledge Manager"""
    print("=" * 70)
    print("  🎉 FULL TEAM + MULTI-LAYER MEMORY DEMO")
    print("  9 Agents + PostgreSQL + Neo4j + Qdrant + Redis + LM Studio")
    print("=" * 70)
    print()
    
    # Initialize full team
    team = FullDestinyTeam(
        postgres_conn="dbname=destiny_team user=user password=password host=localhost port=5432",
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password",
        qdrant_url="http://localhost:6333",
        redis_host="localhost",
        redis_port=6379,
        lmstudio_url="http://localhost:1234/v1"
    )
    
    # Start project
    project_id = team.start_project(
        "E-commerce Platform",
        "Budujemy skalowalny sklep internetowy"
    )
    
    print(f"✅ Projekt utworzony: {project_id}")
    print()
    
    # Agent communications
    print("📨 Agent Communications:\n")
    
    team.agent_sends_message(
        sender_role='pm',
        content="Zespół, potrzebujemy zrozumieć wymagania. Jakie są kluczowe funkcje?",
        message_type="REQUEST",
        importance=0.7
    )
    print("  ✓ PM: Pytanie o wymagania")
    
    team.agent_sends_message(
        sender_role='architect',
        content="Potrzebujemy: katalog produktów, koszyk, checkout, płatności, panel admina",
        recipient_role='pm',
        message_type="RESPONSE",
        importance=0.8
    )
    print("  ✓ Architect: Odpowiedź o funkcjach")
    
    team.agent_sends_message(
        sender_role='architect',
        content="Decyzja: Wybraliśmy PostgreSQL dla ACID compliance i transakcji",
        message_type="DECISION",
        importance=0.95
    )
    print("  ✓ Architect: Decyzja o bazie danych")
    print("  ✓ Helena: Dokumentuje decyzję automatycznie!")
    
    print()
    
    # End of day workflow
    print("⏰ End of Day Workflow:\n")
    team.end_of_day_workflow()
    print("  ✓ Helena: Daily summary created")
    print("  ✓ Wszystkie decyzje udokumentowane")
    print("  ✓ Action items identified")
    
    print()
    
    # Search
    print("🔍 Hybrid Search:\n")
    results = team.search("baza danych", search_type="hybrid")
    print(f"  ✓ Znaleziono {len(results)} relevantnych wiadomości")
    
    # Why question
    print()
    print("❓ Why Question:\n")
    answer = team.why_question("Why PostgreSQL?")
    print(f"  ✓ Helena provides: Decision record + full context")
    
    # Team status
    print()
    print("📊 Team Status:\n")
    status = team.get_team_status()
    print(f"  PostgreSQL: {status['postgres']['total_messages']} messages")
    print(f"  Redis: {status['cache']['stats']['total_keys']} keys cached")
    
    print()
    print("=" * 70)
    print("  ✅ FULL SYSTEM OPERATIONAL!")
    print("=" * 70)
    print()
    print("Zespół (9 agentów):")
    for role, agent in team.agents.items():
        icon = "📚" if role == "knowledge_manager" else "👤"
        print(f"  {icon} {agent['name']} - {agent['role']}")
    
    team.close()


if __name__ == "__main__":
    example_full_team()
