"""
Cross-Team Communication System

Enables communication and collaboration between:
- Technical Team (9 agents)
- Analytical Team (9 agents)

Features:
- Unified agent registry (both teams)
- Cross-team task delegation
- Team discovery
- Communication bus (Redis-based)
"""

import sys
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.task_models import Task, TaskResult, TaskStatus
from agents.agent_registry import AgentRegistry


class UnifiedAgentRegistry:
    """
    Unified registry for both Technical and Analytical teams
    
    Allows agents from both teams to discover and communicate with each other.
    """
    
    def __init__(self):
        """Initialize unified registry"""
        self.technical_team = {}  # Technical team agents
        self.analytical_team = {}  # Analytical team agents
        self.all_agents = {}  # Combined registry
        
        print("🌉 Unified Agent Registry initialized")
    
    def register_technical_team(self, agents: List) -> None:
        """Register all technical team agents"""
        for agent in agents:
            self.technical_team[agent.name] = {
                "agent": agent,
                "team": "technical",
                "role": agent.role,
                "specialization": agent.specialization,
                "status": agent.status.value
            }
            self.all_agents[agent.name] = self.technical_team[agent.name]
        
        print(f"✅ Registered {len(agents)} Technical Team agents")
    
    def register_analytical_team(self, agents: List) -> None:
        """Register all analytical team agents"""
        for agent in agents:
            self.analytical_team[agent.name] = {
                "agent": agent,
                "team": "analytical",
                "role": agent.role,
                "specialization": agent.specialization,
                "status": agent.status.value
            }
            self.all_agents[agent.name] = self.analytical_team[agent.name]
        
        print(f"✅ Registered {len(agents)} Analytical Team agents")
    
    def find_agent(self, agent_name: str) -> Optional[Dict]:
        """Find agent by name across both teams"""
        return self.all_agents.get(agent_name)
    
    def find_agents_by_role(self, role_keyword: str) -> List[Dict]:
        """Find agents by role keyword (e.g., 'developer', 'analyst')"""
        results = []
        keyword_lower = role_keyword.lower()
        
        for name, info in self.all_agents.items():
            if keyword_lower in info["role"].lower() or keyword_lower in info["specialization"].lower():
                results.append({
                    "name": name,
                    "team": info["team"],
                    "role": info["role"],
                    "specialization": info["specialization"]
                })
        
        return results
    
    def find_agents_by_specialization(self, specialization: str) -> List[Dict]:
        """Find agents with specific specialization"""
        results = []
        spec_lower = specialization.lower()
        
        for name, info in self.all_agents.items():
            if spec_lower in info["specialization"].lower():
                results.append({
                    "name": name,
                    "team": info["team"],
                    "role": info["role"],
                    "specialization": info["specialization"]
                })
        
        return results
    
    def get_team_roster(self, team: str) -> List[Dict]:
        """Get all agents from a specific team"""
        if team == "technical":
            return [
                {
                    "name": name,
                    "role": info["role"],
                    "specialization": info["specialization"]
                }
                for name, info in self.technical_team.items()
            ]
        elif team == "analytical":
            return [
                {
                    "name": name,
                    "role": info["role"],
                    "specialization": info["specialization"]
                }
                for name, info in self.analytical_team.items()
            ]
        else:
            return []
    
    def get_all_agents(self) -> Dict[str, List[Dict]]:
        """Get all agents organized by team"""
        return {
            "technical": self.get_team_roster("technical"),
            "analytical": self.get_team_roster("analytical"),
            "total_agents": len(self.all_agents)
        }


class CrossTeamCommunicator:
    """
    Cross-team communication and task delegation
    
    Enables:
    - Agent discovery across teams
    - Cross-team task delegation
    - Collaborative workflows
    """
    
    def __init__(self, technical_team=None, analytical_team=None):
        """
        Initialize cross-team communicator
        
        Args:
            technical_team: Technical team instance
            analytical_team: Analytical team instance
        """
        self.registry = UnifiedAgentRegistry()
        self.technical_team = technical_team
        self.analytical_team = analytical_team
        
        # Register teams if provided
        if technical_team:
            self.registry.register_technical_team(technical_team.agents)
        if analytical_team:
            self.registry.register_analytical_team(analytical_team.agents)
        
        print("🌉 Cross-Team Communication Bridge established!")
    
    def find_expert(self, expertise: str) -> List[Dict]:
        """
        Find expert agents across both teams
        
        Args:
            expertise: What expertise is needed (e.g., "financial analysis", "web development")
        
        Returns:
            List of matching agents with their details
        """
        # Search by role and specialization
        by_role = self.registry.find_agents_by_role(expertise)
        by_spec = self.registry.find_agents_by_specialization(expertise)
        
        # Combine and deduplicate
        experts = {agent["name"]: agent for agent in (by_role + by_spec)}
        
        return list(experts.values())
    
    def delegate_cross_team(
        self,
        from_agent: str,
        to_agent: str,
        task_title: str,
        task_description: str,
        priority: str = "medium"
    ) -> TaskResult:
        """
        Delegate task from one team to another
        
        Args:
            from_agent: Requesting agent name
            to_agent: Target agent name
            task_title: Task title
            task_description: Task description
            priority: Task priority
        
        Returns:
            Task result
        """
        # Find target agent
        target_info = self.registry.find_agent(to_agent)
        
        if not target_info:
            print(f"❌ Agent '{to_agent}' not found in registry")
            return None
        
        target_team = target_info["team"]
        
        print(f"\n🔀 Cross-Team Delegation:")
        print(f"   From: {from_agent}")
        print(f"   To: {to_agent} ({target_team} team)")
        print(f"   Task: {task_title}")
        
        # Delegate to appropriate team
        if target_team == "technical" and self.technical_team:
            return self.technical_team.delegate_to_agent(
                agent_name=to_agent,
                task_title=task_title,
                task_description=task_description,
                priority=priority
            )
        elif target_team == "analytical" and self.analytical_team:
            return self.analytical_team.delegate_to_agent(
                agent_name=to_agent,
                task_title=task_title,
                task_description=task_description,
                priority=priority
            )
        else:
            print(f"❌ Team '{target_team}' not available")
            return None
    
    def collaborative_task(
        self,
        task_description: str,
        required_expertise: List[str],
        coordinator: str = "Aleksander Nowak"  # or "Viktor Kovalenko"
    ) -> Dict[str, TaskResult]:
        """
        Create collaborative task involving both teams
        
        Args:
            task_description: Overall task description
            required_expertise: List of required expertise areas
            coordinator: Which orchestrator coordinates (Aleksander or Viktor)
        
        Returns:
            Dict of results from each expert
        """
        print(f"\n🤝 COLLABORATIVE TASK:")
        print(f"   Description: {task_description}")
        print(f"   Coordinator: {coordinator}")
        print(f"   Required Expertise: {', '.join(required_expertise)}")
        print("=" * 60)
        
        # Find experts for each expertise area
        assigned_agents = {}
        for expertise in required_expertise:
            experts = self.find_expert(expertise)
            if experts:
                # Pick first available expert
                agent = experts[0]
                assigned_agents[expertise] = agent
                print(f"✓ {expertise}: {agent['name']} ({agent['team']} team)")
            else:
                print(f"⚠️  {expertise}: No expert found")
        
        # Execute tasks
        results = {}
        for expertise, agent in assigned_agents.items():
            task_title = f"{expertise.title()} for: {task_description[:50]}"
            task_desc = f"Provide {expertise} expertise for: {task_description}"
            
            result = self.delegate_cross_team(
                from_agent=coordinator,
                to_agent=agent["name"],
                task_title=task_title,
                task_description=task_desc,
                priority="high"
            )
            
            results[agent["name"]] = result
        
        print("\n" + "=" * 60)
        print(f"✅ Collaborative task complete: {len(results)} agents contributed")
        
        return results
    
    def get_team_capabilities(self) -> Dict:
        """Get overview of all team capabilities"""
        return {
            "technical_team": {
                "size": len(self.registry.technical_team),
                "capabilities": [
                    "Software Development",
                    "System Architecture",
                    "Database Design",
                    "DevOps & Infrastructure",
                    "UI/UX Design",
                    "QA & Testing",
                    "AI/ML Engineering",
                    "Documentation"
                ],
                "agents": self.registry.get_team_roster("technical")
            },
            "analytical_team": {
                "size": len(self.registry.analytical_team),
                "capabilities": [
                    "OSINT & Intelligence",
                    "Financial Analysis",
                    "Market Research",
                    "Legal Research",
                    "Data Analysis",
                    "Report Writing",
                    "Investigation",
                    "Document Processing"
                ],
                "agents": self.registry.get_team_roster("analytical")
            },
            "cross_team_enabled": True,
            "total_agents": len(self.registry.all_agents)
        }
    
    def recommend_collaboration(self, project_description: str) -> Dict:
        """
        Recommend which agents from both teams should collaborate
        
        Args:
            project_description: Description of the project
        
        Returns:
            Recommended team composition
        """
        desc_lower = project_description.lower()
        
        recommendations = {
            "project": project_description,
            "recommended_agents": [],
            "reasoning": []
        }
        
        # Technical team patterns
        if any(word in desc_lower for word in ["build", "develop", "code", "implement", "feature"]):
            recommendations["recommended_agents"].extend([
                {"name": "Aleksander Nowak", "team": "technical", "reason": "Orchestrator - project coordination"},
                {"name": "Tomasz Kamiński", "team": "technical", "reason": "Developer - implementation"}
            ])
            recommendations["reasoning"].append("Development work requires technical team")
        
        if any(word in desc_lower for word in ["database", "data model", "schema"]):
            recommendations["recommended_agents"].append(
                {"name": "Maria Wiśniewska", "team": "technical", "reason": "Database specialist"}
            )
        
        if any(word in desc_lower for word in ["ui", "ux", "design", "interface"]):
            recommendations["recommended_agents"].append(
                {"name": "Joanna Mazur", "team": "technical", "reason": "UI/UX Designer"}
            )
        
        # Analytical team patterns
        if any(word in desc_lower for word in ["investigate", "research", "osint", "intelligence"]):
            recommendations["recommended_agents"].extend([
                {"name": "Viktor Kovalenko", "team": "analytical", "reason": "Investigation Director"},
                {"name": "Elena Volkov", "team": "analytical", "reason": "OSINT Specialist"}
            ])
            recommendations["reasoning"].append("Investigation requires analytical team")
        
        if any(word in desc_lower for word in ["financial", "finance", "money", "investment"]):
            recommendations["recommended_agents"].append(
                {"name": "Marcus Chen", "team": "analytical", "reason": "Financial Analyst"}
            )
        
        if any(word in desc_lower for word in ["market", "competitor", "customer", "consumer"]):
            recommendations["recommended_agents"].append(
                {"name": "Sofia Martinez", "team": "analytical", "reason": "Market Research"}
            )
        
        if any(word in desc_lower for word in ["legal", "compliance", "regulation", "contract"]):
            recommendations["recommended_agents"].append(
                {"name": "Adrian Kowalski", "team": "analytical", "reason": "Legal Analyst"}
            )
        
        if any(word in desc_lower for word in ["data analysis", "statistics", "visualization", "dashboard"]):
            recommendations["recommended_agents"].append(
                {"name": "Maya Patel", "team": "analytical", "reason": "Data Analyst"}
            )
        
        if any(word in desc_lower for word in ["report", "documentation", "summary"]):
            recommendations["recommended_agents"].append(
                {"name": "Lucas Rivera", "team": "analytical", "reason": "Report Synthesizer"}
            )
        
        # Cross-team bridge
        if any(word in desc_lower for word in ["document", "pdf", "process", "extract"]):
            recommendations["recommended_agents"].append(
                {"name": "Alex Morgan", "team": "analytical", "reason": "Technical Liaison - document processing"}
            )
        
        # Deduplicate
        seen = set()
        unique_recommendations = []
        for rec in recommendations["recommended_agents"]:
            if rec["name"] not in seen:
                seen.add(rec["name"])
                unique_recommendations.append(rec)
        
        recommendations["recommended_agents"] = unique_recommendations
        recommendations["team_composition"] = {
            "technical": len([r for r in unique_recommendations if r["team"] == "technical"]),
            "analytical": len([r for r in unique_recommendations if r["team"] == "analytical"]),
            "total": len(unique_recommendations)
        }
        
        return recommendations


# Integration helper functions

def connect_teams(technical_team, analytical_team) -> CrossTeamCommunicator:
    """
    Connect Technical and Analytical teams
    
    Args:
        technical_team: Technical team instance
        analytical_team: Analytical team instance
    
    Returns:
        CrossTeamCommunicator instance
    """
    communicator = CrossTeamCommunicator(
        technical_team=technical_team,
        analytical_team=analytical_team
    )
    
    print("\n" + "=" * 60)
    print("🌉 CROSS-TEAM COMMUNICATION ESTABLISHED")
    print("=" * 60)
    
    capabilities = communicator.get_team_capabilities()
    
    print(f"\n📊 TECHNICAL TEAM ({capabilities['technical_team']['size']} agents):")
    for cap in capabilities['technical_team']['capabilities']:
        print(f"   ✓ {cap}")
    
    print(f"\n📊 ANALYTICAL TEAM ({capabilities['analytical_team']['size']} agents):")
    for cap in capabilities['analytical_team']['capabilities']:
        print(f"   ✓ {cap}")
    
    print(f"\n🎯 TOTAL: {capabilities['total_agents']} agents across both teams")
    print("=" * 60)
    
    return communicator


# Quick test
if __name__ == "__main__":
    print("🌉 Cross-Team Communication System\n")
    print("This module enables collaboration between:")
    print("  ✓ Technical Team (Software Development)")
    print("  ✓ Analytical Team (Intelligence & Research)")
    print("\nFeatures:")
    print("  • Unified agent registry")
    print("  • Cross-team task delegation")
    print("  • Expert discovery")
    print("  • Collaborative workflows")
    print("  • Smart team composition recommendations")
