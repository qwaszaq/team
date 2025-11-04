// Create document node
MERGE (d:Document {file_path: 'docs/orchestration/QUICK_START.md'})
SET d.title = '🚀 Quick Start: Transparency System',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);