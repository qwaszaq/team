// Create document node
MERGE (d:Document {file_path: 'IMPLEMENTATION_REPORT_DAY2.md'})
SET d.title = '📊 IMPLEMENTATION REPORT - DAY 2',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);