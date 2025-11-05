# AUTOMATIC TASK ASSIGNMENT: Propagate Change to Databases

**GENERATED AUTOMATICALLY BY:** Change Detection System  
**Date:** 2025-11-05 08:00:00  
**Assigned to:** Helena Kowalczyk  
**Priority:** HIGH  
**Type:** Knowledge Propagation  
**Status:** PENDING  

---

## 🚨 **CHANGE DETECTED**

**File:** `sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql`  
**Type:** database_schema  
**Detected at:** 2025-11-05T08:00:00.583516  

**File Preview:**
```
INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'BATCH_MIGRATION_PLAN.md',
    'architecture',
    'Batch Processing Migration Plan',
    '# Batch Processing Migration Plan

## Executive Summary
Replace real-time database processing with intelligent batch system to resolve PostgreSQL performance crisis.

## Current State (CRITICAL)
- **R',
    157,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_
...
```

---

## 📋 **YOUR TASK (Helena)**

This change was **automatically detected** and requires propagation to ALL databases.

### **What You Must Do:**

1. **Analyze the change:**
   - Read the full file: `sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql`
   - Understand what it does
   - Identify what information needs to be in databases

2. **Update PostgreSQL:**
   - Add to `team_tools` if it's a new tool
   - Add to `agent_capabilities` if it changes agent abilities
   - Add to `project_processes` if it's a new process
   - Create SQL script in `sql/` directory

3. **Update Neo4j:**
   - Create nodes for new tools/processes/agents
   - Create relationships showing connections
   - Create Cypher script in `sql/` directory

4. **Update Qdrant:**
   - Index the documentation semantically
   - Make it searchable by meaning
   - Use script in `scripts/` directory

5. **Update Redis:**
   - Create cache entries for quick access
   - Set appropriate TTL
   - Use docker exec commands

6. **Verify:**
   - Run: `python3 scripts/verify_task_completion.py`
   - All checks must pass
   - Provide evidence

7. **Report:**
   - Create completion report
   - Include verification results
   - Save as: `/Users/artur/coursor-agents-destiny-folder/helena_tasks/completed_20251105_080000.md`

---

## ⚠️ **CRITICAL REQUIREMENTS**

- ✅ You MUST complete this within 4 hours
- ✅ You MUST update ALL 4 databases (PostgreSQL, Neo4j, Qdrant, Redis)
- ✅ You MUST run verification before reporting
- ✅ You MUST provide evidence with completion report
- ✅ If blocked, report IMMEDIATELY to Aleksander

---

## 📊 **VERIFICATION CRITERIA**

Your task is complete ONLY when:

```sql
-- PostgreSQL check
SELECT COUNT(*) FROM team_tools WHERE file_path LIKE '%sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql%';
-- Should return > 0

-- Neo4j check
MATCH (n) WHERE n.file_path CONTAINS 'sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql' RETURN count(n);
-- Should return > 0
```

```bash
# Qdrant check
curl -X POST http://localhost:6333/collections/destiny-team-framework-master/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"filter": {"must": [{"key": "file_path", "match": {"text": "sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql"}}]}}' | jq '.result.points | length'
# Should return > 0

# Redis check
docker exec kg-redis redis-cli KEYS "*pg_20251104_220923_BATCH_MIGRATION_PLAN*"
# Should return > 0
```

---

## 🎯 **ACCOUNTABILITY**

This task was **AUTOMATICALLY GENERATED** because the system detected a change.

**This proves:**
- ✅ System monitors itself
- ✅ No human needs to remember
- ✅ Zero knowledge drift guaranteed
- ✅ Continuous monitoring works

**Helena, you are accountable for:**
1. Executing this task completely
2. Updating all databases
3. Running verification
4. Reporting with evidence

**If you don't complete this task:**
- ❌ Knowledge drift occurs
- ❌ Agents won't discover this change
- ❌ Project soundness degrades
- ❌ System breaks down

---

## 📝 **COMPLETION REPORT TEMPLATE**

When done, create a file with this content:

```markdown
# Task Completion Report

**Task:** Propagate sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql to databases  
**Assigned by:** Automatic Change Detection System  
**Completed by:** Helena Kowalczyk  
**Date:** [DATE]  

## What Was Done:

### PostgreSQL:
- [ ] Updated tables: [list]
- [ ] SQL script: [path]
- [ ] Records added: [count]

### Neo4j:
- [ ] Nodes created: [list]
- [ ] Relationships: [list]
- [ ] Cypher script: [path]

### Qdrant:
- [ ] Documents indexed: [count]
- [ ] Indexing script: [path]

### Redis:
- [ ] Cache keys created: [list]
- [ ] TTL set: [seconds]

## Verification Results:

```
[Paste output of verify_task_completion.py]
```

## Evidence:

- PostgreSQL: [verification query results]
- Neo4j: [verification query results]
- Qdrant: [verification query results]
- Redis: [verification query results]

## Status: ✅ COMPLETE - VERIFIED

Helena Kowalczyk
```

---

**This is an AUTOMATIC task. Complete it to maintain project soundness.**
