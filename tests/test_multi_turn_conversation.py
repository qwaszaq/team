"""
Tests for MultiTurnConversation

Tests:
- Basic turn tracking
- Convergence detection
- Team participation
- Turn threading
- Status updates
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.multi_turn_conversation import MultiTurnConversation


def test_initialization():
    """Test conversation initialization"""
    print("\n🧪 Test 1: Initialization")
    
    conv = MultiTurnConversation(
        topic="Test Topic",
        teams=["team_a", "team_b"]
    )
    
    assert conv.topic == "Test Topic"
    assert conv.teams == ["team_a", "team_b"]
    assert len(conv.turns) == 0
    assert conv.status == "active"
    
    print("   ✅ Initialization working")


def test_add_turn():
    """Test adding turns"""
    print("\n🧪 Test 2: Add Turn")
    
    conv = MultiTurnConversation(
        topic="Test Topic",
        teams=["team_a", "team_b"]
    )
    
    turn = conv.add_turn(
        turn_number=1,
        team="team_a",
        agent="Agent A",
        content="Initial proposal",
        turn_type="proposal"
    )
    
    assert turn["turn"] == 1
    assert turn["team"] == "team_a"
    assert turn["agent"] == "Agent A"
    assert turn["type"] == "proposal"
    assert len(conv.turns) == 1
    
    print("   ✅ Add turn working")


def test_convergence_detection():
    """Test convergence detection"""
    print("\n🧪 Test 3: Convergence Detection")
    
    conv = MultiTurnConversation(
        topic="Convergence Test",
        teams=["analytical", "technical"]
    )
    
    # Add proposal and agreements
    conv.add_turn(1, "analytical", "Lucas", "Proposal", "proposal")
    conv.add_turn(2, "technical", "Tomasz", "Agreed", "agreement")
    conv.add_turn(3, "analytical", "Sofia", "Agreed", "agreement")
    
    convergence = conv._analyze_convergence()
    
    assert convergence["status"] == "converging"
    assert convergence["confidence"] >= 0.8
    assert convergence["recent_agreements"] >= 2
    
    print("   ✅ Convergence detection working")


def test_divergence_detection():
    """Test divergence detection"""
    print("\n🧪 Test 4: Divergence Detection")
    
    conv = MultiTurnConversation(
        topic="Divergence Test",
        teams=["analytical", "technical"]
    )
    
    # Add many challenges
    conv.add_turn(1, "analytical", "Lucas", "Proposal", "proposal")
    conv.add_turn(2, "technical", "Tomasz", "Challenge 1", "challenge")
    conv.add_turn(3, "analytical", "Sofia", "Counter challenge", "challenge")
    conv.add_turn(4, "technical", "Aleksander", "Another challenge", "challenge")
    
    convergence = conv._analyze_convergence()
    
    assert convergence["status"] == "diverging"
    assert convergence["recent_challenges"] >= 2
    
    print("   ✅ Divergence detection working")


def test_turn_threading():
    """Test turn response threading"""
    print("\n🧪 Test 5: Turn Threading")
    
    conv = MultiTurnConversation(
        topic="Threading Test",
        teams=["team_a", "team_b"]
    )
    
    conv.add_turn(1, "team_a", "Agent A", "First", "proposal")
    turn2 = conv.add_turn(2, "team_b", "Agent B", "Response", "response")
    
    # Turn 2 should respond to turn 1
    assert turn2["responses_to"] == 1
    
    turn3 = conv.add_turn(3, "team_a", "Agent A", "Counter", "response")
    
    # Turn 3 should respond to turn 2
    assert turn3["responses_to"] == 2
    
    print("   ✅ Turn threading working")


def test_team_participation():
    """Test team participation metrics"""
    print("\n🧪 Test 6: Team Participation")
    
    conv = MultiTurnConversation(
        topic="Participation Test",
        teams=["analytical", "technical"]
    )
    
    conv.add_turn(1, "analytical", "Lucas", "Turn 1", "proposal")
    conv.add_turn(2, "analytical", "Sofia", "Turn 2", "response")
    conv.add_turn(3, "technical", "Tomasz", "Turn 3", "challenge")
    conv.add_turn(4, "technical", "Aleksander", "Turn 4", "agreement")
    
    participation = conv.get_team_participation()
    
    assert participation["analytical"] == 2
    assert participation["technical"] == 2
    
    print("   ✅ Team participation metrics working")


def test_conversation_flow():
    """Test getting full conversation flow"""
    print("\n🧪 Test 7: Conversation Flow")
    
    conv = MultiTurnConversation(
        topic="Flow Test",
        teams=["team_a", "team_b"]
    )
    
    conv.add_turn(1, "team_a", "Agent A", "Proposal", "proposal")
    conv.add_turn(2, "team_b", "Agent B", "Challenge", "challenge")
    conv.add_turn(3, "team_a", "Agent A", "Response", "response")
    
    flow = conv.get_conversation_flow()
    
    assert flow["topic"] == "Flow Test"
    assert flow["total_turns"] == 3
    assert "convergence_analysis" in flow
    assert "turn_breakdown" in flow
    assert len(flow["turns"]) == 3
    
    print("   ✅ Conversation flow working")


def test_status_updates():
    """Test automatic status updates"""
    print("\n🧪 Test 8: Status Updates")
    
    conv = MultiTurnConversation(
        topic="Status Test",
        teams=["team_a", "team_b"]
    )
    
    assert conv.status == "active"
    
    # Add agreements
    conv.add_turn(1, "team_a", "A", "Proposal", "proposal")
    conv.add_turn(2, "team_b", "B", "Agreed", "agreement")
    conv.add_turn(3, "team_a", "A", "Great", "agreement")
    
    # Should now be converged
    assert conv.status == "converged"
    
    print("   ✅ Status updates working")


def test_export():
    """Test export to dict and JSON"""
    print("\n🧪 Test 9: Export")
    
    conv = MultiTurnConversation(
        topic="Export Test",
        teams=["team_a", "team_b"]
    )
    
    conv.add_turn(1, "team_a", "Agent A", "Test", "proposal")
    
    # Test to_dict
    data = conv.to_dict()
    assert data["topic"] == "Export Test"
    assert data["total_turns"] == 1
    
    # Test to_json
    json_str = conv.to_json()
    assert "Export Test" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 20 + "MULTI-TURN CONVERSATION - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_add_turn,
        test_convergence_detection,
        test_divergence_detection,
        test_turn_threading,
        test_team_participation,
        test_conversation_flow,
        test_status_updates,
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
