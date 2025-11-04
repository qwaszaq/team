
            // Create document node
            MERGE (d:Document {file_path: 'docs/status/MORNING_BRIEF_20251104.md'})
            SET d.title = '🌅 Morning Brief for Aleksander Nowak (Orchestrator)',
                d.document_type = 'status_report',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'status_report'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: 'Actions'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Activity'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Agent'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Agents'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Aleksander'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Alerts'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Automated'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Brief'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Category'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'Collaboration**'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            