"""
Tests for FeedbackLoopTracker

Tests:
- Challenge tracking
- Response tracking
- Improvement detection
- Metrics calculation
- Team statistics
- Top challengers
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.feedback_loop_tracker import FeedbackLoopTracker


def test_initialization():
    """Test tracker initialization"""
    print("\n🧪 Test 1: Initialization")
    
    tracker = FeedbackLoopTracker()
    
    assert len(tracker.loops) == 0
    assert tracker.loop_id_counter == 0
    
    print("   ✅ Initialization working")


def test_track_challenge():
    """Test challenge tracking"""
    print("\n🧪 Test 2: Track Challenge")
    
    tracker = FeedbackLoopTracker()
    
    loop_id = tracker.track_challenge(
        challenger="Tomasz",
        challenger_team="technical",
        target="Proposal A",
        challenge_type="complexity",
        original_proposal="Use complex solution",
        challenge_reason="Too complex"
    )
    
    assert loop_id == 1
    assert len(tracker.loops) == 1
    
    loop = tracker.get_loop(loop_id)
    assert loop["challenger"] == "Tomasz"
    assert loop["type"] == "complexity"
    assert loop["resolution"] is None
    
    print("   ✅ Challenge tracking working")


def test_track_response_accept():
    """Test response tracking - accept"""
    print("\n🧪 Test 3: Track Response (Accept)")
    
    tracker = FeedbackLoopTracker()
    
    loop_id = tracker.track_challenge(
        challenger="Tomasz",
        challenger_team="technical",
        target="Proposal",
        challenge_type="complexity",
        original_proposal="Complex",
        challenge_reason="Too complex"
    )
    
    success = tracker.track_response(
        loop_id=loop_id,
        responder="Sofia",
        response_type="accept",
        response_content="Good point",
        revised_proposal="Simpler solution"
    )
    
    assert success is True
    
    loop = tracker.get_loop(loop_id)
    assert len(loop["responses"]) == 1
    assert loop["resolution"] == "improved"
    assert loop["improvement_achieved"] is True
    
    print("   ✅ Response tracking (accept) working")


def test_track_response_defend():
    """Test response tracking - defend"""
    print("\n🧪 Test 4: Track Response (Defend)")
    
    tracker = FeedbackLoopTracker()
    
    loop_id = tracker.track_challenge(
        challenger="Tomasz",
        challenger_team="technical",
        target="Proposal",
        challenge_type="complexity",
        original_proposal="Complex",
        challenge_reason="Too complex"
    )
    
    tracker.track_response(
        loop_id=loop_id,
        responder="Sofia",
        response_type="defend",
        response_content="Actually, complexity is needed"
    )
    
    loop = tracker.get_loop(loop_id)
    assert loop["resolution"] == "original_maintained"
    assert loop["improvement_achieved"] is False
    
    print("   ✅ Response tracking (defend) working")


def test_improvement_metrics():
    """Test improvement metrics"""
    print("\n🧪 Test 5: Improvement Metrics")
    
    tracker = FeedbackLoopTracker()
    
    # Challenge 1: Accepted
    loop1 = tracker.track_challenge(
        challenger="Tom", challenger_team="tech", target="A",
        challenge_type="complexity", original_proposal="X", challenge_reason="Y"
    )
    tracker.track_response(loop1, "Sofia", "accept", "OK", "Revised")
    
    # Challenge 2: Defended
    loop2 = tracker.track_challenge(
        challenger="Tom", challenger_team="tech", target="B",
        challenge_type="cost", original_proposal="Z", challenge_reason="W"
    )
    tracker.track_response(loop2, "Sofia", "defend", "No")
    
    metrics = tracker.get_improvement_metrics()
    
    assert metrics["total_challenges"] == 2
    assert metrics["improvements_achieved"] == 1
    assert metrics["improvement_rate"] == 0.5
    assert "complexity" in metrics["by_challenge_type"]
    assert "cost" in metrics["by_challenge_type"]
    
    print("   ✅ Improvement metrics working")


def test_challenge_breakdown():
    """Test challenge breakdown"""
    print("\n🧪 Test 6: Challenge Breakdown")
    
    tracker = FeedbackLoopTracker()
    
    tracker.track_challenge("A", "team1", "X", "complexity", "P", "R")
    tracker.track_challenge("B", "team1", "Y", "complexity", "Q", "S")
    tracker.track_challenge("C", "team2", "Z", "cost", "R", "T")
    
    breakdown = tracker.get_challenge_breakdown()
    
    assert breakdown["complexity"] == 2
    assert breakdown["cost"] == 1
    
    print("   ✅ Challenge breakdown working")


def test_resolution_breakdown():
    """Test resolution breakdown"""
    print("\n🧪 Test 7: Resolution Breakdown")
    
    tracker = FeedbackLoopTracker()
    
    # Improved
    loop1 = tracker.track_challenge("A", "team1", "X", "complexity", "P", "R")
    tracker.track_response(loop1, "B", "accept", "OK", "New")
    
    # Original maintained
    loop2 = tracker.track_challenge("C", "team2", "Y", "cost", "Q", "S")
    tracker.track_response(loop2, "D", "defend", "No")
    
    # Unresolved
    tracker.track_challenge("E", "team1", "Z", "time", "R", "T")
    
    breakdown = tracker.get_resolution_breakdown()
    
    assert breakdown["improved"] == 1
    assert breakdown["original_maintained"] == 1
    assert breakdown["unresolved"] == 1
    
    print("   ✅ Resolution breakdown working")


def test_team_challenge_stats():
    """Test team challenge statistics"""
    print("\n🧪 Test 8: Team Challenge Stats")
    
    tracker = FeedbackLoopTracker()
    
    # Team A challenges
    loop1 = tracker.track_challenge("Tom", "team_a", "X", "complexity", "P", "R")
    tracker.track_response(loop1, "B", "accept", "OK", "New")
    
    loop2 = tracker.track_challenge("Ann", "team_a", "Y", "cost", "Q", "S")
    tracker.track_response(loop2, "C", "defend", "No")
    
    # Team B challenge
    tracker.track_challenge("Bob", "team_b", "Z", "time", "R", "T")
    
    stats = tracker.get_team_challenge_stats("team_a")
    
    assert stats["total_challenges"] == 2
    assert stats["improvements_from_challenges"] == 1
    assert stats["success_rate"] == 0.5
    
    print("   ✅ Team challenge stats working")


def test_top_challengers():
    """Test top challengers"""
    print("\n🧪 Test 9: Top Challengers")
    
    tracker = FeedbackLoopTracker()
    
    # Tomasz: 2 challenges, 2 improvements
    loop1 = tracker.track_challenge("Tomasz", "tech", "X", "complexity", "P", "R")
    tracker.track_response(loop1, "B", "accept", "OK", "New")
    
    loop2 = tracker.track_challenge("Tomasz", "tech", "Y", "cost", "Q", "S")
    tracker.track_response(loop2, "C", "accept", "OK", "New2")
    
    # Sofia: 1 challenge, 0 improvements
    loop3 = tracker.track_challenge("Sofia", "analytical", "Z", "time", "R", "T")
    tracker.track_response(loop3, "D", "defend", "No")
    
    top = tracker.get_top_challengers(limit=2)
    
    assert len(top) == 2
    assert top[0]["name"] == "Tomasz"
    assert top[0]["impact_score"] == 1.0
    assert top[1]["name"] == "Sofia"
    assert top[1]["impact_score"] == 0.0
    
    print("   ✅ Top challengers working")


def test_export():
    """Test export functionality"""
    print("\n🧪 Test 10: Export")
    
    tracker = FeedbackLoopTracker()
    
    loop_id = tracker.track_challenge("A", "team1", "X", "complexity", "P", "R")
    tracker.track_response(loop_id, "B", "accept", "OK", "New")
    
    # Test to_dict
    data = tracker.to_dict()
    assert data["total_loops"] == 1
    assert "improvement_metrics" in data
    
    # Test to_json
    json_str = tracker.to_json()
    assert "complexity" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 20 + "FEEDBACK LOOP TRACKER - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_track_challenge,
        test_track_response_accept,
        test_track_response_defend,
        test_improvement_metrics,
        test_challenge_breakdown,
        test_resolution_breakdown,
        test_team_challenge_stats,
        test_top_challengers,
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
