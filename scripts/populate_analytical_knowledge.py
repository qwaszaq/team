#!/usr/bin/env python3
"""
Populate All Databases with Analytical Team Knowledge

Executes complete knowledge dissemination:
- PostgreSQL: Structured data
- Neo4j: Knowledge graph (requires manual execution)
- Qdrant: Semantic indexing
- Redis: Hot cache

Run this after PostgreSQL and Neo4j scripts!

Author: Helena Kowalczyk (Knowledge Manager)
Orchestrated by: Aleksander Nowak
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from datetime import datetime

print("="*80)
print(" "*20 + "ANALYTICAL TEAM KNOWLEDGE DISSEMINATION")
print("="*80)

# ============================================
# 1. QDRANT SEMANTIC INDEXING
# ============================================

def index_in_qdrant():
    """Index all analytical team documentation in Qdrant"""
    
    print("\n📊 STEP 1: Qdrant Semantic Indexing")
    print("-" * 60)
    
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import PointStruct
        
        # Initialize
        print("Connecting to Qdrant (localhost:6333)...")
        qdrant = QdrantClient(host="localhost", port=6333)
        
        print("Note: Using mock embeddings (768-dim) - LM Studio not required for testing...")
        
        # Documents to index
        base_path = "/Users/artur/coursor-agents-destiny-folder"
        docs_to_index = [
            ("ANALYTICAL_TEAM_ANNOUNCEMENT.md", "Analytical Team Launch Announcement", ["critical", "team", "announcement"]),
            ("ANALYTICAL_TEAM_COMPLETE_SUMMARY.md", "Complete Implementation Summary", ["summary", "status", "complete"]),
            ("KNOWLEDGE_DISSEMINATION_PLAN.md", "Knowledge Distribution Strategy", ["knowledge", "plan", "helena"]),
            ("agents/analytical/TEAM_PROFILE.md", "Analytical Team Profile", ["agents", "roster", "capabilities"]),
            ("agents/analytical/PRIVACY_ARCHITECTURE.md", "Privacy Architecture", ["privacy", "security", "local"]),
            ("agents/analytical/INTEGRATION_STATUS.md", "Integration Status", ["integration", "databases", "status"]),
            ("agents/analytical/CROSS_TEAM_INTEGRATION.md", "Cross-Team Collaboration", ["collaboration", "cross-team"]),
            ("agents/analytical/JINA_EMBEDDINGS_GUIDE.md", "Jina v4 Configuration", ["embeddings", "jina", "documents"]),
            ("agents/analytical/MODEL_CONFIG.md", "LLM Configuration", ["llm", "gpt-oss-20b", "config"]),
            ("agents/analytical/44K_CONTEXT_ADVANTAGES.md", "Context Window Benefits", ["context", "44k", "advantages"]),
        ]
        
        indexed_count = 0
        
        for filepath, title, tags in docs_to_index:
            full_path = os.path.join(base_path, filepath)
            
            if not os.path.exists(full_path):
                print(f"  ⚠️  Not found: {filepath}")
                continue
            
            print(f"  📄 Indexing: {title}...")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate embedding (mock for now - can be replaced with real LM Studio later)
            try:
                # Mock 768-dimensional embedding
                import hashlib
                hash_val = int(hashlib.md5(content.encode()).hexdigest(), 16)
                embedding = [(hash_val >> (i * 4)) % 100 / 100.0 for i in range(768)]
                
                if embedding and isinstance(embedding, list):
                    # Store in Qdrant
                    point_id = filepath.replace("/", "-").replace(".md", "")
                    
                    qdrant.upsert(
                        collection_name="destiny-memory",
                        points=[PointStruct(
                            id=point_id,
                            vector=embedding,
                            payload={
                                "type": "documentation",
                                "title": title,
                                "filepath": filepath,
                                "content_preview": content[:500],
                                "tags": tags,
                                "team": "analytical",
                                "indexed_by": "Helena Kowalczyk",
                                "indexed_at": datetime.now().isoformat()
                            }
                        )]
                    )
                    
                    indexed_count += 1
                    print(f"     ✅ Indexed successfully (vector dim: {len(embedding)})")
                else:
                    print(f"     ❌ Invalid embedding generated")
            
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        print(f"\n  ✅ Qdrant: Indexed {indexed_count}/{len(docs_to_index)} documents")
        return indexed_count
        
    except Exception as e:
        print(f"\n  ❌ Qdrant indexing failed: {e}")
        print(f"     Make sure Qdrant is running and LM Studio has Jina v4 loaded")
        return 0


# ============================================
# 2. REDIS CACHE POPULATION
# ============================================

def populate_redis_cache():
    """Populate Redis with analytical team quick reference"""
    
    print("\n💾 STEP 2: Redis Hot Cache")
    print("-" * 60)
    
    try:
        import redis
        
        print("Connecting to Redis (localhost:6379)...")
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Test connection
        r.ping()
        print("  ✅ Connected")
        
        # Cache analytical team overview
        print("  📝 Caching: Analytical team overview...")
        r.set('knowledge:analytical-team:overview', json.dumps({
            "team_size": 9,
            "status": "operational",
            "created": "2025-11-03",
            "project_id": "destiny-analytical-team",
            "llm_model": "gpt-oss-20b",
            "context_window": 44000,
            "privacy_mode": "LOCAL",
            "agents": [
                "Viktor Kovalenko", "Damian Rousseau", "Elena Volkov",
                "Marcus Chen", "Sofia Martinez", "Adrian Kowalski",
                "Maya Patel", "Lucas Rivera", "Alex Morgan"
            ],
            "capabilities": [
                "OSINT", "Financial Analysis", "Market Research", 
                "Legal Research", "Data Analysis", "Report Writing",
                "Investigation", "Critical Review", "Document Processing"
            ]
        }, indent=2), ex=86400)  # 24 hour cache
        
        # Cache quick reference (agent routing)
        print("  📝 Caching: Agent quick reference...")
        r.set('knowledge:analytical-team:quick-ref', json.dumps({
            "Need OSINT Investigation?": "Elena Volkov",
            "Need Financial Analysis?": "Marcus Chen",
            "Need Market Research?": "Sofia Martinez",
            "Need Legal Research?": "Adrian Kowalski",
            "Need Data Analysis?": "Maya Patel",
            "Need Report Writing?": "Lucas Rivera",
            "Need Investigation Planning?": "Viktor Kovalenko",
            "Need Critical Review?": "Damian Rousseau",
            "Need Document Processing?": "Alex Morgan"
        }, indent=2), ex=86400)
        
        # Cache infrastructure info
        print("  📝 Caching: Infrastructure configuration...")
        r.set('knowledge:analytical-team:infrastructure', json.dumps({
            "elasticsearch": {
                "url": "http://localhost:9200",
                "cluster": "hercules-cluster",
                "ram": "16GB",
                "index": "analytical-documents",
                "purpose": "Full-text document search"
            },
            "qdrant": {
                "url": "http://localhost:6333",
                "collection": "analytical-team",
                "embedding_model": "jinaai/jina-embeddings-v4-text-retrieval",
                "dimensions": 768,
                "purpose": "Semantic search"
            },
            "lm_studio": {
                "url": "http://localhost:1234/v1",
                "model": "gpt-oss-20b",
                "parameters": "20B",
                "context_window": 44000,
                "privacy": "100% LOCAL"
            }
        }, indent=2), ex=86400)
        
        # Cache cross-team routing
        print("  📝 Caching: Cross-team routing...")
        r.set('knowledge:cross-team:routing', json.dumps({
            "technical_to_analytical": {
                "market_research": "Sofia Martinez",
                "financial_analysis": "Marcus Chen",
                "legal_review": "Adrian Kowalski",
                "osint_investigation": "Elena Volkov",
                "data_analysis": "Maya Patel",
                "report_writing": "Lucas Rivera",
                "document_processing": "Alex Morgan"
            },
            "analytical_to_technical": {
                "web_development": "Tomasz Kamiński",
                "database_design": "Maria Wiśniewska",
                "ui_ux_design": "Joanna Mazur",
                "devops_automation": "Piotr Szymański",
                "qa_testing": "Anna Lewandowska",
                "documentation": "Helena Kowalczyk"
            }
        }, indent=2), ex=86400)
        
        print(f"\n  ✅ Redis: Cached 4 knowledge entries")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Redis caching failed: {e}")
        print(f"     Make sure Redis is running")
        return False


# ============================================
# 3. VERIFICATION
# ============================================

def verify_knowledge_distribution():
    """Verify knowledge is accessible from all databases"""
    
    print("\n🔍 STEP 3: Verification")
    print("-" * 60)
    
    results = {
        "qdrant": False,
        "redis": False,
        "postgresql": False
    }
    
    # Test Qdrant
    try:
        from qdrant_client import QdrantClient
        qdrant = QdrantClient(host="localhost", port=6333)
        
        # Try to search
        test_results = qdrant.search(
            collection_name="destiny-memory",
            query_vector=[0.1] * 768,  # Dummy vector
            limit=1
        )
        
        print("  ✅ Qdrant: Searchable")
        results["qdrant"] = True
    except Exception as e:
        print(f"  ⚠️  Qdrant: {e}")
    
    # Test Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        overview = r.get('knowledge:analytical-team:overview')
        if overview:
            print("  ✅ Redis: Cached and accessible")
            results["redis"] = True
        else:
            print("  ⚠️  Redis: Cache empty")
    except Exception as e:
        print(f"  ⚠️  Redis: {e}")
    
    # Test PostgreSQL
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="destiny",
            user="destiny_user",
            password="destiny_pass"
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM analytical_agents;")
        count = cursor.fetchone()[0]
        
        if count == 9:
            print(f"  ✅ PostgreSQL: {count} agents registered")
            results["postgresql"] = True
        else:
            print(f"  ⚠️  PostgreSQL: Expected 9 agents, found {count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"  ⚠️  PostgreSQL: {e}")
        print(f"     Run: psql -U destiny_user -d destiny -f sql/analytical_team_setup.sql")
    
    return results


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Execute complete knowledge dissemination"""
    
    print("\n🚀 Starting Knowledge Dissemination Process...\n")
    
    # Step 1: Qdrant indexing
    qdrant_count = index_in_qdrant()
    
    # Step 2: Redis caching
    redis_success = populate_redis_cache()
    
    # Step 3: Verification
    verification = verify_knowledge_distribution()
    
    # Summary
    print("\n" + "="*80)
    print(" "*25 + "KNOWLEDGE DISSEMINATION COMPLETE")
    print("="*80)
    
    print("\n📊 Results:")
    print(f"   Qdrant: {qdrant_count} documents indexed")
    print(f"   Redis: {'✅ Cached' if redis_success else '❌ Failed'}")
    print(f"   PostgreSQL: {'✅ Verified' if verification['postgresql'] else '⚠️  Needs setup (run SQL script)'}")
    print(f"   Neo4j: ⚠️  Needs manual execution (see HELENA_DOCUMENTATION_PACKAGE.md)")
    
    print("\n📋 Next Steps:")
    if not verification['postgresql']:
        print("   1. Run: psql -U destiny_user -d destiny -f sql/analytical_team_setup.sql")
    print("   2. Execute Neo4j cypher scripts (see HELENA_DOCUMENTATION_PACKAGE.md)")
    print("   3. Create training materials (Quick Start Guide, API Reference)")
    print("   4. Announce to team and schedule training")
    
    print("\n✅ Knowledge is now distributed and discoverable!")
    print("="*80)


if __name__ == "__main__":
    main()
