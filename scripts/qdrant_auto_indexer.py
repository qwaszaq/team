#!/usr/bin/env python3
"""
Qdrant Auto-Indexer
===================

Automatically indexes pending documents from qdrant_pending/ to Qdrant.
Runs continuously or as a one-shot batch process.

Author: Helena + System
Created: 2025-11-04
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import requests

PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
PENDING_DIR = PROJECT_ROOT / "qdrant_pending"
ARCHIVE_DIR = PENDING_DIR / "indexed"
FAILED_DIR = PENDING_DIR / "failed"

# Qdrant configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "destiny-team-framework-master"


class QdrantAutoIndexer:
    """Automatically indexes pending documents to Qdrant"""
    
    def __init__(self):
        self.qdrant_url = QDRANT_URL
        self.collection_name = COLLECTION_NAME
        self.indexed_count = 0
        self.failed_count = 0
        
        # Create directories
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        FAILED_DIR.mkdir(parents=True, exist_ok=True)
        
    def check_qdrant_available(self) -> bool:
        """Check if Qdrant is accessible"""
        try:
            response = requests.get(f"{self.qdrant_url}/collections", timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def ensure_collection_exists(self) -> bool:
        """Ensure collection exists, create if needed"""
        try:
            # Check if collection exists
            response = requests.get(
                f"{self.qdrant_url}/collections/{self.collection_name}",
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Collection '{self.collection_name}' exists")
                return True
            elif response.status_code == 404:
                # Create collection
                print(f"📦 Creating collection '{self.collection_name}'...")
                
                create_response = requests.put(
                    f"{self.qdrant_url}/collections/{self.collection_name}",
                    json={
                        "vectors": {
                            "size": 384,  # Jina embeddings size
                            "distance": "Cosine"
                        }
                    },
                    timeout=10
                )
                
                if create_response.status_code in [200, 201]:
                    print(f"✅ Collection created successfully")
                    return True
                else:
                    print(f"❌ Failed to create collection: {create_response.text}")
                    return False
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking/creating collection: {e}")
            return False
            
    def generate_simple_embedding(self, text: str) -> List[float]:
        """Generate simple hash-based embedding (fallback when no embedding service)"""
        # This is a simple fallback - in production you'd use actual embeddings
        # For now, we'll use a deterministic hash-based approach
        import hashlib
        
        # Create 384-dimensional vector based on text hash
        hash_obj = hashlib.sha384(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert bytes to floats in range [-1, 1]
        embedding = []
        for i in range(0, len(hash_bytes), 1):
            # Normalize byte value to [-1, 1] range
            val = (hash_bytes[i] / 127.5) - 1.0
            embedding.append(val)
            
        return embedding
        
    def index_document(self, doc_file: Path) -> bool:
        """Index a single document to Qdrant"""
        try:
            # Load document
            with open(doc_file, 'r') as f:
                doc_data = json.load(f)
                
            # Extract key fields
            file_path = doc_data.get('file_path', '')
            title = doc_data.get('title', 'Untitled')
            content = doc_data.get('content', '')
            doc_type = doc_data.get('document_type', 'unknown')
            
            if not content:
                print(f"  ⚠️  Empty content in {doc_file.name}")
                return False
                
            # Generate embedding (simple fallback for now)
            # In production, you'd call Jina AI API or local embedding model
            embedding = self.generate_simple_embedding(content[:1000])
            
            # Create unique ID from file path
            import hashlib
            doc_id = hashlib.md5(file_path.encode()).hexdigest()
            
            # Prepare point for Qdrant
            point = {
                "id": doc_id,
                "vector": embedding,
                "payload": {
                    "file_path": file_path,
                    "title": title,
                    "document_type": doc_type,
                    "content": content,
                    "indexed_at": datetime.now().isoformat(),
                    "source": "auto_indexer"
                }
            }
            
            # Index to Qdrant
            response = requests.put(
                f"{self.qdrant_url}/collections/{self.collection_name}/points",
                json={
                    "points": [point]
                },
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✅ Indexed: {title[:50]}")
                self.indexed_count += 1
                
                # Move to archive
                archive_path = ARCHIVE_DIR / doc_file.name
                doc_file.rename(archive_path)
                
                return True
            else:
                print(f"  ❌ Failed to index: {response.status_code} - {response.text[:200]}")
                self.failed_count += 1
                
                # Move to failed
                failed_path = FAILED_DIR / doc_file.name
                doc_file.rename(failed_path)
                
                return False
                
        except Exception as e:
            print(f"  ❌ Error indexing {doc_file.name}: {e}")
            self.failed_count += 1
            
            # Move to failed
            try:
                failed_path = FAILED_DIR / doc_file.name
                doc_file.rename(failed_path)
            except:
                pass
                
            return False
            
    def process_pending_documents(self) -> int:
        """Process all pending documents"""
        
        # Get all pending JSON files
        pending_files = list(PENDING_DIR.glob("doc_*.json"))
        
        if not pending_files:
            print("ℹ️  No pending documents to index")
            return 0
            
        print(f"\n📊 Found {len(pending_files)} pending documents")
        print(f"🎯 Target: {self.qdrant_url}/collections/{self.collection_name}")
        print()
        
        # Index each document
        for doc_file in pending_files:
            print(f"📄 Processing: {doc_file.name}")
            self.index_document(doc_file)
            
        return len(pending_files)
        
    def run(self):
        """Main run loop"""
        
        print("="*80)
        print(" "*25 + "🔍 QDRANT AUTO-INDEXER")
        print(" "*20 + "Automatic Document Indexing")
        print("="*80)
        print()
        
        # Check Qdrant
        print("🔍 Checking Qdrant availability...")
        if not self.check_qdrant_available():
            print("❌ Qdrant is not available at " + self.qdrant_url)
            print("   Start Qdrant or check connection")
            return 1
            
        print(f"✅ Qdrant is available")
        print()
        
        # Ensure collection exists
        if not self.ensure_collection_exists():
            print("❌ Could not ensure collection exists")
            return 1
            
        print()
        
        # Process pending documents
        processed = self.process_pending_documents()
        
        # Summary
        print()
        print("="*80)
        print("📊 INDEXING SUMMARY")
        print("="*80)
        print(f"Documents processed: {processed}")
        print(f"Successfully indexed: {self.indexed_count}")
        print(f"Failed: {self.failed_count}")
        print()
        
        if self.indexed_count > 0:
            print(f"✅ {self.indexed_count} documents indexed to Qdrant!")
            print(f"📁 Archived to: {ARCHIVE_DIR}")
        
        if self.failed_count > 0:
            print(f"⚠️  {self.failed_count} documents failed")
            print(f"📁 Check: {FAILED_DIR}")
            
        print("="*80)
        print()
        
        return 0 if self.failed_count == 0 else 1


def main():
    """Main entry point"""
    
    indexer = QdrantAutoIndexer()
    
    try:
        exit_code = indexer.run()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
