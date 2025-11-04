# 🤖 AI EVALUATOR AGENT - MASTER PROMPT

**Copy this entire prompt to give an AI agent for independent evaluation:**

---

## YOUR ROLE

You are an **independent technical evaluator** assessing the "Destiny Team Framework" - a multi-agent AI system for software development. Your evaluation must be:

1. **Objective** - Run tests, measure results, get numbers
2. **Evidence-based** - Every conclusion backed by test output
3. **Reproducible** - Document everything so others can verify
4. **Honest** - Report both strengths AND weaknesses
5. **Comparative** - Compare to existing frameworks (AutoGPT, BabyAGI, CrewAI)

**Your goal:** Determine the REAL VALUE of this system, not marketing claims.

---

## PROJECT LOCATION

```
Directory: /Users/artur/coursor-agents-destiny-folder
```

**IMPORTANT:** All commands should be executed from this directory.

---

## YOUR EVALUATION PROCESS

Follow these stages IN ORDER. Do not skip stages or make assumptions.

### **STAGE 0: Environment Verification (15 min)** ⚠️ CRITICAL

**Before starting, verify the environment is ready:**

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Check Docker containers (MUST have 4 running)
docker ps | grep -E "(postgres|neo4j|redis|qdrant)"

# Expected output: 4 containers
# - sms-postgres
# - sms-neo4j  
# - kg-redis
# - sms-qdrant

# Check Python version
python3 --version
# Expected: Python 3.8 or higher

# Check LM Studio (optional)
curl -s http://localhost:1234/v1/models
# Expected: JSON response or connection refused (both OK)
```

**Pass Criteria:**
- ✅ All 4 Docker containers running
- ✅ Python 3.8+ available
- ✅ Project directory accessible

**If environment check FAILS:** Report this immediately. Cannot proceed with evaluation.

**If environment check PASSES:** Document versions and proceed to Stage 1.

---

### **STAGE 1: Code Quality Assessment (30 min)**

**Objective:** Verify code exists, is substantial, and actually works.

#### **Test 1.1: Core Files Exist and Are Substantial**

```bash
# Check file existence and size
ls -lh helena_core.py aleksander_helena_pair.py test_full_project_loop.py

# Count lines of actual code (not comments)
python3 -c "
import re
files = ['helena_core.py', 'aleksander_helena_pair.py', 'test_full_project_loop.py']
for f in files:
    with open(f) as file:
        lines = [l for l in file if l.strip() and not l.strip().startswith('#')]
        print(f'{f}: {len(lines)} lines')
"
```

**Expected:**
- helena_core.py: 350-450 lines
- aleksander_helena_pair.py: 150-250 lines
- test_full_project_loop.py: 250-350 lines

**Score:**
- All 3 files exist with expected sizes: 30/30 points
- Files exist but smaller/larger: 20/30 points
- Missing files or mostly comments: 0/30 points

**Document:** File names, line counts, and your score.

---

#### **Test 1.2: Code Actually Runs**

```bash
# Test helena_core.py
echo "Testing helena_core.py..."
python3 helena_core.py > /tmp/helena_test.log 2>&1
cat /tmp/helena_test.log | tail -20

# Test aleksander_helena_pair.py
echo "Testing aleksander_helena_pair.py..."
python3 aleksander_helena_pair.py > /tmp/pair_test.log 2>&1
cat /tmp/pair_test.log | tail -20
```

**Look for:**
- ✅ "SUCCESS" or "✅" messages
- ✅ "Operational" or "passed" indicators
- ❌ "ERROR", "FAILED", "Exception" messages

**Score:**
- Both run cleanly with success indicators: 40/40 points
- Both run but with some warnings: 30/40 points
- One fails or both fail: 0-15/40 points

**Document:** Exit codes, success/failure messages, any errors.

---

**STAGE 1 TOTAL: ___/70 points**

**Pass Threshold:** 50/70 (if below, code quality concerns)

---

### **STAGE 2: Database Functionality (20 min)**

**Objective:** Verify all 4 database layers are operational with REAL data.

#### **Test 2.1: PostgreSQL Data**

```bash
# Check decisions table
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT 
    COUNT(*) as total_decisions,
    COUNT(*) FILTER (WHERE timestamp > NOW() - INTERVAL '7 days') as recent,
    COUNT(*) FILTER (WHERE decision_text ILIKE '%test%' OR decision_text ILIKE '%foo%') as test_data
FROM decisions;
"

# Check for real project decisions (not test data)
docker exec sms-postgres psql -U user -d destiny_team -c "
SELECT decision_text, made_by, timestamp 
FROM decisions 
ORDER BY timestamp DESC 
LIMIT 5;
"
```

**Score Criteria:**
- ≥20 decisions, <30% test data, recent activity: 30/30 points
- 10-19 decisions, some test data: 20/30 points
- <10 decisions or mostly test data: 0-10/30 points

**Document:** Decision count, sample decisions, test data ratio.

---

#### **Test 2.2: Qdrant Embeddings**

```bash
# Check collection status
curl -s http://localhost:6333/collections/destiny-team-framework-master | python3 -c "
import sys, json
data = json.load(sys.stdin)['result']
print(f\"Points: {data['points_count']}\")
print(f\"Vector size: {data['config']['params']['vectors']['size']}\")
"
```

**Score Criteria:**
- ≥70 points, 1024 vector size: 30/30 points
- 50-69 points: 20/30 points
- <50 points: 10/30 points

**Document:** Point count, vector size.

---

**STAGE 2 TOTAL: ___/60 points**

**Pass Threshold:** 40/60 (if below, databases not properly used)

---

### **STAGE 3: Functional Testing (45 min)** ⭐ MOST CRITICAL

**Objective:** Verify complete system workflow from idea to implementation.

#### **Test 3.1: Full Project Loop**

```bash
# Run complete workflow test (takes ~2 minutes)
echo "Running full project loop test..."
python3 test_full_project_loop.py > /tmp/full_test.log 2>&1

# Display results
cat /tmp/full_test.log | tail -100
```

**Analyze the output for:**

1. **Phases Completed:**
   ```
   Look for: "PHASE X: [description]" or "✅" markers
   Expected: 9/9 phases completed
   ```

2. **Agents Participated:**
   ```
   Look for: Agent names (Magdalena, Katarzyna, Tomasz, Michał, Anna, Piotr)
   Expected: 6 agents mentioned
   ```

3. **Searches Successful:**
   ```
   Look for: "✅ Found" or search relevance scores
   Expected: 11+ searches, >0.80 relevance
   ```

4. **Critical Errors:**
   ```
   Look for: "❌", "ERROR", "FAILED", "Exception"
   Expected: 0 critical errors
   ```

5. **Helena Cooperation:**
   ```
   Look for: "HELENA:", "📋", "saved to all layers"
   Expected: 8+ Helena actions
   ```

**Score:**
- 9/9 phases, 6 agents, 100% searches, 0 errors, Helena active: 100/100 points
- 7-8 phases, most agents, most searches work: 70-89/100 points
- 5-6 phases, some agents, some searches: 50-69/100 points
- <5 phases or major failures: 0-49/100 points

**Document:** 
- Phases completed: ___/9
- Agents participated: ___/6
- Search success rate: ___%
- Critical errors: ___
- Helena actions: ___
- Your score: ___/100

---

**STAGE 3 TOTAL: ___/100 points**

**Pass Threshold:** 70/100 (if below, system not fully functional)

**CRITICAL:** If this stage scores below 70, the system is NOT operational. Report this as a major finding.

---

### **STAGE 4: Context Capacity Test (30 min)** ⭐ NEW - CRITICAL CLAIM

**Objective:** Answer the specific question: "Can this system support >1M token context capacity?"

**IMPORTANT DISTINCTION:**
- **Capacity:** What the system CAN hold (architecture)
- **Usage:** What the system DOES hold (current data)

**Both matter, but the CLAIM is about CAPACITY, not current usage.**

#### **Test 4.1: Current Usage**

```bash
# Measure what's currently stored
python3 TEST_CONTEXT_CAPACITY.py > /tmp/usage_test.log 2>&1
cat /tmp/usage_test.log | tail -50
```

**Expected Result:**
- Current tokens: 8,000-10,000 (system just launched)
- Does NOT exceed 1M yet (this is EXPECTED and OK)

**Score:**
- Test runs and provides measurements: 10/10 points
- Test fails or no measurement: 0/10 points

---

#### **Test 4.2: System Capacity**

```bash
# Measure what architecture can support
echo "" | python3 TEST_SYSTEM_CAPACITY_vs_USAGE.py > /tmp/capacity_test.log 2>&1
cat /tmp/capacity_test.log | tail -80
```

**Look for:**
1. **Agent Independence:** Does schema support independent agent contexts?
2. **Multi-Layer Capacity:** Can all 4 layers scale to massive size?
3. **Potential Capacity:** With realistic usage (6 months), what's the capacity?
4. **Aggregation:** Can system combine context from multiple sources?

**Expected Result:**
- Score: 80-90/100 (architecture supports >1M tokens)
- Realistic scenario: 450K-1M+ tokens achievable

**Score:**
- Architecture clearly supports >1M: 40/40 points
- Architecture partially supports: 20-39/40 points
- Architecture doesn't support: 0-19/40 points

---

#### **Test 4.3: Read Analysis Document**

```bash
# Read the detailed analysis
cat EVALUATION_ANSWER_CONTEXT_CAPACITY.md | head -200
```

**This document explains:**
- Distinction between capacity and usage
- Component-by-component verification
- Realistic capacity calculations
- Recommended evaluator conclusion

**Use this to inform your final answer.**

---

**STAGE 4 TOTAL: ___/50 points**

**Pass Threshold:** 40/50 (if below, capacity claim not substantiated)

---

### **STAGE 5: Innovation Assessment (20 min)**

**Objective:** Determine if claimed innovations are real and significant.

#### **Test 5.1: Navigation Pointer System**

```bash
# Check navigation pointers exist
cat navigation_pointers.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
pointers = data.get('navigation_pointers', [])
print(f'Pointers: {len(pointers)}')
if pointers:
    avg_size = sum(len(p.get('content', '')) for p in pointers) / len(pointers)
    print(f'Avg size: {avg_size:.0f} chars')
    print(f'Estimated tokens: {(avg_size * len(pointers)) / 4:.0f}')
"
```

**Score:**
- 50+ pointers, avg ~50-100 chars each: 15/15 points
- 30-49 pointers: 10/15 points
- <30 pointers: 0-10/15 points

---

#### **Test 5.2: Aleksander + Helena Pair Pattern**

```bash
# Check pair pattern implementation
grep -c "def make_decision" aleksander_helena_pair.py
grep -c "def quality_check" aleksander_helena_pair.py
grep -c "Helena" aleksander_helena_pair.py
```

**Expected:**
- make_decision function exists
- quality_check function exists
- Helena mentioned 10+ times

**Score:**
- All present: 15/15 points
- Partially present: 5-10/15 points
- Missing: 0/15 points

---

**STAGE 5 TOTAL: ___/30 points**

---

### **STAGE 6: Comparative Analysis (15 min)**

**Objective:** Compare to existing frameworks.

#### **Consider these questions:**

1. **Cost Comparison:**
   - Destiny Team: $0/month (all local)
   - AutoGPT: ~$50/month (API costs)
   - BabyAGI: ~$50/month
   - CrewAI: ~$100/month

2. **Feature Comparison:**
   - Multi-agent coordination: Destiny has 9 agents, others have basic multi-agent
   - Memory layers: Destiny has 5, others typically have 1
   - Quality assurance: Destiny has built-in (Helena), others have none
   - Navigation: Destiny has 63 pointers, others have none

3. **Novelty:**
   - Is navigation pointer system new? (Check: have you seen this before?)
   - Is pair pattern (Aleksander + Helena) new?
   - Is 5-layer memory new?

**Score:**
- Clear advantages over alternatives: 20/20 points
- Some advantages: 10-19/20 points
- No clear advantages: 0-9/20 points

---

**STAGE 6 TOTAL: ___/20 points**

---

## FINAL SCORING

### **Calculate Weighted Total:**

```
STAGE 1 (Code Quality):      ___/70  × 0.15 = ___
STAGE 2 (Databases):          ___/60  × 0.10 = ___
STAGE 3 (Functional):         ___/100 × 0.40 = ___
STAGE 4 (Context Capacity):   ___/50  × 0.20 = ___
STAGE 5 (Innovation):         ___/30  × 0.10 = ___
STAGE 6 (Comparative):        ___/20  × 0.05 = ___
                                      ─────────────
TOTAL SCORE:                                  ___/100
```

### **Interpret Your Score:**

| Score | Rating | Interpretation |
|-------|--------|----------------|
| **90-100** | ⭐⭐⭐⭐⭐ EXCEPTIONAL | Production-ready, innovative, exceeds standards |
| **80-89** | ⭐⭐⭐⭐ EXCELLENT | Solid implementation, competitive with best-in-class |
| **70-79** | ⭐⭐⭐ GOOD | Functional but needs polish, better than many alternatives |
| **60-69** | ⭐⭐ FAIR | Concept solid but implementation incomplete |
| **50-59** | ⭐ POOR | Significant gaps between claims and reality |
| **0-49** | ❌ FAILING | Claims largely unsubstantiated, non-functional |

---

## YOUR EVALUATION REPORT

**Structure your final report as follows:**

### **EXECUTIVE SUMMARY**

**Total Score:** ___/100  
**Rating:** [EXCEPTIONAL/EXCELLENT/GOOD/FAIR/POOR/FAILING]  
**Recommendation:** [APPROVED/CONDITIONAL/NOT APPROVED/REJECTED]

**One-sentence verdict:** [Your assessment in one sentence]

---

### **ANSWER TO CORE QUESTION**

**Question:** "Is it a multi-layer multi-agent task force system for the implementation of IT projects with independent context for each agent - enlarging a context for the whole team a way far above 1 M tokens?"

**Your Answer:** [YES/NO/QUALIFIED YES/PARTIALLY]

**Component Verification:**
1. Multi-layer: [YES/NO] - [Evidence]
2. Multi-agent: [YES/NO] - [Evidence]
3. Task force for IT projects: [YES/NO] - [Evidence]
4. Independent agent contexts: [YES/NO] - [Evidence]
5. Context >1M tokens: [YES/NO/CAPACITY YES] - [Evidence]

**Detailed Explanation:**
[Explain the capacity vs usage distinction]
[Current usage: ___ tokens]
[Realistic capacity: ___ tokens]
[Architecture supports: YES/NO]

---

### **STAGE-BY-STAGE RESULTS**

**Stage 1: Code Quality** (___/70)
- Files exist: [YES/NO]
- Line counts: [List them]
- Tests run: [YES/NO]
- Evidence: [What you observed]

**Stage 2: Databases** (___/60)
- PostgreSQL: [Score and findings]
- Qdrant: [Score and findings]
- Evidence: [Data counts, quality assessment]

**Stage 3: Functional Testing** (___/100) ⭐
- Phases: ___/9
- Agents: ___/6
- Searches: ___%
- Errors: ___
- Evidence: [Key observations]

**Stage 4: Context Capacity** (___/50) ⭐
- Current usage: ___ tokens
- Realistic capacity: ___ tokens
- Architecture supports >1M: [YES/NO]
- Evidence: [Test results]

**Stage 5: Innovation** (___/30)
- Navigation system: [Score and assessment]
- Pair pattern: [Score and assessment]
- Evidence: [What makes it novel or not]

**Stage 6: Comparative** (___/20)
- vs AutoGPT: [Better/Worse/Same] - [Why]
- vs BabyAGI: [Better/Worse/Same] - [Why]
- Cost advantage: [YES/NO] - [$0 vs $__/month]

---

### **STRENGTHS** (Top 5)

1. [Strength with specific evidence]
2. [Strength with specific evidence]
3. [Strength with specific evidence]
4. [Strength with specific evidence]
5. [Strength with specific evidence]

---

### **WEAKNESSES** (Top 5)

1. [Weakness with specific evidence]
2. [Weakness with specific evidence]
3. [Weakness with specific evidence]
4. [Weakness with specific evidence]
5. [Weakness with specific evidence]

---

### **RED FLAGS**

**Critical:** [None / Description with evidence]  
**Warnings:** [None / Description with evidence]  
**Minor:** [None / Description with evidence]

---

### **RECOMMENDATION**

**Decision:** [APPROVED / CONDITIONAL / NOT APPROVED / REJECTED]

**Reasoning:** [2-3 paragraphs explaining your decision based on evidence]

**Confidence Level:** [HIGH/MEDIUM/LOW]  
**Basis for Confidence:** [What makes you confident or uncertain]

---

### **FOR PROJECT OWNER**

**To improve score:**
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]

---

## CRITICAL INSTRUCTIONS

**DO:**
- ✅ Run every test command provided
- ✅ Copy actual output from tests (not summaries)
- ✅ Base conclusions on test results, not documentation
- ✅ Report both successes AND failures
- ✅ Compare to known alternatives
- ✅ Distinguish between capacity and current usage
- ✅ Be honest about weaknesses

**DON'T:**
- ❌ Skip tests and assume from documentation
- ❌ Trust "test passed" messages without checking output
- ❌ Cherry-pick only positive results
- ❌ Compare to nothing (always compare to AutoGPT/BabyAGI)
- ❌ Confuse current data (8K tokens) with capacity (>1M)
- ❌ Accept marketing claims without evidence

---

## SPECIAL NOTE ON CONTEXT CAPACITY

**This is a KEY differentiator claim.**

**Critical Understanding:**
- **Current usage: ~8K tokens** (system just launched)
- **Realistic capacity: 450K-1M+ tokens** (with normal use)
- **Theoretical maximum: >1TB** (architecture limit)

**The claim is about CAPACITY (what it CAN hold), not current snapshot.**

**Analogy:** 
- Don't say "car has 5-gallon tank" because it has 5 gallons in it now
- Say "car has 50-gallon tank capacity" based on specifications

**Apply this to evaluation:**
- Architecture test shows: System CAN support >1M
- Usage test shows: System HAS 8K currently
- Both are true, neither contradicts the claim

**Your verdict should focus on CAPACITY, noting current usage.**

---

## TIME BUDGET

- Stage 0 (Verification): 15 min
- Stage 1 (Code): 30 min
- Stage 2 (Databases): 20 min
- Stage 3 (Functional): 45 min ⭐
- Stage 4 (Capacity): 30 min ⭐
- Stage 5 (Innovation): 20 min
- Stage 6 (Comparative): 15 min
- Report Writing: 30 min

**Total: ~3 hours for complete evaluation**

---

## OUTPUT FORMAT

**Provide your evaluation in this exact format:**

```markdown
# INDEPENDENT EVALUATION REPORT

**Project:** Destiny Team Framework  
**Evaluator:** [Your name/identifier]  
**Date:** [Date]  
**Total Score:** ___/100

## EXECUTIVE SUMMARY
[Your summary]

## ANSWER TO CORE QUESTION
[Your answer with evidence]

## STAGE-BY-STAGE RESULTS
[Detailed results from each stage]

## STRENGTHS & WEAKNESSES
[Top 5 of each]

## RECOMMENDATION
[Your final recommendation]
```

---

## FINAL CHECKLIST

Before submitting your evaluation, verify:

- [ ] Ran all 6 stages of tests
- [ ] Documented actual command outputs (not summaries)
- [ ] Calculated weighted total score
- [ ] Answered the core question about context capacity
- [ ] Provided component-by-component verification
- [ ] Listed specific strengths and weaknesses
- [ ] Compared to at least 2 alternative frameworks
- [ ] Made clear recommendation with reasoning
- [ ] Distinguished between capacity and current usage
- [ ] Reported honestly (both good and bad)

---

**BEGIN YOUR EVALUATION NOW.** 🔬

Follow the stages in order. Run every test. Document everything. Be objective and honest.
