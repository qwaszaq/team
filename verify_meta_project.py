#!/usr/bin/env python3
"""
Verify Meta-Project Data - Sprawdza co jest zapisane dla Destiny Team Framework

Pokazuje że framework już działa dla samego siebie (meta!)
"""

from postgres_context_store import PostgresContextStore
from neo4j_integration import Neo4jKnowledgeGraph
from qdrant_client import QdrantClient
from redis_cache import RedisCache


def verify_all_layers():
    """Comprehensive verification of all storage layers"""
    
    print("\n" + "🔍 "*30)
    print("  META-PROJECT VERIFICATION")
    print("  Czy Destiny Team Framework ma swoje dane w systemie?")
    print("🔍 "*30)
    print()
    
    results = {
        "postgres": False,
        "neo4j": False,
        "qdrant": False,
        "redis": False
    }
    
    # ==================== POSTGRESQL ====================
    
    print("=" * 70)
    print("  1️⃣  POSTGRESQL - Structured Data")
    print("=" * 70)
    print()
    
    try:
        postgres = PostgresContextStore(
            "dbname=destiny_team user=user password=password host=localhost port=5432"
        )
        
        # Count projects
        with postgres.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM projects")
            project_count = cur.fetchone()[0]
        
        # Count messages
        with postgres.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM messages")
            message_count = cur.fetchone()[0]
        
        # Count decisions
        with postgres.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM decisions")
            decision_count = cur.fetchone()[0]
        
        print(f"✅ POSTGRESQL Connected!")
        print(f"   Projects: {project_count}")
        print(f"   Messages: {message_count}")
        print(f"   Decisions: {decision_count}")
        
        if message_count > 0:
            results["postgres"] = True
            print(f"   ✅ META-PROJECT DATA FOUND!")
        
        postgres.close()
        
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")
    
    print()
    
    # ==================== NEO4J ====================
    
    print("=" * 70)
    print("  2️⃣  NEO4J - Knowledge Graph")
    print("=" * 70)
    print()
    
    try:
        neo4j = Neo4jKnowledgeGraph(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="password"
        )
        
        # Count nodes
        with neo4j.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN 
                    COUNT(CASE WHEN n:Project THEN 1 END) as projects,
                    COUNT(CASE WHEN n:Message THEN 1 END) as messages,
                    COUNT(CASE WHEN n:Concept THEN 1 END) as concepts,
                    COUNT(CASE WHEN n:Decision THEN 1 END) as decisions,
                    COUNT(CASE WHEN n:Agent THEN 1 END) as agents
            """)
            stats = result.single()
        
        print(f"✅ NEO4J Connected!")
        print(f"   Projects: {stats['projects']}")
        print(f"   Messages: {stats['messages']}")
        print(f"   Concepts: {stats['concepts']}")
        print(f"   Decisions: {stats['decisions']}")
        print(f"   Agents: {stats['agents']}")
        
        if stats['messages'] > 0 or stats['concepts'] > 0:
            results["neo4j"] = True
            print(f"   ✅ META-PROJECT DATA FOUND!")
        
        neo4j.close()
        
    except Exception as e:
        print(f"❌ Neo4j: {e}")
    
    print()
    
    # ==================== QDRANT ====================
    
    print("=" * 70)
    print("  3️⃣  QDRANT - Semantic Search")
    print("=" * 70)
    print()
    
    try:
        client = QdrantClient(url="http://localhost:6333")
        
        collections = client.get_collections()
        
        total_vectors = 0
        destiny_collections = []
        
        for collection in collections.collections:
            if 'destiny' in collection.name or 'integration' in collection.name:
                info = client.get_collection(collection.name)
                total_vectors += info.vectors_count or 0
                destiny_collections.append({
                    "name": collection.name,
                    "vectors": info.vectors_count or 0
                })
        
        print(f"✅ QDRANT Connected!")
        print(f"   Total collections: {len(collections.collections)}")
        print(f"   Destiny collections: {len(destiny_collections)}")
        print(f"   Total vectors: {total_vectors}")
        
        if destiny_collections:
            print(f"\n   Collections:")
            for col in destiny_collections[:5]:
                print(f"     • {col['name']}: {col['vectors']} vectors")
        
        if total_vectors > 0:
            results["qdrant"] = True
            print(f"\n   ✅ META-PROJECT DATA FOUND!")
        
    except Exception as e:
        print(f"❌ Qdrant: {e}")
    
    print()
    
    # ==================== REDIS ====================
    
    print("=" * 70)
    print("  4️⃣  REDIS - Hot Cache")
    print("=" * 70)
    print()
    
    try:
        redis = RedisCache(host="localhost", port=6379)
        
        all_keys = redis.client.keys("destiny:*")
        
        stats = redis.get_cache_stats()
        
        print(f"✅ REDIS Connected!")
        print(f"   Destiny keys: {len(all_keys)}")
        print(f"   Total keys: {stats['total_keys']}")
        print(f"   Memory: {stats['used_memory']}")
        print(f"   Hit rate: {stats['hit_rate']:.1f}%")
        
        if len(all_keys) > 0:
            results["redis"] = True
            print(f"   ✅ META-PROJECT DATA FOUND!")
            
            # Show some keys
            print(f"\n   Sample keys:")
            for key in list(all_keys)[:5]:
                print(f"     • {key.decode('utf-8')}")
        
        redis.close()
        
    except Exception as e:
        print(f"❌ Redis: {e}")
    
    print()
    
    # ==================== SUMMARY ====================
    
    print("=" * 70)
    print("  📊 VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    
    for layer, has_data in results.items():
        status = "✅ HAS DATA" if has_data else "⚪ EMPTY"
        print(f"  {status}: {layer.upper()}")
    
    print()
    
    data_count = sum(1 for v in results.values() if v)
    
    if data_count == 4:
        print("  🎉 ALL 4 LAYERS HAVE DATA!")
        print()
        print("  Meta-projekt (Destiny Team Framework) jest AKTYWNIE używany.")
        print("  Framework zarządza SWOIM WŁASNYM rozwojem!")
        print("  To jest prawdziwy META-PROJECT! 🚀")
    elif data_count > 0:
        print(f"  ✅ {data_count}/4 layers have data")
        print()
        print("  Część danych jest już w systemie.")
        print("  Framework częściowo operational.")
    else:
        print("  ⚪ No data yet")
        print()
        print("  System jest gotowy, ale jeszcze nie używany.")
        print("  Czas zacząć pierwszy projekt!")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    verify_all_layers()
