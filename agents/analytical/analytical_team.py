"""
Analytical Team - Complete Integration

Full team setup with database integration, task orchestration,
and cooperation mechanisms matching the technical team's level.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import List, Dict, Optional
from datetime import datetime

# Import agents
from agents.analytical.viktor_agent import ViktorAgent
from agents.analytical.damian_agent import DamianAgent
from agents.analytical.elena_agent import ElenaAgent
from agents.analytical.marcus_agent import MarcusAgent
from agents.analytical.sofia_agent import SofiaAgent
from agents.analytical.adrian_agent import AdrianAgent
from agents.analytical.maya_agent import MayaAgent
from agents.analytical.lucas_agent import LucasAgent
from agents.analytical.alex_agent import AlexAgent

# Import core components
from agents.task_models import Task, TaskResult, TaskStatus
from agents.task_queue import TaskQueue
from agents.agent_registry import AgentRegistry

# Import configuration
from agents.analytical.config import AnalyticalConfig


class AnalyticalTeam:
    """
    Analytical Team - Complete Integration
    
    9-Agent analytical intelligence team with:
    - Investigation capabilities
    - Market research
    - Financial analysis
    - Legal research
    - Data analytics
    - Report generation
    - Local LLM processing (privacy-first)
    - Full database integration
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        """Initialize analytical team with all agents"""
        
        self.project_id = project_id
        
        # Initialize task queue (same as technical team)
        self.task_queue = TaskQueue()
        
        # Initialize agent registry
        self.registry = AgentRegistry()
        
        # Initialize all agents
        self.agents = self._initialize_agents()
        
        # Register all agents
        for agent in self.agents:
            self.registry.register(agent)
        
        # Agent lookup
        self.agent_by_name = {agent.name: agent for agent in self.agents}
        
        print(f"✅ Analytical Team initialized with {len(self.agents)} agents")
        print(f"   Project ID: {self.project_id}")
        print(f"   Privacy Mode: {AnalyticalConfig.LLM_MODE}")
    
    def _initialize_agents(self) -> List:
        """Initialize all 9 analytical agents"""
        
        agents = [
            # Orchestrator
            ViktorAgent(project_id=self.project_id),
            
            # Devil's Advocate
            DamianAgent(project_id=self.project_id),
            
            # OSINT Specialist
            ElenaAgent(project_id=self.project_id),
            
            # Financial Analyst
            MarcusAgent(project_id=self.project_id),
            
            # Market Researcher
            SofiaAgent(project_id=self.project_id),
            
            # Legal Analyst
            AdrianAgent(project_id=self.project_id),
            
            # Data Analyst
            MayaAgent(project_id=self.project_id),
            
            # Report Synthesizer
            LucasAgent(project_id=self.project_id),
            
            # Technical Liaison
            AlexAgent(project_id=self.project_id),
        ]
        
        return agents
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: Optional[str] = None,
        priority: str = "medium",
        context: Optional[Dict] = None
    ) -> Task:
        """
        Create and queue a task
        
        Args:
            title: Task title
            description: Detailed task description
            assigned_to: Agent name (or "Viktor Kovalenko" for orchestrator)
            priority: "low", "medium", "high", "critical"
            context: Additional task context (e.g., {"sensitive": True})
        
        Returns:
            Created task
        """
        
        # Default to orchestrator if not specified
        if not assigned_to:
            assigned_to = "Viktor Kovalenko"
        
        # Map priority to int
        priority_map = {"low": 1, "medium": 3, "high": 4, "critical": 5}
        priority_int = priority_map.get(priority, 3)
        
        # Create task using Task factory pattern
        from uuid import uuid4
        task = Task(
            task_id=uuid4(),
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_by="AnalyticalTeam",
            context=context or {},
            priority=priority_int,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        # Add to queue
        self.task_queue.add_task(task)
        
        print(f"✅ Task created: {title}")
        print(f"   Assigned to: {assigned_to}")
        print(f"   Priority: {priority}")
        
        return task
    
    def execute_task(self, task: Task) -> TaskResult:
        """
        Execute a task with the assigned agent
        
        Args:
            task: Task to execute
        
        Returns:
            Task result
        """
        
        agent = self.agent_by_name.get(task.assigned_to)
        
        if not agent:
            print(f"❌ Agent '{task.assigned_to}' not found")
            return TaskResult(
                task_id=task.task_id,
                completed_by="System",
                status=TaskStatus.FAILED,
                output={"error": f"Agent '{task.assigned_to}' not found"},
                thoughts="Agent not found in registry",
                time_taken=0
            )
        
        # Mark agent as busy (if registry supports status tracking)
        # Note: BaseAgent handles its own status
        
        print(f"\n🔄 Executing task: {task.title}")
        print(f"   Agent: {agent.name}")
        
        # Execute
        result = agent.execute_task(task)
        
        # Agent returns to available status automatically
        
        # Update task queue
        self.task_queue.update_task_status(task.task_id, result.status)
        
        print(f"✅ Task completed: {task.title}")
        print(f"   Status: {result.status.value}")
        
        return result
    
    def delegate_to_agent(
        self,
        agent_name: str,
        task_title: str,
        task_description: str,
        priority: str = "medium"
    ) -> TaskResult:
        """
        Delegate a task directly to a specific agent
        
        Args:
            agent_name: Name of agent to delegate to
            task_title: Task title
            task_description: Task description
            priority: Task priority
        
        Returns:
            Task result
        """
        
        task = self.create_task(
            title=task_title,
            description=task_description,
            assigned_to=agent_name,
            priority=priority
        )
        
        return self.execute_task(task)
    
    def investigate(
        self,
        subject: str,
        investigation_type: str = "comprehensive",
        priority: str = "high"
    ) -> Dict:
        """
        Launch full team investigation
        
        Args:
            subject: Investigation subject (company, person, market, etc.)
            investigation_type: "osint", "financial", "legal", "comprehensive"
            priority: Investigation priority
        
        Returns:
            Investigation results from all relevant agents
        """
        
        print(f"\n🔍 LAUNCHING INVESTIGATION: {subject}")
        print(f"   Type: {investigation_type}")
        print(f"   Priority: {priority}")
        print("=" * 60)
        
        results = {}
        
        # Viktor (Orchestrator) plans investigation
        planning_task = self.create_task(
            title=f"Plan investigation: {subject}",
            description=f"Create investigation plan for {subject}. Type: {investigation_type}",
            assigned_to="Viktor Kovalenko",
            priority=priority
        )
        results["planning"] = self.execute_task(planning_task)
        
        # Comprehensive investigation involves multiple agents
        if investigation_type == "comprehensive":
            
            # Elena: OSINT
            elena_task = self.create_task(
                title=f"OSINT investigation: {subject}",
                description=f"Conduct open-source intelligence gathering on {subject}",
                assigned_to="Elena Volkov",
                priority=priority,
                context={"sensitive": True}
            )
            results["osint"] = self.execute_task(elena_task)
            
            # Marcus: Financial
            marcus_task = self.create_task(
                title=f"Financial analysis: {subject}",
                description=f"Analyze financial health and performance of {subject}",
                assigned_to="Marcus Chen",
                priority=priority,
                context={"sensitive": True}
            )
            results["financial"] = self.execute_task(marcus_task)
            
            # Sofia: Market
            sofia_task = self.create_task(
                title=f"Market research: {subject}",
                description=f"Research market position and competitive landscape for {subject}",
                assigned_to="Sofia Martinez",
                priority=priority
            )
            results["market"] = self.execute_task(sofia_task)
            
            # Adrian: Legal
            adrian_task = self.create_task(
                title=f"Legal research: {subject}",
                description=f"Research legal issues, compliance, and risks for {subject}",
                assigned_to="Adrian Kowalski",
                priority=priority,
                context={"sensitive": True}
            )
            results["legal"] = self.execute_task(adrian_task)
            
            # Maya: Data Analysis
            maya_task = self.create_task(
                title=f"Data analysis: {subject}",
                description=f"Analyze available data and generate statistical insights for {subject}",
                assigned_to="Maya Patel",
                priority=priority
            )
            results["data"] = self.execute_task(maya_task)
            
            # Damian: Critical Review
            damian_task = self.create_task(
                title=f"Critical review: {subject}",
                description=f"Challenge findings and propose alternative perspectives on {subject}",
                assigned_to="Damian Rousseau",
                priority=priority
            )
            results["critical_review"] = self.execute_task(damian_task)
            
            # Lucas: Final Report
            lucas_task = self.create_task(
                title=f"Final report: {subject}",
                description=f"Synthesize all findings into comprehensive investigation report for {subject}",
                assigned_to="Lucas Rivera",
                priority=priority
            )
            results["report"] = self.execute_task(lucas_task)
        
        elif investigation_type == "osint":
            # Elena only
            elena_task = self.create_task(
                title=f"OSINT investigation: {subject}",
                description=f"Conduct deep OSINT investigation on {subject}",
                assigned_to="Elena Volkov",
                priority=priority,
                context={"sensitive": True}
            )
            results["osint"] = self.execute_task(elena_task)
        
        elif investigation_type == "financial":
            # Marcus only
            marcus_task = self.create_task(
                title=f"Financial due diligence: {subject}",
                description=f"Conduct comprehensive financial analysis of {subject}",
                assigned_to="Marcus Chen",
                priority=priority,
                context={"sensitive": True}
            )
            results["financial"] = self.execute_task(marcus_task)
        
        elif investigation_type == "legal":
            # Adrian only
            adrian_task = self.create_task(
                title=f"Legal research: {subject}",
                description=f"Conduct legal research and risk assessment for {subject}",
                assigned_to="Adrian Kowalski",
                priority=priority,
                context={"sensitive": True}
            )
            results["legal"] = self.execute_task(adrian_task)
        
        print("\n" + "=" * 60)
        print(f"✅ Investigation complete: {subject}")
        print(f"   Tasks completed: {len(results)}")
        
        return results
    
    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict:
        """Get status of agent(s)"""
        
        if agent_name:
            agent = self.registry.get_agent(agent_name)
            return {
                "name": agent.name if agent else None,
                "role": agent.role if agent else None,
                "status": agent.status.value if agent else "not_found"
            }
        else:
            return {
                name: {
                    "role": agent.role,
                    "status": agent.status.value
                }
                for name, agent in self.registry.agents.items()
            }
    
    def list_agents(self) -> List[Dict]:
        """List all agents with their capabilities"""
        
        agents_info = []
        
        for agent in self.agents:
            info = {
                "name": agent.name,
                "role": agent.role,
                "specialization": agent.specialization,
                "status": agent.status.value
            }
            agents_info.append(info)
        
        return agents_info
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return self.task_queue.get_pending_tasks()
    
    def get_task_history(self, limit: int = 10) -> List[Task]:
        """Get task history"""
        return self.task_queue.get_task_history(limit=limit)


# Quick test
if __name__ == "__main__":
    print("🚀 Initializing Destiny Analytical Team\n")
    
    # Initialize team
    team = AnalyticalTeam()
    
    print("\n📋 Team Roster:")
    for agent_info in team.list_agents():
        print(f"  ✓ {agent_info['name']} - {agent_info['role']}")
    
    print("\n✅ Analytical Team ready for operations!")
    print("\nExample usage:")
    print('  results = team.investigate("Company XYZ", investigation_type="comprehensive")')
    print('  task = team.create_task("Market analysis", "Analyze Q3 trends", assigned_to="Sofia Martinez")')
    print('  result = team.delegate_to_agent("Elena Volkov", "OSINT", "Research target")')
