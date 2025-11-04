#!/usr/bin/env python3
"""
Qdrant Indexing for Analytical Team Documentation
Helena Kowalczyk - Knowledge Manager
"""

import os
import sys
import hashlib
from datetime import datetime

sys.path.insert(0, '/Users/artur/coursor-agents-destiny-folder')

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, VectorParams, Distance
except ImportError:
    print("❌ qdrant-client not installed")
    print("Run: python3 -m pip install --user qdrant-client")
    sys.exit(1)

def generate_mock_embedding(text, dimensions=768):
    """Generate consistent mock embedding from text"""
    hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
    # Generate deterministic values between -1 and 1
    embedding = []
    for i in range(dimensions):
        seed = (hash_val >> (i % 32)) + i
        value = ((seed % 200) - 100) / 100.0
        embedding.append(value)
    return embedding

def index_analytical_docs():
    """Index all analytical team documentation in Qdrant"""
    
    print("="*80)
    print(" "*20 + "QDRANT ANALYTICAL TEAM INDEXING")
    print("="*80)
    print()
    
    # Connect to Qdrant
    print("📊 Connecting to Qdrant (localhost:6333)...")
    try:
        client = QdrantClient(host="localhost", port=6333)
        print("   ✅ Connected")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Check/create collection
    collection_name = "destiny-team-framework-master"
    print(f"\n📚 Working with collection: {collection_name}")
    
    try:
        collections = client.get_collections().collections
        collection_exists = any(c.name == collection_name for c in collections)
        
        if collection_exists:
            print(f"   ✅ Collection exists")
        else:
            print(f"   ⚠️  Collection doesn't exist, creating...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )
            print(f"   ✅ Collection created")
    except Exception as e:
        print(f"   ❌ Collection check failed: {e}")
        return False
    
    # Documents to index
    base_path = "/Users/artur/coursor-agents-destiny-folder"
    docs_to_index = [
        ("ANALYTICAL_TEAM_ANNOUNCEMENT.md", "Analytical Team Launch", ["analytical", "team", "announcement"]),
        ("ANALYTICAL_TEAM_COMPLETE_SUMMARY.md", "Implementation Summary", ["analytical", "summary", "complete"]),
        ("ANALYTICAL_TEAM_QUICK_START.md", "Quick Start Guide", ["analytical", "guide", "quickstart"]),
        ("ANALYTICAL_TOOLKITS_DEEP_DIVE.md", "200+ Toolkit Functions", ["analytical", "toolkits", "functions"]),
        ("agents/analytical/TEAM_PROFILE.md", "Team Profile", ["analytical", "agents", "profiles"]),
        ("agents/analytical/PRIVACY_ARCHITECTURE.md", "Privacy Design", ["analytical", "privacy", "security"]),
        ("agents/analytical/INTEGRATION_STATUS.md", "Integration Status", ["analytical", "integration", "databases"]),
        ("agents/analytical/CROSS_TEAM_INTEGRATION.md", "Cross-Team Guide", ["analytical", "technical", "collaboration"]),
        ("agents/analytical/JINA_EMBEDDINGS_GUIDE.md", "Jina v4 Config", ["analytical", "embeddings", "jina"]),
        ("agents/analytical/44K_CONTEXT_ADVANTAGES.md", "44K Context Benefits", ["analytical", "context", "llm"]),
    ]
    
    indexed_count = 0
    total_docs = len(docs_to_index)
    
    print(f"\n📄 Indexing {total_docs} documents...")
    print()
    
    points_to_upsert = []
    
    for filepath, title, tags in docs_to_index:
        full_path = os.path.join(base_path, filepath)
        
        if not os.path.exists(full_path):
            print(f"  ⚠️  Skipping: {filepath} (not found)")
            continue
        
        print(f"  📄 {title}...")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate embedding
            embedding = generate_mock_embedding(content)
            
            # Create point
            point_id = filepath.replace("/", "-").replace(".md", "").replace(".", "-")
            
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "type": "analytical_documentation",
                    "title": title,
                    "filepath": filepath,
                    "content_preview": content[:500],
                    "full_content": content[:5000],  # Store first 5000 chars
                    "tags": tags,
                    "team": "analytical",
                    "indexed_by": "Helena Kowalczyk",
                    "indexed_at": datetime.now().isoformat(),
                    "word_count": len(content.split()),
                    "char_count": len(content)
                }
            )
            
            points_to_upsert.append(point)
            indexed_count += 1
            print(f"     ✅ Prepared ({len(content.split())} words)")
            
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    # Batch upsert
    if points_to_upsert:
        print(f"\n📤 Uploading {len(points_to_upsert)} points to Qdrant...")
        try:
            client.upsert(
                collection_name=collection_name,
                points=points_to_upsert
            )
            print(f"   ✅ Upload complete")
        except Exception as e:
            print(f"   ❌ Upload failed: {e}")
            return False
    
    # Verify
    print(f"\n🔍 Verifying collection...")
    try:
        collection_info = client.get_collection(collection_name)
        print(f"   ✅ Collection has {collection_info.points_count} total points")
        print(f"   ✅ {indexed_count} analytical docs indexed in this run")
    except Exception as e:
        print(f"   ⚠️  Verification failed: {e}")
    
    # Test search
    print(f"\n🔍 Testing semantic search...")
    try:
        test_query = "How to use OSINT capabilities?"
        test_embedding = generate_mock_embedding(test_query)
        
        results = client.search(
            collection_name=collection_name,
            query_vector=test_embedding,
            limit=3,
            query_filter={
                "must": [{"key": "team", "match": {"value": "analytical"}}]
            }
        )
        
        print(f"   Query: '{test_query}'")
        print(f"   Results: {len(results)} documents")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result.payload.get('title')} (score: {result.score:.4f})")
        
    except Exception as e:
        print(f"   ⚠️  Search test failed: {e}")
    
    print()
    print("="*80)
    print(f"✅ Qdrant indexing complete: {indexed_count}/{total_docs} documents")
    print("="*80)
    print()
    
    return True

if __name__ == "__main__":
    success = index_analytical_docs()
    sys.exit(0 if success else 1)
