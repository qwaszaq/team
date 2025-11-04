
            // Create document node
            MERGE (d:Document {file_path: 'docs/protocols/AUTO_PROPAGATION_VERIFICATION.md'})
            SET d.title = 'Automatyczna Propagacja - Weryfikacja',
                d.document_type = 'general_documentation',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'general_documentation'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: 'Automatyczna'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Automatyczna Propagacja - Weryfikacja'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Cypher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Helena'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Helenę'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'JSON'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Jeśli'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Konkluzja'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Kryteria'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Kryteria Sukcesu'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            