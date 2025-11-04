
            // Create document node
            MERGE (d:Document {file_path: 'docs/protocols/DOCUMENTATION_STRUCTURE_PROTOCOL.md'})
            SET d.title = '📁 Documentation Structure Protocol',
                d.document_type = 'protocol',
                d.indexed_at = datetime(),
                d.source = 'realtime_watcher'
            
            // Link to document type
            MERGE (dt:DocumentType {name: 'protocol'})
            MERGE (d)-[:IS_TYPE]->(dt)
            
            MERGE (c:Concept {name: '

# Save to appropriate location
path = '})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '

path = '})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '
# Database Update Protocol
...
'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '
# Market Research - Q4 2025
...
'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '
# Team Status Report - 2025-11-04
...
'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '
with open(path, \'w\') as f:
    f.write(protocol)

# Watcher detects it instantly
# Helena processes it automatically
# Added to all databases within 10 seconds
```

### Example 2: Aleksander creates team status
```python
status = '})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '
with open(path, \'w\') as f:
    f.write(status)
```

### Example 3: Sofia creates market analysis
```python
analysis = '})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: '# New Protocol'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'ACTIVE'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            
            MERGE (c:Concept {name: 'AGENTS'})
            MERGE (d)-[:CONTAINS_CONCEPT]->(c)
            