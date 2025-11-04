// Create document node
MERGE (d:Document {file_path: 'docs/protocols/AUTO_PROPAGATION_PROTOCOL.md'})
SET d.title = 'Protokół Automatycznej Propagacji Wiedzy',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);