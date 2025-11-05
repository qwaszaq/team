// Create document node
MERGE (d:Document {file_path: 'ENHANCEMENT_ROADMAP.md'})
SET d.title = '🚀 ENHANCEMENT ROADMAP - Areas for Expansion',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);