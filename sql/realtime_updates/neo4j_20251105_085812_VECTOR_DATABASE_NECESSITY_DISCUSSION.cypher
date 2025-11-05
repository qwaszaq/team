// Create document node
MERGE (d:Document {file_path: 'docs/strategy/VECTOR_DATABASE_NECESSITY_DISCUSSION.md'})
SET d.title = '🔍 DYSKUSJA: CZY NAPRAWDĘ POTRZEBUJEMY QDRANT?',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);