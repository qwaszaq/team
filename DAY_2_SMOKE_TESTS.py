"""
Day 2 Smoke Tests - Proper verification of each component
Run after implementing each file to verify it actually works

Usage:
    python3 DAY_2_SMOKE_TESTS.py --step 1  # Test task_models.py
    python3 DAY_2_SMOKE_TESTS.py --step 2  # Test agent_memory.py
    python3 DAY_2_SMOKE_TESTS.py --step 3  # Test base_agent.py
    python3 DAY_2_SMOKE_TESTS.py --step 4  # Test task_queue.py
    python3 DAY_2_SMOKE_TESTS.py --step 5  # Test agent_registry.py
    python3 DAY_2_SMOKE_TESTS.py --all     # Run all tests
"""

import sys
import uuid
from datetime import datetime


def test_task_models():
    """Test task_models.py - More than just import"""
    print("\n" + "="*60)
    print("🧪 SMOKE TEST 1: task_models.py")
    print("="*60)
    
    try:
        from agents.task_models import Task, TaskStatus, TaskResult, TaskAck
        
        # Test 1: Create Task
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Testing task creation",
            assigned_to="Test Agent",
            assigned_by="Tester",
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
        print(f"✅ Task creation: OK")
        print(f"   - ID: {task.task_id}")
        print(f"   - Status: {task.status}")
        
        # Test 2: Create TaskResult
        result = TaskResult(
            task_id=task.task_id,
            completed_by="Test Agent",
            status=TaskStatus.DONE,
            output="Test output",
            thoughts="Test thoughts",
            time_taken=1.0,
            artifacts=[],
            next_steps=None
        )
        print(f"✅ TaskResult creation: OK")
        
        # Test 3: TaskStatus enum
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.DONE.value == "done"
        print(f"✅ TaskStatus enum: OK")
        
        # Test 4: TaskAck
        ack = TaskAck(
            task_id=task.task_id,
            agent="Test Agent",
            status="acknowledged",
            eta_minutes=30
        )
        print(f"✅ TaskAck creation: OK")
        
        print("\n✅ SMOKE TEST 1: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ SMOKE TEST 1: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_memory():
    """Test agent_memory.py - Verify it can save/load"""
    print("\n" + "="*60)
    print("🧪 SMOKE TEST 2: agent_memory.py")
    print("="*60)
    
    try:
        from agents.agent_memory import AgentMemory
        
        # Test 1: Create AgentMemory
        memory = AgentMemory(
            agent_name="Test Agent",
            project_id="test-project"
        )
        print(f"✅ AgentMemory creation: OK")
        
        # Test 2: Save to memory (will hit HelenaCore)
        result = memory.save(
            content="Test memory content",
            importance=0.8,
            context_type="test"
        )
        print(f"✅ Memory save: OK")
        print(f"   - Result: {result.get('success', False)}")
        
        # Test 3: Load from memory (basic query)
        # NOTE: This might return empty if no prior context
        contexts = memory.load("test", limit=1)
        print(f"✅ Memory load: OK")
        print(f"   - Retrieved: {len(contexts)} items")
        
        print("\n✅ SMOKE TEST 2: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ SMOKE TEST 2: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_base_agent():
    """Test base_agent.py - Verify agent can receive/process tasks"""
    print("\n" + "="*60)
    print("🧪 SMOKE TEST 3: base_agent.py")
    print("="*60)
    
    try:
        from agents.base_agent import BaseAgent, AgentStatus
        from agents.task_models import Task, TaskStatus
        
        # Test 1: Create BaseAgent
        agent = BaseAgent(
            name="Test Agent",
            role="Tester",
            specialization="Testing",
            project_id="test-project"
        )
        print(f"✅ BaseAgent creation: OK")
        print(f"   - Name: {agent.name}")
        print(f"   - Status: {agent.status}")
        
        # Test 2: Create and receive task
        task = Task(
            task_id=uuid.uuid4(),
            title="Test Task",
            description="Do something",
            assigned_to=agent.name,
            assigned_by="Tester",
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
        print(f"✅ Task receipt: OK")
        print(f"   - Queue size: {len(agent.task_queue)}")
        
        # Test 3: Process task (calls _execute_work)
        result = agent.process_task(task)
        print(f"✅ Task processing: OK")
        print(f"   - Result status: {result.status}")
        print(f"   - Completed: {agent.tasks_completed}")
        
        # Test 4: Report status
        status = agent.report_status()
        print(f"✅ Status report: OK")
        print(f"   - Agent status: {status['status']}")
        print(f"   - Tasks done: {status['tasks_completed']}")
        
        print("\n✅ SMOKE TEST 3: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ SMOKE TEST 3: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_task_queue():
    """Test task_queue.py - Verify queue operations"""
    print("\n" + "="*60)
    print("🧪 SMOKE TEST 4: task_queue.py")
    print("="*60)
    
    try:
        from agents.task_queue import TaskQueue
        from agents.task_models import Task, TaskStatus, TaskResult
        
        # Test 1: Create TaskQueue
        queue = TaskQueue()
        print(f"✅ TaskQueue creation: OK")
        
        # Test 2: Add tasks
        task1 = Task(
            task_id=uuid.uuid4(),
            title="Task 1",
            description="First task",
            assigned_to="Agent1",
            assigned_by="Tester",
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
            description="Second task (high priority)",
            assigned_to="Agent1",
            assigned_by="Tester",
            context={},
            priority=5,  # Higher priority
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
        print(f"✅ Task addition: OK (2 tasks added)")
        
        # Test 3: Assign to agent
        queue.assign_to_agent(task1.task_id, "Agent1")
        print(f"✅ Task assignment: OK")
        
        # Test 4: Get agent's tasks
        agent_tasks = queue.get_agent_tasks("Agent1")
        print(f"✅ Get agent tasks: OK ({len(agent_tasks)} tasks)")
        
        # Test 5: Complete task
        result = TaskResult(
            task_id=task1.task_id,
            completed_by="Agent1",
            status=TaskStatus.DONE,
            output="Done",
            thoughts="Completed",
            time_taken=1.0,
            artifacts=[],
            next_steps=None
        )
        queue.complete_task(task1.task_id, result)
        print(f"✅ Task completion: OK")
        
        print("\n✅ SMOKE TEST 4: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ SMOKE TEST 4: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_registry():
    """Test agent_registry.py - Verify agent management"""
    print("\n" + "="*60)
    print("🧪 SMOKE TEST 5: agent_registry.py")
    print("="*60)
    
    try:
        from agents.agent_registry import AgentRegistry
        from agents.base_agent import BaseAgent, AgentStatus
        
        # Test 1: Create registry
        registry = AgentRegistry()
        print(f"✅ AgentRegistry creation: OK")
        
        # Test 2: Register agents
        agent1 = BaseAgent("Agent 1", "Role 1", "Spec 1", "test")
        agent2 = BaseAgent("Agent 2", "Role 2", "Spec 2", "test")
        
        registry.register(agent1)
        registry.register(agent2)
        print(f"✅ Agent registration: OK (2 agents)")
        
        # Test 3: Get agent by name
        retrieved = registry.get_agent("Agent 1")
        assert retrieved is not None
        assert retrieved.name == "Agent 1"
        print(f"✅ Get agent: OK")
        
        # Test 4: Get all agents
        all_agents = registry.get_all_agents()
        assert len(all_agents) == 2
        print(f"✅ Get all agents: OK ({len(all_agents)} agents)")
        
        # Test 5: Find by role
        by_role = registry.find_by_role("Role 1")
        assert len(by_role) == 1
        print(f"✅ Find by role: OK")
        
        print("\n✅ SMOKE TEST 5: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ SMOKE TEST 5: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run smoke tests based on command line args"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 DAY_2_SMOKE_TESTS.py [--step N | --all]")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    print("\n" + "🔥"*30)
    print("DAY 2 SMOKE TESTS - Proper Verification")
    print("🔥"*30)
    
    if arg == "--all":
        results = []
        results.append(("Task Models", test_task_models()))
        results.append(("Agent Memory", test_agent_memory()))
        results.append(("Base Agent", test_base_agent()))
        results.append(("Task Queue", test_task_queue()))
        results.append(("Agent Registry", test_agent_registry()))
        
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        for name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {name}")
        
        all_passed = all(r[1] for r in results)
        if all_passed:
            print("\n🎉 ALL TESTS PASSED! Ready for integration!")
        else:
            print("\n❌ Some tests failed. Fix before proceeding.")
            sys.exit(1)
            
    elif arg == "--step":
        if len(sys.argv) < 3:
            print("Usage: python3 DAY_2_SMOKE_TESTS.py --step N")
            sys.exit(1)
        
        step = int(sys.argv[2])
        tests = [
            test_task_models,
            test_agent_memory,
            test_base_agent,
            test_task_queue,
            test_agent_registry
        ]
        
        if 1 <= step <= len(tests):
            success = tests[step - 1]()
            sys.exit(0 if success else 1)
        else:
            print(f"Invalid step: {step}. Must be 1-{len(tests)}")
            sys.exit(1)
    else:
        print(f"Unknown argument: {arg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
