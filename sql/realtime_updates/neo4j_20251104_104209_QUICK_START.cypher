// Create document node
MERGE (d:Document {file_path: 'docs/guides/QUICK_START.md'})
SET d.title = '⚡ Quick Start Guide - Get Running in 5 Minutes!',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);