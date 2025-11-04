
            // Create document node
            MERGE (d:Document {file_path: 'docs/status/AUTOMATION_PROOF_COMPLETE.md'})
            SET d.title = 'Kompletna Automatyzacja - Potwierdzenie',
                d.document_type = 'general_documentation',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'general_documentation'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: '1. Real-Time Watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2. Helena Processor'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '3. Auto-Start System'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Aleksandra'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Archiwizuje'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Auto-Start'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Automation'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Automatyzacja'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Brief'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Destiny'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            