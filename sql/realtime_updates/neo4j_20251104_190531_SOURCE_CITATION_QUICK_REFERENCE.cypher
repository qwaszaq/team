// Create document node
MERGE (d:Document {file_path: 'SOURCE_CITATION_QUICK_REFERENCE.md'})
SET d.title = '📚 SOURCE CITATION - QUICK REFERENCE CARD',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);