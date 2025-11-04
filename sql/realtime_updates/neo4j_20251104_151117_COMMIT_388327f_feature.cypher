// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-04/COMMIT_388327f_feature.md'})
SET d.title = 'Sejm API Analysis System - Real Data from Parliament',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);