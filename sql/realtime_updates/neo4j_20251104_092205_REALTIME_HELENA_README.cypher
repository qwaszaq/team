
            // Create document node
            MERGE (d:Document {file_path: 'docs/team/REALTIME_HELENA_README.md'})
            SET d.title = '🚀 Real-Time Helena Document Processor',
                d.document_type = 'team_documentation',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'team_documentation'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: '# ⏱️  Total time: 6.3 seconds'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '# 🤖 TRIGGERING HELENA AUTO-PROCESSING...'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '... piszesz treść ...'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: './start_realtime_helena.sh'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '2.0.0'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'AUTO-PROCESSING'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Aktywne'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Aktywnie'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Analizuje'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Architektura'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            