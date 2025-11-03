# 🗺️ DATA ROUTING - Gdzie Co Trafia i Dlaczego

## 🎯 **GŁÓWNA ZASADA: Każda warstwa ma swoje zadanie**

```
Pytanie: "Gdzie zapisać X?"
Odpowiedź: WSZĘDZIE! Ale każda warstwa przechowuje inaczej.
```

---

## 📊 **COMPLETE DATA ROUTING MAP**

### **Typ Danych: WIADOMOŚĆ (Message)**

**Przykład:** *"Aleksander → Tomasz: Zaimplementuj authentication"*

**Co trafia gdzie:**

#### 1️⃣ **PostgreSQL** (PRIMARY SOURCE OF TRUTH)
```sql
INSERT INTO messages (...)
VALUES (
  id: "msg-12345",
  project_id: "osint-mvp",
  sender: "Aleksander Nowak",
  recipient: "Tomasz Zieliński",
  content: "Zaimplementuj authentication",
  type: "TASK_ASSIGNMENT",
  importance: 0.9,
  timestamp: NOW()
)
```

**Dlaczego tam:** 
- ✅ Structured data (relacyjne)
- ✅ ACID transactions
- ✅ Query flexibility (SQL)
- ✅ Długoterminowe storage
- ✅ Backup & recovery

**Jak query:**
```sql
SELECT * FROM messages 
WHERE project_id = 'osint-mvp' 
  AND sender = 'Aleksander Nowak'
ORDER BY timestamp DESC
```

---

#### 2️⃣ **Neo4j** (RELATIONSHIPS & GRAPH)
```cypher
CREATE (m:Message {
  id: "msg-12345",
  content: "Zaimplementuj authentication",
  timestamp: datetime()
})

CREATE (sender:Agent {name: "Aleksander Nowak"})
CREATE (recipient:Agent {name: "Tomasz Zieliński"})

CREATE (sender)-[:SENT]->(m)
CREATE (m)-[:TO]->(recipient)

// Extract concepts
CREATE (auth:Concept {name: "Authentication"})
CREATE (m)-[:MENTIONS]->(auth)
```

**Dlaczego tam:**
- ✅ Relationship tracking (kto z kim, o czym)
- ✅ Concept extraction (co było dyskutowane)
- ✅ Graph traversal ("pokaż wszystkie rozmowy o auth")
- ✅ Network analysis (kto z kim najczęściej)

**Jak query:**
```cypher
// Znajdź wszystkie wiadomości o authentication
MATCH (m:Message)-[:MENTIONS]->(c:Concept {name: "Authentication"})
RETURN m

// Kto najczęściej pisze do Tomasza?
MATCH (sender:Agent)-[:SENT]->(:Message)-[:TO]->(tomasz:Agent {name: "Tomasz Zieliński"})
RETURN sender.name, COUNT(*) as message_count
ORDER BY message_count DESC
```

---

#### 3️⃣ **Qdrant** (SEMANTIC MEANING)
```python
# Generate embedding (1024 dimensions)
embedding = embedder.embed("Zaimplementuj authentication")
# → [0.12, -0.45, 0.78, ..., 0.34]

# Store in Qdrant
qdrant.upsert(
  collection="destiny-team-osint-mvp",
  points=[{
    "id": "msg-12345",
    "vector": embedding,  # 1024 floats
    "payload": {
      "content": "Zaimplementuj authentication",
      "sender": "Aleksander Nowak",
      "timestamp": "2025-11-01T10:30:00",
      "importance": 0.9
    }
  }]
)
```

**Dlaczego tam:**
- ✅ Semantic search ("znajdź podobne do auth")
- ✅ Meaning-based (nie tylko keywords)
- ✅ Cross-language (Polski + English works)
- ✅ Fuzzy matching ("autentykacja" finds "authentication")

**Jak query:**
```python
# User pytanie: "jak zrobić logowanie?"
query_embedding = embedder.embed("jak zrobić logowanie")

results = qdrant.search(
  collection="destiny-team-osint-mvp",
  query_vector=query_embedding,
  limit=10
)
# Returns: Messages o authentication, login, security
# Even if they don't contain word "logowanie"!
```

---

#### 4️⃣ **Redis** (HOT CACHE)
```python
# Add to hot memory (last N messages)
redis.lpush(
  "destiny:osint-mvp:hot_memory",
  json.dumps({
    "id": "msg-12345",
    "sender": "Aleksander Nowak",
    "content": "Zaimplementuj authentication",
    "timestamp": "2025-11-01T10:30:00"
  })
)

# Keep only last 10
redis.ltrim("destiny:osint-mvp:hot_memory", 0, 9)

# TTL: 24 hours
redis.expire("destiny:osint-mvp:hot_memory", 86400)
```

**Dlaczego tam:**
- ✅ Ultra-fast access (<1ms)
- ✅ Recent context (last 10 messages)
- ✅ Temporary (expires after 24h)
- ✅ Reduces load on PostgreSQL

**Jak query:**
```python
# Get recent messages instantly
hot = redis.lrange("destiny:osint-mvp:hot_memory", 0, -1)
# Returns: Last 10 messages in <1ms
```

---

### **Typ Danych: DECYZJA (Decision)**

**Przykład:** *"PostgreSQL chosen over MongoDB"*

#### 1️⃣ **PostgreSQL**
```sql
INSERT INTO decisions (...)
VALUES (
  id: 1,
  project_id: "osint-mvp",
  decision_text: "PostgreSQL chosen as primary database",
  decision_type: "TECH_STACK",
  made_by: "Katarzyna Wiśniewska",
  approved_by: ["Tomasz", "Michał"],
  context: {...},
  timestamp: NOW()
)
```

**Dlaczego:** Structured storage + queryable history

---

#### 2️⃣ **Neo4j** (DECISION GRAPH!)
```cypher
// Create decision node
CREATE (d:Decision {
  id: "decision-1",
  text: "PostgreSQL chosen as primary database",
  timestamp: datetime()
})

// Who decided
CREATE (arch:Agent {name: "Katarzyna Wiśniewska"})
CREATE (arch)-[:MADE_DECISION]->(d)

// What was chosen
CREATE (pg:Concept {name: "PostgreSQL"})
CREATE (d)-[:CHOSE]->(pg)

// What was rejected
CREATE (mongo:Concept {name: "MongoDB"})
CREATE (d)-[:REJECTED]->(mongo)

// Why (reasons)
CREATE (acid:Reason {text: "ACID compliance needed"})
CREATE (d)-[:BECAUSE]->(acid)

// Impact
CREATE (deployment:Concept {name: "Deployment"})
CREATE (d)-[:IMPACTS]->(deployment)
```

**Dlaczego tam:** **TO JEST KILLER FEATURE!**
- ✅ Answer "WHY" questions
- ✅ Track decision chains
- ✅ Show alternatives considered
- ✅ Impact analysis

**Query example:**
```cypher
// WHY did we choose PostgreSQL?
MATCH (d:Decision)-[:CHOSE]->(pg:Concept {name: "PostgreSQL"})
MATCH (d)-[:BECAUSE]->(reason:Reason)
MATCH (d)-[:REJECTED]->(rejected:Concept)
MATCH (agent:Agent)-[:MADE_DECISION]->(d)
RETURN 
  agent.name as decided_by,
  d.text as decision,
  collect(reason.text) as reasons,
  collect(rejected.name) as alternatives_rejected
```

**Output:**
```
Decided by: Katarzyna Wiśniewska
Decision: PostgreSQL chosen
Reasons: ["ACID compliance", "Team experience", "Proven tech"]
Rejected: ["MongoDB", "MySQL"]
```

---

### **Typ Danych: STATUS PROJEKTU**

**Przykład:** *"Current phase: Development, 3 tasks in progress"*

#### 1️⃣ **PostgreSQL**
```sql
-- Project metadata
UPDATE projects 
SET current_phase = 'Development',
    updated_at = NOW()
WHERE project_id = 'osint-mvp'

-- Work queue
INSERT INTO agent_work_queue (...)
VALUES 
  ('Tomasz', 'osint-mvp', 'Implement auth', 'in_progress'),
  ('Anna', 'osint-mvp', 'Test auth', 'pending'),
  ('Piotr', 'osint-mvp', 'Deploy staging', 'pending')
```

**Dlaczego:** Canonical source of current state

---

#### 2️⃣ **Redis** (ACTIVE PROJECT STATE)
```python
# Mark project active
redis.setex(
  "destiny:active_project:osint-mvp",
  86400,  # 24h TTL
  json.dumps({
    "phase": "Development",
    "last_activity": "2025-11-01T14:30:00",
    "active_agents": ["Tomasz", "Anna"],
    "tasks_in_progress": 3
  })
)
```

**Dlaczego:** Fast access to current state without hitting PostgreSQL

---

### **Typ Danych: PLANY / ROADMAP**

**Przykład:** *"Next: Complete auth, then start frontend"*

#### 1️⃣ **PostgreSQL**
```sql
INSERT INTO agent_contexts (...)
VALUES (
  'Aleksander Nowak',
  'osint-mvp',
  'plan_immediate',
  '["Complete auth", "Start frontend", "Deploy staging"]',
  0.9
)
```

**Dlaczego:** Persistent plans storage

---

#### 2️⃣ **PROJECT_STATUS.md** (FILE!)
```markdown
## 📅 PLANY

### 🔥 Natychmiastowe Następne Kroki
1. Complete authentication (Tomasz)
2. Start frontend dashboard (Tomasz)
3. Deploy to staging (Piotr)
```

**Dlaczego:** Human-readable dla orchestratora przy starcie sesji!

---

## 🔄 **AUTOMATIC ROUTING - Jak To Działa**

### **Master Orchestrator koordinuje wszystko:**

```python
class MasterOrchestrator:
    def store_message(self, project_id, sender, content, ...):
        """
        ONE call → FOUR destinations!
        """
        
        # 1. PostgreSQL (always)
        self.postgres.store_message(
            StoredMessage(...)
        )
        
        # 2. Neo4j (extract concepts, relationships)
        if self.neo4j:
            # Extract concepts from content
            concepts = extract_concepts(content)
            self.neo4j.add_message_to_graph(
                message_id=msg_id,
                sender=sender,
                concepts=concepts
            )
        
        # 3. Qdrant (generate embedding, semantic index)
        if self.qdrant:
            # Generate embedding via LM Studio
            embedding = self.embedder.embed(content)
            self.qdrant.store_message(
                message_id=msg_id,
                content=content,
                embedding=embedding
            )
        
        # 4. Redis (add to hot memory)
        if self.redis:
            self.redis.add_to_hot_memory(
                project_id=project_id,
                message={
                    "id": msg_id,
                    "sender": sender,
                    "content": content
                }
            )
        
        # DONE! Automatic propagation to all 4 layers!
```

---

## 🔍 **INTELLIGENT SEARCH - Routing Queries**

```python
def search(query: str, search_type: str):
    """
    Different search types use different layers.
    """
    
    if search_type == "keyword":
        # PostgreSQL - exact keyword matching
        return postgres.execute(
            "SELECT * FROM messages WHERE content ILIKE %s",
            f"%{query}%"
        )
    
    elif search_type == "semantic":
        # Qdrant - meaning-based search
        query_embedding = embedder.embed(query)
        return qdrant.search(
            query_vector=query_embedding,
            limit=20
        )
    
    elif search_type == "graph":
        # Neo4j - relationship traversal
        return neo4j.run("""
            MATCH (m:Message)-[:MENTIONS]->(c:Concept)
            WHERE c.name CONTAINS $query
            RETURN m
        """, query=query)
    
    elif search_type == "hot":
        # Redis - recent messages only
        return redis.get_hot_memory(project_id)
    
    elif search_type == "hybrid":
        # ALL LAYERS - merge results using RRF
        keyword_results = search("keyword")
        semantic_results = search("semantic")
        graph_results = search("graph")
        
        return reciprocal_rank_fusion([
            keyword_results,
            semantic_results,
            graph_results
        ])
```

---

## 📊 **DATA FLOW DIAGRAM**

```
USER ACTION: "Aleksander sends message to Tomasz"
     │
     ▼
┌────────────────────────────────┐
│   MASTER ORCHESTRATOR          │
│   (Intelligent Router)         │
└──────┬─────────────────────────┘
       │
       │ Automatic routing...
       │
    ┌──┴──┬────────┬────────┐
    │     │        │        │
    ▼     ▼        ▼        ▼
┌──────┐ ┌────┐ ┌──────┐ ┌──────┐
│ PG   │ │Neo4│ │Qdrant│ │Redis │
│      │ │ j  │ │      │ │      │
│ SQL  │ │Graph│ │Vector│ │Cache │
│ rows │ │nodes│ │embeds│ │json  │
└──────┘ └────┘ └──────┘ └──────┘

Each layer stores SAME data but DIFFERENT format!
```

---

## 🎯 **KEY INSIGHTS**

### **1. Redundancy is GOOD here!**
```
Same message stored 4x?
YES! Because each layer serves different purpose:
- PostgreSQL: Long-term, structured
- Neo4j: Relationships, "why" questions
- Qdrant: Semantic search
- Redis: Speed

NOT duplication - SPECIALIZATION!
```

### **2. Automatic Propagation**
```
You call: orchestrator.store_message()
Framework handles: 
  ✅ PostgreSQL insert
  ✅ Neo4j graph update
  ✅ Qdrant vector indexing
  ✅ Redis cache update
  
Zero manual work!
```

### **3. Query Optimization**
```
"Recent messages" → Redis (0.5ms)
"Messages about X" → PostgreSQL (50ms)  
"Similar to Y" → Qdrant (20ms)
"Why Z decided?" → Neo4j (100ms)

Framework picks fastest layer for each query type!
```

### **4. Isolation**
```
Project A: destiny:project-a:*
Project B: destiny:project-b:*

ZERO cross-contamination!
Each project = isolated namespace in ALL layers.
```

---

## ✅ **PODSUMOWANIE**

**Pytanie:** "Czy wszystkie wytyczne, status, komunikacja, plany są zarządzane do odpowiednich baz?"

**Odpowiedź:** **TAK! I to automatycznie!**

```
┌─────────────────────────────────────────────┐
│         MASTER ORCHESTRATOR                 │
│                                             │
│  ONE call → FOUR destinations               │
│  ONE source → SPECIALIZED storage           │
│  AUTOMATIC routing                          │
│  ZERO manual work                           │
│  GUARANTEED consistency                     │
└─────────────────────────────────────────────┘

         Everything coordinated!
```

**Framework dba o routing.**  
**Ty focus na budowanie aplikacji.**  
**System zarządza danymi automatycznie.** 🎯

---

*This is why it's called a FRAMEWORK.*  
*You use it. It handles complexity.*
