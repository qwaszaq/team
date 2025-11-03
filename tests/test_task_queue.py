"""
Unit tests for TaskQueue class
Optional for Day 2 - if time allows
Priority: MEDIUM (smoke tests are higher priority)
"""

import pytest
import uuid
from datetime import datetime

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.task_queue import TaskQueue
from agents.task_models import Task, TaskStatus, TaskResult


class TestTaskQueueBasics:
    """Test basic queue operations"""
    
    def test_queue_creates_empty(self):
        """Test queue starts empty"""
        queue = TaskQueue()
        
        assert len(queue.tasks) == 0
        assert len(queue.agent_tasks) == 0
        
    def test_add_task(self):
        """Test adding task to queue"""
        queue = TaskQueue()
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to="Agent1",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        task_id = queue.add_task(task)
        
        assert task_id == task.task_id
        assert task_id in queue.tasks
        assert queue.tasks[task_id] == task


class TestTaskAssignment:
    """Test task assignment to agents"""
    
    def test_assign_to_agent(self):
        """Test assigning task to agent"""
        queue = TaskQueue()
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to="Agent1",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        queue.add_task(task)
        queue.assign_to_agent(task.task_id, "Agent1")
        
        agent_tasks = queue.get_agent_tasks("Agent1")
        assert len(agent_tasks) == 1
        assert agent_tasks[0].task_id == task.task_id
        
    def test_get_agent_tasks(self):
        """Test getting tasks for specific agent"""
        queue = TaskQueue()
        
        task1 = Task(
            task_id=uuid.uuid4(),
            title="Task 1",
            description="For Agent1",
            assigned_to="Agent1",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        task2 = Task(
            task_id=uuid.uuid4(),
            title="Task 2",
            description="For Agent2",
            assigned_to="Agent2",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        queue.add_task(task1)
        queue.add_task(task2)
        queue.assign_to_agent(task1.task_id, "Agent1")
        queue.assign_to_agent(task2.task_id, "Agent2")
        
        agent1_tasks = queue.get_agent_tasks("Agent1")
        agent2_tasks = queue.get_agent_tasks("Agent2")
        
        assert len(agent1_tasks) == 1
        assert len(agent2_tasks) == 1
        assert agent1_tasks[0].title == "Task 1"
        assert agent2_tasks[0].title == "Task 2"


class TestTaskCompletion:
    """Test task completion"""
    
    def test_complete_task(self):
        """Test completing a task"""
        queue = TaskQueue()
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to="Agent1",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        queue.add_task(task)
        
        result = TaskResult(
            task_id=task.task_id,
            completed_by="Agent1",
            status=TaskStatus.DONE,
            output="Completed",
            thoughts="All done",
            time_taken=1.0,
            artifacts=[],
            next_steps=None
        )
        
        queue.complete_task(task.task_id, result)
        
        completed_task = queue.get_task(task.task_id)
        assert completed_task.status == TaskStatus.DONE
        assert completed_task.result == result
        
    def test_update_status(self):
        """Test updating task status"""
        queue = TaskQueue()
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to="Agent1",
            assigned_by="Orchestrator",
            context={},
            priority=3,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        queue.add_task(task)
        
        queue.update_status(task.task_id, TaskStatus.IN_PROGRESS)
        
        updated_task = queue.get_task(task.task_id)
        assert updated_task.status == TaskStatus.IN_PROGRESS


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
