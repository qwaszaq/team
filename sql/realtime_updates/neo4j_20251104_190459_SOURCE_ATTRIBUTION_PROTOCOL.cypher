// Create document node
MERGE (d:Document {file_path: 'docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md'})
SET d.title = '📚 SOURCE ATTRIBUTION PROTOCOL - Mandatory for All Investigations',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);