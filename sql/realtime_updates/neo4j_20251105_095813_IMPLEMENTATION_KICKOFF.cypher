// Create document node
MERGE (d:Document {file_path: 'docs/kickoff/IMPLEMENTATION_KICKOFF.md'})
SET d.title = '🚀 KICK-OFF IMPLEMENTACJI - HYBRID ANALYTICAL SYSTEM',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);