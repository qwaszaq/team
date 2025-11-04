// Create document node
MERGE (d:Document {file_path: 'docs/concepts/BELLINGCAT_LEVEL_OSINT.md'})
SET d.title = '🔍 Bellingcat-Level OSINT System - Investigative Journalism & Intelligence',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);