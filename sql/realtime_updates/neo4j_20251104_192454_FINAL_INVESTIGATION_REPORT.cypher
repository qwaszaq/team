// Create document node
MERGE (d:Document {file_path: 'investigations/telus_cpk_land_investigation/FINAL_INVESTIGATION_REPORT.md'})
SET d.title = '🔍 INVESTIGATIVE METHODOLOGY DEMONSTRATION',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);