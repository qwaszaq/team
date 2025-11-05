// Create document node
MERGE (d:Document {file_path: 'docs/team/TEAM_STRUCTURE.md'})
SET d.title = '👥 Destiny Team - Complete Structure',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);