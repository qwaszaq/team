
            // Create document node
            MERGE (d:Document {file_path: 'docs/status/AUTOSTART_SYSTEM_STATUS.md'})
            SET d.title = '✅ Auto-Start System - Status Report',
                d.document_type = 'status_report',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'status_report'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: '# Test'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '1. Sprawdź czy usługi działają'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '1. ✅ Morning Brief Agent'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2. Sprawdź procesy'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2. ✅ Real-Time Watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '3. Sprawdź logi'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '4. Sprawdź morning brief'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '5. Test watcher'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'ACTIVE'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'ALERTS'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            