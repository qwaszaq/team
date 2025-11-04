// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-04/COMMIT_6a77410_documentation.md'})
SET d.title = 'Add dashboard demo and interactive tutorial',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);