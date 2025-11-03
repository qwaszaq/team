"""
Agent Registry for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-03 (Day 2)

Agent discovery and management system.
"""

from typing import Dict, List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent, AgentStatus


class AgentRegistry:
    """
    Agent registry for discovery and management
    
    Maintains a directory of all agents in the system.
    Provides lookup by name, role, status, etc.
    
    Usage:
        registry = AgentRegistry()
        registry.register(agent)
        agent = registry.get_agent("Agent Name")
        available = registry.get_available_agents()
    """
    
    def __init__(self):
        """Initialize empty registry"""
        self.agents: Dict[str, BaseAgent] = {}
        
    def register(self, agent: BaseAgent):
        """
        Register an agent
        
        Args:
            agent: Agent to register
        """
        self.agents[agent.name] = agent
        print(f"📋 Registered: {agent.name} ({agent.role})")
        
    def unregister(self, agent_name: str) -> bool:
        """
        Unregister an agent
        
        Args:
            agent_name: Name of agent to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            print(f"📋 Unregistered: {agent_name}")
            return True
        return False
        
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Get agent by name
        
        Args:
            name: Agent name
            
        Returns:
            Optional[BaseAgent]: Agent or None
        """
        return self.agents.get(name)
        
    def get_all_agents(self) -> List[BaseAgent]:
        """
        Get all registered agents
        
        Returns:
            List[BaseAgent]: All agents
        """
        return list(self.agents.values())
        
    def get_available_agents(self) -> List[BaseAgent]:
        """
        Get agents with status AVAILABLE
        
        Returns:
            List[BaseAgent]: Available agents
        """
        return [a for a in self.agents.values() 
                if a.status == AgentStatus.AVAILABLE]
        
    def get_busy_agents(self) -> List[BaseAgent]:
        """
        Get agents with status BUSY
        
        Returns:
            List[BaseAgent]: Busy agents
        """
        return [a for a in self.agents.values() 
                if a.status == AgentStatus.BUSY]
        
    def find_by_role(self, role: str) -> List[BaseAgent]:
        """
        Find agents by role
        
        Args:
            role: Role to search for
            
        Returns:
            List[BaseAgent]: Agents with matching role
        """
        return [a for a in self.agents.values() 
                if a.role == role]
        
    def find_by_specialization(self, specialization: str) -> List[BaseAgent]:
        """
        Find agents by specialization (substring match)
        
        Args:
            specialization: Specialization to search for
            
        Returns:
            List[BaseAgent]: Agents with matching specialization
        """
        spec_lower = specialization.lower()
        return [a for a in self.agents.values() 
                if spec_lower in a.specialization.lower()]
        
    def get_agent_count(self) -> int:
        """
        Get total number of registered agents
        
        Returns:
            int: Agent count
        """
        return len(self.agents)
        
    def get_stats(self) -> Dict[str, int]:
        """
        Get registry statistics
        
        Returns:
            Dict with status counts
        """
        stats = {
            "total": len(self.agents),
            "available": 0,
            "busy": 0,
            "offline": 0,
            "error": 0
        }
        
        for agent in self.agents.values():
            if agent.status == AgentStatus.AVAILABLE:
                stats["available"] += 1
            elif agent.status == AgentStatus.BUSY:
                stats["busy"] += 1
            elif agent.status == AgentStatus.OFFLINE:
                stats["offline"] += 1
            elif agent.status == AgentStatus.ERROR:
                stats["error"] += 1
                
        return stats
        
    def list_agents(self) -> List[str]:
        """
        Get list of agent names
        
        Returns:
            List[str]: Agent names
        """
        return list(self.agents.keys())


# Module-level test
if __name__ == "__main__":
    print("Testing agent_registry module...")
    
    # Test initialization
    registry = AgentRegistry()
    assert len(registry.agents) == 0
    print("✅ AgentRegistry initialization OK")
    
    # Test register
    agent1 = BaseAgent("Agent 1", "Role 1", "Spec 1", "test")
    agent2 = BaseAgent("Agent 2", "Role 2", "Spec 2", "test")
    
    registry.register(agent1)
    registry.register(agent2)
    assert len(registry.agents) == 2
    print("✅ Register OK")
    
    # Test get agent
    retrieved = registry.get_agent("Agent 1")
    assert retrieved is not None
    assert retrieved.name == "Agent 1"
    print("✅ Get agent OK")
    
    # Test get all
    all_agents = registry.get_all_agents()
    assert len(all_agents) == 2
    print("✅ Get all agents OK")
    
    # Test find by role
    by_role = registry.find_by_role("Role 1")
    assert len(by_role) == 1
    assert by_role[0].name == "Agent 1"
    print("✅ Find by role OK")
    
    # Test get available
    available = registry.get_available_agents()
    assert len(available) == 2  # Both should be available
    print("✅ Get available OK")
    
    # Test stats
    stats = registry.get_stats()
    assert stats["total"] == 2
    assert stats["available"] == 2
    print("✅ Stats OK")
    
    # Test unregister
    removed = registry.unregister("Agent 1")
    assert removed == True
    assert len(registry.agents) == 1
    print("✅ Unregister OK")
    
    print("\n✅ AgentRegistry module ready!")
