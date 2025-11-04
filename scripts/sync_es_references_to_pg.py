#!/usr/bin/env python3
"""
Sync Elasticsearch documents to PostgreSQL as lightweight references.

Instead of duplicating full content, creates reference records with:
- ES document ID
- Metadata (issuer, filename, size, etc.)
- Tags for categorization
- Investigation ID for isolation

Usage:
    python3 sync_es_references_to_pg.py --index osint_reports_pdf
"""
import sys
import subprocess
import json
import argparse
import psycopg2
from datetime import datetime


def get_es_documents(es_url: str, es_user: str, es_password: str, index: str, size: int = 1000):
    """Fetch all documents from Elasticsearch index"""
    print(f"📥 Fetching documents from ES index: {index}")
    
    query = {
        "query": {"match_all": {}},
        "size": size,
        "_source": ["issuer", "report_url", "filename", "file_size", "sha256", "downloaded_at", "content_length"]
    }
    
    cmd = [
        'curl', '-s', '-u', f'{es_user}:{es_password}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(query),
        f'{es_url}/{index}/_search'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        print(f"❌ ES query failed: {result.stderr}")
        return []
    
    response = json.loads(result.stdout)
    hits = response.get('hits', {}).get('hits', [])
    
    print(f"   Found {len(hits)} documents")
    return hits


def sync_to_postgres(docs, pg_conn_str: str, investigation_id: str = None):
    """Sync ES documents to PostgreSQL as references"""
    print(f"\n📤 Syncing {len(docs)} references to PostgreSQL...")
    
    conn = psycopg2.connect(pg_conn_str)
    cur = conn.cursor()
    
    synced = 0
    skipped = 0
    
    for doc in docs:
        es_doc_id = doc['_id']
        source = doc.get('_source', {})
        
        # Extract metadata
        issuer = source.get('issuer', 'Unknown')
        report_url = source.get('report_url', '')
        filename = source.get('filename', '')
        file_size = source.get('file_size', 0)
        sha256 = source.get('sha256', '')
        downloaded_at = source.get('downloaded_at', datetime.now().isoformat())
        
        # Categorize tags based on issuer and type
        tags = ['osint', 'financial_report']
        if 'Grupa Azoty' in issuer:
            tags.extend(['grupa-azoty', 'tarnow'])
        
        # Determine investigation ID from issuer
        if investigation_id:
            inv_id = investigation_id
        elif 'Grupa Azoty' in issuer:
            inv_id = 'grupa_azoty_financial'
        else:
            inv_id = 'general_osint'
        
        # Metadata as JSONB
        metadata = {
            'content_length': source.get('content_length', 0),
            'source_base_url': source.get('source_base_url', ''),
            'report_type': 'periodic_report'
        }
        
        try:
            # Insert or update reference
            cur.execute("""
                INSERT INTO es_document_references 
                (es_index, es_doc_id, doc_type, issuer, report_url, filename, 
                 file_size, sha256, indexed_at, data_classification, investigation_id, tags, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (es_doc_id) 
                DO UPDATE SET
                    issuer = EXCLUDED.issuer,
                    report_url = EXCLUDED.report_url,
                    filename = EXCLUDED.filename,
                    file_size = EXCLUDED.file_size,
                    tags = EXCLUDED.tags,
                    metadata = EXCLUDED.metadata
            """, (
                'osint_reports_pdf',
                es_doc_id,
                'financial_report',
                issuer,
                report_url,
                filename,
                file_size,
                sha256,
                downloaded_at,
                'public',
                inv_id,
                tags,
                json.dumps(metadata)
            ))
            
            synced += 1
            
            if synced % 50 == 0:
                print(f"   ✅ Synced {synced}/{len(docs)}...")
                
        except Exception as e:
            print(f"   ⚠️  Skipped {filename}: {e}")
            skipped += 1
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n✅ Sync complete:")
    print(f"   • Synced: {synced}")
    print(f"   • Skipped: {skipped}")
    
    return synced


def update_agent_contexts(pg_conn_str: str):
    """Update agent contexts with available OSINT sources"""
    print(f"\n🤖 Updating agent contexts...")
    
    conn = psycopg2.connect(pg_conn_str)
    cur = conn.cursor()
    
    # Get summary of sources
    cur.execute("""
        SELECT 
            investigation_id,
            issuer,
            COUNT(*) as doc_count,
            SUM(file_size) as total_size,
            ARRAY_AGG(DISTINCT tag) as all_tags
        FROM es_document_references,
             UNNEST(tags) as tag
        GROUP BY investigation_id, issuer
    """)
    
    sources = cur.fetchall()
    
    for inv_id, issuer, doc_count, total_size, all_tags in sources:
        context_value = {
            'osint_sources': {
                'es_index': 'osint_reports_pdf',
                'investigation_id': inv_id,
                'issuer': issuer,
                'document_count': int(doc_count),
                'total_size_mb': float(round(total_size / (1024*1024), 2)) if total_size else 0.0,
                'tags': list(all_tags) if all_tags else [],
                'available_since': datetime.now().isoformat()
            }
        }
        
        # Update contexts for analytical agents
        agents = ['Marcus', 'Elena', 'Adrian', 'Maya', 'Helena', 'Viktor']
        
        for agent in agents:
            cur.execute("""
                INSERT INTO agent_contexts (agent_name, project_id, context_key, context_value, importance)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (agent_name, project_id, context_key)
                DO UPDATE SET
                    context_value = EXCLUDED.context_value,
                    updated_at = NOW()
            """, (
                agent,
                f'investigation-{inv_id}',
                'osint_sources_available',
                json.dumps(context_value),
                0.9
            ))
        
        print(f"   ✅ Updated contexts for {issuer}: {doc_count} docs available")
    
    conn.commit()
    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default='osint_reports_pdf', help='ES index name')
    parser.add_argument('--es-url', default='http://localhost:9200', help='ES URL')
    parser.add_argument('--es-user', default='elastic', help='ES username')
    parser.add_argument('--es-password', default='changeme123', help='ES password')
    parser.add_argument('--pg-conn', default='dbname=destiny_team user=user password=password host=localhost', help='PG connection')
    parser.add_argument('--investigation-id', default=None, help='Investigation ID')
    args = parser.parse_args()
    
    print("=" * 80)
    print("🔄 ES → PostgreSQL Reference Sync")
    print("=" * 80)
    print()
    
    # Fetch ES documents
    docs = get_es_documents(
        args.es_url,
        args.es_user,
        args.es_password,
        args.index,
        size=1000
    )
    
    if not docs:
        print("❌ No documents to sync")
        return
    
    # Sync to PG
    synced = sync_to_postgres(docs, args.pg_conn, args.investigation_id)
    
    # Update agent contexts
    if synced > 0:
        update_agent_contexts(args.pg_conn)
    
    print()
    print("=" * 80)
    print("✅ Sync completed successfully")
    print("=" * 80)
    print()
    print("📊 Quick verification:")
    print("   psql -h localhost -U user -d destiny_team -c \"SELECT COUNT(*) FROM es_document_references;\"")
    print()


if __name__ == '__main__':
    main()
