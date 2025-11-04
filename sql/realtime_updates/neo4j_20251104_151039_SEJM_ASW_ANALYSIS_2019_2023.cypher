// Create document node
MERGE (d:Document {file_path: 'docs/research/SEJM_ASW_ANALYSIS_2019_2023.md'})
SET d.title = '🏛️ Analiza Pracy Komisji Administracji i Spraw Wewnętrznych',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);