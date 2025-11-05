// Create document node
MERGE (d:Document {file_path: 'docs/strategy/HYBRID_DEPLOYMENT_STRATEGY_SESSION.md'})
SET d.title = '🎯 STRATEGIA WDROŻENIA SYSTEMU HYBRYDOWEGO - SESJA ZESPOŁU',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);