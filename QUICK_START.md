# 🚀 QUICK START - Destiny Analytical System

Get up and running in 5 minutes!

---

## ✅ Prerequisites

```bash
# 1. LMStudio running on 192.168.200.226:1234
#    - Model: openai/gpt-oss-20b OR gemma-3-12b-it
#    - Embeddings: e5-large AND jina

# 2. Python 3.10+
python3 --version

# 3. (Optional) PostgreSQL for persistence
```

---

## 🎯 Run Your First Analysis

### Option 1: Quick Test (No Installation)

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Test LLM
python3 src/llm/lmstudio_client.py

# Test embeddings
python3 src/data/embedding_pipeline.py

# Test agents
python3 src/agents/base_agent.py
```

### Option 2: Full Integration Test

```bash
# Run complete integration test suite
python3 tests/integration/test_end_to_end.py
```

**Expected Result:**
```
🎉 ALL TESTS PASSED! SYSTEM IS OPERATIONAL! 🎉
```

---

## 📝 Your First Analysis Script

Create `my_analysis.py`:

```python
from src.agents.orchestrator import MultiAgentOrchestrator

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator()

# Your documents
documents = [
    {
        "id": "doc_001",
        "content": """
        Q4 2024 Financial Report:
        Revenue: $5M (up 25% YoY)
        Profit margin: 32%
        Cash position: $10M
        """,
        "type": "financial"
    }
]

# Run analysis
analysis = orchestrator.process_case(
    case_id="my_first_case",
    title="My First Analysis",
    documents=documents,
    analysis_types=["financial", "risk"]
)

# View results
print(f"Analysis complete in {analysis.total_time:.2f}s")
print(f"Confidence: {analysis.average_confidence:.2f}")
print(f"\n{analysis.synthesis}")
```

Run it:
```bash
python3 my_analysis.py
```

---

## 🔧 What Each Component Does

### LLM Client (`src/llm/lmstudio_client.py`)
- Connects to your local LLM
- Handles chat completions
- Tracks tokens & performance

### Embedding Pipeline (`src/data/embedding_pipeline.py`)
- Generates embeddings
- Auto-routes to best model
- Chunks documents smartly

### Agents (`src/agents/base_agent.py`)
- Financial analysis
- Legal analysis
- Risk analysis
- Context-aware processing

### Orchestrator (`src/agents/orchestrator.py`)
- Coordinates all agents
- Manages workflow
- Synthesizes results

---

## 📊 Check System Health

```python
from src.llm.lmstudio_client import LMStudioLLMClient

client = LMStudioLLMClient()
healthy = client.health_check()
print(f"System: {'✅ Healthy' if healthy else '❌ Down'}")
```

---

## 🎯 Common Use Cases

### 1. Single Document Analysis
```python
orchestrator.process_case(
    case_id="single_doc",
    title="Quick Analysis",
    documents=[{"id": "doc1", "content": "..."}],
    analysis_types=["financial"]
)
```

### 2. Multi-Document Deep Dive
```python
orchestrator.process_case(
    case_id="deep_dive",
    title="Comprehensive Analysis",
    documents=[doc1, doc2, doc3],
    analysis_types=["financial", "legal", "risk"]
)
```

### 3. Semantic Search (when DB is set up)
```python
results = orchestrator.semantic_search(
    query="What were the revenue trends?",
    case_id="my_case",
    limit=5
)
```

---

## ⚙️ Configuration

### Change LLM Model
```python
from src.llm.lmstudio_client import LMStudioLLMClient

# Use fast model
client = LMStudioLLMClient(model="gemma-3-12b-it")

# Use quality model
client = LMStudioLLMClient(model="openai/gpt-oss-20b")
```

### Change Embedding Model
```python
from src.data.embedding_pipeline import DualEmbeddingSystem

embedder = DualEmbeddingSystem()

# Force specific model
result = embedder.embed("text", force_model="jina")
```

---

## 📈 Performance Expectations

```
Single Agent:     3-10 seconds
Multi-Agent (3):  15-25 seconds
Embeddings:       20-40ms each
Throughput:       40-50 embeddings/sec
```

---

## 🐛 Troubleshooting

### LLM Not Responding
```bash
# Check LMStudio is running
curl http://192.168.200.226:1234/v1/models

# Should return list of models
```

### "No module named 'psycopg2'"
```bash
# PostgreSQL client (optional, for persistence)
pip3 install psycopg2-binary --break-system-packages
```

### Slow Performance
```python
# Use fast model
client = LMStudioLLMClient(model="gemma-3-12b-it")

# Reduce max_tokens
client = LMStudioLLMClient(max_tokens=1000)
```

---

## 🎓 Next Steps

1. ✅ Run integration tests
2. ✅ Try example analysis
3. 📊 Set up PostgreSQL (optional)
4. 📚 Read full documentation
5. 🚀 Build your own agents

---

## 📚 More Resources

- **Full README:** `README.md`
- **Architecture:** `docs/architecture/`
- **API Docs:** `docs/api/`
- **Test Suite:** `tests/integration/`

---

## 💬 Quick Commands

```bash
# Test everything
python3 tests/integration/test_end_to_end.py

# Test LLM only
python3 src/llm/lmstudio_client.py

# Test embeddings only
python3 src/data/embedding_pipeline.py

# Test agents only
python3 src/agents/base_agent.py

# Full orchestration test
python3 src/agents/orchestrator.py

# Count lines of code
find src -name "*.py" -exec wc -l {} + | tail -1
```

---

## ✅ System Status

```
✅ LLM Client: WORKING
✅ Embeddings: WORKING
✅ Agents: WORKING
✅ Orchestrator: WORKING
✅ Tests: 5/5 PASSING
⚠️ Database: OPTIONAL (ready when needed)

Status: FULLY OPERATIONAL 🚀
```

---

*"From zero to analysis in 5 minutes!"*

**Happy analyzing!** 🎉
