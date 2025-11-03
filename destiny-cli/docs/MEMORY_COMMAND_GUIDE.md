# 🧠 destiny-memory Command Guide

**Author:** Joanna Mazur (Data Scientist)  
**Integration:** Helena's 4-Database Architecture  
**Version:** 1.0

## 📖 Overview

`destiny-memory` is a CLI tool for exploring and analyzing the Destiny Team Framework's multi-layer memory system. It provides visibility into all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis) and helps you understand what agents have learned, how they collaborate, and the health of the memory system.

## 🎯 What It Does

### **Core Capabilities:**

1. **Memory Statistics** - See what's stored across all 4 databases
2. **Semantic Search** - Find relevant memories using AI embeddings
3. **Agent Memories** - View what specific agents have learned
4. **Collaboration Network** - Explore agent relationships (Neo4j graph)
5. **Health Monitoring** - Check database connectivity and health
6. **Memory Cleanup** - Remove old test data

---

## 🚀 Quick Start

```bash
# Installation (from destiny-cli directory)
pip install -r requirements.txt

# Basic usage
destiny memory stats              # Show memory statistics
destiny memory search "login"     # Search for memories
destiny memory agent tomasz       # Show Tomasz's memories
destiny memory health             # Check system health
```

---

## 📋 Commands

### 1. **`stats`** - Memory Statistics

Shows overview of all 4 databases with record counts and health status.

**Usage:**
```bash
destiny memory stats [OPTIONS]
```

**Options:**
- `--project, -p TEXT` - Filter by project ID
- `--verbose, -v` - Show detailed statistics including architecture explanation
- `--help` - Show this help message

**Examples:**
```bash
# Basic stats
destiny memory stats

# Specific project
destiny memory stats --project destiny-team-master

# Verbose output with architecture details
destiny memory stats --verbose
```

**Output:**
```
🧠 DESTINY MEMORY SYSTEM - STATISTICS

Project: destiny-team-framework-master

┌────────────────┬────────────┬──────────────┬────────────────┐
│ Database       │ Status     │ Records      │ Details        │
├────────────────┼────────────┼──────────────┼────────────────┤
│ PostgreSQL     │ 🟢 Healthy │ 1,247        │ Structured...  │
│ Neo4j          │ 🟢 Healthy │ 834 nodes    │ Knowledge...   │
│ Qdrant         │ 🟢 Healthy │ 2,156 vectors│ Semantic...    │
│ Redis          │ 🟢 Healthy │ 23 keys      │ Fast cache...  │
└────────────────┴────────────┴──────────────┴────────────────┘

✅ All 4 databases operational (4/4)
```

---

### 2. **`search`** - Semantic Search

Search memories using semantic similarity (powered by Qdrant vector search).

**Usage:**
```bash
destiny memory search QUERY [OPTIONS]
```

**Arguments:**
- `QUERY` - Search term or phrase (required)

**Options:**
- `--agent, -a TEXT` - Filter by agent name
- `--limit, -n INTEGER` - Number of results (default: 5)
- `--threshold, -t FLOAT` - Similarity threshold 0.0-1.0 (default: 0.6)
- `--help` - Show this help message

**Examples:**
```bash
# Basic search
destiny memory search "authentication bug"

# Filter by agent
destiny memory search "login" --agent tomasz

# More results with lower threshold
destiny memory search "architecture" --limit 10 --threshold 0.5

# High-relevance only
destiny memory search "critical" --threshold 0.9
```

**Output:**
```
🔍 MEMORY SEARCH: 'authentication bug'

Found 3 relevant memories:

╔═══════════════════════════════════════════════╗
║ #1 [Tomasz] - TASK                           ║
║ Debugged login authentication issue where... ║
║ 🔥 Very relevant (score: 94%) | 2025-10-15   ║
╚═══════════════════════════════════════════════╝

╔═══════════════════════════════════════════════╗
║ #2 [Anna] - TASK                              ║
║ Created test cases for login security...     ║
║ ✅ Relevant (score: 87%) | 2025-10-20        ║
╚═══════════════════════════════════════════════╝
```

**Relevance Levels:**
- 🔥 **90%+** - Very relevant (exact match)
- ✅ **75-89%** - Relevant (strong match)
- ⚠️ **60-74%** - Somewhat relevant (weak match)

---

### 3. **`agent`** - Agent-Specific Memories

Show all memories for a specific agent from PostgreSQL.

**Usage:**
```bash
destiny memory agent AGENT_NAME [OPTIONS]
```

**Arguments:**
- `AGENT_NAME` - Agent name (e.g., tomasz, anna, michal)

**Options:**
- `--last-days, -d INTEGER` - Show last N days (default: 30)
- `--limit, -n INTEGER` - Number of memories (default: 10)
- `--help` - Show this help message

**Examples:**
```bash
# Tomasz's recent memories
destiny memory agent tomasz

# Anna's last week
destiny memory agent anna --last-days 7

# More results
destiny memory agent michal --limit 20

# Specific time window
destiny memory agent katarzyna --last-days 90 --limit 50
```

**Output:**
```
🤖 AGENT MEMORIES: TOMASZ

Agent: Tomasz
Period: Last 30 days
Memories: 12

┌────────────┬───────────────┬──────────────────────────┬────────────┐
│ Date       │ Type          │ Content                  │ Importance │
├────────────┼───────────────┼──────────────────────────┼────────────┤
│ 2025-11-02 │ task          │ Implemented destiny-...  │ 0.9 🔥     │
│ 2025-11-01 │ decision      │ Chose TypeScript for...  │ 0.8 🔥     │
│ 2025-10-31 │ task          │ Fixed authentication...  │ 0.7        │
└────────────┴───────────────┴──────────────────────────┴────────────┘
```

**Importance Scale:**
- 🔥 **0.8+** - Critical/high importance
- ⚠️ **0.6-0.8** - Medium importance
- (dim) **<0.6** - Low importance

---

### 4. **`relationships`** - Collaboration Network

Explore agent collaboration patterns from Neo4j knowledge graph.

**Usage:**
```bash
destiny memory relationships [OPTIONS]
```

**Options:**
- `--agent, -a TEXT` - Show relationships for specific agent
- `--depth, -d INTEGER` - Relationship depth 1-3 (default: 1)
- `--help` - Show this help message

**Examples:**
```bash
# All relationships
destiny memory relationships

# Tomasz's collaborations
destiny memory relationships --agent tomasz

# Deeper relationships
destiny memory relationships --agent anna --depth 2
```

**Output:**
```
🕸️ AGENT COLLABORATION NETWORK

🕸️ Collaboration Network
├── Tomasz Kamiński
│   ├── ─[REVIEWED_BY]→ Anna (47 times)
│   ├── ─[IMPLEMENTED]→ Michał's designs (23 times)
│   └── ─[COORDINATED_BY]→ Aleksander (89 times)
├── Anna Lewandowska
│   ├── ─[TESTED]→ Tomasz's code (47 times)
│   └── ─[COORDINATED_BY]→ Aleksander (52 times)
```

**Relationship Types:**
- `REVIEWED_BY` - Code reviews
- `IMPLEMENTED` - Architecture implementation
- `TESTED` - QA testing
- `COORDINATED_BY` - Orchestration
- `DESIGNED_BY` - UX/Architecture design
- `DEPLOYED_BY` - DevOps deployment

---

### 5. **`health`** - System Health Check

Check connectivity and health of all 4 databases.

**Usage:**
```bash
destiny memory health [OPTIONS]
```

**Options:**
- `--check-all` - Run detailed health checks
- `--fix` - Attempt to fix common issues (not implemented yet)
- `--help` - Show this help message

**Examples:**
```bash
# Basic health check
destiny memory health

# Detailed check
destiny memory health --check-all

# Attempt fixes
destiny memory health --fix
```

**Output:**
```
🏥 MEMORY SYSTEM HEALTH CHECK

1. PostgreSQL (Structured Events)
   ✅ Connected
   Events: 1,247 | Version: PostgreSQL 15.3...

2. Neo4j (Knowledge Graph)
   ✅ Connected
   Container: sms-neo4j

3. Qdrant (Semantic Vectors)
   ✅ Connected
   Collections: 3

4. Redis (Fast Cache)
   ✅ Connected
   Container: kg-redis

================================================================================

✅ ALL SYSTEMS HEALTHY
All 4 databases are operational
```

**Status Indicators:**
- ✅ **Connected** - Database healthy
- ⚠️ **Warning** - Minor issues (still functional)
- ❌ **Failed** - Critical failure (not accessible)

---

### 6. **`cleanup`** - Memory Cleanup

Clean up old memories (DESTRUCTIVE - use with caution!)

**Usage:**
```bash
destiny memory cleanup [OPTIONS]
```

**Options:**
- `--older-than INTEGER` - Delete memories older than N days (default: 90)
- `--project TEXT` - Project ID to clean up
- `--dry-run/--execute` - Show what would be deleted vs actually delete (default: dry-run)
- `--confirm, -y` - Skip confirmation prompt
- `--help` - Show this help message

**Examples:**
```bash
# Dry run (safe - shows what would be deleted)
destiny memory cleanup --older-than 90 --dry-run

# Clean up test project
destiny memory cleanup --project test-* --dry-run

# Actually delete (DESTRUCTIVE)
destiny memory cleanup --older-than 180 --execute --confirm
```

**Output (Dry Run):**
```
⚠️ MEMORY CLEANUP (DESTRUCTIVE OPERATION)

Target: Memories older than 2025-08-01
Project: destiny-team-framework-master
Mode: DRY RUN (no changes)

Found 50 memories to clean up

✅ DRY RUN COMPLETE
Run with --execute to actually delete these memories
```

**⚠️ WARNING:**
- Cleanup is **PERMANENT** - deleted data cannot be recovered
- Always run `--dry-run` first to verify what will be deleted
- Use `--older-than` carefully (default 90 days is usually safe)
- Production projects: DO NOT use this command without backup

---

## 🏗️ Architecture Integration

### **How It Works:**

`destiny-memory` integrates with Helena's 4-database architecture:

1. **PostgreSQL** - Queries structured event data via `psycopg2`
2. **Neo4j** - Executes Cypher queries via Docker container
3. **Qdrant** - Searches vector embeddings via REST API
4. **Redis** - Checks cache status via Docker container

### **Database Roles:**

```
┌─────────────────────────────────────────────────────────────┐
│                     HELENA'S 4 LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. PostgreSQL  → Structured events, task history          │
│     └─ Tables: events, tasks, agent_metadata               │
│                                                             │
│  2. Neo4j       → Knowledge graph, relationships           │
│     └─ Nodes: Agent, Task, Decision                        │
│     └─ Edges: REVIEWED_BY, COORDINATED_BY, etc.           │
│                                                             │
│  3. Qdrant      → Semantic embeddings, vector search       │
│     └─ Collections: Per-project (1536-dim vectors)         │
│                                                             │
│  4. Redis       → Hot cache, queues, real-time status      │
│     └─ Keys: agent:status, task:queue, session:*          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing

Run tests:
```bash
# From destiny-cli directory
pytest tests/test_memory_command.py -v

# With coverage
pytest tests/test_memory_command.py --cov=destiny_cli.commands.memory

# Specific test
pytest tests/test_memory_command.py::TestMemoryStats -v
```

**Test Coverage:**
- Unit tests for all 6 commands
- Integration tests for Helena initialization
- Mock tests for database interactions
- Error handling tests

---

## 🔧 Troubleshooting

### **Common Issues:**

#### 1. **"ModuleNotFoundError: No module named 'typer'"**

**Solution:**
```bash
pip install -r requirements.txt
# or
pip install typer rich requests psycopg2-binary
```

#### 2. **"PostgreSQL connection failed"**

**Check:**
```bash
# Is PostgreSQL running?
docker ps | grep postgres

# Test connection
psql -h localhost -p 5432 -U user -d destiny_team
```

#### 3. **"Qdrant collection not found"**

**Solution:**
```bash
# Seed the collection first
cd /Users/artur/coursor-agents-destiny-folder
python3 seed_qdrant_test_collection.py
```

#### 4. **"Neo4j query failed"**

**Check:**
```bash
# Is Neo4j container running?
docker ps | grep neo4j

# Test Neo4j
docker exec sms-neo4j cypher-shell -u neo4j -p password "RETURN 'OK'"
```

#### 5. **"Redis ping failed"**

**Check:**
```bash
# Is Redis running?
docker ps | grep redis

# Test Redis
docker exec kg-redis redis-cli PING
```

---

## 📊 Usage Examples

### **Example 1: Daily Standup**

Check team activity:
```bash
# What did everyone work on recently?
destiny memory stats
destiny memory agent tomasz --last-days 1
destiny memory agent anna --last-days 1
```

### **Example 2: Bug Investigation**

Find related work:
```bash
# Search for authentication issues
destiny memory search "authentication" --limit 20

# Check who worked on it
destiny memory agent tomasz
destiny memory relationships --agent tomasz
```

### **Example 3: Project Onboarding**

Understand the system:
```bash
# System overview
destiny memory stats --verbose
destiny memory health

# See what agents do
destiny memory agent tomasz --limit 50
destiny memory relationships
```

### **Example 4: Database Maintenance**

Clean up old test data:
```bash
# Check what would be deleted
destiny memory cleanup --project test-* --dry-run

# Check system health first
destiny memory health

# Execute cleanup
destiny memory cleanup --project test-* --execute --confirm
```

---

## 🎯 Best Practices

### **1. Regular Health Checks**

Run weekly:
```bash
destiny memory health
destiny memory stats
```

### **2. Search Before Creating**

Before starting new work:
```bash
destiny memory search "similar topic"
```

### **3. Monitor Collaboration**

Track team dynamics:
```bash
destiny memory relationships --agent <name>
```

### **4. Clean Up Test Data**

After testing:
```bash
destiny memory cleanup --project test-* --dry-run
# Review output
destiny memory cleanup --project test-* --execute --confirm
```

### **5. Use Verbose Mode for Learning**

Understand the system:
```bash
destiny memory stats --verbose
destiny memory health --check-all
```

---

## 🚀 Advanced Usage

### **Scripting Integration**

```bash
#!/bin/bash
# Daily memory report

echo "=== Daily Memory Report ==="
date

echo -e "\n1. System Health:"
destiny memory health

echo -e "\n2. Memory Statistics:"
destiny memory stats

echo -e "\n3. Recent Activity:"
for agent in tomasz anna magdalena michal; do
    echo -e "\n$agent:"
    destiny memory agent $agent --last-days 1 --limit 5
done

echo -e "\n=== End Report ==="
```

### **Monitoring Script**

```bash
#!/bin/bash
# Check if memory system is healthy

if destiny memory health | grep -q "ALL SYSTEMS HEALTHY"; then
    echo "✅ Memory system operational"
    exit 0
else
    echo "❌ Memory system has issues"
    destiny memory health
    exit 1
fi
```

---

## 📚 Related Commands

- `destiny status` - Check agent and task status
- `destiny task` - Manage tasks
- `destiny agent` - Manage agents (future)
- `destiny demo` - Run demonstrations (future)

---

## 🤝 Contributing

This tool was created by **Joanna Mazur** (Data Scientist) and integrates with **Helena's** memory architecture.

**To extend:**
1. Add new commands in `destiny_cli/commands/memory.py`
2. Add tests in `tests/test_memory_command.py`
3. Update this documentation
4. Follow existing patterns (Rich formatting, error handling)

---

## 📝 Version History

**v1.0** (2025-11-03)
- Initial release
- 6 commands: stats, search, agent, relationships, health, cleanup
- Full integration with 4-database architecture
- Comprehensive tests and documentation

---

## 🎓 Learning Resources

**Understanding the Architecture:**
- `PROJECT_EXECUTIVE_SUMMARY.md` - System overview
- `ARCHITECTURE_EXPLAINED.md` - Database architecture
- `HELENA_CORE_DUTIES.md` - Helena's role

**Related Documentation:**
- `EVALUATOR_COMPREHENSIVE_GUIDE.md` - System evaluation
- `SHOWCASE_GUIDE.md` - Full-team orchestration
- `EPIC_SESSION_FINAL_REPORT.md` - Project history

---

## 💡 Tips & Tricks

1. **Fast search:** Use `--threshold 0.9` for exact matches only
2. **Wide net:** Use `--threshold 0.5 --limit 50` to find anything related
3. **Recent activity:** `--last-days 7` for weekly standups
4. **Pipe to file:** `destiny memory stats > memory_report.txt`
5. **Combine with grep:** `destiny memory agent tomasz | grep "authentication"`

---

**Questions? Issues?**

Check the main README or run any command with `--help` for detailed usage.

🧠 Happy memory exploring!
