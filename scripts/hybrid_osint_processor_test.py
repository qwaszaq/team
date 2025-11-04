#!/usr/bin/env python3
"""
Hybrid OSINT Processor - Test Run
===================================
Processes selected PDFs through the complete hybrid pipeline:
1. Elasticsearch (full-text search)
2. PostgreSQL (smart references + audit)
3. Neo4j (knowledge graph - NEW)
4. Qdrant (semantic embeddings - optional)
5. Redis (agent context cache)

Verifies proper OSINT data separation from project data.
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess

# Add project root to path
sys.path.insert(0, '/Users/artur/coursor-agents-destiny-folder')

try:
    import psycopg2
    from psycopg2.extras import Json, DictCursor
    import requests
    from neo4j import GraphDatabase
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install: pip install psycopg2-binary requests neo4j")
    sys.exit(1)

class HybridOSINTProcessor:
    """Processes OSINT documents through all data layers"""
    
    def __init__(self):
        # Connection parameters
        self.es_url = "http://localhost:9200"
        self.es_auth = ("elastic", "changeme123")
        self.pg_conn_params = {
            "host": "localhost",
            "database": "destiny_team",
            "user": "user",
            "password": "password"
        }
        self.neo4j_uri = "bolt://localhost:7687"
        self.neo4j_auth = ("neo4j", "password")
        self.qdrant_url = "http://localhost:6333"
        
        # Jina embeddings via local LM Studio server
        self.lmstudio_url = "http://localhost:1234/v1/embeddings"
        self.jina_model = "jinaai/jina-embeddings-v3"  # Model loaded in LM Studio
        
        # OSINT separation markers
        self.osint_project_id = "investigation-grupaazoty_financial_001"
        self.osint_tags = ["osint", "financial_reports", "grupa_azoty", "test_batch"]
        
        # Qdrant collection name
        self.qdrant_collection = "osint_financial_documents"
        
        # Stats
        self.stats = {
            "processed": 0,
            "elasticsearch_indexed": 0,
            "postgres_referenced": 0,
            "neo4j_created": 0,
            "qdrant_embedded": 0,
            "errors": []
        }
    
    def get_test_documents(self, count=4):
        """Get list of PDFs to process (test batch)"""
        pdf_dir = Path("/Users/artur/coursor-agents-destiny-folder/investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs")
        
        if not pdf_dir.exists():
            print(f"❌ PDF directory not found: {pdf_dir}")
            return []
        
        pdfs = sorted(pdf_dir.glob("*.pdf"))[:count]
        print(f"📄 Found {len(pdfs)} PDFs for test processing")
        return pdfs
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF using PyMuPDF"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text[:10000]  # Limit to first 10k chars for test
        except ImportError:
            print("⚠️  PyMuPDF not installed, using basic extraction")
            return f"[Text from {pdf_path.name}]"
        except Exception as e:
            print(f"⚠️  Error extracting text: {e}")
            return ""
    
    def index_to_elasticsearch(self, pdf_path, text):
        """Index document to Elasticsearch"""
        try:
            # Calculate document ID
            file_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            doc_id = f"grupaazoty_{pdf_path.stem}"
            
            # Prepare document
            doc = {
                "filename": pdf_path.name,
                "issuer": "Grupa Azoty S.A.",
                "source_url": f"file://{pdf_path}",
                "downloaded_at": datetime.now().isoformat(),
                "file_size_bytes": pdf_path.stat().st_size,
                "sha256": file_hash,
                "content": text,
                "content_length": len(text),
                # OSINT separation
                "document_type": "osint_financial_report",
                "investigation_id": self.osint_project_id,
                "tags": self.osint_tags,
                "metadata": {
                    "data_scope": "investigation",
                    "usage_scope": "osint_analysis",
                    "visibility": "investigation_team"
                }
            }
            
            # Index to ES
            url = f"{self.es_url}/grupaazoty_reports/_doc/{doc_id}"
            response = requests.put(url, json=doc, auth=self.es_auth)
            response.raise_for_status()
            
            print(f"  ✅ Elasticsearch: {doc_id}")
            self.stats["elasticsearch_indexed"] += 1
            return doc_id, doc
            
        except Exception as e:
            error = f"Elasticsearch indexing failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ❌ {error}")
            return None, None
    
    def create_postgres_reference(self, es_doc_id, doc):
        """Create smart reference in PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.pg_conn_params)
            cur = conn.cursor()
            
            # Insert into es_document_references
            cur.execute("""
                INSERT INTO es_document_references (
                    es_doc_id, es_index, filename, issuer, doc_date,
                    doc_type, source_url, file_size_bytes, sha256,
                    tags, investigation_id, metadata, indexed_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (es_doc_id, es_index) DO UPDATE SET
                    updated_at = CURRENT_TIMESTAMP,
                    tags = EXCLUDED.tags,
                    metadata = EXCLUDED.metadata
                RETURNING ref_id
            """, (
                es_doc_id,
                "grupaazoty_reports",
                doc["filename"],
                doc["issuer"],
                None,  # doc_date - could parse from filename
                doc["document_type"],
                doc["source_url"],
                doc["file_size_bytes"],
                doc["sha256"],
                self.osint_tags,
                self.osint_project_id,
                Json(doc["metadata"]),
                datetime.now()
            ))
            
            ref_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            print(f"  ✅ PostgreSQL: ref_id={ref_id}")
            self.stats["postgres_referenced"] += 1
            return ref_id
            
        except Exception as e:
            error = f"PostgreSQL reference creation failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ❌ {error}")
            return None
    
    def create_neo4j_document_node(self, es_doc_id, doc, ref_id):
        """Create Document node in Neo4j with proper OSINT separation"""
        try:
            driver = GraphDatabase.driver(self.neo4j_uri, auth=self.neo4j_auth)
            
            with driver.session() as session:
                # Create Document node with OSINT tags
                result = session.run("""
                    MERGE (d:Document:OSINTDocument {es_doc_id: $es_doc_id})
                    SET d.filename = $filename,
                        d.issuer = $issuer,
                        d.doc_type = $doc_type,
                        d.source_url = $source_url,
                        d.file_size_bytes = $file_size_bytes,
                        d.sha256 = $sha256,
                        d.pg_ref_id = $ref_id,
                        d.investigation_id = $investigation_id,
                        d.tags = $tags,
                        d.data_scope = $data_scope,
                        d.created_at = datetime($created_at),
                        d.updated_at = datetime()
                    
                    // Link to Investigation context (if exists)
                    WITH d
                    OPTIONAL MATCH (ctx:Context {project_id: $investigation_id})
                    FOREACH (c IN CASE WHEN ctx IS NOT NULL THEN [ctx] ELSE [] END |
                        MERGE (d)-[:PART_OF_INVESTIGATION]->(c)
                    )
                    
                    RETURN d.es_doc_id as doc_id, id(d) as node_id
                """, {
                    "es_doc_id": es_doc_id,
                    "filename": doc["filename"],
                    "issuer": doc["issuer"],
                    "doc_type": doc["document_type"],
                    "source_url": doc["source_url"],
                    "file_size_bytes": doc["file_size_bytes"],
                    "sha256": doc["sha256"],
                    "ref_id": ref_id,
                    "investigation_id": self.osint_project_id,
                    "tags": self.osint_tags,
                    "data_scope": "investigation",
                    "created_at": datetime.now().isoformat()
                })
                
                record = result.single()
                node_id = record["node_id"] if record else None
                
            driver.close()
            
            print(f"  ✅ Neo4j: Document node (id={node_id})")
            self.stats["neo4j_created"] += 1
            return node_id
            
        except Exception as e:
            error = f"Neo4j node creation failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ❌ {error}")
            return None
    
    def generate_jina_embedding(self, text):
        """Generate embedding using local LM Studio server (Jina model)"""
        try:
            # Truncate text to reasonable length (Jina v3 supports 8k tokens)
            text_truncated = text[:8000] if len(text) > 8000 else text
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.jina_model,
                "input": text_truncated  # LM Studio expects string, not array
            }
            
            response = requests.post(self.lmstudio_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # LM Studio returns OpenAI-compatible format
            if "data" in result and len(result["data"]) > 0:
                embedding = result["data"][0]["embedding"]
            else:
                raise ValueError("Invalid response format from LM Studio")
            
            return embedding
            
        except Exception as e:
            error = f"Jina embedding generation failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ⚠️  {error}")
            return None
    
    def ensure_qdrant_collection(self):
        """Ensure Qdrant collection exists with proper schema"""
        try:
            # Check if collection exists
            response = requests.get(f"{self.qdrant_url}/collections/{self.qdrant_collection}")
            
            if response.status_code == 404:
                # Create collection (Jina v3 embeddings: auto-detect dimension from first embedding)
                print(f"📦 Creating Qdrant collection: {self.qdrant_collection}")
                # Test embedding to get dimension size
                test_embedding = self.generate_jina_embedding("test")
                if not test_embedding:
                    print(f"  ⚠️  Could not determine embedding dimension")
                    return
                
                embedding_dim = len(test_embedding)
                print(f"  📏 Detected embedding dimension: {embedding_dim}")
                
                collection_config = {
                    "vectors": {
                        "size": embedding_dim,  # Auto-detected from Jina model
                        "distance": "Cosine"
                    }
                }
                response = requests.put(
                    f"{self.qdrant_url}/collections/{self.qdrant_collection}",
                    json=collection_config
                )
                response.raise_for_status()
                print(f"  ✅ Collection created with dimension {embedding_dim}")
            else:
                print(f"  ✅ Collection {self.qdrant_collection} already exists")
            
        except Exception as e:
            error = f"Qdrant collection setup failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ⚠️  {error}")
    
    def index_to_qdrant(self, es_doc_id, doc, text, neo4j_node_id):
        """Index document to Qdrant with Jina embeddings"""
        try:
            # Generate embedding
            print("  🧠 Generating Jina embedding...")
            embedding = self.generate_jina_embedding(text)
            if not embedding:
                return None
            
            # Prepare point
            point = {
                "id": hash(es_doc_id) & 0x7FFFFFFFFFFFFFFF,  # Convert to positive int64
                "vector": embedding,
                "payload": {
                    "es_doc_id": es_doc_id,
                    "filename": doc["filename"],
                    "issuer": doc["issuer"],
                    "doc_type": doc["document_type"],
                    "investigation_id": self.osint_project_id,
                    "tags": self.osint_tags,
                    "neo4j_node_id": neo4j_node_id,
                    "text_preview": text[:500],
                    "indexed_at": datetime.now().isoformat()
                }
            }
            
            # Upsert to Qdrant
            response = requests.put(
                f"{self.qdrant_url}/collections/{self.qdrant_collection}/points",
                json={"points": [point]}
            )
            response.raise_for_status()
            
            print(f"  ✅ Qdrant: Vector indexed (dim={len(embedding)})")
            self.stats["qdrant_embedded"] += 1
            return point["id"]
            
        except Exception as e:
            error = f"Qdrant indexing failed: {e}"
            self.stats["errors"].append(error)
            print(f"  ❌ {error}")
            return None
    
    def verify_osint_separation(self):
        """Verify that OSINT data is properly separated from project data"""
        print("\n" + "="*80)
        print("🔍 VERIFICATION: OSINT Data Separation")
        print("="*80)
        
        issues = []
        
        # Check Neo4j
        try:
            driver = GraphDatabase.driver(self.neo4j_uri, auth=self.neo4j_auth)
            with driver.session() as session:
                # Count OSINT documents
                result = session.run("""
                    MATCH (d:OSINTDocument)
                    WHERE d.investigation_id = $investigation_id
                    RETURN count(d) as osint_count
                """, {"investigation_id": self.osint_project_id})
                osint_count = result.single()["osint_count"]
                
                # Count project documents (should not have OSINT tags)
                result = session.run("""
                    MATCH (d:Document)
                    WHERE NOT d:OSINTDocument
                    AND (d.investigation_id IS NULL OR d.investigation_id <> $investigation_id)
                    RETURN count(d) as project_count
                """, {"investigation_id": self.osint_project_id})
                project_count = result.single()["project_count"]
                
                print(f"\n📊 Neo4j:")
                print(f"  OSINT Documents: {osint_count}")
                print(f"  Project Documents: {project_count}")
                
                if osint_count == 0:
                    issues.append("⚠️  No OSINT documents found in Neo4j")
                else:
                    print(f"  ✅ OSINT documents properly tagged")
                
                # Check for mixed tags
                result = session.run("""
                    MATCH (d:Document)
                    WHERE d:OSINTDocument AND (d.data_scope <> 'investigation' OR d.investigation_id IS NULL)
                    RETURN count(d) as mixed_count
                """)
                mixed_count = result.single()["mixed_count"]
                
                if mixed_count > 0:
                    issues.append(f"⚠️  {mixed_count} documents have inconsistent OSINT tagging")
                else:
                    print(f"  ✅ No mixed/inconsistent tagging detected")
            
            driver.close()
            
        except Exception as e:
            issues.append(f"❌ Neo4j verification failed: {e}")
        
        # Check PostgreSQL
        try:
            conn = psycopg2.connect(**self.pg_conn_params)
            cur = conn.cursor(cursor_factory=DictCursor)
            
            # Count OSINT references
            cur.execute("""
                SELECT COUNT(*) as osint_count
                FROM es_document_references
                WHERE investigation_id = %s
            """, (self.osint_project_id,))
            osint_count = cur.fetchone()["osint_count"]
            
            # Count project messages (should not have osint tag)
            cur.execute("""
                SELECT COUNT(*) as project_count
                FROM messages
                WHERE 'osint' = ANY(tags) = FALSE
            """)
            project_count = cur.fetchone()["project_count"]
            
            print(f"\n📊 PostgreSQL:")
            print(f"  OSINT References: {osint_count}")
            print(f"  Project Messages: {project_count}")
            
            if osint_count == 0:
                issues.append("⚠️  No OSINT references found in PostgreSQL")
            else:
                print(f"  ✅ OSINT references properly stored")
            
            cur.close()
            conn.close()
            
        except Exception as e:
            issues.append(f"❌ PostgreSQL verification failed: {e}")
        
        # Check Elasticsearch
        try:
            # Count OSINT documents
            response = requests.get(
                f"{self.es_url}/grupaazoty_reports/_count",
                json={"query": {"term": {"investigation_id": self.osint_project_id}}},
                auth=self.es_auth
            )
            response.raise_for_status()
            osint_count = response.json()["count"]
            
            print(f"\n📊 Elasticsearch:")
            print(f"  OSINT Documents: {osint_count}")
            
            if osint_count == 0:
                issues.append("⚠️  No OSINT documents found in Elasticsearch")
            else:
                print(f"  ✅ OSINT documents indexed with investigation_id")
            
        except Exception as e:
            issues.append(f"❌ Elasticsearch verification failed: {e}")
        
        # Summary
        print("\n" + "="*80)
        if issues:
            print("⚠️  ISSUES DETECTED:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("✅ VERIFICATION PASSED: OSINT data properly separated from project data")
            print("\nKey separation mechanisms:")
            print("  • investigation_id: Unique identifier for OSINT investigation")
            print("  • OSINTDocument label: Explicit Neo4j node type")
            print("  • data_scope='investigation': Metadata flag")
            print("  • tags=['osint', ...]: Searchable tags in all layers")
            return True
    
    def process_documents(self):
        """Process test batch of documents through hybrid pipeline"""
        print("="*80)
        print("🚀 HYBRID OSINT PROCESSOR - Test Run with Jina AI Embeddings")
        print("="*80)
        print(f"Investigation ID: {self.osint_project_id}")
        print(f"OSINT Tags: {self.osint_tags}")
        print(f"Jina Model: {self.jina_model}")
        print()
        
        # Ensure Qdrant collection exists
        print("🔧 Setting up Qdrant collection...")
        self.ensure_qdrant_collection()
        print()
        
        # Get test documents
        pdfs = self.get_test_documents(count=4)
        if not pdfs:
            print("❌ No PDFs found for processing")
            return
        
        # Process each document
        for i, pdf_path in enumerate(pdfs, 1):
            print(f"\n[{i}/{len(pdfs)}] Processing: {pdf_path.name}")
            print("-" * 80)
            
            # Extract text
            print("  📄 Extracting text...")
            text = self.extract_pdf_text(pdf_path)
            
            # 1. Elasticsearch
            print("  🔍 Indexing to Elasticsearch...")
            es_doc_id, doc = self.index_to_elasticsearch(pdf_path, text)
            if not es_doc_id:
                continue
            
            # 2. PostgreSQL
            print("  🗄️  Creating PostgreSQL reference...")
            ref_id = self.create_postgres_reference(es_doc_id, doc)
            if not ref_id:
                continue
            
            # 3. Neo4j (NEW!)
            print("  🕸️  Creating Neo4j Document node...")
            node_id = self.create_neo4j_document_node(es_doc_id, doc, ref_id)
            
            # 4. Qdrant with Jina embeddings (NEW!)
            print("  🎯 Creating Qdrant vector with Jina AI...")
            qdrant_id = self.index_to_qdrant(es_doc_id, doc, text, node_id)
            
            self.stats["processed"] += 1
            layers_count = sum([
                self.stats["elasticsearch_indexed"] > 0,
                self.stats["postgres_referenced"] > 0,
                self.stats["neo4j_created"] > 0,
                self.stats["qdrant_embedded"] > 0
            ])
            print(f"  ✅ Successfully processed through {layers_count} layers")
        
        # Print stats
        self.print_stats()
        
        # Verify separation
        self.verify_osint_separation()
    
    def print_stats(self):
        """Print processing statistics"""
        print("\n" + "="*80)
        print("📊 PROCESSING STATISTICS")
        print("="*80)
        print(f"Documents processed: {self.stats['processed']}")
        print(f"Elasticsearch indexed: {self.stats['elasticsearch_indexed']}")
        print(f"PostgreSQL referenced: {self.stats['postgres_referenced']}")
        print(f"Neo4j nodes created: {self.stats['neo4j_created']}")
        print(f"Qdrant embeddings: {self.stats['qdrant_embedded']}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5
                print(f"  • {error}")

def main():
    processor = HybridOSINTProcessor()
    processor.process_documents()

if __name__ == "__main__":
    main()
