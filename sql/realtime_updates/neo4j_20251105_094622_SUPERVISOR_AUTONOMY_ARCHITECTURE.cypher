// Create document node
MERGE (d:Document {file_path: 'docs/architecture/SUPERVISOR_AUTONOMY_ARCHITECTURE.md'})
SET d.title = '🎯 ARCHITEKTURA NADZORU I AUTONOMII - HYBRID SUPERVISION',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);