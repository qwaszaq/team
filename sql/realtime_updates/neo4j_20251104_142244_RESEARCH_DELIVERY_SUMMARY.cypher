// Create document node
MERGE (d:Document {file_path: 'docs/research/RESEARCH_DELIVERY_SUMMARY.md'})
SET d.title = '📦 Research Delivery Summary',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);