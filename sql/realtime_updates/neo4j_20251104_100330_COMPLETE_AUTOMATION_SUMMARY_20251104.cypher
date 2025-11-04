// Create document node
MERGE (d:Document {file_path: 'docs/status/COMPLETE_AUTOMATION_SUMMARY_20251104.md'})
SET d.title = '✅ COMPLETE AUTOMATION SUMMARY - 2025-11-04',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);