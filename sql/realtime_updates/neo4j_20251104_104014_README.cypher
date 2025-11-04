// Create document node
MERGE (d:Document {file_path: 'README.md'})
SET d.title = '🤖 Destiny Team Framework - Helena Auto-Execution System',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);