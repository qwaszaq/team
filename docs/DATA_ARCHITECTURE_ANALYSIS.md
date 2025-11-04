# Data Architecture Analysis - ES vs PostgreSQL Separation

## Question: Why is "no OSINT in PostgreSQL" a problem?

### Current State
- **Elasticsearch**: 375 PDF documents (OSINT financial reports)
- **PostgreSQL**: 0 messages with `osint` tag
- **Observation**: Data is NOT propagated from ES → PG

### Is this actually a problem? 🤔

## Architecture Philosophy: Separation of Concerns

### Option 1: ❌ Full Replication (NOT RECOMMENDED)
```
Elasticsearch (375 docs) → PostgreSQL (375 message records)
```

**Problems**:
- ❌ Data duplication (ES already has metadata)
- ❌ Scalability issue (375 docs * chunks = 1000s of PG rows)
- ❌ Different usage patterns (ES = search index, PG = operational store)
- ❌ Sync complexity (keep ES and PG in sync forever)
- ❌ Wrong tool for the job (PG not designed for full-text search)

### Option 2: ✅ Smart References (RECOMMENDED)
```
Elasticsearch (375 docs, source of truth)
      ↓ doc_id reference
PostgreSQL (lightweight reference table)
      ↓ entity links
Neo4j (document → agent/decision relationships)
```

**Benefits**:
- ✅ Single source of truth (ES for documents)
- ✅ Lightweight references in PG
- ✅ Proper separation of concerns
- ✅ Scalable (PG only stores metadata + references)
- ✅ Flexible queries via SearchOrchestrator

## What SHOULD be in PostgreSQL?

### 1. Document Reference Table
```sql
CREATE TABLE es_document_references (
    id SERIAL PRIMARY KEY,
    es_index TEXT NOT NULL,           -- 'osint_reports_pdf'
    es_doc_id TEXT NOT NULL UNIQUE,   -- Elasticsearch document ID
    doc_type TEXT,                    -- 'financial_report'
    issuer TEXT,                      -- 'Grupa Azoty'
    report_url TEXT,
    indexed_at TIMESTAMP,
    data_classification TEXT,         -- 'public', 'confidential'
    investigation_id TEXT,            -- 'telus_cpk_real_001'
    tags TEXT[]                       -- ['osint', 'financial', 'grupa-azoty']
);

CREATE INDEX idx_es_doc_refs_investigation ON es_document_references(investigation_id);
CREATE INDEX idx_es_doc_refs_tags ON es_document_references USING GIN(tags);
```

**Size**: ~375 rows (one per PDF) = lightweight!

### 2. Document Usage Log (Audit Trail)
```sql
CREATE TABLE es_document_usage_log (
    id SERIAL PRIMARY KEY,
    es_doc_id TEXT NOT NULL,
    accessed_by TEXT NOT NULL,        -- agent name
    access_timestamp TIMESTAMP DEFAULT NOW(),
    query_used TEXT,                  -- original search query
    access_purpose TEXT,              -- 'financial_analysis', 'osint_research'
    session_id TEXT
);
```

**Purpose**: Track who/when/why documents were accessed (GDPR compliance)

### 3. Agent Context (Links to ES Documents)
```sql
-- Extend existing agent_contexts table
INSERT INTO agent_contexts (agent_name, project_id, context_key, context_value)
VALUES (
    'Marcus',
    'investigation-telus_cpk_real_001',
    'osint_sources',
    '{"es_doc_ids": ["doc_123", "doc_456"], "count": 375, "issuer": "Grupa Azoty"}'::jsonb
);
```

**Purpose**: Agents know which ES documents are available for their investigation

## What SHOULD NOT be in PostgreSQL?

### ❌ Full Document Content
- Content is already in ES (optimized for full-text search)
- Duplication wastes space
- Wrong tool (PG not designed for this)

### ❌ Chunked Document Text
- Chunks belong in ES (with highlighting) and Qdrant (with embeddings)
- Don't replicate search index functionality in PG

### ❌ Binary PDFs
- PDFs stay in filesystem (`investigations/external/grupa_azoty_reports/`)
- ES indexes text + metadata
- PG only references

## Recommended Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     OSINT PDF Ingestion                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  1. Store PDF in filesystem          │
         │     investigations/external/...      │
         └──────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌────────────┐ ┌─────────────┐
    │ Elasticsearch│ │  Qdrant    │ │ PostgreSQL  │
    │              │ │            │ │             │
    │ Full text +  │ │ Embeddings │ │ Reference + │
    │ metadata     │ │ (chunks)   │ │ usage log   │
    │              │ │            │ │             │
    │ 375 docs     │ │ ~1500 pts  │ │ 375 refs    │
    └──────────────┘ └────────────┘ └─────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
                    ┌──────────────┐
                    │    Neo4j     │
                    │              │
                    │ doc→agent    │
                    │ doc→decision │
                    │ relationships│
                    └──────────────┘
```

## Query Patterns (How Agents Use Data)

### Pattern 1: Full-Text Search (Marcus finds financial reports)
```python
orchestrator = SearchOrchestrator()

# Query ES directly (no need for PG)
reports = orchestrator.full_text_search(
    query="przychody EBITDA",
    index="osint_reports_pdf"
)

# Log usage to PG
for report in reports:
    log_document_access(
        es_doc_id=report.id,
        accessed_by="Marcus",
        query="przychody EBITDA",
        purpose="financial_analysis"
    )
```

### Pattern 2: Check Available Sources (Elena checks what data exists)
```python
# Query PG for available sources
sql = """
    SELECT issuer, COUNT(*) as doc_count, ARRAY_AGG(DISTINCT tags) as all_tags
    FROM es_document_references
    WHERE investigation_id = %s
    GROUP BY issuer
"""
sources = orchestrator.structured_query(sql, ('telus_cpk_real_001',))
```

### Pattern 3: Audit Trail (Adrian checks who accessed data)
```python
# Query PG usage log
sql = """
    SELECT accessed_by, COUNT(*) as access_count, 
           ARRAY_AGG(DISTINCT access_purpose) as purposes
    FROM es_document_usage_log
    WHERE es_doc_id = %s AND access_timestamp >= NOW() - INTERVAL '90 days'
    GROUP BY accessed_by
"""
audit = orchestrator.structured_query(sql, ('doc_abc123',))
```

### Pattern 4: Hybrid Search (Helena combines sources)
```python
# SearchOrchestrator handles cross-layer queries automatically
results = orchestrator.hybrid_search(
    query="financial trends",
    sources=['es', 'qdrant', 'pg'],  # PG returns references + usage stats
    limit=10
)
```

## Conclusion: Not a Bug, It's a Feature! ✅

### The "gap" is actually **good architecture**:

1. **Elasticsearch** = Source of truth for OSINT documents
   - Optimized for full-text search
   - Handles 375 docs easily
   - Scales to millions of documents

2. **PostgreSQL** = References + Usage + Relationships
   - Lightweight reference table (375 rows)
   - Audit log (track access)
   - Agent contexts (which docs are available)

3. **Qdrant** = Semantic search
   - Embeddings of document chunks
   - Fast vector similarity

4. **Neo4j** = Knowledge graph
   - Links between documents and entities
   - Relationship queries

### What ACTUALLY needs to be done (Phase 2):

✅ **Add reference table to PG**
```sql
CREATE TABLE es_document_references (...);
```

✅ **Add usage logging**
```python
@log_access
def full_text_search(...):
    # logs to es_document_usage_log
```

✅ **Add Neo4j links**
```cypher
CREATE (doc:Document {es_doc_id: '...', issuer: 'Grupa Azoty'})
CREATE (agent:Agent {name: 'Marcus'})
CREATE (agent)-[:USED]->(doc)
```

✅ **Update agent contexts**
```python
# Helena tells agents: "You have 375 OSINT docs available"
context = {
    "osint_sources": {
        "es_index": "osint_reports_pdf",
        "count": 375,
        "issuers": ["Grupa Azoty"],
        "coverage": "2007-2025"
    }
}
```

## The Real "Problem" (if any)

The real issue is not "data not in PG" but rather:

### ❌ Agents don't know OSINT data exists
- No reference table → agents can't discover available sources
- No context → agents don't know to query ES

### ❌ No audit trail
- Can't track who accessed which documents
- GDPR compliance issue

### ❌ No links in knowledge graph
- Neo4j doesn't know documents exist
- Can't answer "which documents did Marcus use for this analysis?"

### ✅ Solution: Lightweight integration (not full replication)
- Create reference table (375 rows)
- Log usage (append-only, grows over time)
- Create Neo4j document nodes
- Update agent contexts

## Revised Phase 2 Priority

### HIGH Priority 🔴
1. ✅ Create `es_document_references` table in PG
2. ✅ Implement usage logging decorator
3. ✅ Sync references when PDFs are indexed
4. ✅ Update agent contexts with available sources

### MEDIUM Priority 🟡
5. Create Neo4j document nodes + relationships
6. Build "available sources" query API
7. Audit trail dashboard (Grafana/Kibana)

### Result
- Agents can **discover** OSINT data (via PG reference table)
- Agents can **search** OSINT data (via ES full-text)
- System can **audit** usage (via PG log)
- Graph can **relate** documents to entities (via Neo4j)
- No unnecessary data duplication ✅
