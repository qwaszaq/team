// Create document node
MERGE (d:Document {file_path: 'docs/research/FACE_RECOGNITION_OPENSOURCE_ANALYSIS.md'})
SET d.title = '🎯 Open Source Face Recognition Software - Deep Dive Analysis',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);