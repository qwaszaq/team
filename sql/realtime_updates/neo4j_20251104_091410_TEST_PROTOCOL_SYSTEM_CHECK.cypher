
            // Create document node
            MERGE (d:Document {file_path: 'docs/protocols/TEST_PROTOCOL_SYSTEM_CHECK.md'})
            SET d.title = 'Test Protocol - System Check',
                d.document_type = 'protocol',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'protocol'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: 'Automated'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Behavior'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Check'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Concepts'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Content'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'DOCUMENT'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Detection'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Documents'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Expected'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Expected Behavior'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            