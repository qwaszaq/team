// Create document node
MERGE (d:Document {file_path: 'docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md'})
SET d.title = '🌐 Institutional API Analysis Capability',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);