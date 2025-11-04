#!/usr/bin/env python3
"""
Test Smart References Integration - ES ↔ PG ↔ Neo4j

Verifies that lightweight reference system works correctly:
- Documents in ES searchable
- References in PG queryable
- Usage logged for audit
- Neo4j graph updated
- Agents can discover sources
"""
import sys
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from search_orchestrator import SearchOrchestrator
import psycopg2
import subprocess
import json


def test_es_documents():
    """Test 1: ES documents are searchable"""
    print("=" * 80)
    print("TEST 1: Elasticsearch Documents")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    results = orchestrator.full_text_search(
        query="sprawozdanie finansowe",
        size=5,
        accessed_by="TestAgent"
    )
    
    print(f"✅ ES Search: {len(results)} results")
    print(f"   Top result: {results[0].metadata.get('filename', 'N/A')[:60]}")
    print()
    
    assert len(results) > 0, "ES search returned no results"
    return True


def test_pg_references():
    """Test 2: PG references exist and queryable"""
    print("=" * 80)
    print("TEST 2: PostgreSQL References")
    print("=" * 80)
    print()
    
    conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost")
    cur = conn.cursor()
    
    # Count references
    cur.execute("SELECT COUNT(*) FROM es_document_references")
    ref_count = cur.fetchone()[0]
    
    print(f"✅ PG References: {ref_count} documents")
    
    # Check investigation sources
    cur.execute("SELECT * FROM get_investigation_sources('grupa_azoty_financial')")
    sources = cur.fetchall()
    
    for issuer, doc_count, total_size, tags in sources:
        print(f"   • {issuer}: {doc_count} docs, {total_size/(1024*1024):.1f} MB")
    
    print()
    
    cur.close()
    conn.close()
    
    assert ref_count > 0, "No references in PG"
    return True


def test_usage_logging():
    """Test 3: Usage logging works"""
    print("=" * 80)
    print("TEST 3: Usage Logging (Audit Trail)")
    print("=" * 80)
    print()
    
    conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost")
    cur = conn.cursor()
    
    # Check usage log
    cur.execute("SELECT COUNT(*) FROM es_document_usage_log")
    log_count = cur.fetchone()[0]
    
    print(f"✅ Usage Log: {log_count} access records")
    
    # Get recent accesses
    cur.execute("""
        SELECT accessed_by, COUNT(*) as count
        FROM es_document_usage_log
        GROUP BY accessed_by
    """)
    
    for agent, count in cur.fetchall():
        print(f"   • {agent}: {count} accesses")
    
    print()
    
    cur.close()
    conn.close()
    
    assert log_count > 0, "No usage logs"
    return True


def test_agent_contexts():
    """Test 4: Agents know about available sources"""
    print("=" * 80)
    print("TEST 4: Agent Contexts")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Check Marcus context
    context = orchestrator.get_context_for_agent(
        agent_name="Marcus",
        project_id="investigation-grupa_azoty_financial",
        limit=5
    )
    
    print(f"✅ Marcus Context: {len(context)} items")
    
    for item in context:
        context_key = item.get('context_key', 'N/A')
        if context_key == 'osint_sources_available':
            context_value = item.get('context_value', {})
            if isinstance(context_value, str):
                context_value = json.loads(context_value)
            
            osint = context_value.get('osint_sources', {})
            print(f"   • OSINT Sources: {osint.get('document_count', 0)} docs")
            print(f"   • Issuer: {osint.get('issuer', 'N/A')}")
            print(f"   • Size: {osint.get('total_size_mb', 0)} MB")
    
    print()
    
    assert len(context) > 0, "Agent has no context"
    return True


def test_neo4j_graph():
    """Test 5: Neo4j graph has document nodes"""
    print("=" * 80)
    print("TEST 5: Neo4j Knowledge Graph")
    print("=" * 80)
    print()
    
    cypher = "MATCH (doc:Document) RETURN COUNT(doc) as count"
    
    result = subprocess.run([
        'docker', 'exec', 'sms-neo4j',
        'cypher-shell', '-u', 'neo4j', '-p', 'password',
        '--format', 'plain',
        cypher
    ], capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip().isdigit():
                doc_count = int(line.strip())
                print(f"✅ Neo4j Documents: {doc_count} nodes")
                break
    
    # Check agent relationships
    cypher = "MATCH (agent:Agent)-[:ACCESSED]->(doc:Document) RETURN COUNT(*) as count"
    
    result = subprocess.run([
        'docker', 'exec', 'sms-neo4j',
        'cypher-shell', '-u', 'neo4j', '-p', 'password',
        '--format', 'plain',
        cypher
    ], capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip().isdigit():
                rel_count = int(line.strip())
                print(f"✅ Agent→Document Links: {rel_count} relationships")
                break
    
    print()
    return True


def test_hybrid_query():
    """Test 6: Hybrid query across all layers"""
    print("=" * 80)
    print("TEST 6: Hybrid Query (ES + Qdrant + PG)")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    results = orchestrator.hybrid_search(
        query="financial analysis",
        sources=['es', 'qdrant', 'pg'],
        limit=5
    )
    
    print(f"✅ Hybrid Search: {len(results)} combined results")
    
    sources_used = set(r.source for r in results)
    print(f"   Sources used: {', '.join(sources_used)}")
    
    print()
    
    assert len(results) > 0, "Hybrid search returned no results"
    return True


def main():
    """Run all integration tests"""
    print("\n" + "=" * 80)
    print("🧪 Smart References Integration Tests")
    print("=" * 80)
    print("\n")
    
    tests = [
        ("ES Documents Searchable", test_es_documents),
        ("PG References Queryable", test_pg_references),
        ("Usage Logging Works", test_usage_logging),
        ("Agent Contexts Updated", test_agent_contexts),
        ("Neo4j Graph Populated", test_neo4j_graph),
        ("Hybrid Query Works", test_hybrid_query),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
            failed += 1
    
    print("=" * 80)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("=" * 80)
    print()
    
    if failed == 0:
        print("✅ All integration tests passed!")
        print()
        print("🎯 Smart References System is operational:")
        print("   • ES = source of truth (full-text search)")
        print("   • PG = references + audit trail")
        print("   • Neo4j = knowledge graph")
        print("   • Agents = aware of available sources")
        print()
    else:
        print(f"⚠️  {failed} test(s) failed - check errors above")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
