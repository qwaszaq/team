// Create document node
MERGE (d:Document {file_path: 'docs/concepts/SEJM_API_ANALYSIS_CONCEPT.md'})
SET d.title = '🏛️ Sejm API Analysis System - Complete Concept',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);