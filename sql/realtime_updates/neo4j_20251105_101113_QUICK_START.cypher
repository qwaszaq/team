// Create document node
MERGE (d:Document {file_path: 'QUICK_START.md'})
SET d.title = '🚀 QUICK START - Destiny Analytical System',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);