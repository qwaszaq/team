// Create document node
MERGE (d:Document {file_path: 'investigations/telus_cpk_land_investigation/INVESTIGATION_PLAN.md'})
SET d.title = '🔍 INVESTIGATION PLAN: Robert Telus - CPK Land Transaction',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);