// Create document node
MERGE (d:Document {file_path: 'docs/status/HELENA_PROCESSING_REPORT_20251104.md'})
SET d.title = '📊 Helena Processing Report - Dzisiejsze Zmiany',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);