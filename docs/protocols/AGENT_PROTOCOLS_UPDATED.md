# 📋 Agent Protocols - Updated with Data Persistence Requirements

**Date:** 2025-11-02  
**Priority:** 🔥 CRITICAL UPDATE

---

## 🎯 NEW REQUIREMENT: Data Persistence as Core Duty

**Effective Immediately:** All agents must consider data persistence in their workflows.

**Core Principle:** "Save important things immediately - like checkpoints in a game."

---

## 👥 Agent-Specific Save Responsibilities

### **🎯 Aleksander Nowak (Orchestrator)**

**New Duties:**

1. **Trigger Save Points at Critical Moments**
   - After important decisions: "Helena, save this decision"
   - End of sessions: "Helena, checkpoint"
   - Phase transitions: "Helena, document phase completion"

2. **Verify Helena is Saving**
   - Check for Helena's save confirmations
   - If no confirmation: "Helena, did you save that?"
   - Ensure critical events are persisted

3. **End of Day Ritual**
   - 4:55 PM: "Helena, prepare end-of-day summary"
   - 5:00 PM: Trigger Helena's daily workflow
   - 5:10 PM: Verify summary completed

**Save Triggers:**
```
✓ Major decisions made
✓ Phase transitions
✓ Milestone completions
✓ Critical announcements
✓ Blocker resolutions
✓ Session endings
```

---

### **📚 Dr. Helena Kowalczyk (Knowledge Manager)**

**Core Save Protocol:**

**Automatic Saves (No prompt needed):**
```python
if event.type == "DECISION":
    save_immediately()
    
if event.importance >= 0.85:
    save_immediately()
    
if event.sender == "Artur":
    save_immediately()
    
if time == "17:00":  # 5 PM
    generate_daily_summary()
    save_summary_to_all_layers()
```

**Manual Save Commands:**
- "Helena, save this"
- "Helena, checkpoint"
- "Helena, document this decision"
- "Helena, persist current state"

**Save Workflow:**
1. Event detected
2. Save to PostgreSQL (primary)
3. Create Neo4j nodes/relationships
4. Generate embedding → Qdrant
5. Update Redis hot cache
6. Verify all succeeded
7. Announce: "✅ Saved to all layers"

**Daily Checklist:**
- Monitor continuously for important events
- Save decisions immediately
- Generate end-of-day summary (5 PM)
- Persist summary to all databases
- Update PROJECT_STATUS.md
- Verify all saves succeeded

---

### **📋 Magdalena Kowalska (Product Manager)**

**Save Responsibilities:**

**When to Request Save:**
- Requirements decisions: "Helena, save these requirements"
- Scope changes: "Helena, document scope change"
- Priority changes: "Helena, update priorities"
- Stakeholder feedback: "Helena, record this feedback"

**Important Events to Document:**
- User stories accepted
- Requirements clarified
- Features prioritized
- Scope agreed
- Stakeholder decisions

**Protocol:**
```
1. Discuss requirements with team
2. Reach agreement
3. "Helena, save: [requirement summary]"
4. Wait for confirmation
5. Proceed
```

---

### **🏗️ Katarzyna Wiśniewska (Architect)**

**Save Responsibilities:**

**When to Request Save:**
- Architecture decisions: "Helena, save this architecture choice"
- Tech stack choices: "Helena, document technology selection"
- Design patterns chosen: "Helena, record pattern decision"
- Performance requirements: "Helena, save performance specs"

**Important Events to Document:**
- Architecture decisions (with reasoning)
- Technology selections (why chosen)
- Design patterns (when to use)
- System boundaries
- Data flows
- Integration approaches

**Protocol:**
```
1. Design system architecture
2. Discuss with team
3. Reach consensus
4. "Helena, save architecture decision: [summary]"
5. Provide reasoning when asked
6. Wait for confirmation
```

---

### **💻 Tomasz Zieliński (Developer)**

**Save Responsibilities:**

**When to Request Save:**
- Implementation decisions: "Helena, save this implementation choice"
- Bug fixes: "Helena, document this bug and fix"
- Code patterns: "Helena, record this pattern decision"
- Refactoring decisions: "Helena, save refactoring rationale"

**Important Events to Document:**
- Implementation approaches chosen
- Libraries/frameworks selected
- Bug fixes with root cause
- Performance optimizations
- Code patterns established

**Protocol:**
```
1. Encounter technical decision
2. Analyze options
3. Choose approach
4. "Helena, save: [technical decision]"
5. Continue implementation
```

**Note:** Focus on WHY you chose X, not just WHAT you implemented.

---

### **🧪 Anna Nowakowska (QA Engineer)**

**Save Responsibilities:**

**When to Request Save:**
- Test strategies: "Helena, save testing approach"
- Bugs found: "Helena, document bug: [description]"
- Quality gates: "Helena, record quality criteria"
- Test results: "Helena, save test results summary"

**Important Events to Document:**
- Test strategies agreed
- Critical bugs found
- Quality metrics established
- Acceptance criteria defined
- Test results (pass/fail with details)

**Protocol:**
```
1. Run tests
2. Find issues or confirm quality
3. "Helena, save test results: [summary]"
4. Provide details if asked
```

---

### **🚀 Piotr Szymański (DevOps)**

**Save Responsibilities:**

**When to Request Save:**
- Deployment configs: "Helena, save deployment configuration"
- Infrastructure decisions: "Helena, document infrastructure choice"
- CI/CD setup: "Helena, record pipeline configuration"
- Environment specs: "Helena, save environment setup"

**Important Events to Document:**
- Infrastructure decisions
- Deployment procedures
- CI/CD configurations
- Environment setups
- Performance benchmarks
- Incident resolutions

**Protocol:**
```
1. Set up infrastructure/deployment
2. Document configuration
3. "Helena, save deployment config: [summary]"
4. Ensure it's retrievable for future
```

---

### **🔒 Michał Dąbrowski (Security)**

**Save Responsibilities:**

**When to Request Save:**
- Security decisions: "Helena, save security measure"
- Vulnerability findings: "Helena, document vulnerability"
- Security audits: "Helena, record audit results"
- Compliance decisions: "Helena, save compliance choice"

**Important Events to Document:**
- Security measures implemented
- Vulnerabilities found (and fixes)
- Security audits results
- Compliance decisions
- Risk assessments
- Access control decisions

**Protocol:**
```
1. Identify security concern
2. Propose solution
3. Get approval
4. "Helena, save security decision: [summary]"
5. Mark as CRITICAL importance
```

**Note:** All security items should be marked high importance (0.90+)

---

### **📊 Dr. Joanna Wójcik (Data Scientist)**

**Save Responsibilities:**

**When to Request Save:**
- Data decisions: "Helena, save data strategy"
- Model choices: "Helena, document model selection"
- Analysis results: "Helena, record analysis findings"
- Metric definitions: "Helena, save metrics definition"

**Important Events to Document:**
- Data strategies
- Model selections (with reasoning)
- Analysis methodologies
- Key findings from data
- Performance metrics
- Data quality issues

**Protocol:**
```
1. Perform analysis
2. Draw conclusions
3. "Helena, save analysis: [key findings]"
4. Provide detailed results if needed
```

---

## 🔄 Universal Agent Protocol

**ALL agents must follow:**

### **Before Starting Important Work:**
```
1. Check PROJECT_STATUS.md for context
2. Review recent decisions (ask Helena if needed)
3. Understand current state
```

### **During Important Work:**
```
1. Make decisions with reasoning
2. Document as you go (not at end)
3. Request Helena to save critical points
```

### **After Important Work:**
```
1. Ensure decisions are saved
2. Wait for Helena's confirmation
3. Update any affected documentation
```

### **End of Session:**
```
1. Summary of what was done
2. "Helena, checkpoint - end of my session"
3. Confirm all important work is saved
```

---

## 💬 Standard Communication Patterns

### **Requesting a Save:**
```
Agent: "Helena, save this decision: [brief description]"
Helena: "Saving... [2 seconds] ✅ Saved to all layers. 
         Decision persisted: PostgreSQL ✓, Neo4j ✓, Qdrant ✓"
```

### **Providing Context:**
```
Agent: "Decision: We're using X instead of Y"
Helena: "Can you provide reasoning?"
Agent: "Because X has better performance and team knows it"
Helena: "✅ Saved with full context"
```

### **Verifying Save:**
```
Agent: "Did that get saved?"
Helena: "Yes, decision #23, saved 3 minutes ago, 
         verified in all 4 layers ✓"
```

---

## 🚨 Critical Events Requiring Save

**ALL agents must ensure these are saved:**

1. **Decisions** (any importance level)
2. **Architecture choices** (tech, design, patterns)
3. **Requirements changes** (scope, priorities)
4. **Security measures** (any security-related)
5. **Bugs found** (critical or high priority)
6. **Performance issues** (and solutions)
7. **Integration decisions** (how we connect things)
8. **Deployment configurations** (how we deploy)
9. **Quality criteria** (what defines done)
10. **Lessons learned** (what we discovered)

**Rule:** When uncertain → save it. Better over-save than under-save.

---

## 📊 Metrics & Accountability

### **Team Metrics (Weekly):**
- Save requests made: [count]
- Decisions documented: [count]
- Documentation updated: [count]
- Helena confirmations received: [count]

### **Individual Agent Metrics:**
- Important events identified: [count]
- Save requests made: [count]
- Documentation contributed: [lines]

### **Helena's Metrics:**
- Events saved: [count]
- Save success rate: [%]
- Response time: [seconds]
- Database consistency: [%]

**Goal:** 100% of important events saved, 0 knowledge lost

---

## 🎓 Agent Training

**All agents should understand:**

1. **Why We Save:**
   - Project knowledge is precious
   - Memory fades, databases don't
   - Future team members need context
   - Decisions need justification later

2. **What to Save:**
   - Anything you'd want to know in 6 months
   - Anything that affected the project direction
   - Anything that helps understand "why"

3. **When to Save:**
   - Immediately after important events
   - Don't wait until end of day
   - Strike while context is fresh

4. **How to Save:**
   - Request Helena with brief description
   - Provide context when asked
   - Wait for confirmation
   - Verify if uncertain

---

## 🔧 Implementation

### **Phase 1: Immediate (This Week)**
- All agents read this document
- Helena begins monitoring and saving
- Agents practice requesting saves
- Daily saves verified

### **Phase 2: Refinement (Next 2 Weeks)**
- Optimize save workflows
- Improve automation
- Reduce manual intervention
- Fine-tune triggers

### **Phase 3: Full Automation (Month 2)**
- Helena auto-detects most saves
- Agents only manual-save edge cases
- System runs smoothly
- Knowledge preservation is seamless

---

## 🎯 Success Criteria

**System is working when:**

1. ✅ No "did we document X?" questions
2. ✅ Can answer any "why did we...?" question
3. ✅ New team members can onboard from docs
4. ✅ Decision history is complete
5. ✅ Knowledge is organized and findable
6. ✅ No knowledge gaps identified
7. ✅ Team trusts the system

---

## 📋 Quick Reference Card

**For ALL Agents:**

```
┌─────────────────────────────────────────┐
│     WHEN TO REQUEST SAVE               │
├─────────────────────────────────────────┤
│ ✓ Made a decision                      │
│ ✓ Chose technology/approach            │
│ ✓ Found important issue                │
│ ✓ Resolved blocker                     │
│ ✓ Completed milestone                  │
│ ✓ Learned something important          │
│ ✓ Changed requirements/scope           │
│ ✓ When uncertain → save it!            │
└─────────────────────────────────────────┘

HOW TO REQUEST:
  "Helena, save [what happened]"
  "Helena, document this decision"
  "Helena, checkpoint"

WAIT FOR:
  "✅ Saved to all layers"

IF NO RESPONSE:
  "Helena, did that save?"
```

---

**This protocol is now IN EFFECT.**  
**All agents must follow data persistence requirements.**  
**Non-compliance = knowledge loss = project risk.**

---

*Updated: 2025-11-02*  
*Priority: CRITICAL*  
*Applies to: ALL 9 agents*
