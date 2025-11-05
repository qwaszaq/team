// Create document node
MERGE (d:Document {file_path: 'WEEK1_COMPLETION_REPORT.md'})
SET d.title = '✅ WEEK 1 COMPLETION REPORT',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);