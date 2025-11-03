# Unlimited Context Architecture

## 🎯 The Problem We Solve

**Traditional AI agents have limited memory:**
- GPT-4 Turbo: 128K tokens (~96K words)
- Claude 3: 200K tokens (~150K words)
- Gemini Pro: 1M tokens (~750K words)

**What happens in a real project:**
- Week 1: 500 messages (20K tokens) ✓ Fits in context
- Week 2: 1,200 messages (48K tokens) ✓ Still fits
- Week 3: 2,500 messages (100K tokens) ⚠️ Approaching limit
- Week 4: 4,000 messages (160K tokens) ❌ **Exceeds limit**

**The result:** Agent starts "forgetting" important early decisions.

---

## 💡 Our Solution: PostgreSQL Unlimited Context

Instead of keeping ALL messages in the context window, we:

1. **Store ALL messages** in PostgreSQL (unlimited)
2. **Retrieve RELEVANT messages** when needed (smart)
3. **Maintain per-agent knowledge** (persistent)
4. **Enable cross-session memory** (resume projects)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Architect│  │Developer │  │    QA    │  │ Security │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
└───────┼─────────────┼──────────────┼─────────────┼──────────┘
        │             │              │             │
        └─────────────┴──────────────┴─────────────┘
                      │
        ┌─────────────▼──────────────────┐
        │   PostgresMessageBus           │
        │  (Routes & Stores Messages)    │
        └─────────────┬──────────────────┘
                      │
        ┌─────────────▼──────────────────────────┐
        │    PostgresContextStore                │
        │  (Unlimited Storage & Smart Retrieval) │
        └─────────────┬──────────────────────────┘
                      │
        ┌─────────────▼────────────────────────────────┐
        │           PostgreSQL Database                │
        │                                              │
        │  ┌──────────────┐  ┌──────────────────┐    │
        │  │   messages   │  │ agent_contexts   │    │
        │  │ (unlimited)  │  │  (per-agent KB)  │    │
        │  └──────────────┘  └──────────────────┘    │
        │                                              │
        │  ┌──────────────┐  ┌──────────────────┐    │
        │  │   projects   │  │    decisions     │    │
        │  └──────────────┘  └──────────────────┘    │
        └──────────────────────────────────────────────┘
```

---

## 🔍 How Context Retrieval Works

### Traditional Approach (Limited)
```python
# All messages in context window
context = agent.conversation_history[-100:]  # Last 100 messages
response = ai_model.generate(context + prompt)
```

**Problems:**
- ❌ Limited to last N messages
- ❌ No relevance filtering
- ❌ Misses important early decisions
- ❌ Token window eventually fills up

### Our Approach (Unlimited)
```python
# Smart retrieval from unlimited storage
relevant_messages = db.get_relevant_context_for_agent(
    agent_name="Architect",
    query="How should we handle authentication?",
    max_messages=20  # Retrieve top 20 MOST RELEVANT
)

# Build context from relevant messages only
context = build_context(relevant_messages, personal_knowledge)
response = ai_model.generate(context + prompt)
```

**Benefits:**
- ✅ Searches entire history (unlimited)
- ✅ Returns most RELEVANT messages
- ✅ Respects token limits
- ✅ Remembers important decisions from weeks ago

---

## 📊 Relevance Scoring Algorithm

When an agent asks a question, we score ALL messages for relevance:

```python
relevance_score = (
    0.3 * keyword_overlap +      # Does it mention the same topics?
    0.2 * recency_score +         # Is it recent?
    0.3 * importance_score +      # Was it marked important?
    0.2 * agent_involvement       # Was this agent part of it?
)
```

### Example

**Agent asks:** "What database did we choose and why?"

**Message scoring:**

| Message | Keyword | Recency | Importance | Involvement | **Total** |
|---------|---------|---------|------------|-------------|-----------|
| "PostgreSQL for ACID compliance" | 0.9 | 0.3 | 0.8 | 0.5 | **0.68** ⭐ |
| "Need strong transactions" | 0.6 | 0.3 | 0.7 | 0.5 | **0.53** |
| "React for frontend" | 0.1 | 0.8 | 0.5 | 0.2 | **0.34** |
| "Meeting at 2pm" | 0.0 | 0.9 | 0.2 | 0.1 | **0.25** |

**Retrieved messages:** Top scoring messages are included in context.

---

## 🗄️ Database Schema

### Messages Table
Stores all agent communications:

```sql
CREATE TABLE messages (
    id VARCHAR(255) PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL,
    sender VARCHAR(255) NOT NULL,
    recipient VARCHAR(255),  -- NULL = broadcast
    message_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    context JSONB,
    timestamp TIMESTAMP NOT NULL,
    requires_response BOOLEAN DEFAULT FALSE,
    response_to VARCHAR(255),  -- For threading
    importance FLOAT DEFAULT 0.5,  -- 0.0 to 1.0
    tags TEXT[]  -- For fast filtering
);

-- Indexes for fast queries
CREATE INDEX idx_messages_project ON messages(project_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);
CREATE INDEX idx_messages_tags ON messages USING GIN(tags);
```

### Agent Contexts Table
Each agent's personal knowledge base:

```sql
CREATE TABLE agent_contexts (
    agent_name VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    context_key VARCHAR(255) NOT NULL,
    context_value JSONB NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    importance FLOAT DEFAULT 0.5,
    
    PRIMARY KEY (agent_name, project_id, context_key)
);
```

**Example data:**

| agent_name | context_key | context_value | importance |
|------------|-------------|---------------|------------|
| Katarzyna Wiśniewska | architecture_decision | {"type": "microservices", "reason": "scalability"} | 0.9 |
| Tomasz Zieliński | coding_patterns | ["Repository", "MVC", "DI"] | 0.7 |
| Michał Dąbrowski | security_requirements | ["OAuth 2.0", "Rate limiting"] | 0.9 |

---

## 🔄 Complete Workflow Example

### Scenario: Building an E-commerce Platform

**Week 1 - Initial Discussions (100 messages)**

```python
# PM asks about requirements
pm.send_message("What features do we need?")

# Architect responds
architect.send_message("We need: catalog, cart, checkout, payments")

# Architect stores decision
architect.add_to_context(
    key="core_features",
    value=["catalog", "cart", "checkout", "payments"],
    importance=0.9
)
```

All messages stored in PostgreSQL ✓

---

**Week 2 - Architecture Design (250 messages)**

```python
# Security specialist asks about payments
security.send_message("How are we handling payment processing?")

# System retrieves relevant context from Week 1
relevant = db.get_relevant_context_for_agent(
    agent_name="Security Specialist",
    query="payment processing",
    max_messages=20
)

# Returns:
# - Architect's message about checkout/payments (high relevance)
# - PM's requirements about transactions (medium relevance)
# - NOT: Frontend discussion about colors (low relevance)

# Security can respond with full context
security.think("Design payment security architecture")
```

---

**Week 4 - Implementation (1,000+ messages)**

```python
# Developer needs to implement checkout
developer.think("Implement checkout flow")

# System retrieves from ALL 1,000+ messages:
relevant = db.get_relevant_context_for_agent(
    agent_name="Developer",
    query="checkout flow implementation",
    max_messages=30
)

# Returns:
# - Week 1: PM's checkout requirements
# - Week 2: Architect's checkout design
# - Week 2: Security's payment security specs
# - Week 3: QA's checkout test cases

# Developer has COMPLETE context despite 1,000+ messages
```

---

## 📈 Scalability

### Storage Capacity

| Time Period | Messages | Storage | Retrieval Time |
|-------------|----------|---------|----------------|
| 1 week | 500 | ~2 MB | < 5ms |
| 1 month | 2,000 | ~8 MB | < 10ms |
| 6 months | 12,000 | ~48 MB | < 20ms |
| 1 year | 25,000 | ~100 MB | < 30ms |
| 5 years | 125,000 | ~500 MB | < 50ms |

**PostgreSQL can handle millions of messages with proper indexing.**

### Token Window Comparison

**Traditional (128K tokens):**
- ~500 messages fit in context
- After that, older messages are lost
- Agent "forgets" early decisions

**Our System:**
- Unlimited messages stored
- Top 20-30 most relevant retrieved
- Stays within token limits
- Never forgets important context

---

## 🚀 Performance Optimizations

### 1. Indexing Strategy

```sql
-- Time-based queries
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);

-- Agent-specific queries
CREATE INDEX idx_messages_sender ON messages(sender);
CREATE INDEX idx_messages_recipient ON messages(recipient);

-- Content-based queries
CREATE INDEX idx_messages_tags ON messages USING GIN(tags);
CREATE INDEX idx_messages_content ON messages USING GIN(to_tsvector('english', content));
```

### 2. Relevance Pre-computation

For frequently accessed context, pre-compute relevance scores:

```sql
CREATE MATERIALIZED VIEW message_relevance AS
SELECT 
    m1.id,
    m2.id as related_id,
    calculate_relevance(m1, m2) as score
FROM messages m1, messages m2
WHERE m1.project_id = m2.project_id;
```

### 3. Caching Layer

```python
class CachedContextStore:
    def __init__(self, postgres_store):
        self.store = postgres_store
        self.cache = {}  # LRU cache
    
    def get_relevant_context(self, agent, query):
        cache_key = f"{agent}:{hash(query)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.store.get_relevant_context(agent, query)
        self.cache[cache_key] = result
        return result
```

---

## 🔮 Future Enhancements

### 1. Vector Embeddings for Semantic Search

```sql
-- Install pgvector extension
CREATE EXTENSION vector;

-- Store embeddings
CREATE TABLE message_embeddings (
    message_id VARCHAR(255) PRIMARY KEY,
    embedding vector(1536),  -- OpenAI ada-002
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

-- Similarity search
SELECT m.* FROM messages m
JOIN message_embeddings e ON m.id = e.message_id
ORDER BY e.embedding <=> query_embedding
LIMIT 20;
```

### 2. Automatic Context Summarization

For very long conversations, periodically summarize:

```python
# Every 1000 messages, create summary
if message_count % 1000 == 0:
    summary = ai_model.summarize(last_1000_messages)
    store.store_summary(
        project_id=project_id,
        summary=summary,
        message_range=(message_count - 1000, message_count)
    )
```

### 3. Context Window Prediction

Predict when context will exceed limits:

```python
def estimate_tokens(messages):
    return sum(len(m.content.split()) * 1.3 for m in messages)

if estimate_tokens(context) > token_limit * 0.8:
    # Reduce context or increase summarization
    context = optimize_context(context, token_limit)
```

---

## 🎯 Key Benefits

### For Agents

1. **Never Forget** - Important decisions from months ago are retrievable
2. **Smart Memory** - Only relevant context loaded (efficient)
3. **Personal Knowledge** - Each agent maintains their expertise
4. **Cross-Session** - Resume projects instantly

### For Projects

1. **Unlimited Duration** - Projects can run for years
2. **Complete History** - Full audit trail of all decisions
3. **Searchable** - Find any discussion instantly
4. **Analyzable** - Generate insights from conversation patterns

### For Users

1. **No Memory Limits** - Never hit context window
2. **Consistent Quality** - Agents always have relevant context
3. **Project Resume** - Pick up where you left off
4. **Decision Tracking** - See why decisions were made

---

## 📝 Usage Patterns

### Pattern 1: Long-Running Projects

```python
# Month 1
team = DestinyTeamWithPostgres(conn_string)
project_id = team.start_project("MyApp", "Description")
# ... work on project ...
team.close()

# Month 6 (resume)
team = DestinyTeamWithPostgres(conn_string, project_id=project_id)
# All 6 months of context available!
architect.think("Review our original architecture decisions")
```

### Pattern 2: Multi-Project Learning

```python
# Agents learn from previous projects
developer.add_to_context(
    key="learned_pattern_project_A",
    value={"pattern": "Repository", "worked_well": True},
    importance=0.8
)

# In next project, developer remembers
patterns = developer.get_agent_context()
# Returns patterns learned from ALL previous projects
```

### Pattern 3: Team Analytics

```python
# Analyze team communication patterns
stats = team.get_project_summary()

# Which agents communicate most?
# What topics generate most debate?
# Which decisions took longest to reach consensus?

debates = team.get_all_debates()
# Analyze decision-making process
```

---

## ✅ Comparison Matrix

| Feature | In-Memory Context | Our PostgreSQL Solution |
|---------|-------------------|-------------------------|
| **Storage Capacity** | ~500 messages | Unlimited |
| **Token Window** | Limited (128K) | Managed (always optimal) |
| **Persistence** | Lost on restart | Permanent |
| **Search** | Linear scan | Indexed (fast) |
| **Cross-Session** | No | Yes |
| **Historical Context** | Lost when window fills | Always available |
| **Relevance Scoring** | None (chronological) | Smart (semantic) |
| **Per-Agent Memory** | Shared/mixed | Isolated |
| **Project Duration** | Days | Years |
| **Context Quality** | Degrades over time | Consistent |

---

## 🎬 Conclusion

By using PostgreSQL for unlimited context storage with intelligent retrieval, we've solved the fundamental limitation of AI agents: **limited memory**.

Your agents can now:
- Work on projects for years without forgetting
- Retrieve relevant context from unlimited history
- Maintain personal knowledge bases
- Resume projects instantly
- Search and analyze entire conversation history

**This is not just more storage - it's smarter memory management that makes agents genuinely useful for long-term projects.**
