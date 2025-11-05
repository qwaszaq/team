// Create document node
MERGE (d:Document {file_path: 'FULL_HOG_FINAL_REPORT.md'})
SET d.title = '🐗💨 FULL HOG MODE - FINAL REPORT',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);