# 🚀 Destiny Analytical System - Hybrid Multi-Agent Platform

**Enterprise-grade analytical system combining local LLM (privacy) with Claude supervision (quality)**

---

## 🎯 Overview

Hybrid multi-agent system for analyzing complex cases (financial, legal, investigative):
- **100+ documents** per case
- **4M+ sentences** processing capability
- **Multi-agent analysis** (financial, legal, risk, etc.)
- **Progressive autonomy** (supervised → autonomous)
- **Local LLM** (privacy) + **Claude supervision** (quality)

---

## ✅ Current Status

**Phase:** Week 1 - Foundation ✅  
**Progress:** Core components implemented and tested  
**Date:** 2025-11-05

### Completed:
- ✅ LMStudio LLM client (gpt-oss-20b + gemma-3-12b-it)
- ✅ Dual embedding pipeline (E5-Large + Jina)
- ✅ Base agent framework (sequential multi-agent)
- ✅ Database schema (PostgreSQL + pgvector)
- ✅ Docker infrastructure (4-database stack)

### Performance:
- LLM: ~5s per analysis
- Embeddings: 20-30ms, ~40-50/sec throughput
- Agents: Sequential processing with context

---

## 🏗️ Architecture

```
USER REQUEST
     ↓
┌────────────────┐
│ Local Agents   │ ← gpt-oss-20b (44k context)
│ Sequential     │   Financial, Legal, Risk
└────────┬───────┘   Privacy-first
         │
         │ Work completed
         ↓
┌────────────────┐
│ Claude Review  │ ← Quality supervision (200k context)
│ (Optional)     │   Spot-checks & guidance
└────────┬───────┘
         │
         ↓
    DELIVERED
```

### 4-Database Stack:
- **PostgreSQL + pgvector**: Embeddings & structured data
- **Elasticsearch**: Document storage & full-text search
- **Qdrant**: Scalable vector search
- **Neo4j**: Graph analysis (financial flows, relationships)

---

## 🚀 Quick Start

### Prerequisites:
```bash
# LMStudio running on 192.168.200.226:1234
# Docker Desktop installed
# Python 3.10+
```

### 1. Start Infrastructure:
```bash
docker-compose up -d
```

### 2. Test LLM Client:
```bash
python3 src/llm/lmstudio_client.py
```

### 3. Test Embedding Pipeline:
```bash
python3 src/data/embedding_pipeline.py
```

### 4. Test Agents:
```bash
python3 src/agents/base_agent.py
```

---

## 📦 Components

### 🤖 AI & Agent Layer
- **src/llm/lmstudio_client.py**: Local LLM client
  - Models: openai/gpt-oss-20b, gemma-3-12b-it
  - Context: 44k tokens
  - Performance: 3-10s per analysis

- **src/data/embedding_pipeline.py**: Dual embedding system
  - E5-Large: General text (1024d)
  - Jina: Financial/tabular (1024d)
  - Auto-routing, 40-50 embeddings/sec

- **src/agents/base_agent.py**: Multi-agent framework
  - FinancialAnalystAgent
  - LegalAnalystAgent
  - RiskAnalystAgent
  - Sequential + context passing

- **src/agents/orchestrator.py**: Multi-agent orchestrator
  - Coordinates all agents
  - Pipeline management
  - Result synthesis

### 💾 Database Layer (All 4 Ready!)
- **src/data/postgres_client.py**: PostgreSQL + pgvector
  - Small cases (<100k vectors)
  - Structured data
  - Task tracking

- **src/data/qdrant_client.py**: Qdrant vector DB
  - Large cases (100k+ vectors)
  - Scalable semantic search
  - Advanced filtering

- **src/data/elasticsearch_client.py**: Elasticsearch
  - Document storage
  - Full-text search
  - Metadata management

- **src/data/neo4j_client.py**: Neo4j graph DB
  - Entity relationships
  - Financial flows
  - Graph analysis

- **src/data/smart_router.py**: Smart database router
  - Automatic DB selection
  - Graceful fallbacks
  - Performance optimization

### 👨‍💼 Supervision Layer
- **src/supervision/claude_supervisor.py**: Claude supervision
  - Progressive autonomy (Supervised → Autonomous)
  - Quality grading
  - Post-execution review
  - 200k context advantage

### 🧪 Testing
- **tests/integration/test_end_to_end.py**: Integration tests
  - 5/5 tests passing
  - End-to-end validation
  - Performance benchmarks

### 🏗️ Infrastructure
- **docker-compose.yml**: Full 4-database stack
- **sql/init/**: Database schemas

---

## 💡 Usage Examples

### Simple LLM Analysis:
```python
from src.llm.lmstudio_client import LMStudioLLMClient

client = LMStudioLLMClient()
response = client.simple_prompt("Analyze this: Revenue up 23% to $4.2M")
print(response)
```

### Document Embedding:
```python
from src.data.embedding_pipeline import DocumentEmbeddingPipeline

pipeline = DocumentEmbeddingPipeline()
records = pipeline.process_document(
    document="Your document text...",
    document_id="doc_001",
    document_type="financial"
)
```

### Multi-Agent Analysis:
```python
from src.agents.base_agent import FinancialAnalystAgent, Task

agent = FinancialAnalystAgent()
task = Task(
    task_id="task_001",
    title="Q4 Analysis",
    description="Analyze Q4 performance",
    data={"revenue": "$4.2M", "growth": "23%"}
)

result = agent.execute(task)
print(result.output['summary'])
```

---

## 🎯 Next Steps (Week 1)

- [ ] PostgreSQL connection & storage
- [ ] Semantic search implementation
- [ ] Multi-agent orchestration
- [ ] End-to-end pipeline test (10 documents)
- [ ] Integration tests

---

## 📊 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Embeddings/sec | 40+ | 40-50 ✅ |
| LLM response | <10s | ~5s ✅ |
| Context window | 44k | 44k ✅ |
| Document processing | 100/hour | TBD |

---

## 🔧 Configuration

### LMStudio Server:
```
Host: 192.168.200.226
Port: 1234
Models: openai/gpt-oss-20b, gemma-3-12b-it
Embeddings: e5-large, jina
```

### Database (Docker):
```
PostgreSQL: localhost:5432
Elasticsearch: localhost:9200
Qdrant: localhost:6333
Neo4j: localhost:7474
```

---

## 🏆 Team

- **Aleksander Nowak**: Orchestrator & Supervisor
- **Tomasz Zieliński**: Core Development
- **Paweł Kowalski**: Data Engineering
- **Piotr Szymański**: DevOps
- **Anna Nowakowska**: QA
- **Katarzyna Wiśniewska**: Architecture
- **Dr. Joanna Wójcik**: Data Science
- **Dr. Helena Kowalczyk**: Documentation
- **Michał Dąbrowski**: Security
- **Magdalena Kowalska**: Product

---

## 📚 Documentation

- [Architecture](docs/architecture/)
- [Setup Guide](docs/guides/)
- [API Reference](docs/api/)
- [Deployment Plan](docs/plans/)

---

## 📈 Progress

**Week 1/3**: Foundation ✅ (Day 1 complete)  
**Week 2/3**: Multi-agent system  
**Week 3/3**: Production polish

---

*"Making the impossible merely difficult" - Destiny Team* 🚀
