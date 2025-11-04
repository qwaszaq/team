"""
Tests for EnhancedCrossTeamCollaboration (Integrated System)

Tests:
- System initialization
- Turn tracking
- Challenge-response flow
- Decision evolution
- Position registration
- Agreement tracking
- Complete analysis
- Finalization
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.integrated_system import EnhancedCrossTeamCollaboration


def test_initialization():
    """Test system initialization"""
    print("\n🧪 Test 1: Initialization")
    
    collab = EnhancedCrossTeamCollaboration(
        topic="Test Collaboration",
        teams=["team_a", "team_b"]
    )
    
    assert collab.topic == "Test Collaboration"
    assert collab.teams == ["team_a", "team_b"]
    assert collab.conversation is not None
    assert collab.feedback is not None
    assert collab.evolution is not None
    assert collab.consensus is not None
    assert collab.recognizer is not None
    assert collab.finalized is False
    
    print("   ✅ Initialization working")


def test_add_turn():
    """Test adding turns"""
    print("\n🧪 Test 2: Add Turn")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    turn = collab.add_turn(
        turn_number=1,
        team="team_a",
        agent="Agent A",
        content="Proposal",
        turn_type="proposal"
    )
    
    assert turn["turn"] == 1
    assert len(collab.conversation.turns) == 1
    
    print("   ✅ Add turn working")


def test_challenge_response_flow():
    """Test challenge-response integration"""
    print("\n🧪 Test 3: Challenge-Response Flow")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["analytical", "technical"])
    
    # Turn 1: Proposal
    collab.add_turn(1, "analytical", "Lucas", "Use spaCy", "proposal")
    
    # Turn 2: Challenge
    collab.add_turn(2, "technical", "Tomasz", "Too complex", "challenge")
    loop_id = collab.track_challenge(
        "Tomasz", "technical", "spaCy proposal",
        "complexity", "Use spaCy", "100MB+ library"
    )
    
    # Turn 3: Response
    collab.add_turn(3, "analytical", "Sofia", "Use keywords", "response")
    success = collab.track_response(
        loop_id, "Sofia", "accept", "Good point", "Use keywords"
    )
    
    assert success is True
    assert len(collab.conversation.turns) == 3
    assert len(collab.feedback.loops) == 1
    assert collab.feedback.loops[0]["improvement_achieved"] is True
    
    print("   ✅ Challenge-response flow working")


def test_decision_evolution():
    """Test decision evolution tracking"""
    print("\n🧪 Test 4: Decision Evolution")
    
    collab = EnhancedCrossTeamCollaboration("NLP Choice", ["analytical", "technical"])
    
    # Version 1
    collab.add_decision_version(
        1, "Use spaCy", "Sophisticated", "Lucas", "analytical", 0.7
    )
    
    # Version 2
    collab.add_decision_version(
        2, "Use keywords", "Simpler", "Tomasz", "technical", 0.9, "Simplified"
    )
    
    assert len(collab.evolution.versions) == 2
    
    summary = collab.evolution.get_evolution_summary()
    assert summary["total_versions"] == 2
    assert abs(summary["confidence_improvement"] - 0.2) < 0.001  # Floating point tolerance
    
    print("   ✅ Decision evolution working")


def test_position_registration():
    """Test position registration"""
    print("\n🧪 Test 5: Position Registration")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    pos = collab.register_team_position(
        team="team_a",
        position="Position A",
        key_points=["Point 1", "Point 2"],
        non_negotiables=["Must have"]
    )
    
    assert pos["team"] == "team_a"
    assert "team_a" in collab.consensus.positions
    
    print("   ✅ Position registration working")


def test_agreement_tracking():
    """Test agreement tracking"""
    print("\n🧪 Test 6: Agreement Tracking")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    collab.register_team_position("team_a", "Pos A", ["P1"])
    collab.register_team_position("team_b", "Pos B", ["P2"])
    
    collab.track_agreement(
        ["team_a", "team_b"],
        "Agreed on X",
        "Makes sense"
    )
    
    assert len(collab.consensus.agreements) == 1
    
    print("   ✅ Agreement tracking working")


def test_complete_analysis():
    """Test complete analysis generation"""
    print("\n🧪 Test 7: Complete Analysis")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    # Add some data
    collab.add_turn(1, "team_a", "Agent A", "Proposal", "proposal")
    collab.add_turn(2, "team_b", "Agent B", "Agreement", "agreement")
    collab.register_team_position("team_a", "Pos A", ["P1"])
    collab.register_team_position("team_b", "Pos B", ["P2"])
    
    analysis = collab.get_complete_analysis()
    
    assert "conversation" in analysis
    assert "feedback" in analysis
    assert "evolution" in analysis
    assert "consensus" in analysis
    assert "patterns" in analysis
    assert "insights" in analysis
    
    print("   ✅ Complete analysis working")


def test_finalization():
    """Test finalization"""
    print("\n🧪 Test 8: Finalization")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    collab.add_turn(1, "team_a", "Agent A", "Proposal", "proposal")
    collab.add_turn(2, "team_b", "Agent B", "Agreement", "agreement")
    
    assert collab.finalized is False
    
    analysis = collab.finalize(outcome_quality=0.9)
    
    assert collab.finalized is True
    assert collab.conversation.status in ["converged", "completed"]
    assert len(collab.recognizer.patterns) == 1
    
    # Can't finalize twice
    result = collab.finalize(0.9)
    assert "error" in result
    
    print("   ✅ Finalization working")


def test_insights_generation():
    """Test insights generation"""
    print("\n🧪 Test 9: Insights Generation")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["analytical", "technical"])
    
    # Successful collaboration
    collab.add_turn(1, "analytical", "Lucas", "Proposal", "proposal")
    collab.add_decision_version(1, "Solution A", "Initial", "Lucas", "analytical", 0.7)
    collab.register_team_position("analytical", "Pos A", ["P1", "P2"])
    
    collab.add_turn(2, "technical", "Tomasz", "Challenge", "challenge")
    loop_id = collab.track_challenge("Tomasz", "technical", "A", "complexity", "A", "Complex")
    collab.register_team_position("technical", "Pos B", ["P3", "P4"])
    
    collab.add_turn(3, "analytical", "Sofia", "Agreed", "agreement")
    collab.track_response(loop_id, "Sofia", "accept", "OK", "Solution B")
    collab.add_decision_version(2, "Solution B", "Simpler", "Sofia", "analytical", 0.9, "Simplified")
    collab.track_agreement(["analytical", "technical"], "Solution B", "Better")
    
    analysis = collab.finalize(0.9)
    
    insights = analysis["insights"]
    assert "collaboration_quality" in insights
    assert "key_strengths" in insights
    assert "overall_assessment" in insights
    
    print("   ✅ Insights generation working")


def test_export():
    """Test export functionality"""
    print("\n🧪 Test 10: Export")
    
    collab = EnhancedCrossTeamCollaboration("Test", ["team_a", "team_b"])
    
    collab.add_turn(1, "team_a", "Agent A", "Test", "proposal")
    
    # Test to_dict
    data = collab.to_dict()
    assert data["topic"] == "Test"
    assert "complete_analysis" in data
    
    # Test to_json
    json_str = collab.to_json()
    assert "Test" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 15 + "ENHANCED CROSS-TEAM COLLABORATION - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_add_turn,
        test_challenge_response_flow,
        test_decision_evolution,
        test_position_registration,
        test_agreement_tracking,
        test_complete_analysis,
        test_finalization,
        test_insights_generation,
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
            import traceback
            traceback.print_exc()
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
