# 🏗️ DATA SEPARATION ARCHITECTURE
## Separacja Danych Projektowych od Danych Investigacyjnych

**Date:** 2025-11-04  
**Critical Requirement:** Dane projektowe NIE MOGĄ mieszać się z danymi roboczymi agentów  
**Status:** Design Complete - Ready for Implementation  

---

## 🎯 PROBLEM

**Current State:**
- Wszystkie dane w jednym folderze (`docs/`)
- Bazy danych używają tych samych kolekcji/schematów
- Ryzyko mieszania się danych projektowych z danymi investigacyjnymi
- Brak czystej separacji między "system knowledge" a "investigation data"

**Risk:**
- 🔴 Investigation data zanieczyszcza project knowledge base
- 🔴 Agenci mogą przeszukiwać project files zamiast investigation sources
- 🔴 Backup/recovery complications (wszystko razem)
- 🔴 Privacy concerns (investigation data może być wrażliwe)

---

## ✅ SOLUTION: Complete Data Separation

### **Principle:** Two Completely Separate Data Universes

```
UNIVERSE 1: PROJECT DATA
└── System knowledge, documentation, code, architecture
    └── For: System operation, development, team knowledge
    └── Storage: /docs/, project collections in DBs

UNIVERSE 2: INVESTIGATION DATA  
└── Research sources, findings, evidence, analysis
    └── For: Agent work, investigations, analysis
    └── Storage: /investigations/, investigation collections in DBs

NO MIXING. EVER.
```

---

## 📁 FILESYSTEM STRUCTURE

### **Current Structure (Mixed):**

```
/Users/artur/coursor-agents-destiny-folder/
├── docs/                    # 🔴 MIXED: Project + some investigation
├── helena_tasks/            # Project
├── logs/                    # Mixed
├── agents/                  # Project code
└── investigations/          # Investigation data (isolated but needs more structure)
```

### **New Structure (Separated):**

```
/Users/artur/coursor-agents-destiny-folder/

┌─────────────────────────────────────────────────────────────┐
│  PROJECT UNIVERSE (System Knowledge)                        │
└─────────────────────────────────────────────────────────────┘

├── docs/                              # PROJECT ONLY
│   ├── architecture/                  # System architecture
│   ├── protocols/                     # System protocols
│   ├── guides/                        # User guides
│   ├── team/                          # Team docs
│   ├── capabilities/                  # System capabilities
│   └── concepts/                      # Design concepts
│
├── agents/                            # Agent code (PROJECT)
├── orchestration/                     # Orchestration code (PROJECT)
├── scripts/                           # System scripts (PROJECT)
├── helena_tasks/                      # Helena queue (PROJECT)
│
└── logs/system/                       # SYSTEM LOGS ONLY
    ├── helena/
    ├── database/
    └── errors/

┌─────────────────────────────────────────────────────────────┐
│  INVESTIGATION UNIVERSE (Research Data)                     │
└─────────────────────────────────────────────────────────────┘

└── investigations/                    # INVESTIGATION DATA ONLY
    ├── active/                        # Current investigations
    │   ├── {investigation_id}/
    │   │   ├── sources/               # Collected sources
    │   │   │   ├── web/               # Web pages (archived)
    │   │   │   ├── documents/         # PDFs, docs
    │   │   │   ├── images/            # Images, screenshots
    │   │   │   └── data/              # CSV, JSON, datasets
    │   │   ├── analysis/              # Analysis files
    │   │   │   ├── OSINT_report.md
    │   │   │   ├── financial_analysis.md
    │   │   │   └── timeline.json
    │   │   ├── interim_results/       # Work-in-progress
    │   │   ├── metadata.json          # Investigation metadata
    │   │   └── README.md              # Investigation overview
    │   │
    │   └── {another_investigation_id}/
    │
    ├── completed/                     # Finished investigations
    │   └── {investigation_id}/        # Same structure as active
    │
    ├── archived/                      # Old investigations (compressed)
    │
    └── templates/                     # Investigation templates
        ├── investigation_template/
        └── source_template.md

└── logs/investigations/               # INVESTIGATION LOGS ONLY
    ├── local_llm/                     # LLM execution logs
    │   └── investigation_{id}_{timestamp}.jsonl
    ├── supervisor/                    # Supervisor review logs
    │   └── review_{id}_{timestamp}.json
    └── tool_usage/                    # Tool execution logs
        └── tools_{id}_{timestamp}.log

└── shared_workspace/                  # INVESTIGATION WORKSPACE
    ├── tasks/                         # Investigation tasks
    ├── results/                       # Investigation results
    ├── guidance/                      # Supervisor guidance
    └── reports/                       # Quality reports
```

---

## 🗄️ DATABASE SEPARATION

### **1. QDRANT - Separate Collections**

**Current:** Single collection `destiny-team-framework-master`

**New:** Separate collections with clear prefixes

```python
# PROJECT COLLECTIONS (System Knowledge)
COLLECTION_PROJECT_DOCS = "destiny_project_documentation"
# Contains: Architecture, guides, protocols, team docs
# Embedding: text-embedding-intfloat-multilingual-e5-large-instruct
# TTL: None (permanent)

COLLECTION_PROJECT_CODE = "destiny_project_code"
# Contains: Agent code, scripts, system code
# Embedding: jina-embeddings-v4-text-retrieval (code-optimized)
# TTL: None (permanent)

# INVESTIGATION COLLECTIONS (Research Data)
COLLECTION_INVESTIGATION_SOURCES = "destiny_investigation_sources"
# Contains: Web pages, articles, documents collected during investigations
# Embedding: text-embedding-intfloat-multilingual-e5-large-instruct (standard text)
# TTL: 90 days (or until investigation archived)

COLLECTION_INVESTIGATION_FINANCIAL = "destiny_investigation_financial"
# Contains: Financial reports, PDFs with tables, structured financial data
# Embedding: jina-embeddings-v4-text-retrieval (table-optimized)
# TTL: 90 days (or until investigation archived)

COLLECTION_INVESTIGATION_ANALYSIS = "destiny_investigation_analysis"
# Contains: Agent analysis, findings, reports
# Embedding: text-embedding-intfloat-multilingual-e5-large-instruct
# TTL: 180 days (longer retention for analysis)
```

**Collection Metadata:**

```python
{
    "name": "destiny_investigation_sources",
    "metadata": {
        "universe": "investigation",
        "purpose": "Research sources collected during investigations",
        "embedding_model": "text-embedding-intfloat-multilingual-e5-large-instruct",
        "ttl_days": 90,
        "auto_archive": true,
        "investigation_namespace": true
    }
}
```

---

### **2. POSTGRESQL - Separate Schemas**

**Current:** Tables in public schema

**New:** Separate schemas

```sql
-- PROJECT SCHEMA
CREATE SCHEMA project;

-- Project tables
CREATE TABLE project.documentation (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    title TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    content_hash TEXT,
    metadata JSONB
);

CREATE TABLE project.agents (
    id SERIAL PRIMARY KEY,
    agent_name TEXT NOT NULL,
    role TEXT,
    capabilities JSONB,
    status TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE project.capabilities (
    id SERIAL PRIMARY KEY,
    capability_name TEXT NOT NULL,
    category TEXT,
    status TEXT,
    documentation_path TEXT,
    metadata JSONB
);

-- INVESTIGATION SCHEMA
CREATE SCHEMA investigation;

-- Investigation tables
CREATE TABLE investigation.investigations (
    id TEXT PRIMARY KEY,  -- investigation_id
    title TEXT NOT NULL,
    objective TEXT,
    status TEXT,  -- active, completed, archived
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    assigned_agents TEXT[],
    metadata JSONB
);

CREATE TABLE investigation.sources (
    id SERIAL PRIMARY KEY,
    investigation_id TEXT REFERENCES investigation.investigations(id),
    source_url TEXT,
    source_type TEXT,  -- web, document, image, data
    file_path TEXT,
    archived_at TIMESTAMP DEFAULT NOW(),
    credibility TEXT,  -- high, medium, low
    metadata JSONB
);

CREATE TABLE investigation.findings (
    id SERIAL PRIMARY KEY,
    investigation_id TEXT REFERENCES investigation.investigations(id),
    finding_type TEXT,  -- fact, timeline, financial, legal
    content TEXT,
    confidence TEXT,  -- high, medium, low
    sources_ids INTEGER[],  -- References to sources
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE investigation.quality_reports (
    id SERIAL PRIMARY KEY,
    investigation_id TEXT REFERENCES investigation.investigations(id),
    supervisor TEXT,  -- "Aleksander"
    overall_grade TEXT,
    tool_usage_grade TEXT,
    source_quality_grade TEXT,
    ready_for_publication BOOLEAN,
    report_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Access Control:**

```sql
-- Project schema: Full access for system
GRANT ALL ON SCHEMA project TO destiny_system;

-- Investigation schema: Access for agents + supervisor
GRANT ALL ON SCHEMA investigation TO destiny_agents;
GRANT SELECT ON SCHEMA investigation TO destiny_supervisor;
```

---

### **3. NEO4J - Separate Label Namespaces**

**Current:** All nodes mixed

**New:** Separate label prefixes

```cypher
// PROJECT NODES (System Knowledge)
(:Project:Documentation {path, title, category})
(:Project:Agent {name, role, capabilities})
(:Project:Capability {name, category, status})
(:Project:Tool {name, type, version})

// Relationships
(:Project:Agent)-[:HAS_CAPABILITY]->(:Project:Capability)
(:Project:Agent)-[:USES_TOOL]->(:Project:Tool)
(:Project:Documentation)-[:DESCRIBES]->(:Project:Capability)

// INVESTIGATION NODES (Research Data)
(:Investigation {id, title, status, created_at})
(:Investigation:Source {url, type, credibility, archived_path})
(:Investigation:Finding {type, content, confidence})
(:Investigation:Entity {name, type})  // People, organizations, places
(:Investigation:Event {description, date, location})

// Relationships
(:Investigation)-[:HAS_SOURCE]->(:Investigation:Source)
(:Investigation)-[:PRODUCED_FINDING]->(:Investigation:Finding)
(:Investigation:Finding)-[:CITES]->(:Investigation:Source)
(:Investigation:Entity)-[:MENTIONED_IN]->(:Investigation:Source)
(:Investigation:Event)-[:INVOLVED]->(:Investigation:Entity)
```

**Query Isolation:**

```cypher
// Project queries
MATCH (a:Project:Agent)-[:HAS_CAPABILITY]->(c:Project:Capability)
RETURN a, c

// Investigation queries (completely separate)
MATCH (i:Investigation)-[:HAS_SOURCE]->(s:Investigation:Source)
WHERE i.id = $investigation_id
RETURN i, s
```

---

### **4. REDIS - Separate Key Prefixes**

**Current:** Mixed keys

**New:** Separate namespaces

```python
# PROJECT KEYS
KEY_PREFIX_PROJECT = "project:"

# Examples:
"project:agent:elena:status"
"project:capability:scraping:version"
"project:doc:architecture:hash"
"project:cache:capabilities_registry"

# INVESTIGATION KEYS
KEY_PREFIX_INVESTIGATION = "inv:"

# Examples:
"inv:telus_cpk:status"
"inv:telus_cpk:sources:count"
"inv:telus_cpk:quality:grade"
"inv:telus_cpk:cache:timeline"

# TTL policies
# Project keys: No TTL (permanent)
# Investigation keys: TTL = 7 days (refreshed on access)
```

---

## 🔧 EMBEDDING MODEL ROUTING

### **Intelligent Embedding Selection**

```python
class EmbeddingRouter:
    """
    Route documents to appropriate embedding model
    Based on content type and characteristics
    """
    
    # Models configuration
    MODELS = {
        "standard_text": {
            "name": "text-embedding-intfloat-multilingual-e5-large-instruct",
            "endpoint": "http://localhost:1234/v1/embeddings",
            "use_for": ["text", "articles", "reports_no_tables", "web_content"],
            "dimensions": 1024,
            "context_window": 512
        },
        "financial_tables": {
            "name": "jina-embeddings-v4-text-retrieval",
            "endpoint": "http://localhost:1234/v1/embeddings",
            "use_for": ["financial_pdf", "tables", "structured_data", "spreadsheets"],
            "dimensions": 768,
            "context_window": 8192
        }
    }
    
    def detect_document_type(self, content: str, metadata: dict) -> str:
        """
        Detect document type to select appropriate embedding model
        
        Returns: "standard_text" or "financial_tables"
        """
        # Check metadata first
        if metadata.get("type") == "financial":
            return "financial_tables"
        
        if metadata.get("has_tables", False):
            return "financial_tables"
        
        # Content analysis
        indicators_financial = [
            "PLN", "USD", "EUR", "zł",  # Currencies
            "bilans", "rachunek", "wynik finansowy",  # Financial terms PL
            "balance sheet", "income statement",  # Financial terms EN
            "|", "───", "┌", "└",  # Table characters
        ]
        
        financial_count = sum(
            1 for indicator in indicators_financial
            if indicator.lower() in content.lower()
        )
        
        # If 3+ financial indicators, use financial model
        if financial_count >= 3:
            return "financial_tables"
        
        # Check for table structures
        lines = content.split('\n')
        table_lines = sum(1 for line in lines if '|' in line or '\t\t' in line)
        
        if table_lines > 5:  # More than 5 lines with table indicators
            return "financial_tables"
        
        # Default: standard text model
        return "standard_text"
    
    def get_embedding(
        self,
        text: str,
        metadata: dict = None,
        force_model: str = None
    ) -> list:
        """
        Get embedding using appropriate model
        
        Args:
            text: Text to embed
            metadata: Document metadata (helps with detection)
            force_model: Force specific model ("standard_text" or "financial_tables")
        
        Returns:
            Embedding vector
        """
        # Determine model
        if force_model:
            model_type = force_model
        else:
            model_type = self.detect_document_type(text, metadata or {})
        
        model_config = self.MODELS[model_type]
        
        # Call LMStudio embedding endpoint
        response = requests.post(
            model_config["endpoint"],
            json={
                "model": model_config["name"],
                "input": text
            }
        )
        
        embedding = response.json()["data"][0]["embedding"]
        
        return embedding, model_type


# Usage example
router = EmbeddingRouter()

# Standard article
embedding, model = router.get_embedding(
    "Robert Telus był ministrem rolnictwa...",
    metadata={"type": "article", "source": "gazeta.pl"}
)
# Uses: text-embedding-intfloat-multilingual-e5-large-instruct

# Financial PDF
embedding, model = router.get_embedding(
    "Bilans finansowy 2023\n| Przychód | 1,250,000 PLN |\n| Koszty | 890,000 PLN |",
    metadata={"type": "financial", "has_tables": True}
)
# Uses: jina-embeddings-v4-text-retrieval
```

---

## 🔒 ACCESS CONTROL

### **Investigation Data Isolation**

```python
class DataAccessControl:
    """
    Enforce separation between project and investigation data
    """
    
    UNIVERSES = {
        "project": {
            "filesystem": "/Users/artur/coursor-agents-destiny-folder/docs/",
            "qdrant_collections": [
                "destiny_project_documentation",
                "destiny_project_code"
            ],
            "postgres_schema": "project",
            "neo4j_label_prefix": "Project",
            "redis_key_prefix": "project:",
            "access": ["system", "helena", "developers"]
        },
        "investigation": {
            "filesystem": "/Users/artur/coursor-agents-destiny-folder/investigations/",
            "qdrant_collections": [
                "destiny_investigation_sources",
                "destiny_investigation_financial",
                "destiny_investigation_analysis"
            ],
            "postgres_schema": "investigation",
            "neo4j_label_prefix": "Investigation",
            "redis_key_prefix": "inv:",
            "access": ["agents", "supervisor", "local_llm"]
        }
    }
    
    def validate_access(
        self,
        requester: str,
        universe: str,
        operation: str
    ) -> bool:
        """
        Validate if requester can access universe
        
        Args:
            requester: "helena", "agent_elena", "local_llm", "supervisor"
            universe: "project" or "investigation"
            operation: "read", "write", "delete"
        
        Returns:
            True if allowed, False otherwise
        """
        allowed_roles = self.UNIVERSES[universe]["access"]
        
        # Extract role from requester
        if requester.startswith("agent_"):
            role = "agents"
        elif requester == "local_llm":
            role = "local_llm"
        elif requester == "supervisor":
            role = "supervisor"
        elif requester == "helena":
            role = "helena"
        else:
            role = requester
        
        return role in allowed_roles
    
    def get_qdrant_collection(
        self,
        universe: str,
        content_type: str = "standard"
    ) -> str:
        """
        Get appropriate Qdrant collection for data
        
        Args:
            universe: "project" or "investigation"
            content_type: "standard", "financial", "code", "analysis"
        
        Returns:
            Collection name
        """
        if universe == "project":
            if content_type == "code":
                return "destiny_project_code"
            else:
                return "destiny_project_documentation"
        
        elif universe == "investigation":
            if content_type == "financial":
                return "destiny_investigation_financial"
            elif content_type == "analysis":
                return "destiny_investigation_analysis"
            else:
                return "destiny_investigation_sources"
        
        raise ValueError(f"Unknown universe: {universe}")


# Usage
access = DataAccessControl()

# Agent wants to search investigation data
if access.validate_access("agent_elena", "investigation", "read"):
    collection = access.get_qdrant_collection("investigation", "standard")
    # collection = "destiny_investigation_sources"
    # ✅ Allowed

# Agent wants to search project docs
if access.validate_access("agent_elena", "project", "read"):
    # ❌ Not allowed - agents should only access investigation data
    pass
```

---

## 📊 MIGRATION PLAN

### **Phase 1: Filesystem Separation (1-2 days)**

1. ✅ Create new directory structure
2. ✅ Move existing investigation data to `/investigations/`
3. ✅ Keep `/docs/` strictly for project documentation
4. ✅ Update all file paths in code
5. ✅ Update Helena watcher to monitor both locations separately

### **Phase 2: Database Separation (2-3 days)**

1. 🔨 Create separate Qdrant collections
2. 🔨 Create PostgreSQL schemas (project, investigation)
3. 🔨 Migrate existing data to appropriate schemas
4. 🔨 Update Neo4j to use label prefixes
5. 🔨 Update Redis key patterns

### **Phase 3: Embedding Router (1 day)**

1. 🔨 Implement `EmbeddingRouter` class
2. 🔨 Integrate with Qdrant indexing
3. 🔨 Test both embedding models
4. 🔨 Update `local_orchestrator.py` to use router

### **Phase 4: Access Control (1 day)**

1. 🔨 Implement `DataAccessControl` class
2. 🔨 Update all data access points
3. 🔨 Add validation at each boundary
4. 🔨 Test isolation

### **Phase 5: Testing & Validation (1-2 days)**

1. 🔨 Test complete separation
2. 🔨 Verify no data mixing
3. 🔨 Benchmark performance
4. 🔨 Document usage

**Total Time: 6-9 days**

---

## 🎯 SUCCESS CRITERIA

**System is properly separated when:**

1. ✅ Project docs never appear in investigation queries
2. ✅ Investigation data never appears in project searches
3. ✅ Each universe uses appropriate embedding model
4. ✅ Database queries respect namespace boundaries
5. ✅ Filesystem clearly organized (no mixed folders)
6. ✅ Access control enforced (agents can't access project internals)
7. ✅ Backup/restore can target specific universe
8. ✅ Privacy maintained (investigation data isolated)

---

## 📝 CONFIGURATION

### **Update `local_orchestrator.py`:**

```python
# Local LLM Configuration
LMSTUDIO_CONFIG = {
    "url": "http://localhost:1234/v1",
    "model_name": "gpt-oss-20b",
    "context_window": 44000,  # 44k tokens
    "temperature": 0.7,
    "max_tokens": 2048
}

# Embedding Configuration
EMBEDDING_CONFIG = {
    "standard_text": {
        "model": "text-embedding-intfloat-multilingual-e5-large-instruct",
        "use_for": ["text", "articles", "reports_no_tables"]
    },
    "financial_tables": {
        "model": "jina-embeddings-v4-text-retrieval",
        "use_for": ["financial_pdf", "tables", "structured_data"]
    }
}

# Data Separation
DATA_UNIVERSES = {
    "project": {
        "root": "/Users/artur/coursor-agents-destiny-folder/docs/",
        "access": "read-only"  # Agents can't modify project
    },
    "investigation": {
        "root": "/Users/artur/coursor-agents-destiny-folder/investigations/",
        "access": "read-write"  # Agents work here
    }
}
```

---

## 🚀 NEXT STEPS

**Priority 1 (This Week):**
1. Create investigation directory structure
2. Update `local_orchestrator.py` with your LMStudio config
3. Implement `EmbeddingRouter`
4. Test with one investigation

**Priority 2 (Next Week):**
1. Create separate database schemas/collections
2. Migrate existing data
3. Implement access control
4. Full testing

**Powiedz słowo, a implementuję!** 🎯
