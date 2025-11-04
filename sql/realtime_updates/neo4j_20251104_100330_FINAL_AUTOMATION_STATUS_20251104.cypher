// Create document node
MERGE (d:Document {file_path: 'docs/status/FINAL_AUTOMATION_STATUS_20251104.md'})
SET d.title = '🎉 FINAL STATUS - Automatyzacja 100% Operacyjna',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);