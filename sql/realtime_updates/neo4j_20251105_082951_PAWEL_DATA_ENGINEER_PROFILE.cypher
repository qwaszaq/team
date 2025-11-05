// Create document node
MERGE (d:Document {file_path: 'docs/team/PAWEL_DATA_ENGINEER_PROFILE.md'})
SET d.title = '🔧 Paweł Kowalski - Data Engineer',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);