// Create document node
MERGE (d:Document {file_path: 'VERIFICATION_CHECKLIST.md'})
SET d.title = '✅ SYSTEM VERIFICATION CHECKLIST',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);