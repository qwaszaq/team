// Create document node
MERGE (d:Document {file_path: 'docs/ELASTICSEARCH_BATCH_INTEGRATION.md'})
SET d.title = '🔍 Elasticsearch Batch Integration',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);