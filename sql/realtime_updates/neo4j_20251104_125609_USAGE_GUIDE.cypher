// Create document node
MERGE (d:Document {file_path: 'docs/USAGE_GUIDE.md'})
SET d.title = '🚀 Destiny System - Przewodnik Użycia',
    d.document_type = 'guide',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'guide'})
MERGE (d)-[:IS_TYPE]->(dt);