// Create document node
MERGE (d:Document {file_path: 'docs/guides/HYBRID_SYSTEM_COMPLETE_OVERVIEW.md'})
SET d.title = '🔍 HYBRID ON-PREM INTELLIGENCE SYSTEM',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);