// Create document node
MERGE (d:Document {file_path: 'investigations/telus_cpk_land_investigation/analysis/ELENA_OSINT_REPORT.md'})
SET d.title = '🔍 OSINT REPORT: Robert Telus - CPK Land Transaction',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);