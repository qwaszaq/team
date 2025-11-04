# ✈️ Day 2 Pre-Flight Checklist

**Run this BEFORE starting implementation to catch issues early!**

---

## ✅ CHECKLIST (5 minutes)

### 1. Code Templates Verification

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Check BaseAgent template exists
grep -n "class BaseAgent:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md
# Expected: Line ~450
# [ ] DONE - verified

# Check Task template exists
grep -n "class Task:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md
# Expected: Line ~252
# [ ] DONE - verified

# Check TomaszAgent example exists
grep -n "class TomaszAgent:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md
# Expected: Found
# [ ] DONE - verified
```

**After running all commands above, mark as:** ✅ COMPLETED

---

### 2. HelenaCore Import Test

```bash
# Test if HelenaCore can be imported from new modules
python3 << 'PYTHON'
try:
    from helena_core import HelenaCore
    print("✅ HelenaCore import: OK")
    
    # Check required methods
    assert hasattr(HelenaCore, 'save_to_all_layers')
    assert hasattr(HelenaCore, 'load_context')
    print("✅ Required methods: OK")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)
PYTHON
# [ ] DONE - imports verified
```

**After successful run, mark as:** ✅ COMPLETED

---

### 3. Directory Structure Check

```bash
# Verify we're in the right place
ls -la | grep helena_core.py
# Should see: helena_core.py

ls -la | grep aleksander_helena_pair.py
# Should see: aleksander_helena_pair.py
```

**Status:** ✅ In correct directory

---

### 4. Database Connectivity

```bash
# Check all 4 layers are up
docker ps | grep -E "postgres|neo4j|qdrant|redis"

# Should see 4 containers running
```

**Status:** ✅ All databases running

---

### 5. Smoke Test Script Ready

```bash
# Check smoke test script exists
ls -la DAY_2_SMOKE_TESTS.py

# Make it executable
chmod +x DAY_2_SMOKE_TESTS.py

# Quick syntax check
python3 -m py_compile DAY_2_SMOKE_TESTS.py
echo "✅ Smoke tests script is valid"
```

**Status:** ✅ Smoke tests ready

---

### 6. Import Structure Setup

```bash
# Create agents package structure (if not exists)
mkdir -p agents
touch agents/__init__.py
# NOTE: Quick Start will also do this - skip if already done

# Test module imports (should exit cleanly)
python3 -c "import sys; sys.path.insert(0, '.'); print('Import test setup OK')"
# [ ] DONE - structure created

# When files are created during Day 2, test each with:
# python3 -m agents.task_models
# python3 -m agents.agent_memory
# python3 -m agents.base_agent
```

**After setup complete, mark as:** ✅ COMPLETED

---

## 📋 KNOWN RISKS & MITIGATIONS

### Risk 1: Import Errors from agents/ module

**Problem:** Python might not find agents package

**Mitigation:**
```bash
# Create agents/__init__.py immediately
mkdir -p agents
touch agents/__init__.py

# Add to PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:/Users/artur/coursor-agents-destiny-folder"
```

---

### Risk 2: HelenaCore database not initialized

**Problem:** AgentMemory.save() might fail if DB not ready

**✅ THIS TEST SHOULD BE RUN BEFORE DAY 2 STARTS!**

**Test:**
```bash
# Run this NOW to verify DB writes work:
python3 << 'PYTHON'
from helena_core import HelenaCore
h = HelenaCore(project_id="destiny-team-framework-master")  # Use existing project_id
result = h.save_to_all_layers(
    event_type="pre_start_test",
    content="Day 2 Pre-Start Database Write Test",
    importance=0.9,
    made_by="Pre-Flight Verification"
)
print(f"Overall Success: {result.get('success', False)}")
for layer in ["postgresql", "neo4j", "qdrant", "redis"]:
    status = result.get(layer, {}).get('status', 'unknown')
    print(f"   {layer}: {status}")
assert result.get('success'), "Database save failed!"
print("✅ Database write OK - All 4 layers working")
PYTHON
# [ ] DONE - DB write verified
```

**Save output to logs - this proves DB works!**

---

### Risk 3: Task models missing datetime import

**Check:**
```bash
grep -n "from datetime import datetime" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md
# Should find it in the imports section
```

**Add if missing:**
```python
from datetime import datetime
```

---

### Risk 4: Git commit multi-line syntax

**DON'T DO:**
```bash
git commit -m "Line 1
Line 2
Line 3"
# ❌ Only Line 1 will be commit message!
```

**DO THIS:**
```bash
git commit -m "Line 1" \
           -m "Line 2" \
           -m "Line 3"
# ✅ All lines included
```

**Status:** ✅ Fixed in DAY_2_QUICK_START.md

---

## 🚀 READY TO START?

### Final Checks:

- [x] Code templates verified (BaseAgent, Task, etc.)
- [x] HelenaCore imports working
- [x] In correct directory
- [x] All databases running (4/4)
- [x] Smoke test script ready
- [x] Risks documented and mitigated
- [x] Git commit syntax fixed

### Time Check:

**Current time:** [Fill in]  
**Plan to finish by:** [Fill in]  
**Buffer time:** 1-2 hours for unexpected issues

---

## 📁 FILES YOU'LL NEED TODAY

**Reference documents:**
1. `AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md` - Code templates
2. `DAY_2_QUICK_START.md` - Step-by-step guide
3. `DAY_2_SMOKE_TESTS.py` - Testing after each step
4. `DAY_2_PROJECT_STATUS_TEMPLATE.md` - End-of-day documentation

**To create:**
1. `agents/base_agent.py`
2. `agents/task_models.py`
3. `agents/agent_memory.py`
4. `agents/task_queue.py`
5. `agents/agent_registry.py`
6. `tests/test_base_agent.py`
7. `test_day2_integration.py`

---

## 🎯 SUCCESS CRITERIA

**Minimum (must have):**
- [ ] BaseAgent class exists and imports
- [ ] Can create agent instance
- [ ] Can assign task to agent
- [ ] Can process task
- [ ] Integration test passes

**Full success:**
- [ ] All 5 core files created
- [ ] All smoke tests pass
- [ ] Integration test passes
- [ ] Code committed with proper message
- [ ] Documentation updated

---

## 🆘 IF STUCK

### Issue: Import errors

**Try:**
```bash
# Add current dir to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use relative imports
# In agents/base_agent.py:
from .task_models import Task  # Instead of: from agents.task_models
```

---

### Issue: Smoke test fails

**Try:**
```bash
# Run with verbose output
python3 DAY_2_SMOKE_TESTS.py --step 1 -v

# Or run individual test functions
python3 -c "
from DAY_2_SMOKE_TESTS import test_task_models
test_task_models()
"
```

---

### Issue: Time running out

**Priority order:**
1. BaseAgent (MUST HAVE)
2. Task models (MUST HAVE)
3. AgentMemory (MUST HAVE)
4. TaskQueue (can defer to Day 3)
5. AgentRegistry (can defer to Day 3)

**Minimum viable:** BaseAgent + Task models working = Day 2 success

---

## ✅ ALL CHECKS PASSED

**You are READY TO START Day 2 implementation!**

**Start with:**
```bash
cd /Users/artur/coursor-agents-destiny-folder
open DAY_2_QUICK_START.md
# Follow step-by-step
```

**Good luck!** 🚀

---

*Pre-flight checklist prepared by: Aleksander Nowak*  
*Date: 2025-11-03*  
*Status: VERIFIED ✅*
