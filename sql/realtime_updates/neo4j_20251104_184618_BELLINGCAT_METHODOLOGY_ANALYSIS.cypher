// Create document node
MERGE (d:Document {file_path: 'docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md'})
SET d.title = '🔍 Bellingcat Methodology Analysis - Quality Standards & Investigative Excellence',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);