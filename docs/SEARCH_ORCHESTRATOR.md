# SearchOrchestrator - Unified Search Interface

## Overview

SearchOrchestrator provides a unified API for querying across all Destiny framework data layers:
- **Elasticsearch**: Full-text search, aggregations, time-series queries
- **Qdrant**: Semantic/vector search using embeddings
- **PostgreSQL**: Structured queries, metadata, relationships
- **Neo4j**: Graph queries, decision chains, knowledge graphs

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              SearchOrchestrator                          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Unified API                                    │    │
│  │  - full_text_search()                          │    │
│  │  - semantic_search()                           │    │
│  │  - structured_query()                          │    │
│  │  - graph_query()                               │    │
│  │  - hybrid_search()                             │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │    ES    │ │  Qdrant  │ │ Postgres │ │  Neo4j   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Installation & Setup

```python
from search_orchestrator import SearchOrchestrator

# Initialize with default settings
orchestrator = SearchOrchestrator()

# Or customize connection parameters
orchestrator = SearchOrchestrator(
    es_url="http://localhost:9200",
    es_user="elastic",
    es_password="changeme123",
    qdrant_url="http://localhost:6333",
    postgres_conn="dbname=destiny_team user=user password=password host=localhost",
    neo4j_container="sms-neo4j",
)
```

## Core Methods

### 1. Full-Text Search (Elasticsearch)

```python
# Basic search
results = orchestrator.full_text_search(
    query="financial performance",
    index="osint_reports_pdf",
    size=10,
    highlight=True
)

# With filters
results = orchestrator.full_text_search(
    query="revenue",
    index="osint_reports_pdf",
    filters={"issuer.keyword": "Grupa Azoty"}
)

# Results structure
for result in results:
    print(f"Score: {result.score}")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")
```

### 2. Semantic Search (Qdrant)

```python
# Semantic/vector search
results = orchestrator.semantic_search(
    query="sustainability and climate initiatives",
    collection="destiny-team-framework-master",
    limit=10
)

# Results are automatically ranked by semantic similarity
```

### 3. Structured Query (PostgreSQL)

```python
# Direct SQL query
results = orchestrator.structured_query(
    sql="SELECT * FROM messages WHERE sender = %s LIMIT %s",
    params=("Elena", 10)
)

# Get agent context
context = orchestrator.get_context_for_agent(
    agent_name="Marcus",
    project_id="destiny-team-framework-master",
    limit=5
)
```

### 4. Graph Query (Neo4j)

```python
# Cypher query
results = orchestrator.graph_query(
    cypher="MATCH (d:Decision) RETURN d.text, d.timestamp LIMIT 10"
)

# Get decision chain
decisions = orchestrator.get_decision_chain(
    decision_keyword="architecture",
    limit=5
)
```

### 5. Hybrid Search (Multi-Source)

```python
# Search across ES + Qdrant + Postgres
results = orchestrator.hybrid_search(
    query="system integration",
    sources=['es', 'qdrant', 'pg'],
    limit=10,
    rerank=True  # Re-rank by score
)

# Results are combined and optionally re-ranked
```

## Aggregations

```python
# Elasticsearch aggregations
aggs = orchestrator.aggregate_query(
    index="osint_reports_pdf",
    agg_field="issuer.keyword",
    agg_name="by_issuer",
    size=10
)

# Time-series aggregation example
aggs = orchestrator.aggregate_query(
    index="osint_reports_pdf",
    agg_field="downloaded_at",
    agg_name="by_month",
    agg_type="date_histogram"
)
```

## Health & Monitoring

```python
# Check backend health
health = orchestrator.health_check()
# Returns: {'elasticsearch': True, 'qdrant': True, 'postgres': True, 'neo4j': True}

# Get statistics
stats = orchestrator.get_stats()
# Returns: {'elasticsearch_docs': 375, 'qdrant_points': 409, 'postgres_messages': 108}
```

## Use Cases

### 1. Financial Analysis (Marcus)

```python
# Find revenue-related reports
reports = orchestrator.full_text_search(
    query="przychody zysk EBITDA",
    index="osint_reports_pdf",
    highlight=True
)

# Aggregate by year
yearly_stats = orchestrator.aggregate_query(
    index="osint_reports_pdf",
    agg_field="report_year",
    agg_name="by_year"
)
```

### 2. OSINT Research (Elena)

```python
# Semantic search for topics
results = orchestrator.semantic_search(
    query="corporate governance and compliance",
    limit=20
)

# Full-text search with filters
filtered_results = orchestrator.full_text_search(
    query="board decisions",
    filters={"data_classification": "public"}
)
```

### 3. Compliance Audit (Adrian)

```python
# Check data lineage
audit_trail = orchestrator.structured_query(
    sql="""
        SELECT es_doc_id, report_url, indexed_at, last_accessed
        FROM es_document_metadata
        WHERE indexed_at >= NOW() - INTERVAL '90 days'
        ORDER BY indexed_at DESC
    """
)
```

### 4. Knowledge Management (Helena)

```python
# Get agent context
context = orchestrator.get_context_for_agent("Helena")

# Check decision chain
decisions = orchestrator.get_decision_chain("data_propagation")

# Hybrid search for briefing
briefing_data = orchestrator.hybrid_search(
    query="recent system changes",
    sources=['es', 'qdrant', 'pg'],
    limit=20
)
```

## SearchResult Object

All search methods return `SearchResult` objects:

```python
@dataclass
class SearchResult:
    source: str          # 'elasticsearch', 'qdrant', 'postgres', 'neo4j'
    score: float         # Relevance score
    content: str         # Main content/excerpt
    metadata: Dict       # Full metadata
    id: str             # Document/point ID
    timestamp: str      # Optional timestamp
```

## Error Handling

SearchOrchestrator handles errors gracefully:

```python
# If Elasticsearch is down, returns empty list []
results = orchestrator.full_text_search("query")

# Health check shows which backends are available
health = orchestrator.health_check()
if not health['elasticsearch']:
    print("Elasticsearch unavailable, using fallback...")
    results = orchestrator.semantic_search("query")  # Use Qdrant instead
```

## Performance Considerations

### Query Optimization

1. **Use filters**: Reduce result set before scoring
2. **Limit size**: Only fetch what you need
3. **Disable highlighting**: If not needed for display
4. **Use aggregations**: Instead of fetching all documents

```python
# Optimized query
results = orchestrator.full_text_search(
    query="keyword",
    size=10,                          # Small size
    highlight=False,                  # Disable if not needed
    filters={"issuer.keyword": "..."}  # Pre-filter
)
```

### Caching

For repeated queries, consider caching results:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str):
    return orchestrator.full_text_search(query)
```

## Integration with Agents

### Agent Base Class Extension

```python
from search_orchestrator import SearchOrchestrator

class BaseAgent:
    def __init__(self):
        self.search = SearchOrchestrator()
    
    def gather_context(self, query: str):
        # Hybrid search for agent context
        return self.search.hybrid_search(
            query=query,
            sources=['es', 'qdrant', 'pg'],
            limit=10
        )
```

### Example: Financial Agent

```python
class FinancialAgent(BaseAgent):
    def analyze_company(self, company_name: str):
        # Get financial reports
        reports = self.search.full_text_search(
            query=f"{company_name} financial statements",
            index="osint_reports_pdf",
            filters={"issuer.keyword": company_name}
        )
        
        # Extract metrics (simplified)
        metrics = []
        for report in reports:
            # Parse content for financial figures
            metrics.append(self._extract_metrics(report))
        
        return metrics
```

## Roadmap

### Phase 1 (Weeks 1-2) ✅ COMPLETED
- [x] Core SearchOrchestrator class
- [x] ES, Qdrant, Postgres, Neo4j integration
- [x] Hybrid search
- [x] Health checks and monitoring
- [x] Usage examples

### Phase 2 (Weeks 3-4) - NEXT
- [ ] Advanced aggregations (date_histogram, nested)
- [ ] Query builder DSL
- [ ] Result caching layer
- [ ] Async/parallel queries
- [ ] Enhanced error handling and retry logic

### Phase 3 (Weeks 5-6)
- [ ] Agent-specific search profiles
- [ ] Query performance analytics
- [ ] Auto-suggest and query expansion
- [ ] Integration with Helena's briefing system
- [ ] Production deployment configuration

## Testing

Run tests:

```bash
# Basic functionality
python3 search_orchestrator.py

# Agent usage examples
python3 examples/search_orchestrator_usage.py

# Unit tests (coming in Phase 2)
pytest tests/test_search_orchestrator.py -v
```

## Troubleshooting

### Elasticsearch connection fails
```bash
# Check ES health
curl -u elastic:changeme123 http://localhost:9200/_cluster/health

# Restart ES container
docker restart hercules-elasticsearch
```

### Qdrant returns empty results
```bash
# Check collections
curl http://localhost:6333/collections

# Verify embeddings service is running (LM Studio on port 1234)
```

### PostgreSQL connection error
```bash
# Test connection
psql -h localhost -U user -d destiny_team -c "SELECT 1"
```

## Contributing

To extend SearchOrchestrator:

1. Add new method to class
2. Follow existing naming conventions
3. Return `SearchResult` objects for consistency
4. Add usage example
5. Update documentation

## License

Part of the Destiny Framework. See main project LICENSE.

## Support

For issues or questions:
- Check examples in `examples/search_orchestrator_usage.py`
- Review integration concept in `investigations/concepts/elasticsearch_integration_*.json`
- Contact: Knowledge Management Team (Helena)
