# ⚡ Quick Start Guide - Get Running in 5 Minutes!

**Helena Auto-Execution System - Fastest Path to Success**

---

## 🎯 Goal

Get Helena automatically propagating your documents to all 4 databases in under 5 minutes!

---

## ✅ Prerequisites Checklist

Before starting, verify you have:

- [ ] macOS or Linux system
- [ ] Conda installed (`conda --version`)
- [ ] Conda environment named 'team' (`conda env list | grep team`)
- [ ] Docker running (`docker ps`)
- [ ] Databases running (Qdrant, PostgreSQL, Neo4j, Redis)

```bash
# Quick verification
docker ps | grep -E "qdrant|postgres|neo4j|redis" | wc -l
# Should output: 4 (or more)
```

---

## 🚀 5-Minute Setup

### Step 1: Navigate to Project (10 seconds)

```bash
cd /Users/artur/coursor-agents-destiny-folder
```

### Step 2: Activate Environment (5 seconds)

```bash
conda activate team
```

### Step 3: Verify Dependencies (20 seconds)

```bash
# Quick check - should all return ✅
python -c "import watchdog; print('✅ watchdog')"
python -c "from qdrant_client import QdrantClient; print('✅ qdrant-client')"
python -c "import psycopg2; print('✅ psycopg2')"
python -c "from neo4j import GraphDatabase; print('✅ neo4j')"
python -c "import redis; print('✅ redis')"
```

**If any fail:**
```bash
conda install watchdog qdrant-client psycopg2-binary neo4j redis
```

### Step 4: Start the System (5 seconds)

```bash
./start_watcher_conda.sh
```

**Expected output:**
```
✅ Watcher started with conda team environment (PID: XXXXX)
📝 Log: tail -f logs/watcher.log
```

### Step 5: Verify It's Running (10 seconds)

```bash
# Check process
ps aux | grep realtime_md_watcher | grep -v grep

# Check logs
tail -20 logs/watcher.log
```

**Expected in logs:**
```
🚀 REAL-TIME MARKDOWN WATCHER
📁 Watching: /Users/artur/coursor-agents-destiny-folder
📝 Extensions: .md
✨ How it works: ...
```

---

## 🧪 Test It! (2 minutes)

### Create Test Document

```bash
echo "# My First Auto-Propagated Document

**Created:** $(date)

This document tests Helena's auto-propagation system!

## What Should Happen

Within 10 seconds:
- ✅ Watcher detects this file
- ✅ Helena processes it
- ✅ Document indexed to Qdrant
- ✅ Metadata saved to PostgreSQL
- ✅ Graph node created in Neo4j
- ✅ Cache entry added to Redis

## Verification

Check Qdrant dashboard:
http://localhost:6333/dashboard

Search for this document title!

" > docs/status/first_test_$(date +%s).md

echo "✅ Test document created!"
```

### Watch the Magic (10 seconds)

```bash
# Watch logs in real-time
tail -f logs/watcher.log

# You should see:
# 🔔 DETECTED: docs/status/first_test_...
# ✅ Queued for Helena: realtime_...
# 🤖 Processing: realtime_...
# ✅ Helena processed successfully!
#    📊 4/4 databases updated
```

**Press Ctrl+C to stop watching logs**

### Verify in Qdrant (30 seconds)

```bash
# Open dashboard
open http://localhost:6333/dashboard#/collections/destiny-team-framework-master

# Or check via CLI
curl -s -X POST "http://localhost:6333/collections/destiny-team-framework-master/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1, "with_payload": true, "with_vector": false}' \
  | python3 -m json.tool | head -30
```

**Look for:** Your document with full content in the payload!

---

## ✅ Success Verification

Your system is working if:

- [x] Watcher process is running (`ps aux | grep realtime_md_watcher`)
- [x] Test document was detected (in logs)
- [x] Processing completed successfully (✅ in logs)
- [x] Document visible in Qdrant dashboard
- [x] Point count increased by 1

---

## 🎯 What Happens Automatically Now

Every time you save a `.md` file in `docs/`:

```
1. Save file (YOU)
   ↓ <1 second
2. Watcher detects (AUTOMATIC)
   ↓
3. Helena processes (AUTOMATIC)
   ↓
4. Propagates to all DBs:
   ├─ Qdrant ✅
   ├─ PostgreSQL ✅
   ├─ Neo4j ✅
   └─ Redis ✅
   ↓
5. Dashboard updated (AUTOMATIC)
   ↓
DONE! 🎉
```

**Zero manual intervention needed!**

---

## 📁 Where to Save Documents

Save your `.md` files in these directories:

```
docs/
├── protocols/       # Protocols, procedures, requirements
├── status/          # Status reports, summaries
├── guides/          # User guides, tutorials
├── team/            # Team documentation
├── architecture/    # System design docs
├── analysis/        # Analysis, assessments
├── general/         # General docs
└── tasks/           # Task definitions
```

**Watcher monitors ALL these directories!**

---

## 🛑 How to Stop

```bash
# Stop the watcher
pkill -f realtime_md_watcher

# Verify it stopped
ps aux | grep realtime_md_watcher
# (should return nothing)
```

---

## 🔄 How to Restart

```bash
# Stop if running
pkill -f realtime_md_watcher

# Wait 2 seconds
sleep 2

# Start fresh
./start_watcher_conda.sh
```

---

## 📊 Monitor Your System

### Check Watcher Status

```bash
ps aux | grep realtime_md_watcher | grep -v grep && echo "✅ Running" || echo "❌ Stopped"
```

### View Real-Time Logs

```bash
tail -f logs/watcher.log
```

### Check Qdrant Stats

```bash
curl -s http://localhost:6333/collections/destiny-team-framework-master \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(f\"Points: {r['points_count']}\")"
```

### Check Processing Queue

```bash
echo "Pending: $(ls helena_tasks/realtime_queue/*.json 2>/dev/null | wc -l)"
echo "Processed: $(ls helena_tasks/processed/*.json 2>/dev/null | wc -l)"
```

---

## 🐛 Quick Troubleshooting

### Watcher Won't Start

```bash
# 1. Activate conda
conda activate team

# 2. Check dependencies
conda install watchdog qdrant-client psycopg2-binary neo4j redis

# 3. Make executable
chmod +x start_watcher_conda.sh

# 4. Try again
./start_watcher_conda.sh
```

### Files Not Detected

```bash
# 1. Verify watcher is running
ps aux | grep realtime_md_watcher

# 2. Check logs for errors
tail -50 logs/watcher.log

# 3. Ensure file is in docs/
ls -l docs/status/your_file.md

# 4. Check file size (must be >200 bytes)
ls -lh docs/status/your_file.md
```

### Not Appearing in Qdrant

```bash
# 1. Check Qdrant is running
curl http://localhost:6333/collections

# 2. Manually batch index
conda run -n team python scripts/index_all_pending_qdrant.py

# 3. Check dashboard
open http://localhost:6333/dashboard
```

**More help:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎓 Next Steps

Now that your system is running:

1. **Create Real Documents**
   - Save your actual documentation in `docs/`
   - Watch them auto-propagate!

2. **Explore the Dashboard**
   - http://localhost:6333/dashboard
   - Search your documents
   - View payloads with full content

3. **Check Other Databases**
   - PostgreSQL: `psql -d destiny_team`
   - Neo4j: http://localhost:7474
   - Redis: `docker exec kg-redis redis-cli`

4. **Read Documentation**
   - [README.md](../../README.md) - Complete guide
   - [HELENA_VECTOR_1024_REQUIREMENT.md](../protocols/HELENA_VECTOR_1024_REQUIREMENT.md) - Critical protocol
   - [AUTOMATIC_DATABASE_EXECUTION_PROTOCOL.md](../protocols/AUTOMATIC_DATABASE_EXECUTION_PROTOCOL.md) - How it works

---

## ✨ Pro Tips

### 1. Use Meaningful Filenames
```bash
# Good
docs/protocols/data_retention_policy.md
docs/status/weekly_summary_2025_11_04.md

# Avoid
docs/test.md  # Will be ignored (contains "test")
docs/temp.md  # Too generic
```

### 2. Add Rich Content
```markdown
# Title

Clear introduction...

## Section 1

Detailed content...

## Section 2

More details...

## References

Links, sources...
```

Richer content = better semantic search!

### 3. Check Logs Regularly
```bash
# Add to your .zshrc or .bashrc
alias helena-status='tail -20 /Users/artur/coursor-agents-destiny-folder/logs/watcher.log'
alias helena-restart='pkill -f realtime_md_watcher && sleep 2 && /Users/artur/coursor-agents-destiny-folder/start_watcher_conda.sh'
```

### 4. Batch Operations
If you have many pending documents:
```bash
conda run -n team python scripts/index_all_pending_qdrant.py
```

---

## 🎉 You're All Set!

Your Helena Auto-Execution System is now:
- ✅ Running 24/7
- ✅ Monitoring `docs/` for changes
- ✅ Automatically propagating to all databases
- ✅ Ready for production use!

**Start creating documentation and watch the magic happen!** ✨

---

**Questions?** Check:
- [README.md](../../README.md) - Full documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [docs/INDEX.md](../INDEX.md) - All available docs

---

*From zero to auto-propagation in 5 minutes!* ⚡
