// Create document node
MERGE (d:Document {file_path: 'POSTGRES_STUCK_ANALYSIS.md'})
SET d.title = 'PostgreSQL Stuck Analysis - November 4, 2025',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);