// Create document node
MERGE (d:Document {file_path: 'docs/status/HYBRID_SYSTEM_STATUS_REPORT_TEAM.md'})
SET d.title = '🚀 RAPORT STATUS SYSTEMU HYBRYDOWEGO - ZESPÓŁ DESTINY TEAM',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);