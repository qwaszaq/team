// Create document node
MERGE (d:Document {file_path: 'docs/status/SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.md'})
SET d.title = '📊 Session Summary - OSINT System Development',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);