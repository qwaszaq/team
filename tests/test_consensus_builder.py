"""
Tests for ConsensusBuilder

Tests:
- Position registration
- Common ground detection
- Conflict detection
- Compromise proposals
- Agreement tracking
- Consensus scoring
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration.consensus_builder import ConsensusBuilder


def test_initialization():
    """Test builder initialization"""
    print("\n🧪 Test 1: Initialization")
    
    builder = ConsensusBuilder("Test Topic", ["team_a", "team_b"])
    
    assert builder.topic == "Test Topic"
    assert builder.teams == ["team_a", "team_b"]
    assert len(builder.positions) == 0
    assert len(builder.agreements) == 0
    
    print("   ✅ Initialization working")


def test_register_position():
    """Test position registration"""
    print("\n🧪 Test 2: Register Position")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    pos = builder.register_position(
        team="team_a",
        position="Position A",
        key_points=["Point 1", "Point 2"],
        non_negotiables=["Must have"]
    )
    
    assert pos["team"] == "team_a"
    assert pos["position"] == "Position A"
    assert len(pos["key_points"]) == 2
    assert len(pos["non_negotiables"]) == 1
    assert "team_a" in builder.positions
    
    print("   ✅ Position registration working")


def test_find_common_ground():
    """Test common ground detection"""
    print("\n🧪 Test 3: Find Common Ground")
    
    builder = ConsensusBuilder("Test", ["analytical", "technical"])
    
    builder.register_position(
        "analytical",
        "Position A",
        ["Fast response", "User friendly", "Accurate"]
    )
    
    builder.register_position(
        "technical",
        "Position B",
        ["Fast response", "Simple", "Maintainable"]
    )
    
    common = builder.find_common_ground()
    
    assert "common_ground" in common
    assert "unique_positions" in common
    assert "conflicts" in common
    
    # Should find "Fast response" as common
    assert len(common["common_ground"]) >= 1
    
    print("   ✅ Common ground detection working")


def test_track_agreement():
    """Test agreement tracking"""
    print("\n🧪 Test 4: Track Agreement")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Point 1"])
    builder.register_position("team_b", "Pos B", ["Point 2"])
    
    builder.track_agreement(
        teams_agreeing=["team_a", "team_b"],
        agreed_point="Agreed on X",
        rationale="Makes sense"
    )
    
    assert len(builder.agreements) == 1
    assert builder.agreements[0]["point"] == "Agreed on X"
    assert len(builder.agreements[0]["teams"]) == 2
    
    print("   ✅ Agreement tracking working")


def test_track_disagreement():
    """Test disagreement tracking"""
    print("\n🧪 Test 5: Track Disagreement")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Point 1"])
    builder.register_position("team_b", "Pos B", ["Point 2"])
    
    builder.track_disagreement(
        teams_disagreeing=["team_a", "team_b"],
        disagreement_point="Cannot agree on Y",
        reason="Different priorities"
    )
    
    assert len(builder.disagreements) == 1
    assert builder.disagreements[0]["point"] == "Cannot agree on Y"
    
    print("   ✅ Disagreement tracking working")


def test_consensus_score():
    """Test consensus score calculation"""
    print("\n🧪 Test 6: Consensus Score")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Point 1", "Point 2"])
    builder.register_position("team_b", "Pos B", ["Point 3", "Point 4"])
    
    # No agreements yet
    score1 = builder.get_consensus_score()
    assert score1 >= 0.0
    
    # Add agreement
    builder.track_agreement(["team_a", "team_b"], "Agreed", "Reason")
    
    score2 = builder.get_consensus_score()
    assert score2 > score1  # Score should increase
    
    print("   ✅ Consensus score working")


def test_propose_compromise():
    """Test compromise proposals"""
    print("\n🧪 Test 7: Propose Compromise")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Fast", "Accurate"])
    builder.register_position("team_b", "Pos B", ["Simple", "Fast"])
    
    compromise = builder.propose_compromise()
    
    assert "agreed_points" in compromise
    assert "compromise_proposals" in compromise
    assert "areas_for_discussion" in compromise
    
    print("   ✅ Compromise proposals working")


def test_team_alignment():
    """Test team alignment calculation"""
    print("\n🧪 Test 8: Team Alignment")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b", "team_c"])
    
    builder.register_position("team_a", "Pos A", ["Point 1"])
    builder.register_position("team_b", "Pos B", ["Point 2"])
    builder.register_position("team_c", "Pos C", ["Point 3"])
    
    # Track agreements
    builder.track_agreement(["team_a", "team_b"], "Agree 1", "Reason")
    builder.track_agreement(["team_a", "team_b", "team_c"], "Agree 2", "Reason")
    
    alignment = builder.get_team_alignment()
    
    assert "team_a" in alignment
    assert "team_b" in alignment
    assert "team_c" in alignment
    
    # team_a and team_b should have higher alignment (in both agreements)
    assert alignment["team_a"] == 1.0  # In all agreements
    assert alignment["team_b"] == 1.0  # In all agreements
    assert alignment["team_c"] == 0.5  # In 1 out of 2 agreements
    
    print("   ✅ Team alignment working")


def test_agreement_breakdown():
    """Test agreement breakdown"""
    print("\n🧪 Test 9: Agreement Breakdown")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Point 1"])
    builder.register_position("team_b", "Pos B", ["Point 2"])
    
    builder.track_agreement(["team_a", "team_b"], "Agree 1", "Reason")
    builder.track_agreement(["team_a", "team_b"], "Agree 2", "Reason")
    builder.track_disagreement(["team_a", "team_b"], "Disagree 1", "Reason")
    
    breakdown = builder.get_agreement_breakdown()
    
    assert breakdown["total_agreements"] == 2
    assert breakdown["total_disagreements"] == 1
    assert breakdown["agreement_rate"] == 2/3
    
    print("   ✅ Agreement breakdown working")


def test_export():
    """Test export functionality"""
    print("\n🧪 Test 10: Export")
    
    builder = ConsensusBuilder("Test", ["team_a", "team_b"])
    
    builder.register_position("team_a", "Pos A", ["Point 1"])
    builder.register_position("team_b", "Pos B", ["Point 2"])
    builder.track_agreement(["team_a", "team_b"], "Agreed", "Reason")
    
    # Test to_dict
    data = builder.to_dict()
    assert data["topic"] == "Test"
    assert "consensus_score" in data
    assert "common_ground" in data
    
    # Test to_json
    json_str = builder.to_json()
    assert "Test" in json_str
    assert "consensus_score" in json_str
    
    print("   ✅ Export working")


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 22 + "CONSENSUS BUILDER - TESTS")
    print("=" * 80)
    
    tests = [
        test_initialization,
        test_register_position,
        test_find_common_ground,
        test_track_agreement,
        test_track_disagreement,
        test_consensus_score,
        test_propose_compromise,
        test_team_alignment,
        test_agreement_breakdown,
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
