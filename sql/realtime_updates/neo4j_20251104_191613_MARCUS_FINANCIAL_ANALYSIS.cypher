// Create document node
MERGE (d:Document {file_path: 'investigations/telus_cpk_land_investigation/analysis/MARCUS_FINANCIAL_ANALYSIS.md'})
SET d.title = '💰 FINANCIAL ANALYSIS: Robert Telus - CPK Land Transaction',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);