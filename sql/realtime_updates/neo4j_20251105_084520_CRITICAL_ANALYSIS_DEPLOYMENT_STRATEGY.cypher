// Create document node
MERGE (d:Document {file_path: 'docs/strategy/CRITICAL_ANALYSIS_DEPLOYMENT_STRATEGY.md'})
SET d.title = '🔍 KRYTYCZNA ANALIZA STRATEGII WDROŻENIA - MYŚLENIE KRYTYCZNE',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);