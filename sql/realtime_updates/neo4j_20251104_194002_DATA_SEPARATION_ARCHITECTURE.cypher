// Create document node
MERGE (d:Document {file_path: 'docs/architecture/DATA_SEPARATION_ARCHITECTURE.md'})
SET d.title = '🏗️ DATA SEPARATION ARCHITECTURE',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);