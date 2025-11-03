"""
Task Data Models for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-03 (Day 2)

This module defines the core data structures for task management in the
multi-agent system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, List
from uuid import UUID
from datetime import datetime


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"  # Waiting on dependencies
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """
    Represents a task assigned to an agent
    
    Attributes:
        task_id: Unique identifier
        title: Short task description
        description: Detailed task description
        assigned_to: Agent name who will execute
        assigned_by: Who created/assigned the task
        context: Additional context dict
        priority: 1 (low) to 5 (critical)
        status: Current task status
        created_at: When task was created
        started_at: When agent started working
        completed_at: When task finished
        deadline: Optional deadline
        result: Task execution result
        dependencies: Tasks that must complete first
    """
    task_id: UUID
    title: str
    description: str
    assigned_to: str
    assigned_by: str
    context: dict[str, Any]
    priority: int  # 1-5
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    result: Optional['TaskResult'] = None
    dependencies: List[UUID] = None
    
    def __post_init__(self):
        """Initialize dependencies list if None"""
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class TaskResult:
    """
    Result of task execution
    
    Attributes:
        task_id: ID of completed task
        completed_by: Agent who completed it
        status: Final status (DONE/FAILED)
        output: Agent's work product
        thoughts: Agent's reasoning/process
        time_taken: Execution time in seconds
        artifacts: Files/URLs/resources created
        next_steps: Recommendations for follow-up
    """
    task_id: UUID
    completed_by: str
    status: TaskStatus
    output: Any
    thoughts: str
    time_taken: float
    artifacts: List[str]
    next_steps: Optional[str] = None


@dataclass
class TaskAck:
    """
    Task acknowledgment from agent
    
    Sent when agent receives task to confirm receipt
    and provide estimated completion time.
    """
    task_id: UUID
    agent: str
    status: str  # "acknowledged", "rejected", etc.
    eta_minutes: int  # Estimated time to complete


# Module-level test
if __name__ == "__main__":
    import uuid
    
    print("Testing task_models module...")
    
    # Test TaskStatus enum
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.DONE.value == "done"
    print("✅ TaskStatus enum OK")
    
    # Test Task creation
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
    assert task.title == "Test Task"
    assert task.dependencies == []
    print("✅ Task creation OK")
    
    # Test TaskResult creation
    result = TaskResult(
        task_id=task.task_id,
        completed_by="Agent1",
        status=TaskStatus.DONE,
        output="Done",
        thoughts="Completed successfully",
        time_taken=1.0,
        artifacts=[]
    )
    assert result.completed_by == "Agent1"
    print("✅ TaskResult creation OK")
    
    # Test TaskAck creation
    ack = TaskAck(
        task_id=task.task_id,
        agent="Agent1",
        status="acknowledged",
        eta_minutes=30
    )
    assert ack.agent == "Agent1"
    print("✅ TaskAck creation OK")
    
    print("\n✅ All task_models tests passed!")
