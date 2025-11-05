// Create document node
MERGE (d:Document {file_path: 'docs/strategy/ENTERPRISE_ANALYTICAL_SYSTEM_ARCHITECTURE.md'})
SET d.title = '🎯 ARCHITEKTURA DLA ENTERPRISE ANALYTICAL SYSTEM - WYCOFANIE KRYTYKI',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);