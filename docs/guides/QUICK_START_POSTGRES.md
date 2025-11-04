# Quick Start: Unlimited Context with PostgreSQL

Get your multi-agent team running with unlimited context in 5 minutes!

---

## 🚀 Step 1: Install PostgreSQL (2 minutes)

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from: https://www.postgresql.org/download/windows/

---

## 🗄️ Step 2: Create Database (30 seconds)

```bash
createdb destiny_team
```

---

## 📦 Step 3: Install Dependencies (1 minute)

```bash
cd /Users/artur/coursor-agents-destiny-folder
pip install psycopg2-binary
```

---

## 🎯 Step 4: Initialize Schema (30 seconds)

```bash
python postgres_context_store.py
```

This creates all the necessary tables.

---

## ✅ Step 5: Test It! (1 minute)

```bash
python test_postgres_context.py
```

This runs 5 tests to verify everything works:
- ✓ Basic message storage
- ✓ Intelligent context retrieval
- ✓ Per-agent knowledge bases
- ✓ Full team integration
- ✓ Cross-session persistence

---

## 🎬 Step 6: Use It in Your Code

### Simple Example

```python
from postgres_integration import DestinyTeamWithPostgres

# Initialize team with PostgreSQL backend
team = DestinyTeamWithPostgres(
    postgres_connection_string="dbname=destiny_team user=artur host=localhost"
)

# Start a project
project_id = team.start_project(
    project_name="My Awesome App",
    description="A revolutionary task management application"
)

# Agents communicate (stored in PostgreSQL)
pm = team.agents['pm']
pm.send_message(
    recipient=None,
    message_type=MessageType.REQUEST,
    content="Let's gather requirements for the core features"
)

# Architect thinks with UNLIMITED context
architect = team.agents['architect']
response = architect.think(
    prompt="Design the system architecture for this app",
    project_state=project_state
)

print(response)

# Close connection
team.close()
```

### Resume a Project Later

```python
# Days/weeks later, resume the same project
team = DestinyTeamWithPostgres(
    postgres_connection_string="dbname=destiny_team user=artur host=localhost",
    project_id=project_id  # Same project ID
)

# All context from previous session is available!
history = team.search_project_history("requirements")
print(f"Found {len(history)} messages about requirements from earlier sessions")
```

---

## 💡 Key Concepts

### Unlimited Storage
All agent communications are stored in PostgreSQL - no limits!

### Smart Retrieval
When an agent thinks, the system:
1. Extracts keywords from the question
2. Scores ALL messages for relevance
3. Retrieves top 20 most relevant
4. Builds context from relevant messages only
5. Stays within token limits

### Example:
```python
# Agent asks: "What database should we use?"

# System searches through 10,000+ messages and finds:
# - "PostgreSQL for ACID compliance" (relevance: 0.89)
# - "Need strong transactions" (relevance: 0.72)
# - "Considered MongoDB but chose SQL" (relevance: 0.68)

# NOT included:
# - "Frontend will use React" (relevance: 0.12)
# - "Meeting at 2pm tomorrow" (relevance: 0.05)
```

### Per-Agent Knowledge
Each agent maintains their own knowledge base:

```python
# Architect stores a decision
architect.add_to_context(
    key="architecture_choice",
    value={"type": "microservices", "reason": "scalability"},
    importance=0.9
)

# Later (even in new session), architect remembers
context = architect.context_store.get_agent_context(
    agent_name="Katarzyna Wiśniewska",
    project_id=project_id
)

print(context['architecture_choice'])
# Output: {"type": "microservices", "reason": "scalability"}
```

---

## 📊 What You Can Do

### Search Project History
```python
results = team.search_project_history("security authentication")
print(f"Found {len(results)} messages about security")
```

### Get Project Statistics
```python
summary = team.get_project_summary()
print(f"Total messages: {summary['project_stats']['total_messages']}")
print(f"Active agents: {summary['project_stats']['active_agents']}")
print(f"Debates: {summary['project_stats']['debates']}")
```

### View All Debates
```python
debates = team.get_all_debates()
for debate in debates:
    print(f"{debate.sender}: {debate.content}")
```

### Get Agent Activity
```python
stats = team.context_store.get_agent_activity_summary(
    project_id=project_id,
    agent_name="Katarzyna Wiśniewska"
)
print(f"Messages sent: {stats['messages_sent']}")
print(f"Agents contacted: {stats['agents_contacted']}")
```

---

## 🎯 Real-World Usage Pattern

```python
# === WEEK 1 ===
team = DestinyTeamWithPostgres("dbname=destiny_team user=artur host=localhost")
project_id = team.start_project("E-commerce Platform", "Online store with payments")

# Requirements phase (100 messages)
pm.send_message(None, MessageType.REQUEST, "What are core features?")
# ... more discussion ...

team.close()

# === WEEK 2 ===
team = DestinyTeamWithPostgres("...", project_id=project_id)

# Architecture phase (300 messages)
architect.think("Design system architecture")
# Agent retrieves relevant messages from Week 1 automatically
# ... more work ...

team.close()

# === MONTH 6 ===
team = DestinyTeamWithPostgres("...", project_id=project_id)

# Implementation phase (5,000+ messages)
developer.think("Implement payment processing")
# Agent retrieves relevant context from ALL previous months
# Even though there are 5,000+ messages, developer gets the top 20 most relevant

team.close()
```

---

## 🔧 Troubleshooting

### Can't connect to PostgreSQL?
```bash
# Check if running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Start if not running
brew services start postgresql@15
```

### Database doesn't exist?
```bash
createdb destiny_team
```

### Permission denied?
Edit `pg_hba.conf`:
```
# Change:
host  all  all  127.0.0.1/32  md5

# To:
host  all  all  127.0.0.1/32  trust
```

Then restart PostgreSQL:
```bash
brew services restart postgresql@15
```

---

## 📚 Next Steps

1. **Read the full documentation:**
   - `POSTGRES_SETUP_GUIDE.md` - Complete setup guide
   - `UNLIMITED_CONTEXT_ARCHITECTURE.md` - How it works
   - `postgres_context_store.py` - Core storage system
   - `postgres_integration.py` - Agent integration

2. **Try advanced features:**
   - Vector embeddings for semantic search
   - Context summarization
   - Custom relevance scoring

3. **Monitor your database:**
```bash
# Connect to database
psql destiny_team

# Check message count
SELECT COUNT(*) FROM messages;

# Check storage size
SELECT pg_size_pretty(pg_database_size('destiny_team'));

# View recent messages
SELECT sender, content FROM messages ORDER BY timestamp DESC LIMIT 10;
```

---

## 🎉 You're Done!

Your agents now have **unlimited context**! They can:
- ✅ Store unlimited conversation history
- ✅ Retrieve relevant context intelligently
- ✅ Maintain personal knowledge bases
- ✅ Resume projects across sessions
- ✅ Search entire project history
- ✅ Work on projects for years without forgetting

**Start building amazing multi-agent projects!** 🚀
