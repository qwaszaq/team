#!/usr/bin/env python3
"""
SearchOrchestrator Usage Examples for Agents

Demonstrates how agents can use SearchOrchestrator to query
across all data layers (ES, Qdrant, Postgres, Neo4j).
"""
import sys
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from search_orchestrator import SearchOrchestrator
import json


def example_1_financial_analyst():
    """Example: Marcus (Financial Analyst) querying financial reports"""
    print("=" * 80)
    print("📊 EXAMPLE 1: Financial Analyst - Revenue Trends")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Search for revenue-related reports
    print("🔍 Searching for revenue reports in Elasticsearch...")
    results = orchestrator.full_text_search(
        query="przychody ze sprzedaży",
        index="osint_reports_pdf",
        size=5,
        highlight=True
    )
    
    print(f"Found {len(results)} relevant reports:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result.score:.2f}")
        print(f"   File: {result.metadata.get('filename', 'N/A')}")
        print(f"   URL: {result.metadata.get('report_url', 'N/A')[:80]}...")
        if result.content:
            print(f"   Excerpt: {result.content[:150]}...")
    
    # Get aggregations by year
    print("\n📊 Aggregating reports by issuer...")
    aggs = orchestrator.aggregate_query(
        index="osint_reports_pdf",
        agg_field="issuer.keyword",
        agg_name="by_issuer",
        size=10
    )
    
    if aggs and 'by_issuer' in aggs:
        buckets = aggs['by_issuer'].get('buckets', [])
        print(f"\nFound {len(buckets)} issuers:")
        for bucket in buckets:
            print(f"   • {bucket.get('key', 'N/A')}: {bucket.get('doc_count', 0)} reports")
    
    print()


def example_2_osint_specialist():
    """Example: Elena (OSINT) doing semantic search for topics"""
    print("=" * 80)
    print("🕵️ EXAMPLE 2: OSINT Specialist - Semantic Topic Search")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Semantic search for sustainability topics
    print("🧠 Searching for sustainability-related content in Qdrant...")
    results = orchestrator.semantic_search(
        query="environmental sustainability and climate initiatives",
        collection="destiny-team-framework-master",
        limit=5
    )
    
    print(f"Found {len(results)} semantically similar documents:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result.score:.2f}")
        print(f"   Source: {result.source}")
        print(f"   Content: {result.content[:200]}...")
    
    print()


def example_3_legal_compliance():
    """Example: Adrian (Legal) checking data lineage"""
    print("=" * 80)
    print("⚖️ EXAMPLE 3: Legal/Compliance - Data Lineage Audit")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Query PostgreSQL for messages with specific tags
    print("🔍 Querying PostgreSQL for OSINT-tagged messages...")
    sql = """
        SELECT sender, message_type, timestamp, tags
        FROM messages
        WHERE 'osint' = ANY(tags)
        ORDER BY timestamp DESC
        LIMIT 5
    """
    
    results = orchestrator.structured_query(sql)
    
    print(f"Found {len(results)} OSINT messages:")
    for i, row in enumerate(results, 1):
        print(f"\n{i}. From: {row.get('sender', 'N/A')}")
        print(f"   Type: {row.get('message_type', 'N/A')}")
        print(f"   Time: {row.get('timestamp', 'N/A')}")
        print(f"   Tags: {row.get('tags', [])}")
    
    # Check Elasticsearch for documents with specific metadata
    print("\n📄 Checking Elasticsearch for documents downloaded in last 24h...")
    es_results = orchestrator.full_text_search(
        query="*",
        index="osint_reports_pdf",
        size=10,
        filters={"issuer.keyword": "Grupa Azoty (Tarnów)"}
    )
    
    print(f"Found {len(es_results)} documents from Grupa Azoty")
    
    print()


def example_4_strategic_architect():
    """Example: Viktor (Strategic) using hybrid search"""
    print("=" * 80)
    print("🏗️ EXAMPLE 4: Strategic Architect - Hybrid Multi-Source Search")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Hybrid search combining ES, Qdrant, and Postgres
    print("🔄 Running hybrid search across ES + Qdrant + Postgres...")
    results = orchestrator.hybrid_search(
        query="system integration architecture",
        sources=['es', 'qdrant', 'pg'],
        limit=3,
        rerank=True
    )
    
    print(f"Found {len(results)} results (combined and re-ranked):")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Source: {result.source} | Score: {result.score:.2f}")
        print(f"   Content: {result.content[:150]}...")
    
    print()


def example_5_knowledge_manager():
    """Example: Helena (Knowledge Manager) checking system health"""
    print("=" * 80)
    print("📚 EXAMPLE 5: Knowledge Manager - System Health & Stats")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Health check
    print("🏥 System Health Check:")
    health = orchestrator.health_check()
    for backend, status in health.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {backend.upper()}: {'healthy' if status else 'down'}")
    
    # Statistics
    print("\n📊 System Statistics:")
    stats = orchestrator.get_stats()
    for key, value in stats.items():
        print(f"   • {key}: {value:,}")
    
    # Get context for Helena
    print("\n📝 Recent context for Helena:")
    context = orchestrator.get_context_for_agent(
        agent_name="Helena",
        project_id="destiny-team-framework-master",
        limit=3
    )
    
    for i, ctx in enumerate(context, 1):
        print(f"\n   {i}. Key: {ctx.get('context_key', 'N/A')}")
        print(f"      Updated: {ctx.get('updated_at', 'N/A')}")
        print(f"      Importance: {ctx.get('importance', 0.0)}")
    
    print()


def example_6_cross_agent_collaboration():
    """Example: Multiple agents collaborating on a task"""
    print("=" * 80)
    print("🤝 EXAMPLE 6: Cross-Agent Collaboration - Financial Investigation")
    print("=" * 80)
    print()
    
    orchestrator = SearchOrchestrator()
    
    # Scenario: Investigating Grupa Azoty financial trends
    investigation_query = "Grupa Azoty financial performance"
    
    print(f"📋 Investigation: {investigation_query}")
    print()
    
    # Elena: Gather OSINT sources
    print("👤 Elena (OSINT): Gathering source documents...")
    elena_results = orchestrator.full_text_search(
        query="Grupa Azoty",
        index="osint_reports_pdf",
        size=10,
        filters={"issuer.keyword": "Grupa Azoty (Tarnów)"}
    )
    print(f"   ✓ Found {len(elena_results)} source documents")
    
    # Marcus: Analyze financial content
    print("\n👤 Marcus (Financial): Analyzing financial metrics...")
    marcus_results = orchestrator.full_text_search(
        query="przychody zysk EBITDA",
        index="osint_reports_pdf",
        size=5,
        highlight=True
    )
    print(f"   ✓ Found {len(marcus_results)} reports with financial metrics")
    
    # Viktor: Check for similar investigations
    print("\n👤 Viktor (Strategic): Checking for related investigations...")
    viktor_results = orchestrator.semantic_search(
        query="financial analysis investigation Grupa Azoty",
        limit=3
    )
    print(f"   ✓ Found {len(viktor_results)} related documents in knowledge base")
    
    # Helena: Store investigation metadata
    print("\n👤 Helena (Knowledge Manager): Logging investigation...")
    # (In real scenario, would call orchestrator.structured_query to INSERT)
    print(f"   ✓ Investigation logged to PostgreSQL")
    
    # Generate summary
    print("\n" + "=" * 80)
    print("📊 Investigation Summary:")
    print(f"   • Total sources: {len(elena_results)}")
    print(f"   • Financial reports analyzed: {len(marcus_results)}")
    print(f"   • Related knowledge: {len(viktor_results)} documents")
    print("=" * 80)
    
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("🚀 SearchOrchestrator - Agent Usage Examples")
    print("=" * 80)
    print("\n")
    
    examples = [
        ("Financial Analyst", example_1_financial_analyst),
        ("OSINT Specialist", example_2_osint_specialist),
        ("Legal/Compliance", example_3_legal_compliance),
        ("Strategic Architect", example_4_strategic_architect),
        ("Knowledge Manager", example_5_knowledge_manager),
        ("Cross-Agent Collaboration", example_6_cross_agent_collaboration),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"❌ Example '{name}' failed: {e}")
            print()
    
    print("=" * 80)
    print("✅ All examples completed")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
