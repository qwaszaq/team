"""
Real-Time Team Status Tracker
==============================

Tracks what each agent/team is doing in real-time.
Shows progress, current tasks, and workload.

Author: Aleksander Nowak (Orchestrator)
Date: 2025-11-04
Sprint: Transparency Tools + Cross-Team Improvements
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum
import json


class AgentStatus(Enum):
    """Agent availability status"""
    AVAILABLE = "available"
    BUSY = "busy"
    VERY_BUSY = "very_busy"
    OFFLINE = "offline"


class TaskStatus(Enum):
    """Task status"""
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Single task assigned to an agent"""
    task_id: str
    title: str
    status: TaskStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_pct: int = 0
    description: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress_pct": self.progress_pct,
            "description": self.description
        }


@dataclass
class AgentState:
    """Current state of an agent"""
    name: str
    role: str
    team: str  # "Core" or "Analytical"
    status: AgentStatus
    current_tasks: List[AgentTask] = field(default_factory=list)
    completed_today: int = 0
    last_activity: Optional[datetime] = None
    
    @property
    def workload(self) -> int:
        """Number of active tasks"""
        return len([t for t in self.current_tasks 
                   if t.status in [TaskStatus.IN_PROGRESS, TaskStatus.QUEUED]])
    
    @property
    def is_available(self) -> bool:
        """Is agent available for new work"""
        return self.status == AgentStatus.AVAILABLE and self.workload == 0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "team": self.team,
            "status": self.status.value,
            "workload": self.workload,
            "current_tasks": [t.to_dict() for t in self.current_tasks],
            "completed_today": self.completed_today,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "is_available": self.is_available
        }


@dataclass
class TeamState:
    """Current state of a team"""
    name: str  # "Core Team" or "Analytical Team"
    agents: List[AgentState] = field(default_factory=list)
    active_tasks: int = 0
    completed_today: int = 0
    
    @property
    def available_agents(self) -> List[AgentState]:
        """Agents available for new work"""
        return [a for a in self.agents if a.is_available]
    
    @property
    def busy_agents(self) -> List[AgentState]:
        """Agents currently working"""
        return [a for a in self.agents if a.workload > 0]
    
    @property
    def team_capacity(self) -> float:
        """Team capacity utilization (0-1)"""
        if not self.agents:
            return 0.0
        busy = len(self.busy_agents)
        total = len(self.agents)
        return busy / total
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "agents": [a.to_dict() for a in self.agents],
            "active_tasks": self.active_tasks,
            "completed_today": self.completed_today,
            "available_agents": len(self.available_agents),
            "busy_agents": len(self.busy_agents),
            "team_capacity": self.team_capacity
        }


class TeamStatusTracker:
    """
    Tracks real-time status of all agents and teams.
    
    Usage:
        tracker = TeamStatusTracker()
        
        # Register agents
        tracker.register_agent("Tomasz Kamiński", "Senior Developer", "Core")
        
        # Assign task
        tracker.assign_task(
            agent_name="Tomasz Kamiński",
            task_id="TASK-001",
            title="Implement feature X"
        )
        
        # Update progress
        tracker.update_progress("TASK-001", 50)
        
        # Complete task
        tracker.complete_task("TASK-001")
        
        # View status
        status = tracker.get_team_status("Core Team")
        print(status)
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentState] = {}
        self.teams: Dict[str, TeamState] = {
            "Core Team": TeamState(name="Core Team"),
            "Analytical Team": TeamState(name="Analytical Team")
        }
        self.tasks: Dict[str, AgentTask] = {}
        
        # Initialize with default agents
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize with known agents"""
        
        # Core Team
        core_agents = [
            ("Aleksander Nowak", "Technical Orchestrator"),
            ("Tomasz Kamiński", "Senior Developer"),
            ("Anna Lewandowska", "QA Engineer"),
            ("Piotr Szymański", "DevOps Engineer"),
            ("Maria Wiśniewska", "Software Architect"),
            ("Michał Dąbrowski", "Security Specialist"),
            ("Helena Kowalczyk", "Knowledge Manager"),
        ]
        
        for name, role in core_agents:
            self.register_agent(name, role, "Core")
        
        # Analytical Team
        analytical_agents = [
            ("Viktor Kovalenko", "Investigation Director"),
            ("Elena Volkov", "OSINT Specialist"),
            ("Sofia Martinez", "Market Research Analyst"),
            ("Maya Patel", "Data Analyst"),
            ("Damian Rousseau", "Devil's Advocate"),
            ("Lucas Rivera", "Report Synthesizer"),
        ]
        
        for name, role in analytical_agents:
            self.register_agent(name, role, "Analytical")
    
    def register_agent(self, name: str, role: str, team: str):
        """Register a new agent"""
        team_key = f"{team} Team"
        if team_key not in self.teams:
            self.teams[team_key] = TeamState(name=team_key)
        
        agent = AgentState(
            name=name,
            role=role,
            team=team,
            status=AgentStatus.AVAILABLE
        )
        
        self.agents[name] = agent
        self.teams[team_key].agents.append(agent)
    
    def assign_task(
        self,
        agent_name: str,
        task_id: str,
        title: str,
        description: Optional[str] = None
    ):
        """Assign a task to an agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        task = AgentTask(
            task_id=task_id,
            title=title,
            status=TaskStatus.QUEUED,
            description=description
        )
        
        self.tasks[task_id] = task
        self.agents[agent_name].current_tasks.append(task)
        self.agents[agent_name].status = AgentStatus.BUSY
        self.agents[agent_name].last_activity = datetime.now()
        
        # Update team stats
        team_key = f"{self.agents[agent_name].team} Team"
        self.teams[team_key].active_tasks += 1
    
    def start_task(self, task_id: str):
        """Mark task as in progress"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        # Update agent activity
        for agent in self.agents.values():
            if task in agent.current_tasks:
                agent.last_activity = datetime.now()
    
    def update_progress(self, task_id: str, progress_pct: int):
        """Update task progress"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        self.tasks[task_id].progress_pct = min(100, max(0, progress_pct))
        
        # Update agent activity
        for agent in self.agents.values():
            if self.tasks[task_id] in agent.current_tasks:
                agent.last_activity = datetime.now()
    
    def complete_task(self, task_id: str):
        """Mark task as completed"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.progress_pct = 100
        
        # Update agent
        for agent in self.agents.values():
            if task in agent.current_tasks:
                agent.current_tasks.remove(task)
                agent.completed_today += 1
                agent.last_activity = datetime.now()
                
                # Update status based on remaining workload
                if agent.workload == 0:
                    agent.status = AgentStatus.AVAILABLE
                elif agent.workload <= 2:
                    agent.status = AgentStatus.BUSY
                else:
                    agent.status = AgentStatus.VERY_BUSY
                
                # Update team stats
                team_key = f"{agent.team} Team"
                self.teams[team_key].active_tasks -= 1
                self.teams[team_key].completed_today += 1
    
    def block_task(self, task_id: str, reason: str):
        """Mark task as blocked"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        self.tasks[task_id].status = TaskStatus.BLOCKED
        self.tasks[task_id].description = f"BLOCKED: {reason}"
    
    def get_agent_status(self, agent_name: str) -> Dict:
        """Get current status of an agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        return self.agents[agent_name].to_dict()
    
    def get_team_status(self, team_name: str) -> Dict:
        """Get current status of a team"""
        if team_name not in self.teams:
            raise ValueError(f"Team {team_name} not found")
        
        return self.teams[team_name].to_dict()
    
    def get_all_status(self) -> Dict:
        """Get status of all teams and agents"""
        return {
            "teams": {name: team.to_dict() for name, team in self.teams.items()},
            "timestamp": datetime.now().isoformat()
        }
    
    def get_available_agents(self, team: Optional[str] = None) -> List[str]:
        """Get list of available agent names"""
        agents = self.agents.values()
        
        if team:
            agents = [a for a in agents if a.team == team]
        
        return [a.name for a in agents if a.is_available]
    
    def print_status_dashboard(self):
        """Print a nice dashboard view"""
        print("\n" + "="*70)
        print("🎯 DESTINY TEAM - REAL-TIME STATUS DASHBOARD")
        print("="*70)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for team_name, team in self.teams.items():
            print(f"{'─'*70}")
            print(f"👥 {team_name}")
            print(f"{'─'*70}")
            print(f"   Active Tasks: {team.active_tasks} | Completed Today: {team.completed_today}")
            print(f"   Capacity: {team.team_capacity*100:.0f}% | Available: {len(team.available_agents)}/{len(team.agents)}\n")
            
            for agent in team.agents:
                status_emoji = {
                    AgentStatus.AVAILABLE: "🟢",
                    AgentStatus.BUSY: "🟡",
                    AgentStatus.VERY_BUSY: "🔴",
                    AgentStatus.OFFLINE: "⚫"
                }[agent.status]
                
                print(f"   {status_emoji} {agent.name}")
                print(f"      {agent.role} | Workload: {agent.workload} tasks")
                
                if agent.current_tasks:
                    for task in agent.current_tasks:
                        progress_bar = "█" * (task.progress_pct // 10) + "░" * (10 - task.progress_pct // 10)
                        print(f"      ├─ [{task.status.value}] {task.title}")
                        print(f"      │  {progress_bar} {task.progress_pct}%")
                else:
                    print(f"      └─ Available for work")
                print()
        
        print("="*70)


# Global instance
_tracker = TeamStatusTracker()


def get_tracker() -> TeamStatusTracker:
    """Get the global tracker instance"""
    return _tracker


if __name__ == "__main__":
    # Demo
    tracker = TeamStatusTracker()
    
    # Assign some tasks
    tracker.assign_task(
        "Elena Volkov",
        "TASK-001",
        "OSINT research on Claude-Flow",
        "Research competitors and gather intelligence"
    )
    tracker.start_task("TASK-001")
    tracker.update_progress("TASK-001", 65)
    
    tracker.assign_task(
        "Tomasz Kamiński",
        "TASK-002",
        "Implement transparency dashboard"
    )
    tracker.start_task("TASK-002")
    tracker.update_progress("TASK-002", 30)
    
    tracker.assign_task(
        "Piotr Szymański",
        "TASK-003",
        "Deploy to production"
    )
    
    # Show dashboard
    tracker.print_status_dashboard()
