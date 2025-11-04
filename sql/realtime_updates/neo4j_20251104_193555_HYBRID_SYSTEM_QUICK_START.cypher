// Create document node
MERGE (d:Document {file_path: 'docs/guides/HYBRID_SYSTEM_QUICK_START.md'})
SET d.title = '🚀 HYBRID ON-PREM SYSTEM - Quick Start Guide',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);