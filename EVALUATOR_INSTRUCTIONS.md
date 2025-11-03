# 📋 EVALUATOR INSTRUCTIONS

**Version:** 1.0  
**Purpose:** Complete step-by-step evaluation guide  
**Time Required:** 3 hours for full evaluation  
**Your Role:** Independent technical evaluator

---

## 🎯 YOUR MISSION

You are evaluating the **Destiny Team Framework** - a multi-agent AI system for software development. Your job is to:

1. **Run objective tests** - Execute commands, measure results
2. **Collect evidence** - Document all outputs
3. **Calculate scores** - Use provided rubrics
4. **Answer the core question** - Can this system enlarge context >1M tokens?
5. **Provide honest assessment** - Report strengths AND weaknesses
6. **Write detailed report** - Use provided template

**Critical:** Base conclusions on TEST RESULTS, not documentation or marketing.

---

## 📍 PROJECT LOCATION

```
Working Directory: /Users/artur/coursor-agents-destiny-folder
```

**All commands in this guide assume you're in this directory.**

---

## ⚠️ STAGE 0: ENVIRONMENT VERIFICATION (15 min)

**CRITICAL:** Verify environment before starting evaluation.

### **Test 0.1: Docker Containers**

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Check for 4 required containers
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(postgres|neo4j|redis|qdrant)"
```

**Expected Output:**
```
sms-postgres    Up X minutes
sms-neo4j       Up X minutes  
kg-redis        Up X minutes
sms-qdrant      Up X minutes
```

**Pass Criteria:** All 4 containers running

**If FAIL:** Report "Environment not ready - missing Docker containers" and STOP.

---

### **Test 0.2: Python Version**

```bash
python3 --version
```

**Expected:** Python 3.8.0 or higher

**If FAIL:** Report "Python 3.8+ required" and STOP.

---

### **Test 0.3: Core Files Exist**

```bash
ls -l helena_core.py aleksander_helena_pair.py test_full_project_loop.py TEST_CONTEXT_CAPACITY.py TEST_SYSTEM_CAPACITY_vs_USAGE.py
```

**Expected:** All 5 files exist

**If FAIL:** Report "Missing core files" and STOP.

---

### **Test 0.4: LM Studio (Optional)**

```bash
curl -s -m 5 http://localhost:1234/v1/models 2>/dev/null && echo "LM Studio: Running" || echo "LM Studio: Not running (OK - some tests will skip)"
```

**Expected:** Either running or not running is OK (affects some searches only)

---

**✅ If all Stage 0 tests PASS:** Document versions and proceed to Stage 1.

**❌ If any FAIL:** Cannot evaluate. Report environment issues.

---

## 📊 STAGE 1: CODE QUALITY ASSESSMENT (30 min)

**Objective:** Verify code exists, is substantial, and runs.

### **Test 1.1: File Existence and Size**

```bash
# Check files exist and show line counts
wc -l helena_core.py aleksander_helena_pair.py test_full_project_loop.py
```

**Expected Line Counts:**
- `helena_core.py`: 350-450 lines
- `aleksander_helena_pair.py`: 150-250 lines  
- `test_full_project_loop.py`: 250-350 lines

**Scoring:**
- All 3 files in expected range: **10 points**
- All 3 exist but some outside range: **7 points**
- Missing files or very small: **0-3 points**

**Document:** Actual line counts

---

### **Test 1.2: Code Quality Check**

```bash
# Count functions in each file
grep -c "^def " helena_core.py
grep -c "^def " aleksander_helena_pair.py

# Count docstrings
grep -c '"""' helena_core.py
grep -c '"""' aleksander_helena_pair.py

# Count error handling
grep -c "try:" helena_core.py
grep -c "try:" aleksander_helena_pair.py
```

**Expected:**
- Functions: 5+ per file
- Docstrings: 5+ per file
- Try blocks: 3+ per file

**Scoring:**
- All files have good indicators: **10 points**
- Most files have indicators: **7 points**
- Few indicators: **0-4 points**

**Document:** Counts for each metric

---

### **Test 1.3: helena_core.py Execution**

```bash
python3 helena_core.py > /tmp/helena_test.log 2>&1
echo "Exit code: $?"
tail -30 /tmp/helena_test.log
```

**Look for:**
- ✅ "SUCCESS" or "Operational" messages
- ✅ "✅" indicators
- ✅ Exit code 0
- ❌ Absence of "ERROR" or "FAILED"

**Scoring:**
- Runs cleanly with success indicators: **20 points**
- Runs with warnings but completes: **15 points**
- Fails or crashes: **0-10 points**

**Document:** Exit code, key output lines, any errors

---

### **Test 1.4: aleksander_helena_pair.py Execution**

```bash
python3 aleksander_helena_pair.py > /tmp/pair_test.log 2>&1
echo "Exit code: $?"
tail -30 /tmp/pair_test.log
```

**Same scoring as Test 1.3:** 20 points max

**Document:** Exit code, key output lines, any errors

---

### **Test 1.5: Code Not Mostly Comments**

```bash
# Check that code has more actual code than comments
python3 << 'EOF'
for fname in ['helena_core.py', 'aleksander_helena_pair.py']:
    with open(fname) as f:
        lines = f.readlines()
    code = [l for l in lines if l.strip() and not l.strip().startswith('#')]
    comments = [l for l in lines if l.strip().startswith('#')]
    ratio = len(code) / max(len(lines), 1) * 100
    print(f"{fname}: {ratio:.0f}% code")
EOF
```

**Expected:** >50% code (not comments)

**Scoring:**
- Both files >50% code: **10 points**
- One file >50%: **5 points**
- Both mostly comments: **0 points**

---

**STAGE 1 TOTAL:** ___/70 points

**Pass Threshold:** 50/70

**Weight in Final Score:** 15%

---

## 💾 STAGE 2: DATABASE FUNCTIONALITY (20 min)

**Objective:** Verify all databases operational with REAL data.

### **Test 2.1: PostgreSQL - Decision Count**

```bash
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT COUNT(*) as total_decisions 
FROM decisions;
"
```

**Expected:** ≥20 decisions

**Scoring:**
- ≥20 decisions: **10 points**
- 10-19 decisions: **7 points**
- <10 decisions: **0-5 points**

---

### **Test 2.2: PostgreSQL - Data Quality**

```bash
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE decision_text ILIKE '%test%' OR decision_text ILIKE '%foo%') as test_data
FROM decisions;
"
```

**Expected:** <30% test data (most should be real project decisions)

**Scoring:**
- <30% test data: **10 points**
- 30-50% test data: **5 points**
- >50% test data: **0 points**

---

### **Test 2.3: PostgreSQL - Recent Activity**

```bash
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT 
    COUNT(*) FILTER (WHERE timestamp > NOW() - INTERVAL '7 days') as recent_decisions
FROM decisions;
"
```

**Expected:** >0 (some recent activity)

**Scoring:**
- Recent activity exists: **5 points**
- No recent activity: **0 points**

---

### **Test 2.4: PostgreSQL - Sample Data**

```bash
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT decision_text, made_by, timestamp 
FROM decisions 
ORDER BY timestamp DESC 
LIMIT 3;
"
```

**Look for:** Real project decisions (not "test", "foo", "bar")

**Scoring:**
- Real project decisions visible: **5 points**
- Mix of real and test: **3 points**
- Only test data: **0 points**

---

### **Test 2.5: Qdrant Collection**

```bash
curl -s http://localhost:6333/collections/destiny-team-framework-master | python3 -c "
import sys, json
data = json.load(sys.stdin)['result']
print(f\"Points: {data['points_count']}\")
print(f\"Vector size: {data['config']['params']['vectors']['size']}\")
"
```

**Expected:**
- Points: ≥70
- Vector size: 1024 (E5-Large embeddings)

**Scoring:**
- ≥70 points, size 1024: **20 points**
- 50-69 points: **15 points**
- <50 points: **0-10 points**

---

### **Test 2.6: Neo4j Nodes**

```bash
docker exec sms-neo4j cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n) as total_nodes;" 2>/dev/null | grep -E "^[0-9]+" || echo "0"
```

**Expected:** >30 nodes

**Scoring:**
- >30 nodes: **10 points**
- 10-30 nodes: **5 points**
- <10 nodes: **0 points**

---

**STAGE 2 TOTAL:** ___/60 points

**Pass Threshold:** 40/60

**Weight in Final Score:** 10%

---

## 🚀 STAGE 3: FUNCTIONAL TESTING (45 min) ⭐ MOST CRITICAL

**Objective:** Verify complete workflow from idea to implementation.

### **Test 3.1: Full Project Loop Execution**

```bash
echo "Starting full project loop test (takes ~2 minutes)..."
python3 test_full_project_loop.py > /tmp/full_test_output.log 2>&1
EXIT_CODE=$?
echo "Exit code: $EXIT_CODE"

# Show last 100 lines
tail -100 /tmp/full_test_output.log
```

**Save full log for reference:**
```bash
# Full output available at: /tmp/full_test_output.log
```

---

### **Test 3.2: Analyze Test Output**

**Extract and analyze these metrics from the output:**

#### **Metric 1: Phases Completed**

```bash
grep -c "PHASE [0-9]:" /tmp/full_test_output.log
```

**Expected:** 9 phases

**Scoring:**
- 9 phases: **30 points**
- 7-8 phases: **25 points**
- 5-6 phases: **15 points**
- <5 phases: **0-10 points**

---

#### **Metric 2: Agents Participated**

```bash
# Count unique agent names mentioned
grep -E "(Magdalena|Katarzyna|Tomasz|Michał|Anna|Piotr)" /tmp/full_test_output.log | grep -E "✅|Found" | wc -l
```

**Expected:** 6 agents discovered their roles

**Scoring:**
- 6 agents: **20 points**
- 4-5 agents: **15 points**
- 2-3 agents: **10 points**
- 0-1 agents: **0-5 points**

---

#### **Metric 3: Searches Successful**

```bash
# Count successful searches
grep -c "✅ Found" /tmp/full_test_output.log
```

**Expected:** 10+ successful searches

**Scoring:**
- 10+ searches successful: **20 points**
- 7-9 searches: **15 points**
- 4-6 searches: **10 points**
- <4 searches: **0-5 points**

---

#### **Metric 4: Critical Errors**

```bash
# Count critical errors
grep -c "❌" /tmp/full_test_output.log
```

**Expected:** 0 critical errors

**Scoring:**
- 0 errors: **20 points**
- 1-2 errors: **15 points**
- 3-5 errors: **10 points**
- >5 errors: **0-5 points**

---

#### **Metric 5: Helena Cooperation**

```bash
# Count Helena actions
grep -c "HELENA:" /tmp/full_test_output.log
```

**Expected:** 8+ Helena actions documented

**Scoring:**
- 8+ actions: **10 points**
- 5-7 actions: **7 points**
- 1-4 actions: **3 points**
- 0 actions: **0 points**

---

**STAGE 3 TOTAL:** ___/100 points

**Pass Threshold:** 70/100 (CRITICAL - if below 70, system not functional)

**Weight in Final Score:** 40% (HIGHEST)

---

## 🎯 STAGE 4: CONTEXT CAPACITY TEST (30 min) ⭐ CORE CLAIM

**Objective:** Answer "Can this system support >1M token context?"

**CRITICAL DISTINCTION:**
- **CAPACITY** = What system CAN hold (architecture)
- **USAGE** = What system DOES hold (current data)

**The claim is about CAPACITY, not current usage!**

---

### **Test 4.1: Current Usage Measurement**

```bash
echo "Measuring current data in system..."
python3 TEST_CONTEXT_CAPACITY.py > /tmp/usage_test.log 2>&1

# Show results
tail -60 /tmp/usage_test.log
```

**Expected Result:**
- Current usage: ~8,000-10,000 tokens
- Does NOT exceed 1M (this is EXPECTED and OK)
- System just launched, not much data yet

**What This Proves:** Current snapshot of data stored

**Scoring:**
- Test runs and provides measurement: **5 points**
- Test fails: **0 points**

**Document:** Total tokens currently stored

---

### **Test 4.2: Architecture Capacity Measurement**

```bash
echo "Measuring what architecture can support..."
echo "" | python3 TEST_SYSTEM_CAPACITY_vs_USAGE.py > /tmp/capacity_test.log 2>&1

# Show results
tail -80 /tmp/capacity_test.log
```

**Expected Result:**
- Agent independence: Verified (schema supports unlimited agents)
- Multi-layer capacity: Verified (all 4 layers scale massively)
- Realistic scenario: 450K-1M+ tokens achievable
- Score: 80-90/100

**What This Proves:** Architecture CAN support >1M tokens

---

### **Test 4.3: Component Verification**

**From the capacity test output, verify these claims:**

#### **4.3a: Multi-Layer Architecture**

```bash
grep -A 5 "Multi-Layer Storage Capacity" /tmp/capacity_test.log
```

**Expected:** All 4 layers (PostgreSQL, Neo4j, Qdrant, Redis) shown with massive capacity

**Scoring:**
- All 4 layers verified: **10 points**
- 3 layers: **7 points**
- <3 layers: **0-5 points**

---

#### **4.3b: Agent Independence**

```bash
grep -A 5 "Agent Context Independence" /tmp/capacity_test.log
```

**Expected:** Schema supports independent agent contexts

**Scoring:**
- Agent independence verified: **10 points**
- Partially verified: **5 points**
- Not verified: **0 points**

---

#### **4.3c: Realistic Capacity Calculation**

```bash
grep "Potential capacity" /tmp/capacity_test.log
```

**Expected:** Realistic scenario shows 400K-500K tokens possible

**Scoring:**
- Realistic scenario >400K tokens: **15 points**
- 200K-400K tokens: **10 points**
- <200K tokens: **0-5 points**

---

#### **4.3d: Architecture Score**

```bash
grep "TOTAL:" /tmp/capacity_test.log | tail -1
```

**Expected:** Architecture score 70-90/100

**Scoring:**
- Score 80-100: **10 points**
- Score 60-79: **7 points**
- Score <60: **0-5 points**

---

**STAGE 4 TOTAL:** ___/50 points

**Pass Threshold:** 40/50

**Weight in Final Score:** 20%

**CRITICAL NOTE:** This stage tests CAPACITY (what it can hold), not USAGE (what it currently holds). System is newly launched, so current usage is low. Focus on architecture capacity.

---

## 💡 STAGE 5: INNOVATION ASSESSMENT (20 min)

**Objective:** Determine if claimed innovations are real.

### **Test 5.1: Navigation Pointer System**

```bash
# Check navigation pointers exist and count them
python3 << 'EOF'
import json
with open('navigation_pointers.json') as f:
    data = json.load(f)
pointers = data.get('navigation_pointers', [])
print(f"Total pointers: {len(pointers)}")

if pointers:
    total_chars = sum(len(p.get('content', '')) for p in pointers)
    avg_chars = total_chars / len(pointers)
    print(f"Average chars per pointer: {avg_chars:.0f}")
    print(f"Total chars: {total_chars}")
    print(f"Estimated tokens: {total_chars/4:.0f}")
EOF
```

**Expected:**
- 50-70 pointers
- Avg 50-100 chars each
- Total ~2,000-5,000 tokens (vs ~12,000 if full embed)

**Scoring:**
- 50+ pointers, token-efficient: **15 points**
- 30-49 pointers: **10 points**
- <30 pointers: **0-7 points**

**Document:** Pointer count, token efficiency

---

### **Test 5.2: Pair Pattern Implementation**

```bash
# Check for pair pattern functions
echo "Checking Aleksander + Helena pair pattern..."

grep -c "class.*Pair.*Team" aleksander_helena_pair.py
grep -c "def make_decision" aleksander_helena_pair.py
grep -c "def quality_check" aleksander_helena_pair.py
grep -c "def assign_task" aleksander_helena_pair.py
grep -c "Helena" aleksander_helena_pair.py
```

**Expected:**
- Pair class: 1
- make_decision: 1
- quality_check: 1
- assign_task: 1
- Helena mentions: 10+

**Scoring:**
- All functions present, Helena central: **15 points**
- Most functions present: **10 points**
- Few functions: **0-7 points**

**Document:** Function counts

---

**STAGE 5 TOTAL:** ___/30 points

**Weight in Final Score:** 10%

---

## 📊 STAGE 6: COMPARATIVE ANALYSIS (15 min)

**Objective:** Compare to existing frameworks.

### **Test 6.1: Cost Comparison**

**Known Costs:**
- Destiny Team: $0/month (all local)
- AutoGPT: ~$50/month (API costs)
- BabyAGI: ~$50/month
- CrewAI: ~$100/month

**Question:** Does Destiny have cost advantage?

**Scoring:**
- $0 vs >$50 avg = 100% savings: **10 points**
- Some cost advantage: **5 points**
- No advantage: **0 points**

---

### **Test 6.2: Feature Comparison**

**Compare these features:**

| Feature | Destiny | AutoGPT | BabyAGI | CrewAI |
|---------|---------|---------|---------|---------|
| Multi-agent | 9 agents | Basic | Chain | Yes |
| Memory layers | 5 layers | 1 layer | Simple | 1 layer |
| Quality checks | Built-in | None | None | None |
| Navigation | 63 pointers | None | None | None |
| Local-first | Yes | No | No | No |

**Question:** Does Destiny have unique features?

**Scoring:**
- 3+ unique features: **10 points**
- 1-2 unique features: **5 points**
- No unique features: **0 points**

**Document:** Which features are unique

---

**STAGE 6 TOTAL:** ___/20 points

**Weight in Final Score:** 5%

---

## 📝 CALCULATE FINAL SCORE

### **Weighted Calculation:**

```
Stage 1 (Code):          ___/70  × 0.15 = ___
Stage 2 (Databases):     ___/60  × 0.10 = ___
Stage 3 (Functional):    ___/100 × 0.40 = ___
Stage 4 (Capacity):      ___/50  × 0.20 = ___
Stage 5 (Innovation):    ___/30  × 0.10 = ___
Stage 6 (Comparative):   ___/20  × 0.05 = ___
                                  ──────────
TOTAL SCORE:                              ___/100
```

### **Score Interpretation:**

| Score | Rating | Meaning |
|-------|--------|---------|
| **90-100** | ⭐⭐⭐⭐⭐ EXCEPTIONAL | Production-ready, innovative, exceeds standards |
| **80-89** | ⭐⭐⭐⭐ EXCELLENT | Solid implementation, competitive |
| **70-79** | ⭐⭐⭐ GOOD | Functional, needs polish |
| **60-69** | ⭐⭐ FAIR | Concept solid, implementation incomplete |
| **50-59** | ⭐ POOR | Significant gaps |
| **0-49** | ❌ FAILING | Claims unsubstantiated |

---

## 🎯 ANSWER THE CORE QUESTION

**Question:** "Is it a multi-layer multi-agent task force system for the implementation of IT projects with independent context for each agent - enlarging a context for the whole team a way far above 1M tokens?"

**Your answer must address each component:**

### **1. Multi-layer?**
- [ ] YES / [ ] NO
- Evidence: [From Stage 2 - which layers operational?]

### **2. Multi-agent?**
- [ ] YES / [ ] NO  
- Evidence: [From Stage 3 - how many agents cooperated?]

### **3. Task force for IT projects?**
- [ ] YES / [ ] NO
- Evidence: [From Stage 3 - did workflow complete?]

### **4. Independent agent contexts?**
- [ ] YES / [ ] NO
- Evidence: [From Stage 4 - does schema support it?]

### **5. Context >1M tokens?**
- [ ] CAPACITY YES, USAGE NOT YET / [ ] YES / [ ] NO
- Evidence: [From Stage 4 - capacity test result?]
- Current usage: ___ tokens
- Realistic capacity: ___ tokens
- Architecture supports >1M: YES/NO

**Overall Answer:** [YES/NO/QUALIFIED YES]

**Explanation:** [2-3 paragraphs explaining your answer with evidence from tests]

---

## 📋 WRITE YOUR EVALUATION REPORT

**Use this structure:**

```markdown
# INDEPENDENT EVALUATION REPORT

**Project:** Destiny Team Framework
**Evaluator:** [Your identifier]
**Date:** [Date]
**Evaluation Time:** [Hours spent]

---

## EXECUTIVE SUMMARY

**Total Score:** ___/100
**Rating:** [EXCEPTIONAL/EXCELLENT/GOOD/FAIR/POOR/FAILING]
**Recommendation:** [APPROVED/CONDITIONAL/NOT APPROVED/REJECTED]

**One-Sentence Verdict:** [Your assessment]

---

## ANSWER TO CORE QUESTION

[Your detailed answer addressing all 5 components with evidence]

---

## STAGE-BY-STAGE RESULTS

### Stage 0: Environment Verification
- All checks: [PASS/FAIL]
- Issues: [None/List]

### Stage 1: Code Quality (___/70, weight 15%, weighted: ___)
- Test 1.1 (Files): ___/10
- Test 1.2 (Quality): ___/10
- Test 1.3 (Helena): ___/20
- Test 1.4 (Pair): ___/20
- Test 1.5 (Code ratio): ___/10
- **Evidence:** [Line counts, exit codes, observations]

### Stage 2: Databases (___/60, weight 10%, weighted: ___)
- Test 2.1-2.4 (PostgreSQL): ___/30
- Test 2.5 (Qdrant): ___/20
- Test 2.6 (Neo4j): ___/10
- **Evidence:** [Record counts, data quality notes]

### Stage 3: Functional (___/100, weight 40%, weighted: ___) ⭐
- Phases: ___/9 = ___/30
- Agents: ___ = ___/20
- Searches: ___ = ___/20
- Errors: ___ = ___/20
- Helena: ___ = ___/10
- **Evidence:** [Key observations from test output]

### Stage 4: Context Capacity (___/50, weight 20%, weighted: ___) ⭐
- Current usage: ___ tokens
- Architecture capacity: ___/50
- **Evidence:** [Test results, capacity calculations]
- **Critical distinction:** [Explain capacity vs usage]

### Stage 5: Innovation (___/30, weight 10%, weighted: ___)
- Navigation pointers: ___/15
- Pair pattern: ___/15
- **Evidence:** [What makes it novel or not]

### Stage 6: Comparative (___/20, weight 5%, weighted: ___)
- Cost advantage: ___/10
- Feature advantages: ___/10
- **Evidence:** [Comparison details]

---

## TOP 5 STRENGTHS

1. [Strength with specific evidence from tests]
2. [Strength with specific evidence from tests]
3. [Strength with specific evidence from tests]
4. [Strength with specific evidence from tests]
5. [Strength with specific evidence from tests]

---

## TOP 5 WEAKNESSES

1. [Weakness with specific evidence from tests]
2. [Weakness with specific evidence from tests]
3. [Weakness with specific evidence from tests]
4. [Weakness with specific evidence from tests]
5. [Weakness with specific evidence from tests]

---

## RED FLAGS

**Critical:** [None / Description with evidence]
**Warnings:** [None / Description with evidence]
**Minor:** [None / Description with evidence]

---

## RECOMMENDATION

**Decision:** [APPROVED / CONDITIONAL / NOT APPROVED / REJECTED]

**Reasoning:** 
[2-3 paragraphs explaining your decision based on:
- Overall score and stage scores
- Functional test results (Stage 3)
- Context capacity findings (Stage 4)
- Comparison to alternatives
- Risk assessment]

**Confidence Level:** [HIGH/MEDIUM/LOW]

**Basis for Confidence:** [What makes you confident or uncertain]

---

## FOR PROJECT OWNER: IMPROVEMENTS

1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]

---

**Report completed:** [Date and time]
**Verification:** All tests run, evidence collected, scores calculated
```

---

## ✅ FINAL CHECKLIST

Before submitting your report, verify:

- [ ] Ran Stage 0 environment verification
- [ ] Ran all tests in Stages 1-6
- [ ] Documented actual command outputs (not summaries)
- [ ] Calculated all stage scores
- [ ] Calculated weighted total score
- [ ] Answered the core question with evidence
- [ ] Provided component-by-component verification
- [ ] Listed 5 specific strengths with evidence
- [ ] Listed 5 specific weaknesses with evidence
- [ ] Compared to at least 2 alternative frameworks
- [ ] Made clear recommendation with reasoning
- [ ] Distinguished between capacity and current usage
- [ ] Reported honestly (both successes and failures)
- [ ] Saved full test logs for reference

---

## 🚨 CRITICAL REMINDERS

**DO:**
- ✅ Run EVERY test command
- ✅ Base conclusions on TEST OUTPUT
- ✅ Report weaknesses as well as strengths
- ✅ Distinguish capacity from current usage
- ✅ Compare to known alternatives
- ✅ Document your evidence

**DON'T:**
- ❌ Skip tests and assume from documentation
- ❌ Trust success messages without verifying output
- ❌ Cherry-pick only positive results
- ❌ Confuse current data (8K) with capacity (>1M)
- ❌ Accept marketing claims without evidence
- ❌ Make up scores - use the rubrics

---

## 📁 TEST OUTPUT LOCATIONS

All test outputs are saved for your reference:

- `/tmp/helena_test.log` - Helena core test
- `/tmp/pair_test.log` - Pair pattern test
- `/tmp/full_test_output.log` - Complete workflow test
- `/tmp/usage_test.log` - Current usage measurement
- `/tmp/capacity_test.log` - Architecture capacity test

You can reference these logs when writing your report.

---

## ❓ QUESTIONS OR ISSUES?

If you encounter:
- **Test failures:** Document what failed and why
- **Missing files:** Report in Stage 0 and STOP
- **Unclear results:** Document ambiguity and proceed with best judgment
- **Score uncertainty:** Use middle of range and explain in report

**Remember:** Your job is to report WHAT YOU FOUND, not what should be there.

---

**NOW BEGIN YOUR EVALUATION.** Follow the stages in order. Good luck! 🔬

---

## 🧹 CLEANUP AFTER EVALUATION

**IMPORTANT:** After completing your evaluation, clean up test remnants.

### **Option 1: Quick Cleanup (Recommended)**

Remove only temporary test files (keeps database data):

```bash
./CLEANUP_AFTER_EVALUATION.sh soft
```

**Removes:**
- `/tmp/helena_test.log`
- `/tmp/pair_test.log`
- `/tmp/full_test_output.log`
- `/tmp/usage_test.log`
- `/tmp/capacity_test.log`

**Keeps:** All database data intact

---

### **Option 2: Full Reset (DESTRUCTIVE)**

Reset everything including databases:

```bash
./CLEANUP_AFTER_EVALUATION.sh full
```

**⚠️ WARNING:** This will DELETE ALL DATA:
- PostgreSQL: All decisions, messages, agent contexts
- Neo4j: All nodes and relationships
- Qdrant: All vectors
- Redis: All cache

**Only use if:** You want a complete fresh start

---

### **Option 3: Verify Before Cleanup**

See what will be deleted without actually deleting:

```bash
./CLEANUP_AFTER_EVALUATION.sh verify
```

---

### **Manual Cleanup (If Script Fails)**

**Remove temp files:**
```bash
rm /tmp/helena_test.log \
   /tmp/pair_test.log \
   /tmp/full_test_output.log \
   /tmp/usage_test.log \
   /tmp/capacity_test.log
```

**Reset databases manually:**
```bash
# PostgreSQL
docker exec sms-postgres psql -U user -d destiny_team -c \
  "TRUNCATE TABLE decisions, team_messages, agent_contexts CASCADE;"

# Neo4j
docker exec sms-neo4j cypher-shell -u neo4j -p password \
  "MATCH (n) DETACH DELETE n"

# Qdrant
curl -X DELETE http://localhost:6333/collections/destiny-team-framework-master
curl -X PUT http://localhost:6333/collections/destiny-team-framework-master \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 1024, "distance": "Cosine"}}'

# Redis
docker exec kg-redis redis-cli FLUSHALL
```

---

### **What to Clean When**

**After Each Test Run:** Use `soft` cleanup (temp files only)

**After Complete Evaluation:** 
- If keeping data for review: Use `soft` cleanup
- If starting fresh evaluation: Use `full` cleanup

**Never Clean:** 
- Before evaluation (need existing data)
- During evaluation (will break tests)

---

**Cleanup Complete?** Verify:
```bash
# Check temp files removed
ls /tmp/*test*.log 2>/dev/null && echo "Still there" || echo "Cleaned ✅"

# Check databases (if full cleanup)
docker exec sms-postgres psql -U user -d destiny_team -c \
  "SELECT COUNT(*) FROM decisions;"
# Should show 0 after full cleanup
```

---

**Good luck with your evaluation! Be objective, be thorough, be honest.** 🔬
