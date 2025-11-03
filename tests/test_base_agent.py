"""
Unit tests for BaseAgent class
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

from agents.base_agent import BaseAgent, AgentStatus
from agents.task_models import Task, TaskStatus, TaskResult


class TestBaseAgentInitialization:
    """Test agent initialization"""
    
    def test_agent_creates_successfully(self):
        """Test basic agent creation"""
        agent = BaseAgent(
            name="Test Agent",
            role="Tester",
            specialization="Testing things",
            project_id="test-project"
        )
        
        assert agent.name == "Test Agent"
        assert agent.role == "Tester"
        assert agent.specialization == "Testing things"
        assert agent.status == AgentStatus.AVAILABLE
        assert len(agent.task_queue) == 0
        assert agent.tasks_completed == 0
        assert agent.tasks_failed == 0
        
    def test_agent_has_unique_id(self):
        """Test that each agent gets unique ID"""
        agent1 = BaseAgent("Agent 1", "Role", "Spec", "test")
        agent2 = BaseAgent("Agent 2", "Role", "Spec", "test")
        
        assert agent1.agent_id != agent2.agent_id
        
    def test_agent_has_memory(self):
        """Test that agent has memory system"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        assert hasattr(agent, 'memory')
        assert agent.memory is not None


class TestTaskHandling:
    """Test task receive and process"""
    
    def test_agent_receives_task(self):
        """Test receiving a task"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to=agent.name,
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
        
        ack = agent.receive_task(task)
        
        assert ack.agent == agent.name
        assert ack.task_id == task.task_id
        assert ack.status == "acknowledged"
        assert len(agent.task_queue) == 1
        
    def test_agent_processes_task(self):
        """Test processing a task"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to=agent.name,
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
        
        agent.receive_task(task)
        result = agent.process_task(task)
        
        assert result.task_id == task.task_id
        assert result.completed_by == agent.name
        assert result.status == TaskStatus.DONE
        assert result.output is not None
        assert result.thoughts is not None
        
        # Agent should be available again
        assert agent.status == AgentStatus.AVAILABLE
        assert agent.tasks_completed == 1
        assert len(agent.task_queue) == 0
        
    def test_agent_handles_task_failure(self):
        """Test task failure handling"""
        # This would require mocking _execute_work to raise exception
        # Skip for now - covered by smoke tests
        pass


class TestAgentStatus:
    """Test status reporting"""
    
    def test_report_status(self):
        """Test status report"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        status = agent.report_status()
        
        assert status["name"] == "Test"
        assert status["role"] == "Tester"
        assert status["status"] == AgentStatus.AVAILABLE.value
        assert status["current_task"] is None
        assert status["queue_size"] == 0
        assert status["tasks_completed"] == 0
        
    def test_status_changes_during_task(self):
        """Test status changes to BUSY during task processing"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to=agent.name,
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
        
        agent.receive_task(task)
        
        # During processing, agent should be busy
        # (This is hard to test without threading)
        # Covered by smoke tests
        
        result = agent.process_task(task)
        
        # After processing, should be available
        assert agent.status == AgentStatus.AVAILABLE


class TestTaskQueue:
    """Test task queue management"""
    
    def test_priority_ordering(self):
        """Test that high priority tasks come first"""
        agent = BaseAgent("Test", "Tester", "Testing", "test")
        
        task_low = Task(
            task_id=uuid.uuid4(),
            title="Low Priority",
            description="Low",
            assigned_to=agent.name,
            assigned_by="Orchestrator",
            context={},
            priority=1,  # Low
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        task_high = Task(
            task_id=uuid.uuid4(),
            title="High Priority",
            description="High",
            assigned_to=agent.name,
            assigned_by="Orchestrator",
            context={},
            priority=5,  # High
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=None,
            result=None,
            dependencies=[]
        )
        
        # Add low priority first
        agent.receive_task(task_low)
        agent.receive_task(task_high)
        
        # Get next task - should be high priority
        next_task = agent.get_next_task()
        assert next_task.priority == 5
        assert next_task.title == "High Priority"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
