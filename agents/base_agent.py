"""
Base Agent Class for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-03 (Day 2)

Foundation class that all agents inherit from.
Provides core functionality for task management, memory, and status.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.task_models import Task, TaskStatus, TaskResult, TaskAck
from agents.agent_memory import AgentMemory


class AgentStatus(Enum):
    """Agent availability status"""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class BaseAgent:
    """
    Foundation class for all Destiny Team agents.
    
    Each agent has:
    - Unique identity and role
    - Personal memory system
    - Task queue
    - Specialized behaviors (via inheritance)
    
    Usage:
        agent = BaseAgent("Test Agent", "Tester", "Testing")
        agent.receive_task(task)
        result = agent.process_task(task)
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        specialization: str,
        project_id: str = "destiny-team-framework-master"
    ):
        """
        Initialize base agent
        
        Args:
            name: Agent's full name
            role: Agent's role (e.g., "Developer", "QA Engineer")
            specialization: What agent specializes in
            project_id: Project identifier for memory system
        """
        self.name = name
        self.role = role
        self.specialization = specialization
        self.agent_id = uuid.uuid4()
        self.project_id = project_id
        
        # Memory system
        self.memory = AgentMemory(agent_name=name, project_id=project_id)
        
        # Task management
        self.task_queue: List[Task] = []
        self.current_task: Optional[Task] = None
        self.status = AgentStatus.AVAILABLE
        
        # Statistics
        self.tasks_completed = 0
        self.tasks_failed = 0
        
        print(f"✅ {self.name} ({self.role}) initialized")
        
    def receive_task(self, task: Task) -> TaskAck:
        """
        Receive a task from orchestrator
        
        Args:
            task: Task to execute
            
        Returns:
            TaskAck: Acknowledgment with ETA
        """
        print(f"📥 {self.name}: Received task '{task.title}'")
        
        # Add to queue
        self.task_queue.append(task)
        task.status = TaskStatus.PENDING
        
        # Save to memory
        self.memory.save(
            content=f"Received task: {task.title} - {task.description}",
            importance=0.7,
            context_type="task_received"
        )
        
        return TaskAck(
            task_id=task.task_id,
            agent=self.name,
            status="acknowledged",
            eta_minutes=self._estimate_time(task)
        )
        
    def get_next_task(self) -> Optional[Task]:
        """Get next task from queue (highest priority)"""
        if not self.task_queue:
            return None
            
        # Sort by priority (5 = highest)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        return self.task_queue[0]
        
    def process_task(self, task: Task) -> TaskResult:
        """
        Execute a task
        
        Args:
            task: Task to process
            
        Returns:
            TaskResult: Results of task execution
        """
        print(f"⚙️  {self.name}: Processing '{task.title}'")
        
        self.status = AgentStatus.BUSY
        self.current_task = task
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        try:
            # Agent-specific logic (override in subclasses)
            result = self._execute_work(task)
            
            # Update task
            task.status = TaskStatus.DONE
            task.completed_at = datetime.now()
            task.result = result
            
            # Remove from queue
            if task in self.task_queue:
                self.task_queue.remove(task)
                
            # Statistics
            self.tasks_completed += 1
            
            # Save to memory
            self.memory.save(
                content=f"Completed task: {task.title}\n{result.thoughts}",
                importance=0.85,
                context_type="task_completed"
            )
            
            print(f"✅ {self.name}: Task '{task.title}' complete")
            
        except Exception as e:
            print(f"❌ {self.name}: Task '{task.title}' failed: {e}")
            
            task.status = TaskStatus.FAILED
            result = TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.FAILED,
                output=None,
                thoughts=f"Task failed with error: {str(e)}",
                time_taken=0,
                artifacts=[],
                next_steps="Review error and retry"
            )
            
            self.tasks_failed += 1
            
        finally:
            self.status = AgentStatus.AVAILABLE
            self.current_task = None
            
        return result
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute agent-specific work
        
        OVERRIDE THIS in subclasses!
        
        This is a minimal working implementation for BaseAgent.
        Specialized agents should override with their own logic.
        
        Args:
            task: Task to execute
            
        Returns:
            TaskResult: Work results
        """
        # Minimal working implementation
        # Load relevant context from memory
        context = self.load_context(task.description, limit=2)
        
        # Base agent performs generic work
        thoughts = f"""
GENERIC TASK EXECUTION by {self.name}:

Task: {task.title}
Description: {task.description}
Priority: {task.priority}

Context loaded: {len(context)} relevant memories

Action: Completed task using base agent capabilities.
Note: For specialized work, use a specialized agent (Tomasz, Magdalena, etc.)
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "status": "completed",
                "agent": self.name,
                "task": task.title,
                "context_used": len(context)
            },
            thoughts=thoughts.strip(),
            time_taken=0.5,
            artifacts=[],
            next_steps="Task complete. Consider assigning to specialized agent for better results."
        )
        
    def save_to_memory(
        self,
        content: str,
        importance: float = 0.75,
        context_type: str = "general"
    ):
        """Save content to agent's memory"""
        return self.memory.save(content, importance, context_type)
        
    def load_context(self, query: str, limit: int = 5) -> List[str]:
        """Load relevant context from agent's memory"""
        return self.memory.load(query, limit)
        
    def report_status(self) -> Dict[str, Any]:
        """Report current agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status.value,
            "current_task": self.current_task.title if self.current_task else None,
            "queue_size": len(self.task_queue),
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed
        }
        
    def _estimate_time(self, task: Task) -> int:
        """Estimate task completion time in minutes"""
        # Basic estimation (can be overridden)
        return 30  # 30 minutes default
        
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}')>"


# Module-level test
if __name__ == "__main__":
    print("Testing base_agent module...")
    
    # Test initialization
    agent = BaseAgent(
        name="Test Agent",
        role="Tester",
        specialization="Testing",
        project_id="test-project"
    )
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.AVAILABLE
    print("✅ BaseAgent initialization OK")
    
    # Test task receive
    task = Task(
        task_id=uuid.uuid4(),
        title="Test Task",
        description="Do something",
        assigned_to=agent.name,
        assigned_by="Orchestrator",
        context={},
        priority=3,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    ack = agent.receive_task(task)
    assert ack.agent == agent.name
    assert len(agent.task_queue) == 1
    print("✅ Task receive OK")
    
    # Test task processing
    result = agent.process_task(task)
    assert result.status == TaskStatus.DONE
    assert result.completed_by == agent.name
    assert agent.tasks_completed == 1
    print("✅ Task processing OK")
    
    # Test status report
    status = agent.report_status()
    assert status["name"] == agent.name
    assert status["tasks_completed"] == 1
    print("✅ Status report OK")
    
    print("\n✅ BaseAgent module ready!")
