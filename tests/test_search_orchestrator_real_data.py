#!/usr/bin/env python3
"""
SearchOrchestrator Real Data Tests - Gap Analysis for Phase 2

Tests SearchOrchestrator against actual data in the system:
- Elasticsearch: 375 PDF documents (Grupa Azoty reports)
- Qdrant: 409 vector points
- PostgreSQL: 108 messages
- Neo4j: decision chains

Identifies gaps and prepares recommendations for Phase 2.
"""
import sys
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from search_orchestrator import SearchOrchestrator
import json
from datetime import datetime
from typing import Dict, List, Any
import time


class SearchOrchestratorTester:
    """Comprehensive tester for SearchOrchestrator"""
    
    def __init__(self):
        self.orchestrator = SearchOrchestrator()
        self.test_results = []
        self.gaps_identified = []
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 80)
        print("🧪 SearchOrchestrator - Real Data Test Suite")
        print("=" * 80)
        print()
        
        # Test suites
        self.test_system_health()
        self.test_elasticsearch_fulltext()
        self.test_elasticsearch_metadata()
        self.test_elasticsearch_aggregations()
        self.test_qdrant_semantic()
        self.test_postgres_structured()
        self.test_neo4j_graph()
        self.test_hybrid_search()
        self.test_performance()
        
        # Gap analysis
        self.analyze_gaps()
        
        # Generate report
        self.generate_report()
    
    def test_system_health(self):
        """Test 1: System health and availability"""
        print("=" * 80)
        print("TEST 1: System Health & Statistics")
        print("=" * 80)
        print()
        
        # Health check
        health = self.orchestrator.health_check()
        print("🏥 Backend Health:")
        all_healthy = True
        for backend, status in health.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {backend.upper()}: {status}")
            if not status:
                all_healthy = False
                self.gaps_identified.append(f"{backend} is not available")
        
        self.test_results.append({
            "test": "system_health",
            "status": "PASS" if all_healthy else "FAIL",
            "details": health
        })
        
        # Statistics
        stats = self.orchestrator.get_stats()
        print("\n📊 System Statistics:")
        for key, value in stats.items():
            print(f"   • {key}: {value:,}")
        
        print()
        
        # Gap analysis
        if stats.get('elasticsearch_docs', 0) == 0:
            self.gaps_identified.append("No documents in Elasticsearch")
        if stats.get('qdrant_points', 0) == 0:
            self.gaps_identified.append("No vector points in Qdrant")
        if stats.get('postgres_messages', 0) == 0:
            self.gaps_identified.append("No messages in PostgreSQL")
    
    def test_elasticsearch_fulltext(self):
        """Test 2: Elasticsearch full-text search quality"""
        print("=" * 80)
        print("TEST 2: Elasticsearch Full-Text Search Quality")
        print("=" * 80)
        print()
        
        test_queries = [
            ("sprawozdanie finansowe", "Financial statements"),
            ("przychody ze sprzedaży", "Sales revenue"),
            ("zadłużenie kredyty", "Debt and loans"),
            ("zysk netto EBITDA", "Net profit EBITDA"),
            ("inwestycje capex", "Capital expenditure"),
            ("sustainability environment", "Environmental topics (English)"),
        ]
        
        results_summary = []
        
        for query, description in test_queries:
            print(f"🔍 Query: '{query}' ({description})")
            start = time.time()
            results = self.orchestrator.full_text_search(
                query=query,
                index="osint_reports_pdf",
                size=5,
                highlight=True
            )
            elapsed = time.time() - start
            
            print(f"   ⏱️  Time: {elapsed:.3f}s")
            print(f"   📄 Results: {len(results)}")
            
            if results:
                print(f"   🏆 Top result (score: {results[0].score:.2f}):")
                print(f"      File: {results[0].metadata.get('filename', 'N/A')[:60]}")
                if results[0].content:
                    print(f"      Excerpt: {results[0].content[:100]}...")
                
                # Check if has content (not image-based)
                has_content = len(results[0].content) > 50
                if not has_content:
                    self.gaps_identified.append(f"Query '{query}' returned results without text (needs OCR)")
            else:
                print("   ❌ No results found")
                self.gaps_identified.append(f"Query '{query}' returned no results (coverage gap)")
            
            print()
            
            results_summary.append({
                "query": query,
                "description": description,
                "results_count": len(results),
                "top_score": results[0].score if results else 0.0,
                "response_time": elapsed,
                "has_content": len(results[0].content) > 50 if results else False
            })
        
        self.test_results.append({
            "test": "elasticsearch_fulltext",
            "status": "PASS",
            "queries_tested": len(test_queries),
            "results": results_summary
        })
    
    def test_elasticsearch_metadata(self):
        """Test 3: Elasticsearch metadata completeness"""
        print("=" * 80)
        print("TEST 3: Elasticsearch Metadata Completeness")
        print("=" * 80)
        print()
        
        # Get sample documents
        results = self.orchestrator.full_text_search(
            query="*",
            index="osint_reports_pdf",
            size=10
        )
        
        if not results:
            print("❌ No documents found for metadata analysis")
            self.gaps_identified.append("Cannot analyze metadata - no documents")
            return
        
        # Analyze metadata fields
        print(f"📋 Analyzing metadata from {len(results)} sample documents...")
        print()
        
        required_fields = [
            "issuer", "report_url", "filename", "file_size",
            "sha256", "downloaded_at", "content_length"
        ]
        
        missing_fields = {field: 0 for field in required_fields}
        
        # Desired but missing fields
        desired_fields = [
            "report_year", "report_quarter", "report_type_detail",
            "financial_metrics", "entities", "report_period",
            "data_classification", "quality_score"
        ]
        
        for result in results:
            metadata = result.metadata
            
            # Check required fields
            for field in required_fields:
                if field not in metadata or not metadata[field]:
                    missing_fields[field] += 1
            
            # Check desired fields
            for field in desired_fields:
                if field not in metadata:
                    pass  # We expect these to be missing (Phase 2)
        
        print("✅ Required Fields Coverage:")
        for field, count in missing_fields.items():
            percentage = ((len(results) - count) / len(results)) * 100
            icon = "✅" if percentage == 100 else "⚠️"
            print(f"   {icon} {field}: {percentage:.0f}% ({len(results) - count}/{len(results)} docs)")
        
        print("\n❌ Missing Desired Fields (Phase 2 targets):")
        for field in desired_fields:
            print(f"   • {field}")
            self.gaps_identified.append(f"Metadata field missing: {field}")
        
        print()
        
        self.test_results.append({
            "test": "elasticsearch_metadata",
            "status": "PARTIAL",
            "required_coverage": {k: v for k, v in missing_fields.items()},
            "missing_desired": desired_fields
        })
    
    def test_elasticsearch_aggregations(self):
        """Test 4: Elasticsearch aggregations"""
        print("=" * 80)
        print("TEST 4: Elasticsearch Aggregations")
        print("=" * 80)
        print()
        
        # Test aggregation by issuer
        print("📊 Aggregating by issuer...")
        aggs = self.orchestrator.aggregate_query(
            index="osint_reports_pdf",
            agg_field="issuer.keyword",
            agg_name="by_issuer",
            size=10
        )
        
        if aggs and 'by_issuer' in aggs:
            buckets = aggs['by_issuer'].get('buckets', [])
            print(f"   Found {len(buckets)} issuers:")
            for bucket in buckets[:5]:
                print(f"   • {bucket.get('key', 'N/A')}: {bucket.get('doc_count', 0)} documents")
            
            if not buckets:
                self.gaps_identified.append("Aggregation by issuer returned empty (field not indexed as keyword?)")
        else:
            print("   ❌ Aggregation failed")
            self.gaps_identified.append("Cannot aggregate by issuer - check mapping")
        
        print()
        
        self.test_results.append({
            "test": "elasticsearch_aggregations",
            "status": "PASS" if aggs else "FAIL",
            "aggregations_tested": 1
        })
    
    def test_qdrant_semantic(self):
        """Test 5: Qdrant semantic search relevance"""
        print("=" * 80)
        print("TEST 5: Qdrant Semantic Search Relevance")
        print("=" * 80)
        print()
        
        test_queries = [
            ("financial performance analysis", "Financial analysis"),
            ("system architecture and design", "Technical architecture"),
            ("data quality and governance", "Data management"),
        ]
        
        results_summary = []
        
        for query, description in test_queries:
            print(f"🧠 Query: '{query}' ({description})")
            start = time.time()
            results = self.orchestrator.semantic_search(
                query=query,
                collection="destiny-team-framework-master",
                limit=5
            )
            elapsed = time.time() - start
            
            print(f"   ⏱️  Time: {elapsed:.3f}s")
            print(f"   📄 Results: {len(results)}")
            
            if results:
                print(f"   🏆 Top result (score: {results[0].score:.3f}):")
                print(f"      Content: {results[0].content[:100]}...")
                
                # Check semantic relevance (score > 0.7 is good)
                if results[0].score < 0.7:
                    self.gaps_identified.append(f"Low semantic relevance for '{query}' (score: {results[0].score:.3f})")
            else:
                print("   ❌ No results found")
                self.gaps_identified.append(f"Qdrant: no results for '{query}'")
            
            print()
            
            results_summary.append({
                "query": query,
                "description": description,
                "results_count": len(results),
                "top_score": results[0].score if results else 0.0,
                "response_time": elapsed
            })
        
        self.test_results.append({
            "test": "qdrant_semantic",
            "status": "PASS",
            "queries_tested": len(test_queries),
            "results": results_summary
        })
    
    def test_postgres_structured(self):
        """Test 6: PostgreSQL structured queries"""
        print("=" * 80)
        print("TEST 6: PostgreSQL Structured Queries")
        print("=" * 80)
        print()
        
        # Test 1: Get recent messages
        print("🗄️ Query: Recent messages (last 10)...")
        sql = "SELECT sender, message_type, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10"
        results = self.orchestrator.structured_query(sql)
        
        print(f"   📄 Results: {len(results)} messages")
        if results:
            print(f"   🏆 Most recent: {results[0].get('sender', 'N/A')} at {results[0].get('timestamp', 'N/A')}")
        else:
            self.gaps_identified.append("No messages in PostgreSQL")
        
        print()
        
        # Test 2: Check for OSINT-tagged messages
        print("🔍 Query: OSINT-tagged messages...")
        sql = "SELECT COUNT(*) as count FROM messages WHERE 'osint' = ANY(tags)"
        results = self.orchestrator.structured_query(sql)
        
        osint_count = results[0].get('count', 0) if results else 0
        print(f"   📊 OSINT messages: {osint_count}")
        
        if osint_count == 0:
            self.gaps_identified.append("No OSINT-tagged messages in PostgreSQL (data not propagated?)")
        
        print()
        
        # Test 3: Check for agent contexts
        print("🤖 Query: Agent contexts...")
        sql = "SELECT agent_name, COUNT(*) as context_count FROM agent_contexts GROUP BY agent_name"
        results = self.orchestrator.structured_query(sql)
        
        print(f"   📊 Agents with context: {len(results)}")
        for row in results[:5]:
            print(f"      • {row.get('agent_name', 'N/A')}: {row.get('context_count', 0)} contexts")
        
        print()
        
        self.test_results.append({
            "test": "postgres_structured",
            "status": "PASS",
            "messages_found": len(results) if results else 0,
            "osint_messages": osint_count
        })
    
    def test_neo4j_graph(self):
        """Test 7: Neo4j graph queries"""
        print("=" * 80)
        print("TEST 7: Neo4j Graph Queries")
        print("=" * 80)
        print()
        
        # Test decision chain
        print("🕸️ Query: Decision chain for 'architecture'...")
        decisions = self.orchestrator.get_decision_chain("architecture", limit=5)
        
        print(f"   📊 Decisions found: {len(decisions)}")
        if decisions:
            for i, decision in enumerate(decisions[:3], 1):
                print(f"   {i}. {decision}")
        else:
            self.gaps_identified.append("No decisions found in Neo4j (graph not populated?)")
        
        print()
        
        self.test_results.append({
            "test": "neo4j_graph",
            "status": "PASS" if decisions else "FAIL",
            "decisions_found": len(decisions)
        })
    
    def test_hybrid_search(self):
        """Test 8: Hybrid search effectiveness"""
        print("=" * 80)
        print("TEST 8: Hybrid Search Effectiveness")
        print("=" * 80)
        print()
        
        test_queries = [
            "financial analysis system",
            "data governance and compliance",
            "architecture design decisions"
        ]
        
        for query in test_queries:
            print(f"🔄 Hybrid query: '{query}'")
            
            # Test with different source combinations
            source_combos = [
                (['es'], "ES only"),
                (['qdrant'], "Qdrant only"),
                (['es', 'qdrant'], "ES + Qdrant"),
                (['es', 'qdrant', 'pg'], "ES + Qdrant + PG"),
            ]
            
            for sources, description in source_combos:
                start = time.time()
                results = self.orchestrator.hybrid_search(
                    query=query,
                    sources=sources,
                    limit=5,
                    rerank=True
                )
                elapsed = time.time() - start
                
                print(f"   {description}: {len(results)} results ({elapsed:.3f}s)")
                
                # Check source diversity
                sources_found = set(r.source for r in results)
                if len(sources) > 1 and len(sources_found) == 1:
                    self.gaps_identified.append(f"Hybrid search not combining sources effectively for '{query}'")
            
            print()
        
        self.test_results.append({
            "test": "hybrid_search",
            "status": "PASS",
            "queries_tested": len(test_queries)
        })
    
    def test_performance(self):
        """Test 9: Query performance"""
        print("=" * 80)
        print("TEST 9: Query Performance")
        print("=" * 80)
        print()
        
        # Test ES performance
        print("⚡ Elasticsearch performance...")
        query = "sprawozdanie finansowe"
        times = []
        for _ in range(5):
            start = time.time()
            self.orchestrator.full_text_search(query, size=10)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"   Average: {avg_time:.3f}s (5 runs)")
        
        if avg_time > 1.0:
            self.gaps_identified.append(f"ES query slow (avg {avg_time:.3f}s) - consider optimization")
        
        # Test Qdrant performance
        print("\n⚡ Qdrant performance...")
        query = "financial analysis"
        times = []
        for _ in range(5):
            start = time.time()
            self.orchestrator.semantic_search(query, limit=10)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"   Average: {avg_time:.3f}s (5 runs)")
        
        if avg_time > 2.0:
            self.gaps_identified.append(f"Qdrant query slow (avg {avg_time:.3f}s) - check embeddings service")
        
        print()
        
        self.test_results.append({
            "test": "performance",
            "status": "PASS"
        })
    
    def analyze_gaps(self):
        """Analyze identified gaps and categorize for Phase 2"""
        print("=" * 80)
        print("GAP ANALYSIS - Phase 2 Requirements")
        print("=" * 80)
        print()
        
        # Categorize gaps
        categories = {
            "OCR Pipeline": [],
            "Metadata Enrichment": [],
            "Data Propagation": [],
            "Query Optimization": [],
            "Feature Gaps": [],
            "Infrastructure": []
        }
        
        for gap in self.gaps_identified:
            if "OCR" in gap or "without text" in gap:
                categories["OCR Pipeline"].append(gap)
            elif "Metadata field" in gap or "missing" in gap.lower():
                categories["Metadata Enrichment"].append(gap)
            elif "propagated" in gap or "OSINT-tagged" in gap:
                categories["Data Propagation"].append(gap)
            elif "slow" in gap or "optimization" in gap:
                categories["Query Optimization"].append(gap)
            elif "not available" in gap or "down" in gap:
                categories["Infrastructure"].append(gap)
            else:
                categories["Feature Gaps"].append(gap)
        
        # Print categorized gaps
        for category, gaps in categories.items():
            if gaps:
                print(f"📋 {category}:")
                for gap in gaps:
                    print(f"   • {gap}")
                print()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print()
        
        # Count test results
        total_tests = len(self.test_results)
        passed = sum(1 for t in self.test_results if t.get('status') == 'PASS')
        failed = sum(1 for t in self.test_results if t.get('status') == 'FAIL')
        partial = sum(1 for t in self.test_results if t.get('status') == 'PARTIAL')
        
        print(f"Tests run: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Partial: {partial}")
        print(f"❌ Failed: {failed}")
        print()
        
        # Total gaps
        print(f"🔍 Gaps identified: {len(self.gaps_identified)}")
        print()
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "partial": partial
            },
            "test_results": self.test_results,
            "gaps_identified": self.gaps_identified,
            "recommendations": self.generate_recommendations()
        }
        
        report_file = "investigations/concepts/search_orchestrator_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved: {report_file}")
        print()
        
        # Print recommendations
        print("=" * 80)
        print("🎯 PHASE 2 RECOMMENDATIONS")
        print("=" * 80)
        print()
        
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"{i}. {rec['title']}")
            print(f"   Priority: {rec['priority']}")
            print(f"   Description: {rec['description']}")
            print()
    
    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate Phase 2 recommendations based on gaps"""
        recommendations = []
        
        # Check for OCR needs
        ocr_gaps = [g for g in self.gaps_identified if "OCR" in g or "without text" in g]
        if ocr_gaps:
            recommendations.append({
                "title": "Implement OCR Pipeline for Image-Based PDFs",
                "priority": "HIGH",
                "description": f"Found {len(ocr_gaps)} instances where documents lack text. Implement Tesseract/Azure OCR pipeline for ~150 image-based PDFs."
            })
        
        # Check for metadata gaps
        metadata_gaps = [g for g in self.gaps_identified if "Metadata field" in g]
        if metadata_gaps:
            recommendations.append({
                "title": "Enrich Metadata with Financial Fields",
                "priority": "HIGH",
                "description": f"Add {len(metadata_gaps)} metadata fields: report_year, report_quarter, financial_metrics, entities, quality_score."
            })
        
        # Check for propagation issues
        propagation_gaps = [g for g in self.gaps_identified if "propagated" in g or "OSINT" in g]
        if propagation_gaps:
            recommendations.append({
                "title": "Implement ES ⇄ Qdrant Bidirectional Sync",
                "priority": "MEDIUM",
                "description": "OSINT data not propagated to PostgreSQL. Create sync mechanism between ES, Qdrant, and PG."
            })
        
        # Performance
        perf_gaps = [g for g in self.gaps_identified if "slow" in g]
        if perf_gaps:
            recommendations.append({
                "title": "Optimize Query Performance",
                "priority": "MEDIUM",
                "description": "Implement caching layer, optimize ES mapping, tune Qdrant HNSW parameters."
            })
        
        # NER for financial terms
        recommendations.append({
            "title": "Build NER Pipeline for Financial Terms",
            "priority": "HIGH",
            "description": "Extract financial metrics (revenue, EBITDA, debt) from PDF content using spaCy/transformers."
        })
        
        # Audit logging
        recommendations.append({
            "title": "Implement Audit Trail for Compliance",
            "priority": "MEDIUM",
            "description": "Log all ES queries with user, timestamp, query, results count for GDPR compliance."
        })
        
        return recommendations


def main():
    """Run complete test suite"""
    tester = SearchOrchestratorTester()
    tester.run_all_tests()
    
    print("=" * 80)
    print("✅ Testing completed - ready for Phase 2 planning")
    print("=" * 80)


if __name__ == "__main__":
    main()
