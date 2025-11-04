// Create document node
MERGE (d:Document {file_path: 'investigations/active/telus_cpk_real_001/FINAL_OSINT_REPORT.md'})
SET d.title = 'Raport OSINT: Robert Telus — CPK (real data)',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);