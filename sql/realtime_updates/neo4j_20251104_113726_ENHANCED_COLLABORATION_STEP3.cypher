// Create document node
MERGE (d:Document {file_path: 'docs/team/ENHANCED_COLLABORATION_STEP3.md'})
SET d.title = 'Enhanced Collaboration System - Step 3: Decision Evolution Tracker',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);