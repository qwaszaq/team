// Create document node
MERGE (d:Document {file_path: 'GETTING_STARTED.md'})
SET d.title = '🚀 GETTING STARTED - Destiny Analytical System',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);