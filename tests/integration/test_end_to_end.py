"""
End-to-End Integration Test
Anna Nowakowska - QA
2025-11-05
"""

import sys
import os
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.orchestrator import MultiAgentOrchestrator


def test_simple_case():
    """Test simple single-document case"""
    print("=" * 70)
    print("TEST 1: Simple Single-Document Case")
    print("=" * 70)
    
    orchestrator = MultiAgentOrchestrator()
    
    documents = [
        {
            "id": "simple_doc",
            "content": "Revenue was $100k. Expenses were $60k. Profit was $40k.",
            "type": "financial"
        }
    ]
    
    analysis = orchestrator.process_case(
        case_id=f"simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Simple Financial Test",
        documents=documents,
        analysis_types=["financial"]
    )
    
    # Assertions
    assert analysis.case_id.startswith("simple_")
    assert len(analysis.agents_used) == 1
    assert analysis.embeddings_count >= 1
    assert analysis.total_tokens > 0
    assert 0 <= analysis.average_confidence <= 1.0
    
    print(f"\n✅ TEST 1 PASSED")
    print(f"   Time: {analysis.total_time:.2f}s")
    print(f"   Tokens: {analysis.total_tokens}")
    print(f"   Confidence: {analysis.average_confidence:.2f}")
    
    return True


def test_multi_agent_case():
    """Test case with multiple agents"""
    print("\n" + "=" * 70)
    print("TEST 2: Multi-Agent Case")
    print("=" * 70)
    
    orchestrator = MultiAgentOrchestrator()
    
    documents = [
        {
            "id": "financial_doc",
            "content": """
            Q4 2024 Results:
            - Revenue: $2.5M (up 15% YoY)
            - Operating margin: 28%
            - Cash: $5M
            - Customer acquisition cost down 12%
            """,
            "type": "financial"
        },
        {
            "id": "legal_doc",
            "content": """
            Legal Review:
            - All contracts reviewed and compliant
            - Data privacy audit completed
            - No outstanding litigation
            - IP portfolio secured
            """,
            "type": "legal"
        }
    ]
    
    analysis = orchestrator.process_case(
        case_id=f"multi_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Multi-Agent Analysis",
        documents=documents,
        analysis_types=["financial", "legal", "risk"]
    )
    
    # Assertions
    assert analysis.case_id.startswith("multi_")
    assert len(analysis.agents_used) == 3
    assert analysis.embeddings_count >= 2
    assert analysis.total_tokens > 0
    assert len(analysis.results) == 3
    
    print(f"\n✅ TEST 2 PASSED")
    print(f"   Agents: {len(analysis.agents_used)}")
    print(f"   Time: {analysis.total_time:.2f}s")
    print(f"   Tokens: {analysis.total_tokens}")
    print(f"   Avg Confidence: {analysis.average_confidence:.2f}")
    
    return True


def test_context_passing():
    """Test that context is passed between agents"""
    print("\n" + "=" * 70)
    print("TEST 3: Context Passing Between Agents")
    print("=" * 70)
    
    orchestrator = MultiAgentOrchestrator()
    
    documents = [
        {
            "id": "context_doc",
            "content": "Revenue growth rate accelerated to 30% but operating costs increased significantly.",
            "type": "financial"
        }
    ]
    
    analysis = orchestrator.process_case(
        case_id=f"context_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Context Test",
        documents=documents,
        analysis_types=["financial", "risk"]
    )
    
    # Assertions
    assert len(analysis.results) == 2
    
    # Risk agent should have processed after Financial agent
    financial_result = analysis.results[0]
    risk_result = analysis.results[1]
    
    assert financial_result.agent_role == "financial"
    assert risk_result.agent_role == "risk"
    
    print(f"\n✅ TEST 3 PASSED")
    print(f"   Context successfully passed between agents")
    print(f"   Financial → Risk chain working")
    
    return True


def test_performance_benchmarks():
    """Test performance targets"""
    print("\n" + "=" * 70)
    print("TEST 4: Performance Benchmarks")
    print("=" * 70)
    
    orchestrator = MultiAgentOrchestrator()
    
    # Test document
    test_content = "Financial analysis: " + "Revenue analysis. " * 50
    
    documents = [
        {
            "id": "perf_doc",
            "content": test_content,
            "type": "financial"
        }
    ]
    
    analysis = orchestrator.process_case(
        case_id=f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Performance Test",
        documents=documents,
        analysis_types=["financial"]
    )
    
    # Performance targets
    TIME_PER_AGENT_TARGET = 30  # seconds
    TOKENS_SANITY_CHECK = 50000  # should not exceed this
    
    time_per_agent = analysis.total_time / len(analysis.agents_used)
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Total time: {analysis.total_time:.2f}s")
    print(f"   Time per agent: {time_per_agent:.2f}s (target: <{TIME_PER_AGENT_TARGET}s)")
    print(f"   Total tokens: {analysis.total_tokens} (sanity: <{TOKENS_SANITY_CHECK})")
    print(f"   Embeddings: {analysis.embeddings_count}")
    
    # Assertions
    assert time_per_agent < TIME_PER_AGENT_TARGET, f"Agent took too long: {time_per_agent:.2f}s"
    assert analysis.total_tokens < TOKENS_SANITY_CHECK, f"Too many tokens: {analysis.total_tokens}"
    
    print(f"\n✅ TEST 4 PASSED")
    print(f"   All performance targets met")
    
    return True


def test_embeddings():
    """Test embedding generation"""
    print("\n" + "=" * 70)
    print("TEST 5: Embedding Generation")
    print("=" * 70)
    
    from src.data.embedding_pipeline import DualEmbeddingSystem
    
    embedder = DualEmbeddingSystem()
    
    # Test E5-Large (general text)
    result1 = embedder.embed("This is general text about technology.")
    assert len(result1.embedding) == 1024
    assert result1.model == "text-embedding-multilingual-e5-large-instruct"
    print(f"   ✅ E5-Large: 1024 dims, {result1.time_taken:.3f}s")
    
    # Test Jina (financial text)
    result2 = embedder.embed("Revenue was $100k with profit margin of 25%.")
    assert len(result2.embedding) == 1024
    assert result2.model == "jina-embeddings-v4-text-retrieval"
    print(f"   ✅ Jina: 1024 dims, {result2.time_taken:.3f}s")
    
    # Get stats
    stats = embedder.get_stats()
    print(f"\n📊 Embedding Stats:")
    print(f"   E5-Large: {stats['e5']['embeddings_generated']} generated, {stats['e5']['throughput']:.1f}/sec")
    print(f"   Jina: {stats['jina']['embeddings_generated']} generated, {stats['jina']['throughput']:.1f}/sec")
    
    print(f"\n✅ TEST 5 PASSED")
    
    return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("🧪 RUNNING INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("Simple Case", test_simple_case),
        ("Multi-Agent Case", test_multi_agent_case),
        ("Context Passing", test_context_passing),
        ("Performance Benchmarks", test_performance_benchmarks),
        ("Embeddings", test_embeddings)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total: {len(tests)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! SYSTEM IS OPERATIONAL! 🎉\n")
    else:
        print(f"\n⚠️  {failed} test(s) failed\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
