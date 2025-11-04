// Create document node
MERGE (d:Document {file_path: 'docs/protocols/HELENA_VECTOR_1024_REQUIREMENT.md'})
SET d.title = '🎯 OBOWIĄZEK: Helena - Vectors 1024 Dimensions',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);