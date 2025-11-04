# 🎯 EVALUATOR QUICK REFERENCE CARD

**Keep this open while evaluating!**

---

## 🚀 **QUICK COMMANDS**

```bash
# Installation
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pip3 install -e .

# Health check
destiny memory health

# See team status
destiny status

# Monitor progress
destiny memory stats
destiny memory search "dashboard"
destiny memory relationships

# Get agent output
destiny memory agent tomasz
destiny memory agent anna
```

---

## 📊 **WHAT TO WATCH FOR**

### **✅ REAL Agents:**
- Different terminology per role
- Unique artifacts (code, designs, tests)
- Build on each other's work
- Reference previous decisions

### **❌ THEATRICAL Agents:**
- Similar text structure
- Generic language
- No collaboration
- Isolated outputs

---

## 🎯 **SCORING CHEAT SHEET**

| Score | Meaning | What You'll See |
|-------|---------|-----------------|
| **A+ (135-150)** | Exceptional | Working dashboard, <15% similarity |
| **A (120-134)** | Excellent | Clear differentiation, good collaboration |
| **B (105-119)** | Very Good | Some differentiation, decent output |
| **C (90-104)** | Good | Mixed results, some theatrical elements |
| **D (75-89)** | Acceptable | Mostly theatrical, some variety |
| **F (<75)** | Failing | All agents sound the same |

---

## 📋 **EVALUATION CHECKLIST**

### **Phase 1: Tools (30 min)**
- [ ] `destiny memory stats` works
- [ ] `destiny memory search` works
- [ ] `destiny memory health` works
- [ ] `destiny memory agent` works
- [ ] `destiny memory relationships` works

### **Phase 2: Execution (45 min)**
- [ ] Task given to team
- [ ] Agents start working
- [ ] Progress visible
- [ ] Outputs saved to memory
- [ ] Collaboration visible

### **Phase 3: Analysis (30 min)**
- [ ] Measure output similarity
- [ ] Count unique artifacts
- [ ] Check collaboration patterns
- [ ] Verify memory growth
- [ ] Final scoring

---

## 🔍 **KEY QUESTIONS**

1. **Are outputs <20% similar?** (Target: YES)
2. **Do agents use different terminology?** (Target: YES)
3. **Do they create unique artifacts?** (Target: YES)
4. **Do they collaborate?** (Target: YES)
5. **Is memory system used?** (Target: YES)

---

## 💡 **COMMON ISSUES**

### **"No data found"**
- System is fresh, needs more agent tasks
- Run the challenge task first
- Check databases are running

### **"Collection not found"**
- Qdrant collection not seeded
- Run: `python3 seed_qdrant_test_collection.py`
- Not critical, tool handles gracefully

### **"PostgreSQL connection failed"**
- Missing "events" table
- Database setup issue, not code issue
- Other 3 DBs should work

---

## 🎯 **EXPECTED RESULTS**

### **After Challenge Task:**

**Memory Growth:**
- PostgreSQL: +20-50 events
- Neo4j: +15-30 relationships
- Qdrant: +10-25 vectors
- Redis: Variable (real-time cache)

**Unique Outputs:**
- PRD document (Katarzyna)
- UI mockups (Magdalena)
- Architecture diagram (Michał)
- Code files (Tomasz)
- Test files (Anna)
- Docker files (Piotr)

**Similarity:**
- Target: <20%
- Good: 20-30%
- Concerning: >40%

---

## 📁 **FILE LOCATIONS**

**Evaluator Guides:**
- `EVALUATOR_FINAL_PACKAGE.md` ← Main guide
- `EVALUATOR_QUICK_REFERENCE.md` ← This file
- `EVALUATOR_DESTINY_MEMORY.md` ← destiny-memory specific

**Challenge:**
- `CHALLENGE_TASK.md` ← Give to team

**Reference:**
- `MEMORY_COMMAND_GUIDE.md` ← Command details
- `INSTALLATION_GUIDE.md` ← Installation help
- `PROJECT_EXECUTIVE_SUMMARY.md` ← System overview

**Results:**
- `showcase_outputs/` ← Agent outputs
- Check with: `ls -la showcase_outputs/`

---

## 🎨 **TERMINAL COMMANDS FOR MONITORING**

### **Real-Time Monitoring (4 terminals):**

**Terminal 1:**
```bash
watch -n 5 'destiny memory stats'
```

**Terminal 2:**
```bash
watch -n 10 'destiny memory search "dashboard" --limit 3'
```

**Terminal 3:**
```bash
watch -n 15 'destiny status'
```

**Terminal 4:**
```bash
watch -n 20 'destiny memory relationships'
```

---

## 🎯 **ONE-PAGE SUMMARY**

### **What You're Evaluating:**
- Multi-agent system (9 agents)
- New CLI tool (destiny-memory)
- 4-database memory system
- Real task execution

### **How Long:**
- Phase 1 (Tools): 30 min
- Phase 2 (Execution): 45 min
- Phase 3 (Analysis): 30 min
- Report: 30 min
- **Total: ~2.5 hours**

### **What Matters Most:**
1. Are agents different? (<20% similarity)
2. Do they collaborate? (build on each other)
3. Does memory work? (data persists)
4. Is it production-ready? (quality code)

### **Final Output:**
- Score: ___/150
- Grade: A/B/C/D/F
- Recommendation: Ship / Fix / Reject

---

## 📞 **HELP**

**If stuck:**
1. Check `EVALUATOR_FINAL_PACKAGE.md` (full guide)
2. Check `MEMORY_COMMAND_GUIDE.md` (command help)
3. Run: `destiny --help`
4. Run: `destiny memory --help`

**Common fixes:**
```bash
# Reinstall if issues
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pip3 install --force-reinstall -e .

# Check databases
destiny memory health

# Verify installation
destiny --version
which destiny
```

---

## ✅ **PRE-FLIGHT CHECKLIST**

Before starting evaluation:

- [ ] destiny-cli installed (`pip3 install -e .`)
- [ ] `destiny --help` works
- [ ] `destiny memory stats` runs
- [ ] Databases checked (3-4 should be 🟢)
- [ ] Challenge task read (`CHALLENGE_TASK.md`)
- [ ] Evaluation template ready
- [ ] Timer ready (track time)
- [ ] Note-taking setup

**Ready?** Let's go! 🚀

---

## 🎉 **GOOD LUCK!**

You're about to:
- Test real CLI tools
- Watch agents collaborate
- Measure real differentiation
- Determine production readiness

**Be thorough. Be fair. Find the truth!** 🔍

---

**Time Started:** ___:___  
**Expected End:** ___:___

**Now go to:** `EVALUATOR_FINAL_PACKAGE.md` and begin! 🎯
