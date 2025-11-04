// Create document node
MERGE (d:Document {file_path: 'docs/team/SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.md'})
SET d.title = '✅ SOURCE ATTRIBUTION PROTOCOL - Training Compliance Record',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);