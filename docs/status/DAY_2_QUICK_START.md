# 🚀 DAY 2 QUICK START - Agent Framework Core

**Date:** 2025-11-03 (Tomorrow)  
**Phase:** Core Implementation  
**Owner:** Tomasz Kamiński (Developer)  
**Goal:** Working BaseAgent + Task system  

---

## ☕ MORNING SESSION (3-4 hours)

### Step 1: Create File Structure (15 min)

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Create agents directory
mkdir -p agents
mkdir -p agents/specialized
mkdir -p tests

# Create core files
touch agents/base_agent.py
touch agents/task_models.py
touch agents/task_queue.py
touch agents/agent_memory.py
touch agents/agent_registry.py
touch agents/__init__.py

# Create test files
touch tests/test_base_agent.py
touch tests/test_task_queue.py
touch tests/__init__.py
```

---

### Step 2: Implement Task Models (30 min)

**File:** `agents/task_models.py`

**Copy from:** AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md section "Template 2"

**Key classes:**
- `TaskStatus` enum
- `Task` dataclass
- `TaskResult` dataclass
- `TaskAck` dataclass

**Test:**
```bash
# FIRST: Sanity check imports (5 sec)
python3 -m agents.task_models
# Should exit cleanly (no output = good)

# THEN: Run comprehensive smoke test
python3 DAY_2_SMOKE_TESTS.py --step 1
# This will verify Task creation, TaskResult, TaskStatus enum, etc.
```

---

### Step 3: Implement AgentMemory (30 min)

**File:** `agents/agent_memory.py`

**Wrapper around HelenaCore for per-agent storage**

**Test:**
```bash
# FIRST: Sanity check imports
python3 -m agents.agent_memory

# THEN: Run smoke test with save/load verification:
python3 DAY_2_SMOKE_TESTS.py --step 2
# This will verify save() and load() actually work with HelenaCore
```

---

### Step 4: Implement BaseAgent (90 min)

**File:** `agents/base_agent.py`

**Copy template from guide, customize as needed**

**Key methods:**
- `__init__` - Initialize agent
- `receive_task` - Accept task
- `process_task` - Execute task
- `_execute_work` - Override point for specializations
- `save_to_memory` - Save context
- `load_context` - Load context

**Test:**
```bash
# FIRST: Sanity check imports
python3 -m agents.base_agent

# THEN: Run smoke test that verifies task receive/process:
python3 DAY_2_SMOKE_TESTS.py --step 3
# This will test receive_task(), process_task(), and report_status()
```

---

## 🍕 LUNCH BREAK (1 hour)

**Check progress - ALL smoke tests must PASS:**
- [ ] Task models created ✅
- [ ] Smoke test 1: `python3 DAY_2_SMOKE_TESTS.py --step 1` → PASS ✅
- [ ] AgentMemory working ✅
- [ ] Smoke test 2: `python3 DAY_2_SMOKE_TESTS.py --step 2` → PASS ✅
- [ ] BaseAgent functional ✅
- [ ] Smoke test 3: `python3 DAY_2_SMOKE_TESTS.py --step 3` → PASS ✅

**⚠️ If any smoke test fails, debug before continuing!**

---

## 🌆 AFTERNOON SESSION (3-4 hours)

### Step 5: Implement TaskQueue (60 min)

**File:** `agents/task_queue.py`

**Priority queue with task management**

**Test:**
```bash
# Run smoke test that verifies queue operations:
python3 DAY_2_SMOKE_TESTS.py --step 4
# This will test add_task(), assign_to_agent(), complete_task(), etc.
```

---

### Step 6: Implement AgentRegistry (45 min)

**File:** `agents/agent_registry.py`

**Agent discovery and routing**

**Test:**
```bash
# Run smoke test that verifies registry operations:
python3 DAY_2_SMOKE_TESTS.py --step 5
# This will test register(), get_agent(), find_by_role(), etc.
```

---

### Step 7: Integration Test (60 min)

**Create:** `test_day2_integration.py`

**Test workflow:**
```python
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskStatus
from agents.task_queue import TaskQueue
from agents.agent_registry import AgentRegistry
import uuid
from datetime import datetime

# Initialize components
queue = TaskQueue()
registry = AgentRegistry()

# Create agent
agent = BaseAgent("Test Agent", "Tester", "Testing")
registry.register(agent)

# Create task
task = Task(
    task_id=uuid.uuid4(),
    title="Test Task",
    description="Test the system",
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

# Workflow
queue.add_task(task)
agent.receive_task(task)
result = agent.process_task(task)

# Verify
assert result.status == TaskStatus.DONE
assert result.completed_by == agent.name
print("✅ INTEGRATION TEST PASSED!")
```

**Run:**
```bash
python3 test_day2_integration.py
```

---

### Step 8: Documentation & Commit (30 min)

**Update:** `PROJECT_STATUS_FINAL.md`

**Use prepared template:**
```bash
# Copy from DAY_2_PROJECT_STATUS_TEMPLATE.md
# Fill in:
# - Actual commit hash
# - Test results
# - Issues encountered (if any)
# - Time taken
# - Lessons learned

# Then append to PROJECT_STATUS_FINAL.md
cat DAY_2_PROJECT_STATUS_TEMPLATE.md >> PROJECT_STATUS_FINAL.md
```

**Template location:** `DAY_2_PROJECT_STATUS_TEMPLATE.md`  
**Instructions:** Fill in bracketed sections before committing

**Commit:**
```bash
git add agents/ tests/ DAY_2_SMOKE_TESTS.py

# Multi-line commit (proper syntax):
# NOTE: Adjust "Testing:" section based on what actually got done!

# If BOTH unit tests AND smoke tests done:
git commit -m "Implement Agent Framework Core - Phase 1 (Day 2)" \
           -m "Core Infrastructure:" \
           -m "- BaseAgent foundation class (~250 lines)" \
           -m "- Task management system (Task, TaskQueue, TaskResult)" \
           -m "- AgentMemory integration with HelenaCore" \
           -m "- AgentRegistry for agent discovery" \
           -m "" \
           -m "Testing:" \
           -m "- Unit tests for BaseAgent and TaskQueue" \
           -m "- Comprehensive smoke tests (5 components)" \
           -m "- Integration test for full workflow" \
           -m "- All tests passing ✅" \
           -m "" \
           -m "Progress: Day 2/5 complete (40%)" \
           -m "Next: Day 3 - Implement 9 specialized agent classes"

# If ONLY smoke tests done (no time for unit tests):
git commit -m "Implement Agent Framework Core - Phase 1 (Day 2)" \
           -m "Core Infrastructure:" \
           -m "- BaseAgent foundation class (~250 lines)" \
           -m "- Task management system (Task, TaskQueue, TaskResult)" \
           -m "- AgentMemory integration with HelenaCore" \
           -m "- AgentRegistry for agent discovery" \
           -m "" \
           -m "Testing:" \
           -m "- Comprehensive smoke tests (5 components)" \
           -m "- Integration test for full workflow" \
           -m "- All tests passing ✅" \
           -m "- Unit tests deferred to Day 3" \
           -m "" \
           -m "Progress: Day 2/5 complete (40%)" \
           -m "Next: Day 3 - Implement specialized agents + unit tests"

# Get commit hash for documentation:
git log -1 --oneline
```

---

## ✅ END OF DAY 2 CHECKLIST

### Core Files
- [ ] All 5 core files created (base_agent, task_models, etc.)
- [ ] BaseAgent class functional
- [ ] Task system working

### Testing (MANDATORY - All must PASS)
- [ ] Smoke test 1 (task_models): `python3 DAY_2_SMOKE_TESTS.py --step 1` → **PASS** ✅
- [ ] Smoke test 2 (agent_memory): `python3 DAY_2_SMOKE_TESTS.py --step 2` → **PASS** ✅
- [ ] Smoke test 3 (base_agent): `python3 DAY_2_SMOKE_TESTS.py --step 3` → **PASS** ✅
- [ ] Smoke test 4 (task_queue): `python3 DAY_2_SMOKE_TESTS.py --step 4` → **PASS** ✅
- [ ] Smoke test 5 (agent_registry): `python3 DAY_2_SMOKE_TESTS.py --step 5` → **PASS** ✅
- [ ] Integration test: `python3 test_day2_integration.py` → **PASS** ✅

**⚠️ Save smoke test output to project log for documentation!**

### Documentation & Git
- [ ] Code committed (with appropriate message variant)
- [ ] Documentation updated (PROJECT_STATUS_FINAL.md)
- [ ] Commit hash recorded

### Ready for Day 3
- [ ] All tests passing
- [ ] Core infrastructure complete
- [ ] Ready for specialized agents

---

## 📊 SUCCESS METRICS

**Code Created:**
- Lines of code: ~600-800
- Files: 5 core files
- Tests: 2-3 test files

**Functionality:**
- ✅ Agent can receive tasks
- ✅ Agent can process tasks
- ✅ Agent saves to memory
- ✅ Task queue manages tasks
- ✅ Registry tracks agents

**Time:**
- Planned: 6-8 hours
- Actual: [Record here]

---

## 🚨 IF STUCK

**Problem: Code doesn't work**
- Check AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md for examples
- Verify all imports
- Run tests individually
- Ask Helena for context

**Problem: Integration issues**
- Verify HelenaCore still works
- Check database connections
- Test each component separately

**Problem: Time running out**
- Focus on BaseAgent ONLY
- Skip AgentRegistry if needed (add Day 3)
- Skip some tests (add later)
- Goal: Working BaseAgent is minimum

---

## 🎯 TOMORROW'S FOCUS

**One clear goal:**

> **Build working BaseAgent class that can receive and execute tasks**

Everything else is supporting that goal.

If Day 2 ends with working BaseAgent + Task system = SUCCESS ✅

---

## 💪 MOTIVATION

After Day 2, we'll have:
- Foundation for all 9 agents
- Task management system
- Clear path to completion

This is the hardest day. Days 3-5 will be easier (repeating patterns).

**You got this!** 🚀

---

**Quick Start Guide by:** Aleksander Nowak  
**For:** Day 2 Implementation  
**Status:** Ready to use tomorrow morning  
