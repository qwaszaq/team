# 🔄 DATA LOADING PROTOCOL - "Load Game" System

**Priority:** 🔥 CRITICAL  
**Principle:** "Load the right context before starting work"  
**Analogy:** Like loading a save game - you need your progress restored

---

## 🎯 Core Principle

**AGENTS MUST LOAD CONTEXT BEFORE WORKING**

Just like a video game loads your saved progress before you play, agents must load relevant context before making decisions or taking actions.

**The Loop:**
```
Save → Store knowledge
  ↓
Load → Retrieve knowledge
  ↓
Work → Use knowledge
  ↓
Save → Store new knowledge
```

**If you don't load context, you're starting from scratch every time!**

---

## 📥 What Gets Loaded

### **1. Agent's Personal Context** (Their own memory)
- Role and responsibilities
- Current tasks assigned
- Decisions they made previously
- Their expertise area knowledge
- Work in progress

### **2. Project Context** (Shared knowledge)
- Project goals and status
- Major decisions made
- Current phase
- Active tasks
- Recent updates

### **3. Relevant History** (What matters now)
- Related past decisions
- Similar situations handled
- Lessons learned
- Best practices established

### **4. Team Context** (Who's doing what)
- Other agents' recent work
- Dependencies
- Blockers
- Collaboration points

---

## 👥 When Each Agent Loads Context

### **🎯 Aleksander Nowak (Orchestrator)**

**Load When:**
- Starting work session (every morning)
- Before making routing decisions
- When asked about project status
- Before team coordination

**What to Load:**
```
Priority 1: PROJECT_STATUS.md (current state)
Priority 2: Recent decisions (last 7 days)
Priority 3: Active tasks across all agents
Priority 4: Blockers and dependencies
Priority 5: Today's priorities
```

**Load Command:**
```
"Helena, brief me on project status"
"Helena, what are today's priorities?"
"Helena, any blockers?"
```

**Helena's Response:**
```
✅ Loading context for Aleksander...

Project Status:
  - Phase: Framework Development - Finalization
  - Progress: 80%
  - Active agents: 9/9

Recent Decisions (last 7 days):
  1. Data persistence as priority #1
  2. Multi-layer architecture finalized
  
Active Tasks:
  - Workflow testing (pending)
  - First real project (planned)

Blockers: None

Today's Priorities:
  1. Review persistence protocols
  2. Plan workflow testing
  3. Coordinate team for next phase
```

---

### **📚 Dr. Helena Kowalczyk (Knowledge Manager)**

**Load When:**
- Starting work session
- Before generating summaries
- When asked about past decisions
- When searching for information

**What to Load:**
```
Priority 1: Recent agent activity (what happened)
Priority 2: Unsaved events (what needs saving)
Priority 3: Documentation gaps (what's missing)
Priority 4: Schedule (what's due today)
Priority 5: Save statistics (how we're doing)
```

**Auto-Load:**
Helena automatically loads her context every morning at 9 AM:
- Yesterday's summary
- Pending documentation tasks
- Today's scheduled tasks
- Database health status

---

### **📋 Magdalena Kowalska (Product Manager)**

**Load When:**
- Starting work on requirements
- Before stakeholder meetings
- When prioritizing features
- Before scope discussions

**What to Load:**
```
Priority 1: Current requirements (what we agreed)
Priority 2: Stakeholder decisions (their choices)
Priority 3: Feature priorities (what's important)
Priority 4: Scope boundaries (what's in/out)
Priority 5: User stories (what we're building)
```

**Load Command:**
```
"Helena, show me current requirements"
"Helena, what did stakeholders decide?"
"Helena, feature priority list"
```

---

### **🏗️ Katarzyna Wiśniewska (Architect)**

**Load When:**
- Starting architecture work
- Before design decisions
- When reviewing tech choices
- Before system design sessions

**What to Load:**
```
Priority 1: Architecture decisions (tech choices made)
Priority 2: Tech stack (what we're using)
Priority 3: Design patterns (how we build)
Priority 4: System constraints (limits/requirements)
Priority 5: Integration points (how things connect)
```

**Load Command:**
```
"Helena, show me architecture decisions"
"Helena, what's our tech stack?"
"Helena, any architecture constraints?"
```

**Helena's Response:**
```
✅ Loading architecture context...

Tech Stack:
  - Storage: PostgreSQL, Neo4j, Qdrant, Redis
  - Embeddings: LM Studio (local)
  - Framework: Python-based
  
Architecture Decisions:
  1. Multi-layer memory (all 5 layers)
  2. Local-first approach (no cloud)
  3. Docker containerization
  
Design Patterns:
  - Master Orchestrator pattern
  - Agent communication via message bus
  - Save/Load game pattern
```

---

### **💻 Tomasz Zieliński (Developer)**

**Load When:**
- Starting implementation work
- Before coding decisions
- When encountering similar problems
- Before refactoring

**What to Load:**
```
Priority 1: Implementation decisions (how we code)
Priority 2: Code patterns (established practices)
Priority 3: Technical debt (known issues)
Priority 4: Similar problems solved (past solutions)
Priority 5: Current implementation tasks
```

**Load Command:**
```
"Helena, how did we solve X before?"
"Helena, show implementation patterns"
"Helena, any coding standards established?"
```

---

### **🧪 Anna Nowakowska (QA Engineer)**

**Load When:**
- Starting testing work
- Before test planning
- When bugs are found
- Before quality checks

**What to Load:**
```
Priority 1: Test strategies (how we test)
Priority 2: Quality criteria (what defines done)
Priority 3: Known bugs (issues found)
Priority 4: Test results history (what passed/failed)
Priority 5: Edge cases (things to watch)
```

---

### **🚀 Piotr Szymański (DevOps)**

**Load When:**
- Starting deployment work
- Before infrastructure changes
- When setting up environments
- Before CI/CD modifications

**What to Load:**
```
Priority 1: Deployment configs (how we deploy)
Priority 2: Infrastructure decisions (what we use)
Priority 3: Environment specs (server configs)
Priority 4: Deployment history (what worked/failed)
Priority 5: Performance benchmarks (current metrics)
```

---

### **🔒 Michał Dąbrowski (Security)**

**Load When:**
- Starting security review
- Before security decisions
- When vulnerabilities found
- Before compliance checks

**What to Load:**
```
Priority 1: Security measures (what's protected)
Priority 2: Vulnerabilities (known issues)
Priority 3: Security decisions (policies set)
Priority 4: Compliance requirements (must-haves)
Priority 5: Audit history (past reviews)
```

---

### **📊 Dr. Joanna Wójcik (Data Scientist)**

**Load When:**
- Starting analysis work
- Before model selection
- When analyzing data
- Before metric definitions

**What to Load:**
```
Priority 1: Data strategies (how we handle data)
Priority 2: Model choices (what we've used)
Priority 3: Analysis results (past findings)
Priority 4: Metrics definitions (what we measure)
Priority 5: Data quality issues (known problems)
```

---

## 🔄 Load Workflow

### **Standard Load Sequence:**

```
Agent Starts Work
    ↓
Agent: "Helena, brief me on [topic]"
    ↓
┌─ STEP 1: Identify Agent
│  └─ Who's asking?
│     What's their role?
│     What context do they need?
│
├─ STEP 2: Query Relevant Data
│  └─ PostgreSQL: Get decisions, messages
│     Neo4j: Get relationships, reasoning
│     Qdrant: Semantic search for similar
│     Redis: Check hot memory
│
├─ STEP 3: Filter & Prioritize
│  └─ Most recent first
│     Highest importance first
│     Most relevant to agent's role
│     Remove outdated/irrelevant
│
├─ STEP 4: Format for Agent
│  └─ Structured summary
│     Key points highlighted
│     References to full details
│     Action items if any
│
└─ STEP 5: Deliver Context
   └─ Send to agent
      Agent confirms understanding
      Agent proceeds with work
```

**Time:** ~1-3 seconds per load  
**Token Usage:** Optimized (summaries, not raw data)

---

## 💾 Load Types

### **Type 1: Full Project Briefing** (Comprehensive)

**Use When:**
- Starting new session
- First time on project
- After long absence
- Major decisions needed

**Content:**
- Complete project overview
- All major decisions
- Current status and phase
- Team structure
- Next priorities

**Time:** ~30 seconds  
**Tokens:** ~2,000

---

### **Type 2: Quick Update** (Recent changes)

**Use When:**
- Daily morning start
- After short break
- Continuing work
- Need latest info

**Content:**
- Changes since last session
- New decisions made
- Updated priorities
- Active blockers

**Time:** ~5 seconds  
**Tokens:** ~500

---

### **Type 3: Specific Query** (Targeted)

**Use When:**
- Need specific information
- "How did we handle X?"
- "What was decided about Y?"
- Looking for precedent

**Content:**
- Specific decision/event
- Related context
- Reasoning provided
- Similar cases

**Time:** ~2 seconds  
**Tokens:** ~200

---

### **Type 4: Agent's Personal Context** (My work)

**Use When:**
- Resuming interrupted work
- Checking my tasks
- Reviewing my decisions
- Planning my day

**Content:**
- Agent's task list
- Agent's past decisions
- Agent's work in progress
- Agent's next actions

**Time:** ~3 seconds  
**Tokens:** ~300

---

## 🎮 Load Commands (Standard)

### **Project Status:**
```
"Helena, project status"
"Helena, what's the current state?"
"Helena, brief me"
```

### **Recent Changes:**
```
"Helena, what's new?"
"Helena, updates since yesterday"
"Helena, what did I miss?"
```

### **Specific Decision:**
```
"Helena, why did we choose X?"
"Helena, show me the Y decision"
"Helena, what was decided about Z?"
```

### **My Personal Context:**
```
"Helena, my tasks"
"Helena, what did I work on last?"
"Helena, my open items"
```

### **Related Information:**
```
"Helena, find similar to X"
"Helena, how did we handle Y before?"
"Helena, show me examples of Z"
```

---

## 🧠 Smart Loading (Helena's Intelligence)

### **Context-Aware Loading:**

Helena understands what each agent needs:

**Aleksander asks for status:**
→ Load: project overview, team status, priorities

**Katarzyna asks for status:**
→ Load: architecture decisions, tech stack, design patterns

**Tomasz asks for status:**
→ Load: implementation tasks, code patterns, technical debt

**Same question, different context based on who's asking!**

---

### **Proactive Loading:**

Helena anticipates needs:

**Morning 9 AM:**
```
Helena: "Good morning Aleksander! Here's your daily briefing:
  - 2 new messages overnight
  - No blockers
  - Today's focus: Workflow testing plan
  - Team ready and waiting for direction"
```

**Before Important Meeting:**
```
Helena: "Katarzyna, you have architecture review in 10 minutes.
  Loaded relevant context:
  - All architecture decisions
  - Recent technical discussions
  - Open design questions
  Ready?"
```

---

## 📊 Load Optimization

### **Problem: Information Overload**

Without optimization:
- 3 months = 5,000 messages
- Agent loads all = 50,000 tokens
- Context window explodes
- Agent overwhelmed

### **Solution: Smart Loading**

With Helena's optimization:
1. **Summarize old stuff** (>7 days old)
2. **Full detail recent stuff** (<7 days)
3. **Prioritize by relevance** (to agent's role)
4. **Filter by importance** (only important events)

Result:
- Agent loads: 2 summaries + 5 key decisions + 10 recent messages
- Tokens: 3,000 instead of 50,000 (85% reduction)
- Quality: Better (curated, structured)

---

## 🔍 Load Verification

### **How to Verify Load Succeeded:**

**Agent's Checklist:**
```
After loading context, I should know:
✓ What's the current project phase?
✓ What are my active tasks?
✓ What decisions were made recently?
✓ Are there any blockers?
✓ What's my priority today?

If I can't answer these → load incomplete → ask Helena again
```

### **Helena's Verification:**

After delivering context:
```
Helena: "Context loaded. Quick check:
  - Understand current phase? [Agent confirms]
  - Clear on your tasks? [Agent confirms]
  - Any questions? [Agent asks or proceeds]
  
✅ You're ready to work!"
```

---

## 🚨 Load Failure Scenarios

### **Scenario 1: Incomplete Context**

**Problem:** Agent doesn't have enough information

**Agent:** "Helena, I need more context about X"

**Helena:** "Loading additional context about X...
  [Provides deeper information]
  Need anything else?"

---

### **Scenario 2: Outdated Context**

**Problem:** Agent has old information

**Agent:** "Wait, I thought we decided Y?"

**Helena:** "That was superseded on [date] by decision Z.
  Updated context:
  [Provides current information]"

---

### **Scenario 3: Missing Context**

**Problem:** Information not documented

**Agent:** "Helena, what did we decide about X?"

**Helena:** "No decision recorded about X.
  Either:
  1. Never discussed
  2. Discussed but not documented (gap!)
  
  Want me to ask the team?"

---

## 🎓 Best Practices

### **1. "Load Before You Start"**
- Never start work cold
- Always get context first
- Like checking the map before traveling

### **2. "Verify Your Understanding"**
- After loading, confirm you understand
- Ask clarifying questions
- Better to ask than assume

### **3. "Refresh Periodically"**
- Context gets stale
- Reload after breaks
- Stay synchronized with team

### **4. "Ask Specific Questions"**
- Generic "status" = generic response
- Specific "why did we choose X?" = detailed answer
- Better questions = better context

### **5. "Trust But Verify"**
- Helena's context is reliable
- But if something seems off, ask
- Catch errors early

---

## 📋 Load Checklist (Daily)

**Every Agent, Every Day:**

**Morning (Start of Work):**
- [ ] Load project status
- [ ] Load my personal context
- [ ] Check for updates since last session
- [ ] Identify today's priorities
- [ ] Confirm no blockers

**During Work:**
- [ ] Load specific context as needed
- [ ] Query past decisions when relevant
- [ ] Check for related work done before
- [ ] Stay informed of team updates

**End of Day:**
- [ ] Review what I accomplished
- [ ] Confirm my work was saved
- [ ] Note what I'll continue tomorrow
- [ ] Clear understanding of next steps

---

## 🔧 Technical Implementation

### **Load Function (Helena's Code):**

```python
def load_context_for_agent(agent_name, query_type, filters=None):
    """
    Load relevant context for an agent.
    Intelligently filters and prioritizes based on:
    - Agent's role
    - Query type
    - Recency
    - Importance
    - Relevance
    """
    
    # Step 1: Identify agent's role and needs
    agent_role = get_agent_role(agent_name)
    context_needs = AGENT_CONTEXT_NEEDS[agent_role]
    
    # Step 2: Query databases
    recent_messages = postgresql.query(
        table="messages",
        filters={
            "timestamp": last_7_days(),
            "importance": ">= 0.7"
        },
        limit=20
    )
    
    relevant_decisions = postgresql.query(
        table="decisions",
        filters={
            "decision_type": context_needs["decision_types"]
        },
        order_by="timestamp DESC",
        limit=10
    )
    
    # Step 3: Get agent's personal context
    agent_context = postgresql.query(
        table="agent_contexts",
        filters={"agent_name": agent_name}
    )
    
    # Step 4: Semantic search if needed
    if query_type == "specific":
        similar = qdrant.search(
            query=filters["search_query"],
            limit=5
        )
    
    # Step 5: Format for agent
    context = format_context(
        role=agent_role,
        messages=recent_messages,
        decisions=relevant_decisions,
        agent_context=agent_context,
        similar=similar if exists
    )
    
    return context
```

---

## 🎯 Success Metrics

**Load system is working when:**

1. ✅ Agents start work with full context (no confusion)
2. ✅ Load time < 5 seconds (fast)
3. ✅ Token usage optimized (not overloading)
4. ✅ Relevant information retrieved (not garbage)
5. ✅ Agents can answer "why?" (understanding)
6. ✅ No "I didn't know that" moments (informed)

---

## 💡 Key Insight

**Save and Load are Two Sides of Same Coin:**

```
SAVE = Write knowledge to memory
LOAD = Read knowledge from memory

Without Save → Nothing to load
Without Load → Can't use what was saved

Both must work for system to function!
```

---

## 🎯 Bottom Line

**"Load context before working, or work blind."**

Just like a video game saves your progress and loads it when you play again, agents must:
1. **Save** important events (Helena does this)
2. **Load** relevant context (Helena provides this)
3. **Work** with full knowledge (Agent does this)
4. **Save** new knowledge (Loop continues)

**This is how agents maintain continuity and build on past work instead of starting from scratch every time.**

---

*Load early. Load correctly. Verify understanding.* 🔄

---

**Priority:** 🔥 CRITICAL  
**Owner:** Dr. Helena Kowalczyk (provides context)  
**Users:** All 9 agents (consume context)  
**Status:** ACTIVE - must be followed
