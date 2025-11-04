// Create document node
MERGE (d:Document {file_path: 'docs/SEARCH_ORCHESTRATOR.md'})
SET d.title = 'SearchOrchestrator - Unified Search Interface',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);