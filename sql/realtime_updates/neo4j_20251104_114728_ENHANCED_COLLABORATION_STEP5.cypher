// Create document node
MERGE (d:Document {file_path: 'docs/team/ENHANCED_COLLABORATION_STEP5.md'})
SET d.title = 'Enhanced Collaboration System - Step 5: Collaboration Pattern Recognizer',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);