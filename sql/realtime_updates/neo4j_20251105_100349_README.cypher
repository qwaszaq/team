// Create document node
MERGE (d:Document {file_path: 'README.md'})
SET d.title = '🚀 Destiny Analytical System - Hybrid Multi-Agent Platform',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);