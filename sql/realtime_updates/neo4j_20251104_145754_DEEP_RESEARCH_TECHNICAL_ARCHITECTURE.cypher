// Create document node
MERGE (d:Document {file_path: 'docs/concepts/DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.md'})
SET d.title = '🏗️ Deep Research System - Technical Architecture',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);