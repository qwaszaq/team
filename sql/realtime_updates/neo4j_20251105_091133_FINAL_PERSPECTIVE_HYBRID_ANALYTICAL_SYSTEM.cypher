// Create document node
MERGE (d:Document {file_path: 'docs/strategy/FINAL_PERSPECTIVE_HYBRID_ANALYTICAL_SYSTEM.md'})
SET d.title = '🎭 SPOJRZENIE Z DYSTANSU - HYBRID ANALYTICAL SYSTEM',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);