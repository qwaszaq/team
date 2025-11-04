// Create document node
MERGE (d:Document {file_path: 'investigations/active/telus_cpk_real_001/INVESTIGATION_STATUS.md'})
SET d.title = '🔍 Investigation Status: Telus-CPK Real Data',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);