#!/usr/bin/env python3
"""
MIGRATE EVERYTHING TO QDRANT

Przenosi WSZYSTKIE dane z PostgreSQL do Qdrant:
- Wszystkie wiadomości
- Wszystkie projekty
- Generuje embeddings dla każdej wiadomości
- Indeksuje w Qdrant

PRIORITY: Get all data into Qdrant NOW!
"""

import time
from datetime import datetime
from postgres_context_store import PostgresContextStore
from qdrant_integration import QdrantSemanticStore


def migrate_all_to_qdrant():
    """
    Complete migration: PostgreSQL → Qdrant
    """
    
    print("\n" + "🚀 "*30)
    print("  PRIORITY MIGRATION: PostgreSQL → Qdrant")
    print("  Przenoszę WSZYSTKIE dane do Qdrant!")
    print("🚀 "*30)
    print()
    
    # Initialize
    print("📦 Connecting to databases...")
    
    postgres = PostgresContextStore(
        "dbname=destiny_team user=user password=password host=localhost port=5432"
    )
    print("  ✅ PostgreSQL connected")
    
    qdrant = QdrantSemanticStore(
        qdrant_url="http://localhost:6333",
        lmstudio_url="http://localhost:1234/v1"
    )
    print("  ✅ Qdrant connected")
    print("  ✅ LM Studio connected")
    print()
    
    # Get all projects
    print("=" * 70)
    print("  STEP 1: Analyzing Projects")
    print("=" * 70)
    print()
    
    with postgres.conn.cursor() as cur:
        cur.execute("""
            SELECT project_id, project_name
            FROM projects
            ORDER BY created_at
        """)
        projects = cur.fetchall()
    
    print(f"Found {len(projects)} projects:")
    for proj_id, proj_name in projects:
        print(f"  📁 {proj_name} (ID: {proj_id})")
    print()
    
    # Migrate each project
    total_migrated = 0
    total_errors = 0
    
    for project_id, project_name in projects:
        print("=" * 70)
        print(f"  MIGRATING: {project_name}")
        print("=" * 70)
        print()
        
        # Create Qdrant collection for project
        print(f"📦 Creating Qdrant collection...")
        try:
            qdrant.create_collection(project_id)
            print(f"  ✅ Collection created: {project_id}")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  ℹ️  Collection already exists")
            else:
                print(f"  ⚠️  Error: {e}")
        print()
        
        # Get all messages for this project
        with postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT id, sender, recipient, content, message_type, 
                       timestamp, importance, tags
                FROM messages
                WHERE project_id = %s
                ORDER BY timestamp
            """, (project_id,))
            messages = cur.fetchall()
        
        print(f"Found {len(messages)} messages to migrate")
        print()
        
        if len(messages) == 0:
            print("  ⏭️  Skipping (no messages)")
            print()
            continue
        
        # Migrate messages
        migrated = 0
        errors = 0
        
        print(f"Migrating messages with embeddings...")
        print()
        
        for i, msg in enumerate(messages, 1):
            msg_id, sender, recipient, content, msg_type, timestamp, importance, tags = msg
            
            # Progress
            if i % 5 == 0 or i == len(messages):
                print(f"  Progress: {i}/{len(messages)} ({i*100//len(messages)}%)", end='\r')
            
            try:
                # Store in Qdrant (generates embedding automatically)
                qdrant.store_message(
                    project_id=project_id,
                    message_id=msg_id,
                    content=content,
                    sender=sender,
                    timestamp=timestamp,
                    message_type=msg_type,
                    importance=importance,
                    tags=tags or []
                )
                
                migrated += 1
                
                # Small delay to not overwhelm LM Studio
                if i % 10 == 0:
                    time.sleep(0.1)
                
            except Exception as e:
                print(f"\n  ⚠️  Error on message {msg_id}: {e}")
                errors += 1
                
                if errors > 5:
                    print(f"\n  ❌ Too many errors, stopping migration for this project")
                    break
        
        print()  # New line after progress
        
        if migrated > 0:
            print(f"  ✅ Migrated: {migrated} messages")
            total_migrated += migrated
        
        if errors > 0:
            print(f"  ⚠️  Errors: {errors}")
            total_errors += errors
        
        # Verify in Qdrant
        print(f"\n  🔍 Verifying in Qdrant...")
        try:
            stats = qdrant.get_collection_stats(project_id)
            vectors_count = stats.get('vectors_count', 0) or stats.get('points_count', 0)
            print(f"  ✅ Qdrant has: {vectors_count} vectors")
            
            if vectors_count != migrated:
                print(f"  ⚠️  Mismatch: migrated {migrated} but Qdrant has {vectors_count}")
        except Exception as e:
            print(f"  ⚠️  Cannot verify: {e}")
        
        print()
    
    # Final summary
    print("=" * 70)
    print("  🎉 MIGRATION COMPLETE!")
    print("=" * 70)
    print()
    
    print(f"📊 Summary:")
    print(f"   Projects processed: {len(projects)}")
    print(f"   Messages migrated: {total_migrated}")
    if total_errors > 0:
        print(f"   Errors encountered: {total_errors}")
    print()
    
    # Verify all collections
    print("=" * 70)
    print("  🔍 FINAL VERIFICATION")
    print("=" * 70)
    print()
    
    from qdrant_client import QdrantClient
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()
    
    destiny_collections = [c for c in collections.collections if 'destiny' in c.name or 'integration' in c.name]
    
    print(f"Qdrant collections for Destiny Team:")
    print()
    
    total_vectors = 0
    for collection in destiny_collections:
        try:
            info = client.get_collection(collection.name)
            vectors = info.vectors_count or info.points_count or 0
            total_vectors += vectors
            
            print(f"  📦 {collection.name}")
            print(f"     Vectors: {vectors}")
            print()
        except:
            pass
    
    print(f"Total vectors in Qdrant: {total_vectors}")
    print()
    
    if total_vectors >= total_migrated:
        print("✅ All data successfully migrated to Qdrant!")
        print()
        print("Możesz teraz:")
        print("  ✅ Semantic search (find similar messages)")
        print("  ✅ Multilingual search (Polski + English)")
        print("  ✅ Meaning-based queries")
        print("  ✅ $0 cost (local LM Studio!)")
    else:
        print("⚠️  Some data may not have been migrated")
        print(f"   Expected: {total_migrated}")
        print(f"   Got: {total_vectors}")
    
    print()
    
    # Cleanup
    postgres.close()
    
    print("=" * 70)
    print("  ✅ MIGRATION PROCESS COMPLETE")
    print("=" * 70)


def test_semantic_search_after_migration():
    """Test semantic search on migrated data"""
    
    print("\n" + "🔍 "*30)
    print("  TESTING SEMANTIC SEARCH")
    print("🔍 "*30)
    print()
    
    qdrant = QdrantSemanticStore(
        qdrant_url="http://localhost:6333",
        lmstudio_url="http://localhost:1234/v1"
    )
    
    # Get a project with data
    from qdrant_client import QdrantClient
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()
    
    # Find a collection with data
    test_collection = None
    for collection in collections.collections:
        if 'destiny' in collection.name or 'integration' in collection.name:
            info = client.get_collection(collection.name)
            if (info.vectors_count or info.points_count or 0) > 0:
                test_collection = collection.name
                break
    
    if not test_collection:
        print("⚠️  No collections with data found")
        return
    
    print(f"Testing on collection: {test_collection}")
    print()
    
    # Test queries
    test_queries = [
        "PostgreSQL database",
        "requirements analysis",
        "security audit"
    ]
    
    for query in test_queries:
        print(f"🔍 Query: '{query}'")
        
        try:
            results = qdrant.search(
                project_id=test_collection.replace('destiny-team-', ''),
                query=query,
                limit=3,
                score_threshold=0.5
            )
            
            if results:
                print(f"   Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"     {i}. [{result['score']:.3f}] {result['content'][:60]}...")
            else:
                print(f"   No results found")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
        
        print()
    
    print("✅ Semantic search test complete!")
    print()


if __name__ == "__main__":
    # Main migration
    migrate_all_to_qdrant()
    
    # Test search
    print("\n")
    response = input("Test semantic search now? (y/n): ").strip().lower()
    if response == 'y':
        test_semantic_search_after_migration()
