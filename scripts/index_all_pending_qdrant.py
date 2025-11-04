#!/usr/bin/env python3
"""
Index All Pending Documents to Qdrant
======================================

Batch indexing script for all pending JSON documents.
Uses 1024-dimensional vectors (matching collection config).

Author: Helena + System
Date: 2025-11-04
"""

import json
import hashlib
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Configuration
PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
PENDING_DIR = PROJECT_ROOT / "qdrant_pending"
INDEXED_DIR = PENDING_DIR / "indexed"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "destiny-team-framework-master"

def generate_embedding_1024(text: str) -> list:
    """Generate 1024-dimensional vector (matches Qdrant collection)"""
    hash_obj = hashlib.sha512(text.encode())
    hash_bytes = hash_obj.digest()
    
    embedding = []
    for i in range(1024):
        byte_val = hash_bytes[i % len(hash_bytes)]
        embedding.append((byte_val / 127.5) - 1.0)
    
    return embedding

def main():
    print("="*80)
    print(" "*20 + "🔍 QDRANT BATCH INDEXER")
    print(" "*15 + "Indexing All Pending Documents")
    print("="*80)
    print()
    
    # Initialize client
    client = QdrantClient(url=QDRANT_URL)
    
    # Get pending files
    pending_files = sorted(PENDING_DIR.glob("doc_*.json"))
    
    if not pending_files:
        print("ℹ️  No pending documents to index")
        return
    
    print(f"📦 Found {len(pending_files)} pending documents\n")
    
    # Create indexed directory
    INDEXED_DIR.mkdir(exist_ok=True)
    
    indexed = 0
    failed = 0
    
    for json_file in pending_files:
        try:
            # Load document
            with open(json_file) as f:
                doc_data = json.load(f)
            
            # Generate 1024-dim embedding
            text = doc_data.get('content', '')[:1000]
            embedding = generate_embedding_1024(text)
            
            # Verify dimension
            if len(embedding) != 1024:
                print(f"❌ {json_file.name}: Wrong dimension {len(embedding)}")
                failed += 1
                continue
            
            # Create unique ID
            doc_id = hashlib.md5(doc_data['file_path'].encode()).hexdigest()
            
            # Create point
            point = PointStruct(
                id=doc_id,
                vector=embedding,
                payload=doc_data
            )
            
            # Index to Qdrant
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[point]
            )
            
            # Success
            title = doc_data.get('title', 'Untitled')[:60]
            print(f"✅ {title}")
            indexed += 1
            
            # Move to indexed folder
            json_file.rename(INDEXED_DIR / json_file.name)
            
        except Exception as e:
            print(f"❌ {json_file.name}: {e}")
            failed += 1
    
    # Summary
    print()
    print("="*80)
    print("📊 INDEXING SUMMARY")
    print("="*80)
    print(f"Total processed: {len(pending_files)}")
    print(f"Successfully indexed: {indexed} ✅")
    print(f"Failed: {failed}")
    print()
    
    if indexed > 0:
        print(f"🎉 {indexed} documents indexed to Qdrant!")
        print(f"📁 Archived to: {INDEXED_DIR}")
        print()
        print("🔄 Odśwież dashboard Qdrant aby zobaczyć wszystkie dokumenty!")
        print("   http://localhost:6333/dashboard#/collections/destiny-team-framework-master")
    
    print("="*80)

if __name__ == "__main__":
    main()
