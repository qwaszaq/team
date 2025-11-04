"""
Tests for CollaborationPatternRecognizer

Tests:
- Pattern analysis
- Success detection
- Best practices extraction
- Pattern comparison
- Statistics
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.pattern_recognizer import CollaborationPatternRecognizer


# Mock conversation class
class MockConversation:
    def __init__(self, turns, teams):
        self.turns = turns
        self.teams = teams


def test_initialization():
    """Test recognizer initialization"""
    print("\n🧪 Test 1: Initialization")
    
    recognizer = CollaborationPatternRecognizer()
    
    assert len(recognizer.patterns) == 0
    assert len(recognizer.success_indicators) == 0
    
    print("   ✅ Initialization working")


def test_analyze_conversation():
    """Test conversation analysis"""
    print("\n🧪 Test 2: Analyze Conversation")
    
    recognizer = CollaborationPatternRecognizer()
    
    conv = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a", "team_b"]
    )
    
    pattern = recognizer.analyze_conversation(conv, outcome_quality=0.9)
    
    assert pattern["total_turns"] == 3
    assert pattern["outcome_quality"] == 0.9
    assert len(recognizer.patterns) == 1
    
    print("   ✅ Conversation analysis working")


def test_success_detection():
    """Test success pattern detection"""
    print("\n🧪 Test 3: Success Detection")
    
    recognizer = CollaborationPatternRecognizer()
    
    conv = MockConversation(
        turns=[{"type": "proposal", "timestamp": datetime.now()}],
        teams=["team_a"]
    )
    
    # Low quality - should not be marked as success
    recognizer.analyze_conversation(conv, outcome_quality=0.5)
    assert len(recognizer.success_indicators) == 0
    
    # High quality - should be marked as success
    recognizer.analyze_conversation(conv, outcome_quality=0.9)
    assert len(recognizer.success_indicators) == 1
    
    print("   ✅ Success detection working")


def test_convergence_path_detection():
    """Test convergence path detection"""
    print("\n🧪 Test 4: Convergence Path Detection")
    
    recognizer = CollaborationPatternRecognizer()
    
    # Quick agreement
    conv1 = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a", "team_b"]
    )
    
    pattern1 = recognizer.analyze_conversation(conv1, 0.9)
    assert pattern1["convergence_path"] == "quick_agreement_after_challenge"
    
    print("   ✅ Convergence path detection working")


def test_best_practices():
    """Test best practices extraction"""
    print("\n🧪 Test 5: Best Practices")
    
    recognizer = CollaborationPatternRecognizer()
    
    # No patterns yet
    practices1 = recognizer.get_best_practices()
    assert "Not enough successful patterns" in practices1.get("message", "")
    
    # Add successful patterns
    conv = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a", "team_b"]
    )
    
    recognizer.analyze_conversation(conv, 0.9)
    recognizer.analyze_conversation(conv, 0.85)
    
    practices2 = recognizer.get_best_practices()
    assert "optimal_turn_count" in practices2
    assert "recommendations" in practices2
    assert len(practices2["recommendations"]) > 0
    
    print("   ✅ Best practices extraction working")


def test_pattern_comparison():
    """Test pattern comparison"""
    print("\n🧪 Test 6: Pattern Comparison")
    
    recognizer = CollaborationPatternRecognizer()
    
    conv1 = MockConversation(
        turns=[{"type": "proposal", "timestamp": datetime.now()}],
        teams=["team_a"]
    )
    conv2 = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a"]
    )
    
    recognizer.analyze_conversation(conv1, 0.6)
    recognizer.analyze_conversation(conv2, 0.9)
    
    comparison = recognizer.compare_patterns(0, 1)
    
    assert "comparison" in comparison
    assert abs(comparison["comparison"]["quality_difference"] - 0.3) < 0.001  # Floating point tolerance
    assert comparison["comparison"]["better_pattern"] == 1
    
    print("   ✅ Pattern comparison working")


def test_pattern_statistics():
    """Test pattern statistics"""
    print("\n🧪 Test 7: Pattern Statistics")
    
    recognizer = CollaborationPatternRecognizer()
    
    # Add multiple patterns
    conv = MockConversation(
        turns=[{"type": "proposal", "timestamp": datetime.now()}],
        teams=["team_a"]
    )
    
    recognizer.analyze_conversation(conv, 0.7)
    recognizer.analyze_conversation(conv, 0.9)
    recognizer.analyze_conversation(conv, 0.5)
    
    stats = recognizer.get_pattern_statistics()
    
    assert stats["total_patterns"] == 3
    assert "quality" in stats
    assert "turns" in stats
    assert abs(stats["quality"]["average"] - 0.7) < 0.001  # Floating point tolerance
    
    print("   ✅ Pattern statistics working")


def test_recommend_approach():
    """Test approach recommendation"""
    print("\n🧪 Test 8: Recommend Approach")
    
    recognizer = CollaborationPatternRecognizer()
    
    # No data
    rec1 = recognizer.recommend_approach({"teams": 2})
    assert rec1["confidence"] == 0.0
    
    # With data
    conv = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a", "team_b"]
    )
    
    recognizer.analyze_conversation(conv, 0.9)
    
    rec2 = recognizer.recommend_approach({"teams": 2})
    assert "recommended_turns" in rec2
    assert "confidence" in rec2
    assert rec2["confidence"] > 0
    
    print("   ✅ Approach recommendation working")


def test_turn_type_analysis():
    """Test turn type analysis"""
    print("\n🧪 Test 9: Turn Type Analysis")
    
    recognizer = CollaborationPatternRecognizer()
    
    conv = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["team_a", "team_b"]
    )
    
    recognizer.analyze_conversation(conv, 0.9)
    
    practices = recognizer.get_best_practices()
    analysis = practices.get("turn_type_analysis", {})
    
    assert "counts" in analysis
    assert "percentages" in analysis
    assert analysis["counts"]["proposal"] == 2
    
    print("   ✅ Turn type analysis working")


def test_export():
    """Test export functionality"""
    print("\n🧪 Test 10: Export")
    
    recognizer = CollaborationPatternRecognizer()
    
    conv = MockConversation(
        turns=[{"type": "proposal", "timestamp": datetime.now()}],
        teams=["team_a"]
    )
    
    recognizer.analyze_conversation(conv, 0.8)
    
    # Test to_dict
    data = recognizer.to_dict()
    assert data["total_patterns"] == 1
    assert "best_practices" in data
    
    # Test to_json
    json_str = recognizer.to_json()
    assert "total_patterns" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 17 + "COLLABORATION PATTERN RECOGNIZER - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_analyze_conversation,
        test_success_detection,
        test_convergence_path_detection,
        test_best_practices,
        test_pattern_comparison,
        test_pattern_statistics,
        test_recommend_approach,
        test_turn_type_analysis,
        test_export
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
