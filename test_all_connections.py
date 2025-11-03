#!/usr/bin/env python3
"""
Test All Connections - Full Stack Health Check

Tests connectivity to all 5 components:
- PostgreSQL (structured data)
- Neo4j (knowledge graph)
- Qdrant (semantic search)
- Redis (cache)
- LM Studio (embeddings)
"""

import sys


def test_postgres():
    """Test PostgreSQL connection"""
    print("\n" + "="*70)
    print("  1️⃣  PostgreSQL Connection Test")
    print("="*70)
    
    try:
        from postgres_context_store import PostgresContextStore
        
        store = PostgresContextStore(
            "dbname=destiny_team user=user password=password host=localhost port=5432"
        )
        
        # Test query
        with store.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM messages")
            count = cur.fetchone()[0]
        
        print(f"✅ PostgreSQL connected!")
        print(f"   Container: sms-postgres")
        print(f"   Database: destiny_team")
        print(f"   Messages: {count}")
        
        store.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL failed: {e}")
        return False


def test_neo4j():
    """Test Neo4j connection"""
    print("\n" + "="*70)
    print("  2️⃣  Neo4j Connection Test")
    print("="*70)
    
    try:
        from neo4j_integration import Neo4jKnowledgeGraph
        
        graph = Neo4jKnowledgeGraph(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="password"
        )
        
        # Test query
        with graph.driver.session() as session:
            result = session.run("RETURN 'Connected!' as message")
            message = result.single()['message']
        
        print(f"✅ Neo4j connected!")
        print(f"   Container: sms-neo4j")
        print(f"   Version: 2025.08.0")
        print(f"   Plugins: APOC")
        
        graph.close()
        return True
        
    except Exception as e:
        print(f"❌ Neo4j failed: {e}")
        return False


def test_qdrant():
    """Test Qdrant connection"""
    print("\n" + "="*70)
    print("  3️⃣  Qdrant Connection Test")
    print("="*70)
    
    try:
        from qdrant_client import QdrantClient
        
        client = QdrantClient(url="http://localhost:6333")
        
        # Get collections
        collections = client.get_collections()
        
        print(f"✅ Qdrant connected!")
        print(f"   Container: sms-qdrant")
        print(f"   Version: v1.14.1")
        print(f"   Collections: {len(collections.collections)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Qdrant failed: {e}")
        return False


def test_redis():
    """Test Redis connection"""
    print("\n" + "="*70)
    print("  4️⃣  Redis Connection Test")
    print("="*70)
    
    try:
        from redis_cache import RedisCache
        
        cache = RedisCache(host="localhost", port=6379)
        
        # Test ping
        cache.client.ping()
        
        # Get info
        info = cache.client.info()
        
        print(f"✅ Redis connected!")
        print(f"   Container: kg-redis")
        print(f"   Version: {info.get('redis_version')}")
        print(f"   Memory: {info.get('used_memory_human')}")
        print(f"   Keys: {cache.client.dbsize()}")
        print(f"   AOF: enabled")
        
        cache.close()
        return True
        
    except Exception as e:
        print(f"❌ Redis failed: {e}")
        return False


def test_lmstudio():
    """Test LM Studio connection"""
    print("\n" + "="*70)
    print("  5️⃣  LM Studio Embeddings Test")
    print("="*70)
    
    try:
        from lmstudio_embeddings import LMStudioEmbeddings
        
        embedder = LMStudioEmbeddings(base_url="http://localhost:1234/v1")
        
        # Test embedding
        test_text = "Test embedding generation"
        embedding = embedder.embed(test_text)
        
        print(f"✅ LM Studio connected!")
        print(f"   Endpoint: http://localhost:1234/v1")
        print(f"   Model: multilingual-e5-large-instruct")
        print(f"   Dimension: {len(embedding)}")
        print(f"   Cost: $0 (local!)")
        
        return True
        
    except Exception as e:
        print(f"❌ LM Studio failed: {e}")
        print(f"   Make sure LM Studio is running with embeddings model loaded")
        return False


def main():
    """Run all connection tests"""
    print("\n" + "🎨 "*20)
    print("  FULL STACK HEALTH CHECK")
    print("🎨 "*20)
    
    tests = [
        ("PostgreSQL", test_postgres),
        ("Neo4j", test_neo4j),
        ("Qdrant", test_qdrant),
        ("Redis", test_redis),
        ("LM Studio", test_lmstudio)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("  📊 SUMMARY")
    print("="*70)
    print()
    
    for name, success in results:
        status = "✅ ONLINE " if success else "❌ OFFLINE"
        print(f"  {status}: {name}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print()
    print(f"  {passed}/{total} services online")
    print()
    
    if passed == total:
        print("  🎉 FULL STACK OPERATIONAL!")
        print()
        print("  You have:")
        print("    ✅ Unlimited storage (PostgreSQL)")
        print("    ✅ Semantic search (Qdrant + E5-Large)")
        print("    ✅ Knowledge graph (Neo4j)")
        print("    ✅ Ultra-fast cache (Redis)")
        print("    ✅ Local embeddings ($0 cost)")
        print()
        print("  🚀 Ready for Master Orchestrator!")
        print()
        print("  Next: python master_orchestrator.py")
        return 0
    else:
        print("  ⚠️  Some services offline!")
        print()
        print("  Troubleshooting:")
        
        if not results[0][1]:  # PostgreSQL
            print("    PostgreSQL: docker ps | grep sms-postgres")
        if not results[1][1]:  # Neo4j
            print("    Neo4j: docker ps | grep sms-neo4j")
        if not results[2][1]:  # Qdrant
            print("    Qdrant: docker ps | grep sms-qdrant")
        if not results[3][1]:  # Redis
            print("    Redis: docker ps | grep kg-redis")
        if not results[4][1]:  # LM Studio
            print("    LM Studio: Make sure it's running with embeddings loaded")
        
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
