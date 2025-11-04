// Create document node
MERGE (d:Document {file_path: 'docs/team/SYSTEM_CAPABILITIES_UPDATE_2025_11_04.md'})
SET d.title = '🚀 SYSTEM CAPABILITIES UPDATE - November 4, 2025',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);