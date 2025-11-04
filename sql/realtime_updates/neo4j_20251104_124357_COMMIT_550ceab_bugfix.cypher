// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-04/COMMIT_550ceab_bugfix.md'})
SET d.title = 'Resolve false-positive warnings in database connectivity checks',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);