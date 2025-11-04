// Create document node
MERGE (d:Document {file_path: 'docs/team/ADAPTIVE_LEARNING_SYSTEM.md'})
SET d.title = '🧠 Adaptive Learning System - Intelligence That Grows',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);