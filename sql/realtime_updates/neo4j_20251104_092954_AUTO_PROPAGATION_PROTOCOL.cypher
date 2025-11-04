
            // Create document node
            MERGE (d:Document {file_path: 'docs/protocols/AUTO_PROPAGATION_PROTOCOL.md'})
            SET d.title = 'Protokół Automatycznej Propagacji Wiedzy',
                d.document_type = 'protocol',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'protocol'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: '1. Wprowadzenie'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2. Architektura Systemu'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2.1 Komponenty'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2.2 Workflow'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '3. Gwarancje Systemu'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '4. Weryfikacja'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Analizuje'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Architektura'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Archiwizuje'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Automatycznej'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            