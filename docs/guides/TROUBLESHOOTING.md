# 🔧 Troubleshooting Guide - Helena Auto-Execution System

**Common issues and their solutions**

---

## 📋 Table of Contents

1. [Watcher Issues](#watcher-issues)
2. [Qdrant Issues](#qdrant-issues)
3. [Database Connection Issues](#database-connection-issues)
4. [Environment Issues](#environment-issues)
5. [Performance Issues](#performance-issues)
6. [Common Error Messages](#common-error-messages)

---

## 🔍 Watcher Issues

### Watcher Not Starting

**Symptoms:**
- `./start_watcher_conda.sh` runs but no process visible
- No log output in `logs/watcher.log`

**Diagnosis:**
```bash
# Check if process is running
ps aux | grep realtime_md_watcher

# Check logs for errors
cat logs/watcher.log
cat logs/watcher_error.log
```

**Solutions:**

1. **Conda environment not activated:**
```bash
conda activate team
./start_watcher_conda.sh
```

2. **Missing watchdog package:**
```bash
conda activate team
conda install watchdog
```

3. **Permission issues:**
```bash
chmod +x start_watcher_conda.sh
chmod +x scripts/realtime_md_watcher.py
```

4. **Port/file already in use:**
```bash
# Kill existing watcher
pkill -f realtime_md_watcher

# Wait 2 seconds
sleep 2

# Restart
./start_watcher_conda.sh
```

---

### Files Not Being Detected

**Symptoms:**
- Save a `.md` file but watcher doesn't react
- No queue files created in `helena_tasks/realtime_queue/`

**Diagnosis:**
```bash
# Check if watcher is running
ps aux | grep realtime_md_watcher

# Check recent log output
tail -20 logs/watcher.log

# Manually test file detection
echo "# Test" > docs/status/test_detection.md
sleep 2
tail -10 logs/watcher.log
```

**Solutions:**

1. **File saved outside monitored directory:**
   - **Problem:** Only `docs/` directory is monitored
   - **Solution:** Save files in `docs/` subdirectories

2. **File too small (<200 bytes):**
```bash
# Check file size
ls -lh docs/your_file.md

# Add more content
echo "

## More Content

This makes the file larger than 200 bytes.

" >> docs/your_file.md
```

3. **Filename contains exclusion keywords:**
   - **Problem:** Files with "test", "demo", "example" in name are excluded
   - **Solution:** Rename file without these keywords

4. **Watcher crashed:**
```bash
# Check for crash in logs
tail -50 logs/watcher.log | grep -i error

# Restart watcher
pkill -f realtime_md_watcher
./start_watcher_conda.sh
```

---

### Watcher Crashes Repeatedly

**Symptoms:**
- Watcher starts but stops after few seconds
- Error messages in logs

**Diagnosis:**
```bash
# Check error log
cat logs/watcher_error.log

# Run watcher in foreground for debugging
conda run -n team python scripts/realtime_md_watcher.py
```

**Solutions:**

1. **Module import errors:**
```bash
conda activate team
conda install watchdog qdrant-client psycopg2-binary neo4j redis
```

2. **Path errors:**
   - Check that PROJECT_ROOT in scripts matches your actual path
   - Default: `/Users/artur/coursor-agents-destiny-folder`

3. **Permission errors:**
```bash
# Fix permissions
chmod -R u+w helena_tasks/
chmod -R u+w logs/
chmod -R u+w qdrant_pending/
```

---

## 🗄️ Qdrant Issues

### Documents Not Appearing in Dashboard

**Symptoms:**
- Watcher detects file
- Processing completes
- But document not visible in Qdrant dashboard

**Diagnosis:**
```bash
# Check Qdrant is running
curl -s http://localhost:6333/collections/destiny-team-framework-master | python3 -m json.tool

# Check current point count
curl -s http://localhost:6333/collections/destiny-team-framework-master \
  | python3 -c "import json,sys; print('Points:', json.load(sys.stdin)['result']['points_count'])"

# Check for pending documents
ls -l qdrant_pending/doc_*.json
```

**Solutions:**

1. **Vector dimension mismatch:**
```bash
# Verify collection uses 1024 dimensions
curl -s http://localhost:6333/collections/destiny-team-framework-master \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['config']['params']['vectors'])"

# Should output: {'size': 1024, 'distance': 'Cosine'}

# If mismatch, check helena_realtime_processor_simple.py
grep -n "1024" scripts/helena_realtime_processor_simple.py
```

2. **qdrant-client not available:**
```bash
conda activate team
conda install qdrant-client

# Verify
python -c "from qdrant_client import QdrantClient; print('✅ OK')"
```

3. **Indexing failed silently:**
```bash
# Check processor logs in watcher.log
grep "Qdrant" logs/watcher.log | tail -10

# Look for "✅ INDEXED" vs "⚠️ Indexing failed"
```

4. **Pending documents not indexed:**
```bash
# Manually batch index
conda run -n team python scripts/index_all_pending_qdrant.py
```

---

### "Dimension Mismatch" Error

**Symptoms:**
```
Error: Vector dimension mismatch!
Expected: 1024, Got: 384
```

**Diagnosis:**
```bash
# Check vector generation code
grep -A 10 "generate_embedding" scripts/helena_realtime_processor_simple.py
```

**Solution:**

**CRITICAL:** Helena MUST use 1024 dimensions!

```python
# ✅ CORRECT - 1024 dimensions
hash_obj = hashlib.sha512(text.encode())
hash_bytes = hash_obj.digest()

embedding = []
for i in range(1024):
    byte_val = hash_bytes[i % len(hash_bytes)]
    embedding.append((byte_val / 127.5) - 1.0)

# len(embedding) == 1024 ✅
```

See [HELENA_VECTOR_1024_REQUIREMENT.md](../protocols/HELENA_VECTOR_1024_REQUIREMENT.md)

---

## 🔌 Database Connection Issues

### PostgreSQL Connection Failed

**Symptoms:**
```
⚠️  DB execution failed: could not connect to server
```

**Diagnosis:**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U user -d destiny_team -c "SELECT 1;"
```

**Solutions:**

1. **Container not running:**
```bash
docker start hercules-postgres
# or
docker start sms-postgres
```

2. **Wrong credentials in config:**
   - Check `DB_CONFIG['postgres']` in `helena_realtime_processor_simple.py`
   - Default: `user:password@localhost:5432/destiny_team`

3. **Database doesn't exist:**
```bash
# Create database
psql -h localhost -U user -c "CREATE DATABASE destiny_team;"
```

4. **Table 'documents' doesn't exist:**
   - SQL file will be generated as backup
   - Create table manually or run migration scripts

**Graceful Fallback:** Even if PostgreSQL is unavailable, SQL files are saved in `sql/realtime_updates/`

---

### Neo4j Connection Failed

**Symptoms:**
```
⚠️  DB execution failed: ServiceUnavailable
```

**Diagnosis:**
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Test connection
curl http://localhost:7474
```

**Solutions:**

1. **Container not running:**
```bash
docker start sms-neo4j
```

2. **Wrong credentials:**
   - Check `DB_CONFIG['neo4j']` in processor
   - Default: `neo4j:password@bolt://localhost:7687`

3. **Cypher syntax error:**
   - Check generated Cypher files in `sql/realtime_updates/`
   - Look for single quote escaping issues

**Graceful Fallback:** Cypher files saved in `sql/realtime_updates/` for manual execution

---

### Redis Connection Failed

**Symptoms:**
```
⚠️  Execution failed: Connection refused
```

**Diagnosis:**
```bash
# Check if Redis is running
docker ps | grep redis

# Test connection
docker exec kg-redis redis-cli PING
# Should return: PONG
```

**Solutions:**

1. **Container not running:**
```bash
docker start kg-redis
```

2. **Wrong host/port:**
   - Check `DB_CONFIG['redis']` in processor
   - Default: `localhost:6379, db=0`

**Graceful Fallback:** Redis commands saved in `redis_pending/` for manual execution

---

## 🐍 Environment Issues

### "ModuleNotFoundError"

**Symptoms:**
```
ModuleNotFoundError: No module named 'qdrant_client'
ModuleNotFoundError: No module named 'watchdog'
```

**Diagnosis:**
```bash
# Check active environment
conda env list | grep '*'

# List installed packages
conda list | grep -E "qdrant|watchdog|psycopg2|neo4j|redis"
```

**Solutions:**

1. **Wrong conda environment:**
```bash
# Activate correct environment
conda activate team

# Verify
which python
# Should output: /opt/miniconda3/envs/team/bin/python
```

2. **Packages not installed:**
```bash
conda activate team
conda install watchdog qdrant-client psycopg2-binary neo4j redis
```

3. **Using system Python instead of conda:**
```bash
# Check watcher startup script
cat start_watcher_conda.sh

# Should use: conda run -n team python ...
```

---

### "ImportError: cannot import name..."

**Symptoms:**
```
ImportError: cannot import name 'PointStruct' from 'qdrant_client.models'
```

**Solution:**

**Version mismatch:**
```bash
conda activate team

# Update to compatible versions
conda install qdrant-client=1.15.1
conda install neo4j=6.0.2
conda install redis=7.0.1
```

---

## ⚡ Performance Issues

### Slow Processing (>30 seconds)

**Symptoms:**
- File detected quickly but processing takes long
- "Processing..." message in logs for extended time

**Diagnosis:**
```bash
# Check processor execution time in logs
grep "Total time:" logs/watcher.log | tail -5
```

**Solutions:**

1. **Large file content:**
   - Files >10MB may take longer
   - Consider splitting into smaller documents

2. **Database slow:**
```bash
# Check database container resources
docker stats --no-stream

# Increase memory/CPU if needed
```

3. **Network latency:**
   - Check localhost connections are not proxied
   - Verify no firewall blocking localhost

---

### High Memory Usage

**Symptoms:**
- Watcher process using >1GB RAM
- System slowdown

**Diagnosis:**
```bash
# Check memory usage
ps aux | grep realtime_md_watcher | awk '{print $4 "%", $6/1024 "MB"}'
```

**Solutions:**

1. **Too many pending documents:**
```bash
# Clear processed documents
mv helena_tasks/realtime_queue/*.json helena_tasks/processed/

# Batch index pending Qdrant
conda run -n team python scripts/index_all_pending_qdrant.py
```

2. **Memory leak:**
```bash
# Restart watcher daily via cron
0 4 * * * pkill -f realtime_md_watcher && sleep 5 && /path/to/start_watcher_conda.sh
```

---

## 🚨 Common Error Messages

### "relation 'documents' does not exist"

**Meaning:** PostgreSQL table not created

**Solution:**
```sql
-- Create table manually
CREATE TABLE IF NOT EXISTS documents (
    file_path TEXT PRIMARY KEY,
    document_type TEXT,
    title TEXT,
    content_preview TEXT,
    line_count INTEGER,
    created_at TIMESTAMP,
    indexed_at TIMESTAMP,
    source TEXT
);
```

Or use generated SQL files from `sql/realtime_updates/`

---

### "ServiceUnavailable: Failed to establish connection"

**Meaning:** Neo4j not accessible

**Solution:**
```bash
# Start Neo4j
docker start sms-neo4j

# Wait for startup
sleep 10

# Verify
curl http://localhost:7474
```

---

### "vector dimension mismatch"

**Meaning:** Vector is not 1024 dimensions

**Solution:** See [Vector Dimension Requirement](#vector-dimension-mismatch-error)

---

### "Not significant enough for database propagation"

**Meaning:** File too small or contains excluded keywords

**Solution:**
- Add more content (>200 bytes)
- Avoid "test", "demo", "example" in filename
- Check logs for specific reason:
```bash
grep "Not significant" logs/watcher.log | tail -5
```

---

## 📞 Quick Diagnostic Commands

```bash
# System Status Check
echo "=== WATCHER STATUS ==="
ps aux | grep realtime_md_watcher | grep -v grep && echo "✅ Running" || echo "❌ Not running"

echo -e "\n=== CONDA ENVIRONMENT ==="
conda env list | grep team

echo -e "\n=== DATABASE CONTAINERS ==="
docker ps | grep -E "qdrant|postgres|neo4j|redis"

echo -e "\n=== QDRANT STATUS ==="
curl -s http://localhost:6333/collections/destiny-team-framework-master \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(f\"Points: {r['points_count']}, Vector size: {r['config']['params']['vectors']['size']}\")"

echo -e "\n=== RECENT LOGS ==="
tail -10 logs/watcher.log

echo -e "\n=== PENDING TASKS ==="
echo "Helena queue: $(ls helena_tasks/realtime_queue/*.json 2>/dev/null | wc -l)"
echo "Qdrant pending: $(ls qdrant_pending/doc_*.json 2>/dev/null | wc -l)"
```

---

## 🆘 Emergency Recovery

If nothing works:

```bash
# 1. Stop everything
pkill -f realtime_md_watcher

# 2. Clear queues
mkdir -p helena_tasks/emergency_backup
mv helena_tasks/realtime_queue/*.json helena_tasks/emergency_backup/ 2>/dev/null

# 3. Verify environment
conda activate team
conda install watchdog qdrant-client psycopg2-binary neo4j redis

# 4. Test databases
docker ps | grep -E "qdrant|postgres|neo4j|redis"

# 5. Restart clean
./start_watcher_conda.sh

# 6. Monitor logs
tail -f logs/watcher.log
```

---

## 📚 See Also

- [README.md](../../README.md) - Quick start guide
- [HELENA_VECTOR_1024_REQUIREMENT.md](../protocols/HELENA_VECTOR_1024_REQUIREMENT.md) - Vector requirements
- [AUTOMATIC_DATABASE_EXECUTION_PROTOCOL.md](../protocols/AUTOMATIC_DATABASE_EXECUTION_PROTOCOL.md) - Execution protocol

---

**Need more help?** Check the logs:
- `logs/watcher.log` - Main watcher log
- `logs/watcher_error.log` - Error output
- Helena task files in `helena_tasks/` - Processing details

---

*Built with resilience in mind. Every error has a solution!* 🔧
