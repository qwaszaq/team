// Create document node
MERGE (d:Document {file_path: 'docs/team/ENHANCED_COLLABORATION_STEP6.md'})
SET d.title = 'Enhanced Collaboration System - Step 6: Integrated System',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);