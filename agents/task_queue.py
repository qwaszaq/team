"""
Task Queue System for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-03 (Day 2)

Centralized task management with priority queue and status tracking.
"""

from typing import Dict, List, Optional
from uuid import UUID
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.task_models import Task, TaskStatus, TaskResult


class TaskQueue:
    """
    Centralized task queue with priority management
    
    Features:
    - Priority-based task ordering
    - Per-agent task tracking
    - Status management
    - Task completion with results
    
    Usage:
        queue = TaskQueue()
        queue.add_task(task)
        queue.assign_to_agent(task_id, "Agent Name")
        task = queue.get_next_for_agent("Agent Name")
    """
    
    def __init__(self):
        """Initialize empty task queue"""
        self.tasks: Dict[UUID, Task] = {}  # All tasks by ID
        self.agent_tasks: Dict[str, List[Task]] = {}  # Tasks per agent
        
    def add_task(self, task: Task) -> UUID:
        """
        Add task to queue
        
        Args:
            task: Task to add
            
        Returns:
            UUID: Task ID
        """
        self.tasks[task.task_id] = task
        return task.task_id
        
    def assign_to_agent(self, task_id: UUID, agent_name: str):
        """
        Assign task to specific agent
        
        Args:
            task_id: Task to assign
            agent_name: Agent to assign to
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.assigned_to = agent_name
        
        # Add to agent's task list
        if agent_name not in self.agent_tasks:
            self.agent_tasks[agent_name] = []
        self.agent_tasks[agent_name].append(task)
        
    def get_next_for_agent(self, agent_name: str) -> Optional[Task]:
        """
        Get next task for specific agent (highest priority pending)
        
        Args:
            agent_name: Agent name
            
        Returns:
            Optional[Task]: Next task or None
        """
        if agent_name not in self.agent_tasks:
            return None
            
        # Filter pending tasks
        pending = [t for t in self.agent_tasks[agent_name] 
                   if t.status == TaskStatus.PENDING]
        
        if not pending:
            return None
            
        # Sort by priority (highest first)
        pending.sort(key=lambda t: t.priority, reverse=True)
        return pending[0]
        
    def update_status(self, task_id: UUID, status: TaskStatus):
        """
        Update task status
        
        Args:
            task_id: Task to update
            status: New status
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        self.tasks[task_id].status = status
        
    def complete_task(self, task_id: UUID, result: TaskResult):
        """
        Mark task as complete with results
        
        Args:
            task_id: Task to complete
            result: Task execution results
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.status = result.status
        task.result = result
        
    def get_agent_tasks(self, agent_name: str) -> List[Task]:
        """
        Get all tasks for agent
        
        Args:
            agent_name: Agent name
            
        Returns:
            List[Task]: Agent's tasks (empty if none)
        """
        return self.agent_tasks.get(agent_name, [])
        
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """
        Get specific task
        
        Args:
            task_id: Task ID
            
        Returns:
            Optional[Task]: Task or None
        """
        return self.tasks.get(task_id)
        
    def get_blocked_tasks(self) -> List[Task]:
        """
        Get tasks blocked by dependencies
        
        Returns:
            List[Task]: Blocked tasks
        """
        return [t for t in self.tasks.values() 
                if t.status == TaskStatus.BLOCKED]
        
    def get_stats(self) -> Dict[str, int]:
        """
        Get queue statistics
        
        Returns:
            Dict with counts per status
        """
        stats = {
            "total": len(self.tasks),
            "pending": 0,
            "in_progress": 0,
            "done": 0,
            "failed": 0,
            "blocked": 0,
            "cancelled": 0
        }
        
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                stats["pending"] += 1
            elif task.status == TaskStatus.IN_PROGRESS:
                stats["in_progress"] += 1
            elif task.status == TaskStatus.DONE:
                stats["done"] += 1
            elif task.status == TaskStatus.FAILED:
                stats["failed"] += 1
            elif task.status == TaskStatus.BLOCKED:
                stats["blocked"] += 1
            elif task.status == TaskStatus.CANCELLED:
                stats["cancelled"] += 1
                
        return stats


# Module-level test
if __name__ == "__main__":
    import uuid
    from datetime import datetime
    
    print("Testing task_queue module...")
    
    # Test initialization
    queue = TaskQueue()
    assert len(queue.tasks) == 0
    print("✅ TaskQueue initialization OK")
    
    # Test add task
    task = Task(
        task_id=uuid.uuid4(),
        title="Test Task",
        description="Testing",
        assigned_to="Agent1",
        assigned_by="Orchestrator",
        context={},
        priority=3,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    task_id = queue.add_task(task)
    assert task_id == task.task_id
    assert len(queue.tasks) == 1
    print("✅ Add task OK")
    
    # Test assign to agent
    queue.assign_to_agent(task_id, "Agent1")
    agent_tasks = queue.get_agent_tasks("Agent1")
    assert len(agent_tasks) == 1
    print("✅ Assign to agent OK")
    
    # Test get next task
    next_task = queue.get_next_for_agent("Agent1")
    assert next_task is not None
    assert next_task.task_id == task_id
    print("✅ Get next task OK")
    
    # Test complete task
    result = TaskResult(
        task_id=task_id,
        completed_by="Agent1",
        status=TaskStatus.DONE,
        output="Done",
        thoughts="Completed",
        time_taken=1.0,
        artifacts=[]
    )
    queue.complete_task(task_id, result)
    completed_task = queue.get_task(task_id)
    assert completed_task.status == TaskStatus.DONE
    print("✅ Complete task OK")
    
    # Test stats
    stats = queue.get_stats()
    assert stats["total"] == 1
    assert stats["done"] == 1
    print("✅ Stats OK")
    
    print("\n✅ TaskQueue module ready!")
