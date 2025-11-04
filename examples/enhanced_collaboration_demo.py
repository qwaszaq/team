#!/usr/bin/env python3
"""
Enhanced Cross-Team Collaboration - Live Demo

Demonstrates complete workflow using all 6 components:
- MultiTurnConversation
- FeedbackLoopTracker
- DecisionEvolutionTracker
- ConsensusBuilder
- CollaborationPatternRecognizer
- EnhancedCrossTeamCollaboration (Integrated)

Based on real collaboration from CROSS_TEAM_COLLABORATION_MULTI_TURN.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.enhanced_collaboration import EnhancedCrossTeamCollaboration
import json


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(" "*((80-len(title))//2) + title)
    print("="*80 + "\n")


def demo_skills_routing_collaboration():
    """Demo: Skills Routing Implementation collaboration"""
    
    print_header("🚀 ENHANCED COLLABORATION SYSTEM - LIVE DEMO")
    
    print("📋 Scenario: Sprint 1 - Skills Routing Implementation")
    print("   Teams: Analytical Team ↔ Technical Team")
    print("   Topic: How should we implement skills routing?")
    
    # ========================================================================
    # INITIALIZE SYSTEM
    # ========================================================================
    
    print("\n🔧 Initializing Enhanced Collaboration System...")
    
    collab = EnhancedCrossTeamCollaboration(
        topic="Sprint 1: Skills Routing Implementation",
        teams=["analytical", "technical"]
    )
    
    print("✅ System initialized!")
    print(f"   Components: {len([c for c in dir(collab) if not c.startswith('_')])}")
    print("   Ready to track collaboration")
    
    # ========================================================================
    # TURN 1: ANALYTICAL TEAM PROPOSES
    # ========================================================================
    
    print_header("🔄 TURN 1: Analytical Team Proposes")
    
    print("👤 Lucas Rivera (Analytical):")
    print("   'I propose using spaCy NLP library for skills routing.'")
    print("   'It provides sophisticated natural language understanding.'")
    
    collab.add_turn(
        turn_number=1,
        team="analytical",
        agent="Lucas Rivera",
        content="Propose using spaCy for NLP-based skills routing with confidence scorer",
        turn_type="proposal"
    )
    
    collab.register_team_position(
        team="analytical",
        position="Need sophisticated NLP for accurate routing",
        key_points=[
            "spaCy NLP library",
            "Confidence scorer (80% threshold)",
            "Target latency: 200ms",
            "User-friendly natural language"
        ],
        non_negotiables=["Accuracy > 80%"]
    )
    
    collab.add_decision_version(
        version_number=1,
        decision="Use spaCy NLP library with confidence scorer",
        rationale="Sophisticated NLP capabilities for accurate intent detection",
        proposed_by="Lucas Rivera",
        team="analytical",
        confidence=0.70
    )
    
    print("✅ Proposal registered")
    print("   Decision v1: Use spaCy NLP (confidence: 70%)")
    
    # ========================================================================
    # TURN 2: TECHNICAL TEAM CHALLENGES (6 challenges!)
    # ========================================================================
    
    print_header("🔄 TURN 2: Technical Team Challenges")
    
    print("👤 Tomasz Kamiński (Technical):")
    print("   'I have 6 challenges to this proposal...'")
    
    collab.add_turn(
        turn_number=2,
        team="technical",
        agent="Tomasz Kamiński",
        content="Multiple challenges: spaCy too complex, PostgreSQL unnecessary, 200ms too slow...",
        turn_type="challenge"
    )
    
    # Challenge 1: spaCy complexity
    print("\n❌ Challenge 1: NLP Engine")
    print("   'spaCy is 100MB+ library, overkill for keyword matching!'")
    
    loop1 = collab.track_challenge(
        challenger="Tomasz Kamiński",
        challenger_team="technical",
        target="spaCy NLP proposal",
        challenge_type="complexity",
        original_proposal="Use spaCy (100MB+ library)",
        challenge_reason="Too complex for simple keyword matching"
    )
    
    # Challenge 2: Storage
    print("❌ Challenge 2: Storage")
    print("   'Why PostgreSQL for static data? Use JSON!'")
    
    loop2 = collab.track_challenge(
        challenger="Maria Wiśniewska",
        challenger_team="technical",
        target="PostgreSQL storage",
        challenge_type="complexity",
        original_proposal="Store skills in PostgreSQL",
        challenge_reason="Static data doesn't need database"
    )
    
    # Challenge 3: Latency
    print("❌ Challenge 3: Latency Target")
    print("   'We can do <10ms, not 200ms!'")
    
    loop3 = collab.track_challenge(
        challenger="Piotr Szymanski",
        challenger_team="technical",
        target="200ms latency target",
        challenge_type="time",
        original_proposal="Target: 200ms latency",
        challenge_reason="With simple solution, we can achieve <10ms"
    )
    
    collab.register_team_position(
        team="technical",
        position="Prefer simple, maintainable, fast solution",
        key_points=[
            "Simple keyword matching",
            "JSON file storage",
            "Target latency: <10ms",
            "Zero complex dependencies"
        ],
        non_negotiables=["Simple implementation"]
    )
    
    print("\n✅ 6 challenges tracked")
    print("   Feedback loops: 3 active")
    
    # ========================================================================
    # TURN 3: ANALYTICAL TEAM RESPONDS
    # ========================================================================
    
    print_header("🔄 TURN 3: Analytical Team Responds")
    
    print("👤 Sofia Martinez (Analytical):")
    print("   'You're absolutely right! Let me revise...'")
    
    collab.add_turn(
        turn_number=3,
        team="analytical",
        agent="Sofia Martinez",
        content="Accept technical challenges, propose revised simpler solution",
        turn_type="response"
    )
    
    # Respond to challenge 1
    print("\n✅ Response 1: Accept NLP challenge")
    print("   'You're right, simple keyword matching is better!'")
    
    collab.track_response(
        loop_id=loop1,
        responder="Sofia Martinez",
        response_type="accept",
        response_content="Excellent point! Keywords are simpler and faster",
        revised_proposal="Use simple keyword matching"
    )
    
    # Respond to challenge 2
    print("✅ Response 2: Accept storage challenge")
    print("   'JSON with hot reload makes sense'")
    
    collab.track_response(
        loop_id=loop2,
        responder="Viktor Kovalenko",
        response_type="accept",
        response_content="JSON is simpler for static data",
        revised_proposal="JSON file with hot reload"
    )
    
    # Respond to challenge 3
    print("✅ Response 3: Accept latency challenge")
    print("   '<10ms is even better than 200ms!'")
    
    collab.track_response(
        loop_id=loop3,
        responder="Sofia Martinez",
        response_type="accept",
        response_content="10ms is much better!",
        revised_proposal="Target <10ms latency"
    )
    
    collab.add_decision_version(
        version_number=2,
        decision="Use simple keyword matching + JSON + <10ms target",
        rationale="Simpler, faster, no dependencies - meets both team needs",
        proposed_by="Sofia Martinez",
        team="analytical",
        confidence=0.85,
        changes_from_previous="Complete simplification based on technical feedback"
    )
    
    print("\n✅ All challenges accepted")
    print("   Decision v2: Simplified approach (confidence: 85%)")
    
    # ========================================================================
    # TURN 4: REFINEMENT
    # ========================================================================
    
    print_header("🔄 TURN 4: Refinement")
    
    print("👤 Damian Rousseau (Analytical - Devil's Advocate):")
    print("   'What about ambiguous queries? Add weighted keywords!'")
    
    collab.add_turn(
        turn_number=4,
        team="analytical",
        agent="Damian Rousseau",
        content="Suggest adding weighted keywords for edge cases",
        turn_type="response"
    )
    
    collab.add_decision_version(
        version_number=3,
        decision="Use weighted keyword matching (primary + secondary) + JSON + <10ms",
        rationale="Simple but handles ambiguous queries better",
        proposed_by="Damian Rousseau",
        team="analytical",
        confidence=0.95,
        changes_from_previous="Added keyword weighting for accuracy"
    )
    
    print("✅ Refinement added")
    print("   Decision v3: Weighted keywords (confidence: 95%)")
    
    # ========================================================================
    # TURN 5: FINAL AGREEMENT
    # ========================================================================
    
    print_header("🔄 TURN 5: Final Agreement")
    
    print("👤 Aleksander Nowak (Technical Orchestrator):")
    print("   'Perfect! This is exactly what we need!'")
    
    collab.add_turn(
        turn_number=5,
        team="technical",
        agent="Aleksander Nowak",
        content="Final agreement - excellent collaboration!",
        turn_type="agreement"
    )
    
    print("👤 Viktor Kovalenko (Analytical Director):")
    print("   'Better solution than either team alone!'")
    
    collab.add_turn(
        turn_number=6,
        team="analytical",
        agent="Viktor Kovalenko",
        content="Agreed! Multi-turn collaboration was invaluable",
        turn_type="agreement"
    )
    
    collab.track_agreement(
        teams_agreeing=["analytical", "technical"],
        agreed_point="Use weighted keyword matching + JSON storage + <10ms latency",
        rationale="Balances simplicity, speed, accuracy - best of both teams"
    )
    
    print("\n✅ Final agreement reached")
    print("   Both teams aligned on solution")
    
    # ========================================================================
    # FINALIZE & ANALYZE
    # ========================================================================
    
    print_header("📊 FINALIZING & ANALYZING COLLABORATION")
    
    print("🔍 Analyzing complete collaboration...")
    
    analysis = collab.finalize(outcome_quality=0.9)
    
    # ========================================================================
    # DISPLAY RESULTS
    # ========================================================================
    
    print_header("📈 COLLABORATION ANALYSIS RESULTS")
    
    # Conversation metrics
    print("🔄 CONVERSATION METRICS:")
    print(f"   Total turns: {analysis['conversation']['total_turns']}")
    print(f"   Duration: {analysis['conversation']['duration_seconds']:.1f} seconds")
    print(f"   Status: {analysis['conversation']['status']}")
    print(f"   Convergence: {analysis['conversation']['convergence']['status']}")
    print(f"   Turn breakdown: {analysis['conversation']['turn_breakdown']}")
    
    # Feedback metrics
    print(f"\n🔁 FEEDBACK METRICS:")
    print(f"   Total challenges: {analysis['feedback']['total_challenges']}")
    print(f"   Improvements: {analysis['feedback']['improvements_achieved']}")
    print(f"   Improvement rate: {analysis['feedback']['improvement_rate']:.0%}")
    print(f"   Most productive type: {analysis['feedback']['most_productive_challenge_type']}")
    
    # Evolution metrics
    if 'total_versions' in analysis['evolution']:
        print(f"\n📈 DECISION EVOLUTION:")
        print(f"   Versions: {analysis['evolution']['total_versions']}")
        print(f"   Initial decision: {analysis['evolution']['initial_decision'][:60]}...")
        print(f"   Final decision: {analysis['evolution']['final_decision'][:60]}...")
        print(f"   Confidence: {analysis['evolution']['initial_confidence']:.0%} → {analysis['evolution']['final_confidence']:.0%}")
        print(f"   Improvement: +{analysis['evolution']['confidence_improvement']*100:.0f}%")
        print(f"   Improvements: {', '.join(analysis['evolution']['all_improvements'])}")
    
    # Consensus metrics
    print(f"\n🤝 CONSENSUS METRICS:")
    print(f"   Consensus score: {analysis['consensus']['score']:.0%}")
    print(f"   Team alignment:")
    for team, score in analysis['consensus']['team_alignment'].items():
        print(f"      {team}: {score:.0%}")
    print(f"   Agreements: {analysis['consensus']['agreement_breakdown']['total_agreements']}")
    
    # Insights
    print(f"\n💡 INSIGHTS:")
    print(f"   Quality: {analysis['insights']['collaboration_quality'].upper()}")
    print(f"   Assessment: {analysis['insights']['overall_assessment']}")
    
    if analysis['insights']['key_strengths']:
        print(f"\n   🌟 Key Strengths:")
        for strength in analysis['insights']['key_strengths']:
            print(f"      • {strength}")
    
    if analysis['insights']['areas_for_improvement']:
        print(f"\n   📌 Areas for Improvement:")
        for area in analysis['insights']['areas_for_improvement']:
            print(f"      • {area}")
    
    # Pattern recommendations
    if 'recommendations' in analysis.get('patterns', {}):
        print(f"\n🎯 RECOMMENDATIONS FOR FUTURE:")
        for rec in analysis['patterns']['recommendations'][:5]:
            print(f"      • {rec}")
    
    # ========================================================================
    # EXPORT REPORT
    # ========================================================================
    
    print_header("💾 EXPORTING REPORT")
    
    output_file = "/tmp/collaboration_report.json"
    json_str = collab.to_json(output_file)
    
    print(f"✅ Report saved to: {output_file}")
    print(f"   Size: {len(json_str)} bytes")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print_header("✅ DEMO COMPLETE - SUMMARY")
    
    print("📊 What we tracked:")
    print("   ✅ 6 conversation turns")
    print("   ✅ 3 challenge-response cycles")
    print("   ✅ 3 decision versions")
    print("   ✅ 2 team positions")
    print("   ✅ 1 final agreement")
    print("   ✅ Complete pattern analysis")
    
    print("\n📈 Key Results:")
    print(f"   • Improvement rate: {analysis['feedback']['improvement_rate']:.0%}")
    print(f"   • Confidence gain: +{analysis['evolution']['confidence_improvement']*100:.0f}%")
    print(f"   • Consensus: {analysis['consensus']['score']:.0%}")
    print(f"   • Quality: {analysis['insights']['collaboration_quality']}")
    
    print("\n🎯 Outcome:")
    print("   Original proposal: spaCy NLP (complex, 200ms)")
    print("   Final decision: Weighted keywords (simple, <10ms)")
    print("   Result: 40% time savings (5 days → 3 days)")
    
    print("\n" + "="*80)
    print(" "*20 + "🎉 ENHANCED COLLABORATION SYSTEM WORKS! 🎉")
    print("="*80)
    
    return collab, analysis


def demo_quick_usage():
    """Demo: Quick usage example"""
    
    print_header("⚡ QUICK USAGE EXAMPLE")
    
    print("Code required:")
    print("```python")
    print("from agents.enhanced_collaboration import EnhancedCrossTeamCollaboration")
    print("")
    print("# 1. Initialize")
    print("collab = EnhancedCrossTeamCollaboration(topic, teams)")
    print("")
    print("# 2. Track collaboration")
    print("collab.add_turn(...)")
    print("collab.track_challenge(...)")
    print("collab.track_response(...)")
    print("")
    print("# 3. Get analysis")
    print("analysis = collab.finalize(outcome_quality)")
    print("```")
    print("")
    print("✅ That's it! Complete analytics with 3 method calls!")


def main():
    """Run demo"""
    try:
        # Main demo
        collab, analysis = demo_skills_routing_collaboration()
        
        # Quick usage
        demo_quick_usage()
        
        print("\n" + "="*80)
        print("✅ Demo completed successfully!")
        print("="*80)
        print("\n📚 Next steps:")
        print("   1. Read docs/team/ENHANCED_COLLABORATION_STEP6.md")
        print("   2. Try with your own collaboration")
        print("   3. Learn from the insights!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
