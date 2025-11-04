
            // Create document node
            MERGE (d:Document {file_path: 'docs/protocols/TEST_AUTO_WATCHER_20251104_091904.md'})
            SET d.title = 'Test Auto-Watcher',
                d.document_type = 'protocol',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'protocol'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: 'Auto-Watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Helena'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Sprawdzenie'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Test'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Test Auto-Watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Utworzony'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Wykrywa'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            