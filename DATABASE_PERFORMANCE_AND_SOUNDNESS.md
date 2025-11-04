# Database Performance & Project Soundness

**Created:** November 3, 2025  
**Author:** Aleksander Nowak  
**Critical Lesson:** 584-second query exposed lack of index  
**Purpose:** Prevent performance disasters, ensure project soundness  

---

## ⚠️ **THE 584-SECOND PROBLEM**

### **What Happened:**

```sql
SELECT COUNT(*), MAX(timestamp) 
FROM events 
WHERE project_id = 'destiny-team-framework-master';

-- Execution time: 584 seconds (9 minutes 44 seconds) ⚠️
```

### **Root Cause:**
❌ **NO INDEX on `project_id` column**

**What actually happened:**
```
PostgreSQL without index:
├─ Full Table Scan (reads EVERY row)
├─ Millions of rows examined
├─ Heavy disk I/O (read entire table from disk)
├─ CPU at 100% for 10 minutes
├─ Other queries blocked/delayed
└─ System appears "frozen"
```

**What SHOULD happen with proper index:**
```
PostgreSQL with index:
├─ Index Scan (jumps directly to matching rows)
├─ Only relevant rows examined
├─ Minimal disk I/O
├─ CPU usage minimal
├─ Query completes in milliseconds
└─ System responsive
```

### **Impact on "System Soundness":**

When database queries take 10 minutes:
- ❌ Application appears frozen
- ❌ Other queries queue up and wait
- ❌ Connection pool exhausted
- ❌ Users frustrated
- ❌ Agents can't work
- ❌ **Project unusable**

**THIS IS WHY DATABASE OPTIMIZATION IS CRITICAL FOR PROJECT SOUNDNESS!**

---

## 🎯 **DATABASE ROLE IN PROJECT SOUNDNESS**

### **Your Docker Database Stack:**

```
Project Soundness = ALL databases working FAST and CORRECTLY

PostgreSQL (sms-postgres)
├─ Role: Source of truth, structured data
├─ Critical for: Tasks, agents, results, history
├─ Performance needs: INDICES on frequently queried columns
└─ Without optimization: Full table scans = DISASTER

Redis (kg-redis)
├─ Role: Fast cache layer
├─ Critical for: Real-time performance
├─ Performance needs: Proper TTL, memory management
└─ Without optimization: Cache misses = Slow system

Neo4j (sms-neo4j)
├─ Role: Knowledge graph, relationships
├─ Critical for: Agent discovery, collaboration paths
├─ Performance needs: Proper constraints, indices
└─ Without optimization: Slow graph traversal

Qdrant (sms-qdrant)
├─ Role: Semantic memory, vector search
├─ Critical for: Intelligent retrieval
├─ Performance needs: Proper collection config, HNSW parameters
└─ Without optimization: Slow semantic search

Elasticsearch (hercules-elasticsearch)
├─ Role: Full-text search, document indexing
├─ Critical for: Document discovery
├─ Performance needs: Proper mapping, sharding
└─ Without optimization: Slow searches, memory issues
```

**If ANY database is slow → ENTIRE project is slow!**

---

## 🔧 **SOLUTION: Database Optimization Checklist**

### **1. PostgreSQL Index Strategy:**

**Rule:** Every column used in `WHERE`, `JOIN`, or `ORDER BY` should have an index!

```sql
-- Check existing indices
\di

-- For events table (when it exists):
CREATE INDEX IF NOT EXISTS idx_events_project_id 
ON events (project_id);

CREATE INDEX IF NOT EXISTS idx_events_timestamp 
ON events (timestamp DESC);

-- Composite index for common query patterns
CREATE INDEX IF NOT EXISTS idx_events_project_timestamp 
ON events (project_id, timestamp DESC);

-- For our new analytical tables:
CREATE INDEX IF NOT EXISTS idx_analytical_agents_team 
ON analytical_agents (team);

CREATE INDEX IF NOT EXISTS idx_team_capabilities_team_agent 
ON team_capabilities (team, agent_name);

CREATE INDEX IF NOT EXISTS idx_cross_team_routing_teams 
ON cross_team_routing (from_team, to_team);
```

**Verify indices work:**
```sql
EXPLAIN ANALYZE SELECT COUNT(*) 
FROM events 
WHERE project_id = 'destiny-team-framework-master';

-- Should show "Index Scan" not "Seq Scan"
```

---

### **2. Redis Optimization:**

```bash
# Check memory usage
docker exec kg-redis redis-cli INFO memory | grep used_memory_human

# Set TTL on all keys (don't let cache grow forever)
docker exec kg-redis redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Check slow queries
docker exec kg-redis redis-cli SLOWLOG GET 10
```

---

### **3. Neo4j Optimization:**

```cypher
// Create constraints (improves lookups)
CREATE CONSTRAINT agent_name_unique IF NOT EXISTS
FOR (a:Agent) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT team_id_unique IF NOT EXISTS
FOR (t:Team) REQUIRE t.team_id IS UNIQUE;

// Create indices
CREATE INDEX agent_team_idx IF NOT EXISTS
FOR (a:Agent) ON (a.team);

CREATE INDEX capability_name_idx IF NOT EXISTS
FOR (c:Capability) ON (c.name);

// Check slow queries
CALL dbms.listQueries() YIELD queryId, query, elapsedTimeMillis
WHERE elapsedTimeMillis > 1000
RETURN queryId, query, elapsedTimeMillis;
```

---

### **4. Qdrant Optimization:**

```python
# Proper collection config
client.create_collection(
    collection_name="my-collection",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE,
        hnsw_config=HnswConfigDiff(
            m=16,              # Number of connections (higher = better search, more memory)
            ef_construct=100,  # Construction quality (higher = better, slower indexing)
        )
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,  # Start indexing after this many points
    )
)

# Monitor performance
collection_info = client.get_collection("my-collection")
print(f"Points: {collection_info.points_count}")
print(f"Status: {collection_info.status}")
```

---

## 📋 **BEST PRACTICES FOR PROJECT SOUNDNESS**

### **1. Index Strategy:**

**✅ DO:**
- Create indices on `project_id`, `team`, `agent_name`, `timestamp`
- Use composite indices for common query patterns
- Test with `EXPLAIN ANALYZE` before deploying
- Monitor slow query logs

**❌ DON'T:**
- Create indices on every column (wastes space)
- Forget to update indices when schema changes
- Index low-cardinality columns (like boolean flags)
- Ignore query performance warnings

---

### **2. Query Patterns:**

**✅ GOOD:**
```sql
-- Uses index
SELECT * FROM events 
WHERE project_id = 'xxx' 
AND timestamp > NOW() - INTERVAL '1 day'
ORDER BY timestamp DESC 
LIMIT 100;
```

**❌ BAD:**
```sql
-- Full table scan!
SELECT * FROM events 
WHERE LOWER(project_id) = 'xxx';  -- Function prevents index use

SELECT COUNT(*) FROM events;  -- Counts everything, no filter
```

---

### **3. Table Maintenance:**

```sql
-- Regular maintenance (prevents bloat)
VACUUM ANALYZE events;

-- Check table bloat
SELECT 
    schemaname, 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

---

### **4. Connection Pool Management:**

```python
# Use connection pooling
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,  # Adjust based on load
    host="localhost",
    port=5432,
    database="destiny",
    user="user"
)

# Always close connections
conn = connection_pool.getconn()
try:
    # Use connection
    cursor.execute(query)
finally:
    connection_pool.putconn(conn)  # Return to pool
```

---

## 🎯 **VERIFICATION: Are Our Analytical Tables Optimized?**

Let me check what we created:

<function_calls>
<invoke name="Shell">
<parameter name="command">docker exec sms-postgres psql -U user -d destiny << 'SQL'
-- Check if our analytical tables have proper indices
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN ('analytical_agents', 'team_capabilities', 'cross_team_routing', 'analytical_team_docs', 'analytical_infrastructure')
ORDER BY tablename, indexname;
SQL
