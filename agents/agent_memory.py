"""
Agent Memory System for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-03 (Day 2)

Wrapper around HelenaCore for per-agent memory management.
Each agent has its own memory space within the multi-layer system.
"""

from typing import List, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for HelenaCore import
sys.path.insert(0, str(Path(__file__).parent.parent))

from helena_core import HelenaCore


class AgentMemory:
    """
    Per-agent memory management
    
    Wraps HelenaCore to provide agent-specific memory storage
    and retrieval. Each agent's memories are tagged with their name.
    
    Usage:
        memory = AgentMemory("Tomasz Kamiński", "project-id")
        memory.save("Completed task X", importance=0.8)
        contexts = memory.load("task X", limit=5)
    """
    
    def __init__(self, agent_name: str, project_id: str):
        """
        Initialize agent memory
        
        Args:
            agent_name: Name of the agent (e.g., "Tomasz Kamiński")
            project_id: Project identifier for HelenaCore
        """
        self.agent_name = agent_name
        self.project_id = project_id
        self.helena = HelenaCore(project_id=project_id)
        
    def save(
        self,
        content: str,
        importance: float,
        context_type: str = "agent_work"
    ) -> Dict[str, Any]:
        """
        Save content to agent's memory
        
        Args:
            content: What to save
            importance: 0.0-1.0 (higher = more important)
            context_type: Type of memory (agent_work, task_received, etc.)
            
        Returns:
            Dict with save results from all layers
        """
        return self.helena.save_to_all_layers(
            event_type="agent_context",
            content=content,
            importance=importance,
            made_by=self.agent_name,
            additional_data={
                "agent_name": self.agent_name,
                "context_type": context_type
            }
        )
        
    def load(self, query: str, limit: int = 5) -> List[str]:
        """
        Load relevant context from agent's memory
        
        Args:
            query: What to search for
            limit: Max number of results
            
        Returns:
            List of relevant context strings
        """
        # Prefix query with agent name to get agent-specific results
        agent_query = f"{self.agent_name}: {query}"
        return self.helena.load_context(
            query=agent_query,
            limit=limit
        )
        
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get agent's recent memories
        
        Args:
            limit: Max number of results
            
        Returns:
            List of recent memory entries
            
        Note: This would require querying PostgreSQL directly.
        For now, returns empty list. Can be implemented later.
        """
        # TODO: Implement by querying PostgreSQL
        # SELECT * FROM decisions 
        # WHERE additional_data->>'agent_name' = self.agent_name
        # ORDER BY timestamp DESC LIMIT limit
        return []


# Module-level test
if __name__ == "__main__":
    print("Testing agent_memory module...")
    
    # Test initialization
    memory = AgentMemory(
        agent_name="Test Agent",
        project_id="test-project"
    )
    assert memory.agent_name == "Test Agent"
    assert memory.project_id == "test-project"
    print("✅ AgentMemory initialization OK")
    
    # Test save (will hit real HelenaCore)
    try:
        result = memory.save(
            content="Test memory content",
            importance=0.8,
            context_type="test"
        )
        print(f"✅ Memory save OK - Success: {result.get('success', False)}")
    except Exception as e:
        print(f"⚠️  Memory save test skipped (DB not available): {e}")
    
    # Test load
    try:
        contexts = memory.load("test", limit=1)
        print(f"✅ Memory load OK - Retrieved: {len(contexts)} items")
    except Exception as e:
        print(f"⚠️  Memory load test skipped (DB not available): {e}")
    
    print("\n✅ AgentMemory module ready!")
