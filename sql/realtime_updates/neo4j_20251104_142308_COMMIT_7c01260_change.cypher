// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-04/COMMIT_7c01260_change.md'})
SET d.title = 'research: Face Recognition Open Source Software Analysis',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);