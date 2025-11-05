// Create document node
MERGE (d:Document {file_path: 'COMPLETE_SYSTEM_OVERVIEW.md'})
SET d.title = '🚀 COMPLETE SYSTEM OVERVIEW - Destiny Analytical System',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);