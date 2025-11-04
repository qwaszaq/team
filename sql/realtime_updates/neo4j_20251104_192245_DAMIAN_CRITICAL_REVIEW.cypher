// Create document node
MERGE (d:Document {file_path: 'investigations/telus_cpk_land_investigation/analysis/DAMIAN_CRITICAL_REVIEW.md'})
SET d.title = '🎭 CRITICAL REVIEW: Robert Telus Investigation - Devil''s Advocate Analysis',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);