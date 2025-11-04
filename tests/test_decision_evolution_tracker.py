"""
Tests for DecisionEvolutionTracker

Tests:
- Version tracking
- Confidence evolution
- Simplification detection
- Improvement indicators
- Evolution summary
- Change analysis
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.decision_evolution_tracker import DecisionEvolutionTracker


def test_initialization():
    """Test tracker initialization"""
    print("\n🧪 Test 1: Initialization")
    
    tracker = DecisionEvolutionTracker("Test Decision")
    
    assert tracker.topic == "Test Decision"
    assert len(tracker.versions) == 0
    
    print("   ✅ Initialization working")


def test_add_version():
    """Test adding versions"""
    print("\n🧪 Test 2: Add Version")
    
    tracker = DecisionEvolutionTracker("Test Decision")
    
    version = tracker.add_version(
        version_number=1,
        decision="Use Solution A",
        rationale="Because X",
        proposed_by="Alice",
        team="team_a",
        confidence=0.7
    )
    
    assert version["version"] == 1
    assert version["decision"] == "Use Solution A"
    assert version["confidence"] == 0.7
    assert len(tracker.versions) == 1
    
    print("   ✅ Add version working")


def test_version_comparison():
    """Test version comparison"""
    print("\n🧪 Test 3: Version Comparison")
    
    tracker = DecisionEvolutionTracker("Test Decision")
    
    # Version 1
    tracker.add_version(1, "Complex solution", "Initial", "Alice", "team_a", 0.6)
    
    # Version 2 - simpler and higher confidence
    v2 = tracker.add_version(2, "Simple solution", "Better", "Bob", "team_b", 0.8)
    
    assert v2["comparison"] is not None
    assert v2["comparison"]["decision_changed"] is True
    assert v2["comparison"]["confidence_improved"] is True
    assert abs(v2["comparison"]["confidence_delta"] - 0.2) < 0.001  # Floating point tolerance
    
    print("   ✅ Version comparison working")


def test_simplification_detection():
    """Test simplification detection"""
    print("\n🧪 Test 4: Simplification Detection")
    
    tracker = DecisionEvolutionTracker("Test Decision")
    
    # Version 1: Complex
    tracker.add_version(
        1, 
        "Use complex architecture with multiple frameworks and libraries",
        "Initial",
        "Alice",
        "team_a",
        0.6
    )
    
    # Version 2: Simpler
    v2 = tracker.add_version(
        2,
        "Use simple approach",
        "Simpler is better",
        "Bob",
        "team_b",
        0.8
    )
    
    assert v2["comparison"]["simplification"] is True
    
    print("   ✅ Simplification detection working")


def test_improvement_indicators():
    """Test improvement indicator detection"""
    print("\n🧪 Test 5: Improvement Indicators")
    
    tracker = DecisionEvolutionTracker("Test Decision")
    
    tracker.add_version(1, "Solution A", "Initial", "Alice", "team_a", 0.6)
    
    # Version with performance improvement
    v2 = tracker.add_version(
        2,
        "Solution B",
        "Much faster and simpler, reduces cost significantly",
        "Bob",
        "team_b",
        0.9
    )
    
    improvements = v2["comparison"]["improvement_indicators"]
    
    # Check that key improvements are detected
    assert "increased_confidence" in improvements
    assert any(kw in improvements for kw in ["performance_improved", "simplified_approach", "cost_reduced"])
    
    print("   ✅ Improvement indicators working")


def test_evolution_summary():
    """Test evolution summary"""
    print("\n🧪 Test 6: Evolution Summary")
    
    tracker = DecisionEvolutionTracker("NLP Choice")
    
    tracker.add_version(1, "Use spaCy", "Sophisticated", "Alice", "analytical", 0.7)
    tracker.add_version(2, "Use keywords", "Simpler", "Bob", "technical", 0.85)
    tracker.add_version(3, "Weighted keywords", "Best", "Charlie", "analytical", 0.95)
    
    summary = tracker.get_evolution_summary()
    
    assert summary["topic"] == "NLP Choice"
    assert summary["total_versions"] == 3
    assert summary["initial_confidence"] == 0.7
    assert summary["final_confidence"] == 0.95
    assert summary["confidence_improvement"] == 0.25
    assert len(summary["teams_involved"]) == 2
    
    print("   ✅ Evolution summary working")


def test_confidence_evolution():
    """Test confidence evolution tracking"""
    print("\n🧪 Test 7: Confidence Evolution")
    
    tracker = DecisionEvolutionTracker("Test")
    
    tracker.add_version(1, "A", "R", "Alice", "team_a", 0.5)
    tracker.add_version(2, "B", "R", "Bob", "team_b", 0.7)
    tracker.add_version(3, "C", "R", "Charlie", "team_a", 0.9)
    
    evolution = tracker.get_confidence_evolution()
    
    assert evolution["initial"] == 0.5
    assert evolution["final"] == 0.9
    assert evolution["min"] == 0.5
    assert evolution["max"] == 0.9
    assert evolution["trend"] == "increasing"
    assert evolution["total_change"] == 0.4
    
    print("   ✅ Confidence evolution working")


def test_changes_summary():
    """Test changes summary"""
    print("\n🧪 Test 8: Changes Summary")
    
    tracker = DecisionEvolutionTracker("Test")
    
    tracker.add_version(1, "A", "Initial", "Alice", "team_a", 0.6)
    tracker.add_version(2, "B", "Simpler", "Bob", "team_b", 0.8, "Changed to B")
    
    changes = tracker.get_changes_summary()
    
    assert len(changes) == 2
    assert changes[0]["type"] == "initial"
    assert changes[1]["type"] == "revision"
    assert abs(changes[1]["confidence_change"] - 0.2) < 0.001  # Floating point tolerance
    
    print("   ✅ Changes summary working")


def test_get_latest_version():
    """Test getting latest version"""
    print("\n🧪 Test 9: Get Latest Version")
    
    tracker = DecisionEvolutionTracker("Test")
    
    tracker.add_version(1, "A", "R1", "Alice", "team_a", 0.6)
    tracker.add_version(2, "B", "R2", "Bob", "team_b", 0.8)
    tracker.add_version(3, "C", "R3", "Charlie", "team_c", 0.9)
    
    latest = tracker.get_latest_version()
    
    assert latest["version"] == 3
    assert latest["decision"] == "C"
    assert latest["confidence"] == 0.9
    
    print("   ✅ Get latest version working")


def test_export():
    """Test export functionality"""
    print("\n🧪 Test 10: Export")
    
    tracker = DecisionEvolutionTracker("Test")
    
    tracker.add_version(1, "A", "Initial", "Alice", "team_a", 0.7)
    tracker.add_version(2, "B", "Revised", "Bob", "team_b", 0.9)
    
    # Test to_dict
    data = tracker.to_dict()
    assert data["topic"] == "Test"
    assert data["total_versions"] == 2
    assert "evolution_summary" in data
    assert "confidence_evolution" in data
    
    # Test to_json
    json_str = tracker.to_json()
    assert "Test" in json_str
    assert "evolution_summary" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 17 + "DECISION EVOLUTION TRACKER - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_add_version,
        test_version_comparison,
        test_simplification_detection,
        test_improvement_indicators,
        test_evolution_summary,
        test_confidence_evolution,
        test_changes_summary,
        test_get_latest_version,
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
