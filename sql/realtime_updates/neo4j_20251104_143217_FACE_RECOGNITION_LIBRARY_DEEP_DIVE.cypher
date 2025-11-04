// Create document node
MERGE (d:Document {file_path: 'docs/research/FACE_RECOGNITION_LIBRARY_DEEP_DIVE.md'})
SET d.title = '🔍 face_recognition Library - Complete Deep Dive',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);