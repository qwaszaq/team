// Create document node
MERGE (d:Document {file_path: 'docs/status/FINAL_SUCCESS_QDRANT_AUTO_EXECUTION.md'})
SET d.title = '✅ FINALNY SUKCES - Qdrant Auto-Execution Complete!',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);