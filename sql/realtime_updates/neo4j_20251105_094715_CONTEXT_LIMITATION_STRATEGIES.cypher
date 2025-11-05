// Create document node
MERGE (d:Document {file_path: 'docs/architecture/CONTEXT_LIMITATION_STRATEGIES.md'})
SET d.title = '⚠️ CONTEXT LIMITATION - STRATEGIE I ROZWIĄZANIA',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);