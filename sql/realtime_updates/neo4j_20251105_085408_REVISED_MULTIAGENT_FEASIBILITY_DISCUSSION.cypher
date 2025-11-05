// Create document node
MERGE (d:Document {file_path: 'docs/strategy/REVISED_MULTIAGENT_FEASIBILITY_DISCUSSION.md'})
SET d.title = '🔄 PONOWNA DYSKUSJA - WYKONALNOŚĆ SYSTEMU MULTIAGENTOWEGO',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);