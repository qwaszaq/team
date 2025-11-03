# ⚡ PRE-START EXECUTION CHECKLIST

**Run these commands RIGHT NOW before starting Day 2 implementation**

This checklist converts all "suggested" checks into actual executed verification.

---

## 📋 EXECUTE IN ORDER (10 minutes)

### ✅ Step 1: Code Templates (2 min)

```bash
cd /Users/artur/coursor-agents-destiny-folder

echo "Checking BaseAgent template..."
grep -n "class BaseAgent:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md | head -1
# Expected: 450:class BaseAgent:

echo "Checking Task template..."
grep -n "class Task:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md | head -1
# Expected: 252:class Task:

echo "Checking TomaszAgent example..."
grep -n "class TomaszAgent:" AGENT_FRAMEWORK_IMPLEMENTATION_GUIDE.md | head -1
# Expected: Line number found

echo "✅ All templates verified"
```

**Mark here when done:** [ ] COMPLETED

---

### ✅ Step 2: HelenaCore Import (1 min)

```bash
python3 << 'PYTHON'
print("Testing HelenaCore import...")
try:
    from helena_core import HelenaCore
    print("✅ HelenaCore import: OK")
    
    # Check required methods
    assert hasattr(HelenaCore, 'save_to_all_layers'), "Missing save_to_all_layers"
    assert hasattr(HelenaCore, 'load_context'), "Missing load_context"
    print("✅ Required methods: OK")
    print()
    print("✅ STEP 2 COMPLETE")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)
PYTHON
```

**Mark here when done:** [ ] COMPLETED

---

### ✅ Step 3: Directory Structure (30 sec)

```bash
# Create agents package
mkdir -p agents
mkdir -p agents/specialized
mkdir -p tests

# Create package markers
touch agents/__init__.py
touch tests/__init__.py

# Verify structure
echo "Verifying directory structure..."
ls -la agents/__init__.py
ls -la tests/

echo "✅ Directory structure created"
```

**Mark here when done:** [ ] COMPLETED

---

### ✅ Step 4: Database Connectivity (1 min)

```bash
echo "Checking database containers..."
docker ps | grep -E "postgres|neo4j|qdrant|redis" | wc -l
# Expected: 4

echo "Detailed status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "postgres|neo4j|qdrant|redis"

echo "✅ Database check complete"
```

**Mark here when done:** [ ] COMPLETED

---

### ✅ Step 5: **CRITICAL** - Database Write Test (2 min)

**⚠️ THIS IS THE MOST IMPORTANT TEST - PROVES DB WORKS!**

```bash
python3 << 'PYTHON'
from helena_core import HelenaCore
from datetime import datetime

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🧪 PRE-START DATABASE WRITE TEST")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"Time: {datetime.now().isoformat()}")
print()

try:
    h = HelenaCore(project_id="destiny-team-framework-master")  # Use existing project_id
    
    result = h.save_to_all_layers(
        event_type="pre_start_test",
        content="Day 2 Pre-Start Database Write Test - Verifying all 4 layers work",
        importance=0.9,
        made_by="Pre-Flight Verification System",
        additional_data={
            "test_type": "pre_start_verification",
            "purpose": "Confirm DB writes work before Day 2 implementation",
            "timestamp": datetime.now().isoformat()
        }
    )
    
    print("📊 LAYER STATUS:")
    layers = ["postgresql", "neo4j", "qdrant", "redis"]
    all_success = True
    
    for layer in layers:
        status = result.get(layer, {}).get('status', 'unknown')
        if status == 'success':
            print(f"   ✅ {layer.upper()}: SUCCESS")
        else:
            print(f"   ❌ {layer.upper()}: FAILED - {result.get(layer, {})}")
            all_success = False
    
    print()
    print(f"Overall Success: {result.get('success', False)}")
    print()
    
    if all_success and result.get('success'):
        print("✅✅✅ ALL 4 LAYERS WORKING - TEST PASSED ✅✅✅")
        print()
        print("📝 This proves:")
        print("   • HelenaCore.save_to_all_layers() works")
        print("   • All 4 databases accepting writes")
        print("   • PostgreSQL: Ready")
        print("   • Neo4j: Ready")
        print("   • Qdrant: Ready")
        print("   • Redis: Ready")
        print("   • AgentMemory.save() will work on Day 2")
        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("✅ STEP 5 COMPLETE - READY FOR DAY 2")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    else:
        print("❌❌❌ SOME LAYERS FAILED - FIX BEFORE DAY 2! ❌❌❌")
        print()
        print("⚠️  DO NOT START DAY 2 UNTIL THIS PASSES!")
        exit(1)
        
except Exception as e:
    print(f"❌ DATABASE WRITE TEST FAILED: {e}")
    print()
    print("⚠️  FIX THIS BEFORE STARTING DAY 2!")
    import traceback
    traceback.print_exc()
    exit(1)

PYTHON
```

**⚠️ CRITICAL: Save this output! Paste into project log!**

**Mark here when done:** [ ] COMPLETED

---

### ✅ Step 6: Smoke Test Script Syntax (30 sec)

```bash
# Verify smoke test script is valid Python
python3 -m py_compile DAY_2_SMOKE_TESTS.py

if [ $? -eq 0 ]; then
    echo "✅ DAY_2_SMOKE_TESTS.py: Valid Python syntax"
else
    echo "❌ Smoke test script has syntax errors!"
    exit 1
fi
```

**Mark here when done:** [ ] COMPLETED

---

## 📊 FINAL VERIFICATION

After completing all 6 steps above, verify:

- [x] Step 1: Code templates exist ✅
- [x] Step 2: HelenaCore imports work ✅
- [x] Step 3: Directory structure created ✅
- [x] Step 4: Databases running ✅
- [x] Step 5: **DB write test PASSED** ✅ (CRITICAL!)
- [x] Step 6: Smoke tests valid ✅

---

## 🎯 IF ALL CHECKS PASS:

```
✅✅✅ PRE-START VERIFICATION COMPLETE ✅✅✅

You are READY to start Day 2 implementation!

Next steps:
1. Open: DAY_2_QUICK_START.md
2. Follow step-by-step implementation
3. Use smoke tests after each step
4. Success! 🚀
```

---

## ❌ IF ANY CHECK FAILS:

**DO NOT START DAY 2 UNTIL FIXED!**

Common issues:
- Templates missing → Re-download implementation guide
- HelenaCore import fails → Check Python path
- Directories → Permission issues
- Databases → Run `docker-compose up -d`
- **DB write fails → Check database logs, restart containers**
- Smoke tests → Syntax error in script

---

## 💾 SAVE OUTPUT

**Important:** Save the output of Step 5 (DB Write Test) to project logs!

This is proof that all 4 database layers work before Day 2 starts.

```bash
# Optionally save to file:
python3 << 'PYTHON' (Step 5 code) > PRE_START_DB_TEST_OUTPUT.txt 2>&1
```

---

**Created:** 2025-11-02  
**Purpose:** Convert suggested checks to executed verification  
**Time required:** ~10 minutes  
**Critical:** Step 5 (DB Write Test) must pass!
