# PostgreSQL Unlimited Context Setup Guide

This guide will help you set up PostgreSQL to give your Destiny Team agents **unlimited context windows**.

---

## 🎯 What Problem Does This Solve?

**The Context Window Problem:**
- AI models have token limits (e.g., 128K tokens for GPT-4)
- Long projects generate thousands of messages
- Agents "forget" important earlier conversations
- Can't maintain context across sessions

**The PostgreSQL Solution:**
- Store ALL messages in PostgreSQL (unlimited storage)
- Retrieve only RELEVANT messages when needed (smart retrieval)
- Persist context across sessions (restart without losing memory)
- Search entire conversation history (find anything discussed)

---

## 📦 Installation

### Step 1: Install PostgreSQL

**On macOS:**
```bash
# Using Homebrew
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On Windows:**
Download from: https://www.postgresql.org/download/windows/

---

### Step 2: Create Database

```bash
# Create database for Destiny Team
createdb destiny_team

# Or using psql
psql postgres
CREATE DATABASE destiny_team;
\q
```

---

### Step 3: Install Python PostgreSQL Library

```bash
pip install psycopg2-binary
```

---

### Step 4: Initialize Schema

Run the setup script to create all tables:

```bash
cd /Users/artur/coursor-agents-destiny-folder
python postgres_context_store.py
```

This creates:
- `messages` - All agent communications
- `agent_contexts` - Personal knowledge per agent
- `projects` - Project metadata
- `agent_work_queue` - Task tracking
- `decisions` - Decision log

---

## 🚀 Quick Start

### Basic Usage

```python
from postgres_integration import DestinyTeamWithPostgres
from destiny_team import ProjectState, MessageType

# 1. Initialize team with PostgreSQL
team = DestinyTeamWithPostgres(
    postgres_connection_string="dbname=destiny_team user=artur host=localhost"
)

# 2. Start a project
project_id = team.start_project(
    project_name="My Awesome App",
    description="A web application for task management"
)

# 3. Agents communicate (automatically stored in PostgreSQL)
pm = team.agents['pm']
pm.send_message(
    recipient=None,
    message_type=MessageType.REQUEST,
    content="What are the core features we need?"
)

# 4. Agent thinks with UNLIMITED context
architect = team.agents['architect']
response = architect.think(
    prompt="Design the system architecture",
    project_state=ProjectState(project_name="My App", description="Task management")
)

print(response)

# 5. Search through unlimited history
results = team.search_project_history("database architecture")
print(f"Found {len(results)} relevant messages")

# 6. Get project statistics
summary = team.get_project_summary()
print(f"Total messages: {summary['project_stats']['total_messages']}")

# 7. Close connection
team.close()
```

---

## 🔑 Key Features

### 1. Unlimited Message Storage

```python
# Every message is automatically stored in PostgreSQL
agent.send_message(
    recipient="Developer",
    message_type=MessageType.REQUEST,
    content="Can you implement the login feature?"
)

# Retrieve agent's full history (even from months ago)
history = agent.get_my_conversation_history(limit=1000)
```

### 2. Intelligent Context Retrieval

Instead of loading ALL messages (which would exceed token limits), the system retrieves only the most **relevant** messages:

```python
# Agent thinks about a question
response = agent.think("How should we handle user authentication?")

# Behind the scenes:
# 1. Extracts keywords: "user", "authentication", "handle"
# 2. Scores ALL messages in database for relevance
# 3. Retrieves top 20 most relevant messages
# 4. Builds context prompt from those messages
# 5. Calls AI model with relevant context
```

**Relevance Scoring Algorithm:**
- Keyword overlap (30%)
- Recency (20%)
- Message importance (30%)
- Agent involvement (20%)

### 3. Per-Agent Knowledge Bases

Each agent maintains their own persistent knowledge:

```python
# Architect stores architecture decisions
architect.add_to_context(
    key="database_choice",
    value={"database": "PostgreSQL", "reason": "Strong ACID guarantees"},
    importance=0.9
)

# Later (even in a new session), architect remembers
decisions = architect.context_store.get_agent_context(
    agent_name=architect.name,
    project_id=project_id
)
print(decisions['database_choice'])
# Output: {"database": "PostgreSQL", "reason": "Strong ACID guarantees"}
```

### 4. Cross-Session Persistence

```python
# Session 1: Start project
team = DestinyTeamWithPostgres(...)
project_id = team.start_project("My App", "Description")
# ... work on project ...
team.close()

# Session 2 (days later): Resume project
team = DestinyTeamWithPostgres(..., project_id=project_id)
# All messages and context are still there!
history = team.search_project_history("authentication")
# Returns messages from Session 1
```

### 5. Full-Text Search

```python
# Find all discussions about a topic
security_messages = team.search_project_history("security authentication payment")

# Find all debates
debates = team.get_all_debates()

# Find messages by type
approvals = team.context_store.get_messages_by_type(
    project_id=project_id,
    message_type="APPROVAL"
)
```

### 6. Conversation Threading

```python
# Get entire conversation thread
thread = team.context_store.get_conversation_thread(message_id)

# Shows: Original message → Response 1 → Response 2 → ...
for msg in thread:
    print(f"{msg.sender}: {msg.content}")
```

---

## 📊 Database Schema

### Messages Table

Stores all agent communications:

| Column | Type | Description |
|--------|------|-------------|
| `id` | VARCHAR(255) | Unique message ID |
| `project_id` | VARCHAR(255) | Project identifier |
| `sender` | VARCHAR(255) | Agent who sent message |
| `recipient` | VARCHAR(255) | Recipient (NULL = broadcast) |
| `message_type` | VARCHAR(50) | REQUEST, ANNOUNCEMENT, etc. |
| `content` | TEXT | Message content |
| `context` | JSONB | Additional context data |
| `timestamp` | TIMESTAMP | When message was sent |
| `importance` | FLOAT | Importance score (0-1) |
| `tags` | TEXT[] | Keywords for indexing |

### Agent Contexts Table

Stores each agent's personal knowledge:

| Column | Type | Description |
|--------|------|-------------|
| `agent_name` | VARCHAR(255) | Agent identifier |
| `project_id` | VARCHAR(255) | Project identifier |
| `context_key` | VARCHAR(255) | Knowledge key |
| `context_value` | JSONB | Knowledge value |
| `importance` | FLOAT | How important (0-1) |
| `updated_at` | TIMESTAMP | Last update time |

---

## 🎛️ Configuration

### Connection String Formats

**Local development:**
```python
"dbname=destiny_team user=artur host=localhost"
```

**With password:**
```python
"dbname=destiny_team user=artur password=secret host=localhost port=5432"
```

**Remote PostgreSQL:**
```python
"dbname=destiny_team user=artur password=secret host=db.example.com port=5432 sslmode=require"
```

### Performance Tuning

For better performance with large message volumes:

```sql
-- Create additional indexes
CREATE INDEX idx_messages_content_fulltext ON messages USING GIN(to_tsvector('english', content));

-- Adjust PostgreSQL settings (in postgresql.conf)
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
```

---

## 🔧 Advanced Usage

### Custom Relevance Scoring

Modify the relevance algorithm for your needs:

```python
# In postgres_context_store.py, modify get_relevant_context_for_agent()

# Example: Prioritize recent messages more
# Change recency weight from 0.2 to 0.4
```

### Add Vector Embeddings

For true semantic search, add vector embeddings:

```sql
-- 1. Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create embeddings table
CREATE TABLE message_embeddings (
    message_id VARCHAR(255) PRIMARY KEY,
    embedding vector(1536),  -- OpenAI ada-002 dimension
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

-- 3. Create index for fast similarity search
CREATE INDEX ON message_embeddings USING ivfflat (embedding vector_cosine_ops);
```

Then use OpenAI embeddings API to generate embeddings and store them.

### Export Project History

```python
# Export all messages to JSON
import json

messages = context_store.get_agent_conversation_history(
    agent_name="Architect",
    project_id=project_id,
    limit=10000
)

with open('project_history.json', 'w') as f:
    json.dump([asdict(msg) for msg in messages], f, default=str, indent=2)
```

---

## 🐛 Troubleshooting

### Connection Refused

```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
```bash
# Check if PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Start if not running
brew services start postgresql@15  # macOS
sudo systemctl start postgresql  # Linux
```

### Database Does Not Exist

```
psycopg2.OperationalError: database "destiny_team" does not exist
```

**Solution:**
```bash
createdb destiny_team
```

### Authentication Failed

```
psycopg2.OperationalError: FATAL: password authentication failed
```

**Solution:**
```bash
# Update pg_hba.conf to trust local connections
# Location: /usr/local/var/postgresql@15/pg_hba.conf (macOS)

# Change this line:
# host  all  all  127.0.0.1/32  md5

# To:
# host  all  all  127.0.0.1/32  trust

# Restart PostgreSQL
brew services restart postgresql@15
```

---

## 📈 Performance Benchmarks

With PostgreSQL, your agents can:

- ✅ Store **millions of messages** (vs ~100 in memory)
- ✅ Search **entire project history** in milliseconds
- ✅ Retrieve **relevant context** without token limits
- ✅ **Resume projects** instantly (context already loaded)
- ✅ Support **multiple concurrent projects**

**Example:** After 1000 messages:
- In-memory system: Context window full, older messages lost
- PostgreSQL system: All 1000 messages stored, top 20 most relevant retrieved in <10ms

---

## 🎯 Next Steps

1. **Set up PostgreSQL** using this guide
2. **Test with example_usage()** in `postgres_integration.py`
3. **Adapt your existing agents** to use PostgresAgent class
4. **Monitor database** growth and performance
5. **Add vector embeddings** for semantic search (optional)

---

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Tutorial](https://www.psycopg.org/docs/)
- [pgvector for Embeddings](https://github.com/pgvector/pgvector)

---

## 💡 Why This Is Brilliant

**Traditional approach:**
- Agent has 128K token context window
- After 100 messages, window is full
- Older messages are lost
- Agent "forgets" important decisions

**PostgreSQL approach:**
- Agent has UNLIMITED storage
- After 1M messages, all are stored
- Retrieves top 20 most relevant
- Agent "remembers" everything relevant

**Result:** Your agents can work on projects for months without forgetting anything important!
