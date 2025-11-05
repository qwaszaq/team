#!/usr/bin/env python3
"""
System Health Check
Team Destiny - 2025-11-05

Quick health check for all system components
"""

import sys
import os

# Add to path
sys.path.insert(0, os.path.dirname(__file__))


def check_imports():
    """Check if all modules can be imported"""
    print("🔍 Checking imports...")
    
    checks = []
    
    # Core components
    try:
        from src.llm.lmstudio_client import LMStudioLLMClient
        checks.append(("LLM Client", True, None))
    except Exception as e:
        checks.append(("LLM Client", False, str(e)))
    
    try:
        from src.data.embedding_pipeline import DualEmbeddingSystem
        checks.append(("Embedding Pipeline", True, None))
    except Exception as e:
        checks.append(("Embedding Pipeline", False, str(e)))
    
    try:
        from src.agents.base_agent import FinancialAnalystAgent
        checks.append(("Base Agents", True, None))
    except Exception as e:
        checks.append(("Base Agents", False, str(e)))
    
    try:
        from src.agents.additional_agents import DataScienceAgent
        checks.append(("Additional Agents", True, None))
    except Exception as e:
        checks.append(("Additional Agents", False, str(e)))
    
    try:
        from src.agents.orchestrator import MultiAgentOrchestrator
        checks.append(("Orchestrator", True, None))
    except Exception as e:
        checks.append(("Orchestrator", False, str(e)))
    
    try:
        from src.supervision.claude_supervisor import ClaudeSupervisor
        checks.append(("Supervision", True, None))
    except Exception as e:
        checks.append(("Supervision", False, str(e)))
    
    # Database clients
    try:
        from src.data.postgres_client import PostgresClient
        checks.append(("PostgreSQL Client", True, None))
    except Exception as e:
        checks.append(("PostgreSQL Client", False, str(e)))
    
    try:
        from src.data.qdrant_client import QdrantClient
        checks.append(("Qdrant Client", True, None))
    except Exception as e:
        checks.append(("Qdrant Client", False, str(e)))
    
    try:
        from src.data.elasticsearch_client import ElasticsearchClient
        checks.append(("Elasticsearch Client", True, None))
    except Exception as e:
        checks.append(("Elasticsearch Client", False, str(e)))
    
    try:
        from src.data.neo4j_client import Neo4jClient
        checks.append(("Neo4j Client", True, None))
    except Exception as e:
        checks.append(("Neo4j Client", False, str(e)))
    
    try:
        from src.data.smart_router import SmartDatabaseRouter
        checks.append(("Smart Router", True, None))
    except Exception as e:
        checks.append(("Smart Router", False, str(e)))
    
    # Print results
    for name, status, error in checks:
        if status:
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name}: {error}")
    
    return all(status for _, status, _ in checks)


def check_lmstudio():
    """Check LMStudio connection"""
    print("\n🔍 Checking LMStudio...")
    
    try:
        from src.llm.lmstudio_client import LMStudioLLMClient
        
        client = LMStudioLLMClient()
        healthy = client.health_check()
        
        if healthy:
            print(f"   ✅ LMStudio: Connected")
            return True
        else:
            print(f"   ❌ LMStudio: Not responding")
            return False
    except Exception as e:
        print(f"   ❌ LMStudio: Error - {e}")
        return False


def check_databases():
    """Check database connections"""
    print("\n🔍 Checking databases...")
    
    results = []
    
    # PostgreSQL
    try:
        from src.data.postgres_client import PostgresClient
        client = PostgresClient()
        healthy = client.health_check()
        results.append(("PostgreSQL", healthy))
        print(f"   {'✅' if healthy else '❌'} PostgreSQL: {'Connected' if healthy else 'Not available'}")
    except Exception as e:
        results.append(("PostgreSQL", False))
        print(f"   ❌ PostgreSQL: {e}")
    
    # Qdrant
    try:
        from src.data.qdrant_client import QdrantClient
        client = QdrantClient()
        results.append(("Qdrant", client.available))
        print(f"   {'✅' if client.available else '❌'} Qdrant: {'Connected' if client.available else 'Not available'}")
    except Exception as e:
        results.append(("Qdrant", False))
        print(f"   ❌ Qdrant: {e}")
    
    # Elasticsearch
    try:
        from src.data.elasticsearch_client import ElasticsearchClient
        client = ElasticsearchClient()
        results.append(("Elasticsearch", client.available))
        print(f"   {'✅' if client.available else '❌'} Elasticsearch: {'Connected' if client.available else 'Not available'}")
    except Exception as e:
        results.append(("Elasticsearch", False))
        print(f"   ❌ Elasticsearch: {e}")
    
    # Neo4j
    try:
        from src.data.neo4j_client import Neo4jClient
        client = Neo4jClient()
        results.append(("Neo4j", client.available))
        print(f"   {'✅' if client.available else '❌'} Neo4j: {'Connected' if client.available else 'Not available'}")
    except Exception as e:
        results.append(("Neo4j", False))
        print(f"   ❌ Neo4j: {e}")
    
    return results


def check_config():
    """Check configuration"""
    print("\n🔍 Checking configuration...")
    
    try:
        from config import config
        
        print(f"   Environment: {config.ENVIRONMENT}")
        print(f"   LMStudio Host: {config.LMSTUDIO_HOST}:{config.LMSTUDIO_PORT}")
        print(f"   Claude API: {'✅ Configured' if config.ANTHROPIC_API_KEY else '⚠️  Not configured'}")
        
        if config.validate():
            print(f"   ✅ Configuration: Valid")
            return True
        else:
            print(f"   ⚠️  Configuration: Has issues")
            return False
    except Exception as e:
        print(f"   ❌ Configuration: Error - {e}")
        return False


def main():
    """Run all health checks"""
    print("="*70)
    print("DESTINY ANALYTICAL SYSTEM - HEALTH CHECK")
    print("="*70)
    
    # Check imports
    imports_ok = check_imports()
    
    # Check LMStudio
    lmstudio_ok = check_lmstudio()
    
    # Check databases
    db_results = check_databases()
    
    # Check configuration
    config_ok = check_config()
    
    # Summary
    print("\n" + "="*70)
    print("HEALTH CHECK SUMMARY")
    print("="*70)
    
    print(f"\nCore Components: {'✅ OK' if imports_ok else '❌ Issues'}")
    print(f"LMStudio: {'✅ Connected' if lmstudio_ok else '❌ Not available'}")
    print(f"Configuration: {'✅ Valid' if config_ok else '⚠️  Issues'}")
    
    print(f"\nDatabases:")
    for name, status in db_results:
        print(f"  {name}: {'✅ Connected' if status else '❌ Not available'}")
    
    # Overall status
    critical_ok = imports_ok and lmstudio_ok
    
    print("\n" + "="*70)
    if critical_ok:
        print("OVERALL STATUS: 🟢 SYSTEM OPERATIONAL")
        print("\nCore system is working!")
        print("Databases are optional - start with: docker-compose up -d")
    else:
        print("OVERALL STATUS: 🔴 CRITICAL ISSUES")
        print("\nPlease fix critical issues before using the system.")
    
    print("="*70)
    
    return critical_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
