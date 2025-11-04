// Create document node
MERGE (d:Document {file_path: 'docs/capabilities/DUCKDUCKGO_SEARCH_METHOD.md'})
SET d.title = '🔍 DUCKDUCKGO SEARCH METHOD',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);