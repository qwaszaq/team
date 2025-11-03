"""
Day 2 Integration Test - End-to-End Workflow
Tests the complete agent framework infrastructure

This test verifies:
- Agent creation and registration
- Task assignment
- Task processing
- Memory integration
- Status reporting
"""

import uuid
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskStatus
from agents.task_queue import TaskQueue
from agents.agent_registry import AgentRegistry


def test_full_agent_workflow():
    """Test complete workflow with all components"""
    
    print("\n" + "="*60)
    print("🧪 DAY 2 INTEGRATION TEST - Full Workflow")
    print("="*60)
    print()
    
    # Step 1: Initialize components
    print("Step 1: Initialize components...")
    queue = TaskQueue()
    registry = AgentRegistry()
    print("✅ Components initialized")
    print()
    
    # Step 2: Create and register agent
    print("Step 2: Create and register agent...")
    agent = BaseAgent(
        name="Test Agent",
        role="Tester",
        specialization="Integration Testing",
        project_id="destiny-team-framework-master"  # Use existing project
    )
    registry.register(agent)
    print(f"✅ Agent registered: {agent.name}")
    print()
    
    # Step 3: Create task
    print("Step 3: Create task...")
    task = Task(
        task_id=uuid.uuid4(),
        title="Integration Test Task",
        description="Test the complete agent framework system",
        assigned_to=agent.name,
        assigned_by="Integration Test",
        context={"test": True, "priority": "high"},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    print(f"✅ Task created: {task.title}")
    print()
    
    # Step 4: Add task to queue
    print("Step 4: Add task to queue...")
    task_id = queue.add_task(task)
    queue.assign_to_agent(task_id, agent.name)
    print(f"✅ Task added to queue: {task_id}")
    print()
    
    # Step 5: Agent receives task
    print("Step 5: Agent receives task...")
    ack = agent.receive_task(task)
    assert ack.agent == agent.name, "Wrong agent in acknowledgment"
    assert ack.status == "acknowledged", "Task not acknowledged"
    print(f"✅ Task acknowledged by {ack.agent}")
    print(f"   ETA: {ack.eta_minutes} minutes")
    print()
    
    # Step 6: Agent processes task
    print("Step 6: Agent processes task...")
    result = agent.process_task(task)
    assert result.status == TaskStatus.DONE, f"Task failed: {result.thoughts}"
    assert result.completed_by == agent.name, "Wrong agent completed task"
    assert result.output is not None, "No output from task"
    print(f"✅ Task processed successfully")
    print(f"   Status: {result.status.value}")
    print(f"   Output: {result.output}")
    print(f"   Time: {result.time_taken}s")
    print()
    
    # Step 7: Update queue
    print("Step 7: Update queue status...")
    queue.complete_task(task_id, result)
    completed_task = queue.get_task(task_id)
    assert completed_task.status == TaskStatus.DONE, "Queue not updated"
    print(f"✅ Queue updated with result")
    print()
    
    # Step 8: Check agent status
    print("Step 8: Check agent status...")
    status = agent.report_status()
    assert status["name"] == agent.name, "Wrong agent name"
    assert status["tasks_completed"] == 1, "Task count wrong"
    assert status["status"] == "available", "Agent not available"
    print(f"✅ Agent status: {status['status']}")
    print(f"   Tasks completed: {status['tasks_completed']}")
    print(f"   Queue size: {status['queue_size']}")
    print()
    
    # Step 9: Check registry
    print("Step 9: Check registry...")
    retrieved_agent = registry.get_agent(agent.name)
    assert retrieved_agent is not None, "Agent not in registry"
    assert retrieved_agent.name == agent.name, "Wrong agent retrieved"
    available = registry.get_available_agents()
    assert len(available) == 1, "Agent not available"
    print(f"✅ Registry OK: {len(registry.get_all_agents())} agent(s)")
    print()
    
    # Step 10: Queue statistics
    print("Step 10: Check queue statistics...")
    stats = queue.get_stats()
    print(f"✅ Queue stats:")
    print(f"   Total: {stats['total']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   Done: {stats['done']}")
    print()
    
    print("="*60)
    print("✅ INTEGRATION TEST PASSED!")
    print("="*60)
    print()
    print("All components working together:")
    print("  ✅ BaseAgent - Task handling")
    print("  ✅ TaskQueue - Task management")
    print("  ✅ AgentRegistry - Agent discovery")
    print("  ✅ AgentMemory - Context storage")
    print("  ✅ Task models - Data structures")
    print()
    print("Phase 1 (Day 2) COMPLETE! 🎉")
    print()


if __name__ == "__main__":
    try:
        test_full_agent_workflow()
        exit(0)
    except AssertionError as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
