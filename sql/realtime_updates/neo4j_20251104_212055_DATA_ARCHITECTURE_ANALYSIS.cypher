// Create document node
MERGE (d:Document {file_path: 'docs/DATA_ARCHITECTURE_ANALYSIS.md'})
SET d.title = 'Data Architecture Analysis - ES vs PostgreSQL Separation',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);