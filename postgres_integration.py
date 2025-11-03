"""
Integration between Destiny Team agents and PostgreSQL unlimited context store.

This module adapts the existing Agent classes to use PostgreSQL for unlimited context.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from postgres_context_store import PostgresContextStore, StoredMessage, AgentWithUnlimitedContext
from destiny_team import (
    Agent, AgentPersonality, MessageBus, ProjectState,
    MessageType as OriginalMessageType
)


class PostgresMessageBus(MessageBus):
    """
    Enhanced MessageBus that stores all messages in PostgreSQL.
    
    This gives the team unlimited conversation history that persists
    across sessions and can be queried intelligently.
    """
    
    def __init__(self, context_store: PostgresContextStore, project_id: str):
        super().__init__()
        self.context_store = context_store
        self.project_id = project_id
    
    def post(self, message):
        """Post message and store in PostgreSQL"""
        # Store in PostgreSQL
        stored_msg = StoredMessage(
            id=message.id,
            project_id=self.project_id,
            sender=message.sender,
            recipient=message.recipient,
            message_type=message.message_type.value,
            content=message.content,
            context=message.context,
            timestamp=message.timestamp,
            requires_response=message.requires_response,
            response_to=message.response_to,
            importance=self._calculate_importance(message),
            tags=self._extract_tags(message)
        )
        
        self.context_store.store_message(stored_msg)
        
        # Also route through regular message bus
        super().post(message)
    
    def _calculate_importance(self, message) -> float:
        """Calculate message importance score"""
        importance = 0.5  # Base importance
        
        # Critical message types
        if message.message_type in [OriginalMessageType.APPROVAL, OriginalMessageType.DEBATE]:
            importance += 0.3
        
        # Requires response means important
        if message.requires_response:
            importance += 0.2
        
        return min(importance, 1.0)
    
    def _extract_tags(self, message) -> List[str]:
        """Extract relevant tags from message for indexing"""
        tags = []
        
        # Add message type as tag
        tags.append(message.message_type.value.lower())
        
        # Extract key concepts from content (simple version)
        content_lower = message.content.lower()
        
        concept_keywords = [
            'architecture', 'security', 'testing', 'deployment', 'database',
            'api', 'frontend', 'backend', 'performance', 'bug', 'feature',
            'requirement', 'design', 'implementation', 'review', 'approval'
        ]
        
        for keyword in concept_keywords:
            if keyword in content_lower:
                tags.append(keyword)
        
        return tags


class PostgresAgent(Agent):
    """
    Enhanced Agent with unlimited context via PostgreSQL.
    
    Instead of keeping conversation history in memory (limited by token windows),
    this agent retrieves relevant context from PostgreSQL on demand.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        personality: AgentPersonality,
        model_name: str,
        message_bus: PostgresMessageBus,
        context_store: PostgresContextStore,
        project_id: str,
        context_window_size: int = 100000
    ):
        super().__init__(name, role, personality, model_name, message_bus, context_window_size)
        self.context_store = context_store
        self.project_id = project_id
    
    def think(
        self,
        prompt: str,
        project_state: ProjectState,
        include_shared_knowledge: bool = True,
        max_context_messages: int = 30
    ) -> str:
        """
        Think with UNLIMITED context access via PostgreSQL.
        
        Instead of managing token windows, we retrieve only the most
        relevant messages from our unlimited PostgreSQL history.
        """
        # Retrieve relevant context from PostgreSQL
        relevant_messages = self.context_store.get_relevant_context_for_agent(
            agent_name=self.name,
            project_id=self.project_id,
            query=prompt,
            max_messages=max_context_messages,
            time_window_days=None,  # Search all time
            min_importance=0.3  # Only moderately important or higher
        )
        
        # Get personal knowledge base from PostgreSQL
        personal_context = self.context_store.get_agent_context(
            agent_name=self.name,
            project_id=self.project_id
        )
        
        # Build comprehensive context prompt
        context_prompt = self._build_postgres_context(
            prompt,
            project_state,
            relevant_messages,
            personal_context
        )
        
        # In production: Call actual AI model
        # response = call_cursor_ai(context_prompt, model=self.model_name)
        
        # For now, simulate
        response = self._generate_response(prompt, project_state)
        
        # Store this thinking session in agent's context
        self.context_store.store_agent_context(
            agent_name=self.name,
            project_id=self.project_id,
            context_key=f"thought_{datetime.now().isoformat()}",
            context_value={
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat()
            },
            importance=0.3
        )
        
        return response
    
    def _build_postgres_context(
        self,
        prompt: str,
        project_state: ProjectState,
        relevant_messages: List[StoredMessage],
        personal_context: Dict[str, Any]
    ) -> str:
        """Build context from PostgreSQL data"""
        parts = []
        
        # Agent identity
        parts.append(f"You are {self.name}, a {self.role}.")
        parts.append(f"Personality: {', '.join(self.personality.traits)}")
        parts.append(f"Communication style: {self.personality.communication_style}")
        
        # Personal knowledge base
        if personal_context:
            parts.append("\n--- YOUR ACCUMULATED KNOWLEDGE ---")
            important_items = sorted(
                personal_context.items(),
                key=lambda x: x[1]['importance'],
                reverse=True
            )[:10]  # Top 10 most important
            
            for key, data in important_items:
                parts.append(f"• {key}: {data['value']}")
        
        # Project context
        parts.append(f"\n--- PROJECT: {project_state.project_name} ---")
        parts.append(f"Phase: {project_state.current_phase.value}")
        parts.append(f"Description: {project_state.description}")
        
        # Relevant conversation history
        if relevant_messages:
            parts.append("\n--- RELEVANT TEAM COMMUNICATIONS (from unlimited history) ---")
            for msg in relevant_messages[:15]:  # Top 15 most relevant
                time_str = msg.timestamp.strftime("%Y-%m-%d %H:%M")
                recipient_str = msg.recipient if msg.recipient else "EVERYONE"
                parts.append(f"[{time_str}] {msg.sender} → {recipient_str}:")
                parts.append(f"  {msg.content[:200]}...")  # Truncate long messages
                parts.append("")
        
        # Current prompt
        parts.append("\n--- CURRENT QUESTION ---")
        parts.append(prompt)
        
        return "\n".join(parts)
    
    def add_to_context(self, key: str, value: Any, importance: float = 0.5):
        """
        Add to agent's personal context, stored in PostgreSQL.
        
        This replaces the in-memory context with persistent storage.
        """
        self.context_store.store_agent_context(
            agent_name=self.name,
            project_id=self.project_id,
            context_key=key,
            context_value=value,
            importance=importance
        )
        
        # Also update in-memory for compatibility
        super().add_to_context(key, value)
    
    def get_my_conversation_history(self, limit: int = 50) -> List[StoredMessage]:
        """Get this agent's conversation history from PostgreSQL"""
        return self.context_store.get_agent_conversation_history(
            agent_name=self.name,
            project_id=self.project_id,
            limit=limit
        )
    
    def search_past_conversations(self, query: str) -> List[StoredMessage]:
        """Search through unlimited conversation history"""
        return self.context_store.search_messages(
            project_id=self.project_id,
            search_query=query,
            limit=30
        )


class DestinyTeamWithPostgres:
    """
    Destiny Team with PostgreSQL unlimited context storage.
    
    This is the main class you'll use - it creates a team where all agents
    have access to unlimited context via PostgreSQL.
    """
    
    def __init__(
        self,
        postgres_connection_string: str,
        project_id: Optional[str] = None
    ):
        """
        Initialize team with PostgreSQL backend.
        
        Args:
            postgres_connection_string: PostgreSQL connection string
                Example: "dbname=destiny_team user=artur host=localhost"
            project_id: Optional project ID (generated if not provided)
        """
        self.context_store = PostgresContextStore(postgres_connection_string)
        self.project_id = project_id or str(uuid.uuid4())
        self.message_bus = PostgresMessageBus(self.context_store, self.project_id)
        
        # Create agents with PostgreSQL integration
        self.agents = self._create_agents()
        
        # Register all agents
        for agent in self.agents.values():
            self.message_bus.register_agent(agent)
    
    def _create_agents(self) -> Dict[str, PostgresAgent]:
        """Create all agents with PostgreSQL context"""
        agents = {}
        
        # Orchestrator
        agents['orchestrator'] = PostgresAgent(
            name="Aleksander Nowak",
            role="Orchestrator",
            personality=AgentPersonality(
                name="Aleksander Nowak",
                role="Orchestrator",
                traits=["calm", "strategic", "coordinator"],
                tendencies=["always has backup plans"],
                communication_style="Clear, structured"
            ),
            model_name="claude-sonnet-4.5",
            message_bus=self.message_bus,
            context_store=self.context_store,
            project_id=self.project_id
        )
        
        # Product Manager
        agents['pm'] = PostgresAgent(
            name="Magdalena Kowalska",
            role="Product Manager",
            personality=AgentPersonality(
                name="Magdalena Kowalska",
                role="Product Manager",
                traits=["user-focused", "empathetic", "questioning"],
                tendencies=["asks great questions", "can scope creep"],
                communication_style="Empathetic, business-focused"
            ),
            model_name="gpt-5",
            message_bus=self.message_bus,
            context_store=self.context_store,
            project_id=self.project_id
        )
        
        # Architect
        agents['architect'] = PostgresAgent(
            name="Katarzyna Wiśniewska",
            role="Architect",
            personality=AgentPersonality(
                name="Katarzyna Wiśniewska",
                role="Architect",
                traits=["visionary", "pragmatic", "elegant"],
                tendencies=["can over-engineer"],
                communication_style="Technical but clear"
            ),
            model_name="gpt-5",
            message_bus=self.message_bus,
            context_store=self.context_store,
            project_id=self.project_id
        )
        
        # Developer
        agents['developer'] = PostgresAgent(
            name="Tomasz Zieliński",
            role="Developer",
            personality=AgentPersonality(
                name="Tomasz Zieliński",
                role="Developer",
                traits=["practical", "quality-focused", "efficient"],
                tendencies=["can get lost in optimization"],
                communication_style="Direct, solution-focused"
            ),
            model_name="claude-codex",
            message_bus=self.message_bus,
            context_store=self.context_store,
            project_id=self.project_id
        )
        
        # Add other agents similarly...
        
        return agents
    
    def start_project(self, project_name: str, description: str) -> str:
        """Start a new project with PostgreSQL storage"""
        # Create project in PostgreSQL
        self.context_store.create_project(
            project_id=self.project_id,
            project_name=project_name,
            description=description,
            metadata={"created_by": "user"}
        )
        
        # Orchestrator announces project
        orchestrator = self.agents['orchestrator']
        orchestrator.send_message(
            recipient=None,
            message_type=OriginalMessageType.ANNOUNCEMENT,
            content=f"🚀 New project: {project_name}\n\n{description}\n\nTeam, let's begin!",
            context={"project_id": self.project_id}
        )
        
        return self.project_id
    
    def get_project_summary(self) -> Dict[str, Any]:
        """Get comprehensive project summary from PostgreSQL"""
        stats = self.context_store.get_project_statistics(self.project_id)
        
        # Get each agent's activity
        agent_activities = {}
        for agent_name, agent in self.agents.items():
            agent_activities[agent_name] = self.context_store.get_agent_activity_summary(
                project_id=self.project_id,
                agent_name=agent.name
            )
        
        return {
            "project_stats": stats,
            "agent_activities": agent_activities
        }
    
    def search_project_history(self, query: str) -> List[StoredMessage]:
        """Search through entire project history"""
        return self.context_store.search_messages(
            project_id=self.project_id,
            search_query=query,
            limit=50
        )
    
    def get_all_debates(self) -> List[StoredMessage]:
        """Get all debate messages - useful for seeing team discussions"""
        return self.context_store.get_messages_by_type(
            project_id=self.project_id,
            message_type="DEBATE",
            limit=100
        )
    
    def close(self):
        """Close PostgreSQL connection"""
        self.context_store.close()


# ==================== EXAMPLE USAGE ====================

def example_usage():
    """
    Example showing how to use Destiny Team with unlimited PostgreSQL context.
    """
    
    # Step 1: Initialize team with PostgreSQL
    team = DestinyTeamWithPostgres(
        postgres_connection_string="dbname=destiny_team user=artur host=localhost"
    )
    
    # Step 2: Start a project
    project_id = team.start_project(
        project_name="E-commerce Platform",
        description="Build a scalable e-commerce platform with payment integration"
    )
    
    print(f"✅ Project started: {project_id}")
    
    # Step 3: Agents communicate (all stored in PostgreSQL)
    pm = team.agents['pm']
    pm.send_message(
        recipient=None,
        message_type=OriginalMessageType.REQUEST,
        content="Team, I need to understand the requirements better. What are the key features?"
    )
    
    # Step 4: Agent thinks with unlimited context
    architect = team.agents['architect']
    response = architect.think(
        prompt="Design the system architecture for this e-commerce platform",
        project_state=ProjectState(
            project_name="E-commerce Platform",
            description="Build a scalable e-commerce platform"
        )
    )
    
    print(f"\n🏗️ Architect's response:\n{response}")
    
    # Step 5: Search through unlimited history
    security_discussions = team.search_project_history("security authentication payment")
    print(f"\n🔍 Found {len(security_discussions)} messages about security")
    
    # Step 6: Get project statistics
    summary = team.get_project_summary()
    print(f"\n📊 Project Summary:")
    print(f"  Total messages: {summary['project_stats']['total_messages']}")
    print(f"  Active agents: {summary['project_stats']['active_agents']}")
    
    # Step 7: Close connection
    team.close()


if __name__ == "__main__":
    print("PostgreSQL Integration for Destiny Team")
    print("=" * 60)
    print("\nThis module integrates unlimited context storage with your agent team.")
    print("\nKey features:")
    print("  ✓ Unlimited conversation history (no token limits)")
    print("  ✓ Intelligent context retrieval (relevance-based)")
    print("  ✓ Persistent across sessions")
    print("  ✓ Searchable and analyzable")
    print("  ✓ Per-agent knowledge bases")
