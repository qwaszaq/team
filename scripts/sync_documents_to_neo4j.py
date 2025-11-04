#!/usr/bin/env python3
"""
Sync document references to Neo4j knowledge graph.

Creates Document nodes and relationships:
- (Document) nodes with metadata
- (Document)-[:PART_OF]->(Investigation)
- (Agent)-[:ACCESSED]->(Document)
"""
import subprocess
import psycopg2
import json


def sync_documents_to_neo4j(
    pg_conn_str: str,
    neo4j_container: str = "sms-neo4j",
    neo4j_user: str = "neo4j",
    neo4j_password: str = "password"
):
    """Sync document references from PG to Neo4j"""
    print("=" * 80)
    print("🔄 PostgreSQL → Neo4j Document Sync")
    print("=" * 80)
    print()
    
    # Get documents from PG
    print("📥 Fetching documents from PostgreSQL...")
    conn = psycopg2.connect(pg_conn_str)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT es_doc_id, issuer, filename, investigation_id, tags, file_size
        FROM es_document_references
    """)
    
    docs = cur.fetchall()
    print(f"   Found {len(docs)} documents")
    print()
    
    # Create Document nodes in Neo4j
    print("📤 Creating Document nodes in Neo4j...")
    
    synced = 0
    for es_doc_id, issuer, filename, inv_id, tags, file_size in docs:
        # Escape quotes for Cypher
        safe_issuer = issuer.replace("'", "\\'") if issuer else "Unknown"
        safe_filename = filename.replace("'", "\\'") if filename else "Unknown"
        safe_inv_id = inv_id.replace("'", "\\'") if inv_id else "general"
        safe_tags = json.dumps(tags) if tags else '[]'
        
        cypher = f"""
        MERGE (doc:Document {{es_doc_id: '{es_doc_id}'}})
        ON CREATE SET
            doc.issuer = '{safe_issuer}',
            doc.filename = '{safe_filename}',
            doc.investigation_id = '{safe_inv_id}',
            doc.tags = {safe_tags},
            doc.file_size = {file_size or 0},
            doc.created_at = datetime()
        ON MATCH SET
            doc.updated_at = datetime()
        
        MERGE (inv:Investigation {{id: '{safe_inv_id}'}})
        ON CREATE SET inv.name = '{safe_inv_id}'
        
        MERGE (doc)-[:PART_OF]->(inv)
        """
        
        try:
            result = subprocess.run([
                'docker', 'exec', neo4j_container,
                'cypher-shell', '-u', neo4j_user, '-p', neo4j_password,
                cypher
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                synced += 1
                if synced % 50 == 0:
                    print(f"   ✅ Synced {synced}/{len(docs)}...")
            else:
                print(f"   ⚠️  Failed: {filename[:40]} - {result.stderr[:100]}")
                
        except Exception as e:
            print(f"   ⚠️  Error: {filename[:40]} - {e}")
    
    print()
    print(f"✅ Neo4j sync complete: {synced}/{len(docs)} documents")
    
    # Create agent relationships
    print()
    print("🤖 Creating Agent access relationships...")
    
    cur.execute("""
        SELECT DISTINCT accessed_by, es_doc_id
        FROM es_document_usage_log
    """)
    
    accesses = cur.fetchall()
    
    agent_links = 0
    for agent_name, es_doc_id in accesses:
        safe_agent = agent_name.replace("'", "\\'")
        
        cypher = f"""
        MERGE (agent:Agent {{name: '{safe_agent}'}})
        WITH agent
        MATCH (doc:Document {{es_doc_id: '{es_doc_id}'}})
        MERGE (agent)-[:ACCESSED]->(doc)
        """
        
        try:
            result = subprocess.run([
                'docker', 'exec', neo4j_container,
                'cypher-shell', '-u', neo4j_user, '-p', neo4j_password,
                cypher
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                agent_links += 1
                
        except Exception:
            pass
    
    print(f"✅ Created {agent_links} agent→document relationships")
    
    cur.close()
    conn.close()
    
    print()
    print("=" * 80)
    print("✅ Neo4j sync completed")
    print("=" * 80)


if __name__ == '__main__':
    sync_documents_to_neo4j(
        pg_conn_str="dbname=destiny_team user=user password=password host=localhost"
    )
