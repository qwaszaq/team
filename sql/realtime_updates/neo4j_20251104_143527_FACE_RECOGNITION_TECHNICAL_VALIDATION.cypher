// Create document node
MERGE (d:Document {file_path: 'docs/research/FACE_RECOGNITION_TECHNICAL_VALIDATION.md'})
SET d.title = '✅ Technical Validation Report: face_recognition Library',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);