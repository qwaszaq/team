"""
Enhanced Cross-Team Collaboration - Integrated System

Complete collaboration tracking system integrating all components:
- MultiTurnConversation
- FeedbackLoopTracker
- DecisionEvolutionTracker
- ConsensusBuilder
- CollaborationPatternRecognizer
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from .multi_turn_conversation import MultiTurnConversation
from .feedback_loop_tracker import FeedbackLoopTracker
from .decision_evolution_tracker import DecisionEvolutionTracker
from .consensus_builder import ConsensusBuilder
from .pattern_recognizer import CollaborationPatternRecognizer


class EnhancedCrossTeamCollaboration:
    """
    Complete enhanced cross-team collaboration system
    
    Integrates all 5 components into a unified, easy-to-use interface
    for tracking and analyzing multi-turn team collaborations.
    """
    
    def __init__(self, topic: str, teams: List[str]):
        """
        Initialize integrated collaboration system
        
        Args:
            topic: Collaboration topic
            teams: List of participating teams
        """
        self.topic = topic
        self.teams = teams
        
        # Initialize all components
        self.conversation = MultiTurnConversation(topic, teams)
        self.feedback = FeedbackLoopTracker()
        self.evolution = DecisionEvolutionTracker(topic)
        self.consensus = ConsensusBuilder(topic, teams)
        self.recognizer = CollaborationPatternRecognizer()
        
        self.finalized = False
        
    def add_turn(
        self,
        turn_number: int,
        team: str,
        agent: str,
        content: str,
        turn_type: str,  # "proposal", "challenge", "response", "agreement"
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Add a turn to the conversation
        
        Automatically updates all relevant trackers.
        
        Args:
            turn_number: Turn sequence number
            team: Speaking team
            agent: Speaking agent
            content: Turn content
            turn_type: Type of turn
            metadata: Optional metadata
            
        Returns:
            Turn object
        """
        turn = self.conversation.add_turn(
            turn_number, team, agent, content, turn_type, metadata
        )
        
        return turn
    
    def track_challenge(
        self,
        challenger: str,
        challenger_team: str,
        target: str,
        challenge_type: str,
        original_proposal: str,
        challenge_reason: str
    ) -> int:
        """
        Track a challenge (integrates with FeedbackLoopTracker)
        
        Args:
            challenger: Name of challenger
            challenger_team: Team of challenger
            target: What is being challenged
            challenge_type: Type of challenge
            original_proposal: Original proposal
            challenge_reason: Reason for challenge
            
        Returns:
            Loop ID for tracking responses
        """
        loop_id = self.feedback.track_challenge(
            challenger, challenger_team, target,
            challenge_type, original_proposal, challenge_reason
        )
        
        return loop_id
    
    def track_response(
        self,
        loop_id: int,
        responder: str,
        response_type: str,
        response_content: str,
        revised_proposal: Optional[str] = None
    ) -> bool:
        """
        Track response to challenge
        
        Args:
            loop_id: Loop ID from track_challenge
            responder: Person responding
            response_type: Type of response
            response_content: Response content
            revised_proposal: Revised proposal if any
            
        Returns:
            Success status
        """
        return self.feedback.track_response(
            loop_id, responder, response_type,
            response_content, revised_proposal
        )
    
    def add_decision_version(
        self,
        version_number: int,
        decision: str,
        rationale: str,
        proposed_by: str,
        team: str,
        confidence: float,
        changes_from_previous: Optional[str] = None
    ) -> Dict:
        """
        Add a decision version (integrates with DecisionEvolutionTracker)
        
        Args:
            version_number: Version number
            decision: Decision text
            rationale: Reasoning
            proposed_by: Proposer
            team: Team
            confidence: Confidence score
            changes_from_previous: Description of changes
            
        Returns:
            Version object
        """
        return self.evolution.add_version(
            version_number, decision, rationale,
            proposed_by, team, confidence, changes_from_previous
        )
    
    def register_team_position(
        self,
        team: str,
        position: str,
        key_points: List[str],
        non_negotiables: Optional[List[str]] = None
    ) -> Dict:
        """
        Register a team's position (integrates with ConsensusBuilder)
        
        Args:
            team: Team name
            position: Position statement
            key_points: Key points
            non_negotiables: Non-negotiable requirements
            
        Returns:
            Position object
        """
        return self.consensus.register_position(
            team, position, key_points, non_negotiables
        )
    
    def track_agreement(
        self,
        teams_agreeing: List[str],
        agreed_point: str,
        rationale: str
    ):
        """
        Track agreement between teams
        
        Args:
            teams_agreeing: Teams in agreement
            agreed_point: What was agreed
            rationale: Why
        """
        self.consensus.track_agreement(teams_agreeing, agreed_point, rationale)
    
    def finalize(self, outcome_quality: float) -> Dict:
        """
        Finalize collaboration and generate complete analysis
        
        Args:
            outcome_quality: Quality score (0-1)
            
        Returns:
            Complete analysis
        """
        if self.finalized:
            return {"error": "Already finalized"}
        
        # Finalize conversation
        self.conversation.finalize()
        
        # Analyze pattern
        pattern = self.recognizer.analyze_conversation(
            self.conversation, outcome_quality
        )
        
        self.finalized = True
        
        # Generate complete analysis
        return self.get_complete_analysis()
    
    def get_complete_analysis(self) -> Dict:
        """
        Get complete analysis from all components
        
        Returns:
            Comprehensive analysis
        """
        # Get data from all components
        conversation_flow = self.conversation.get_conversation_flow()
        feedback_metrics = self.feedback.get_improvement_metrics()
        evolution_summary = self.evolution.get_evolution_summary() if self.evolution.versions else {}
        consensus_score = self.consensus.get_consensus_score()
        best_practices = self.recognizer.get_best_practices() if self.recognizer.patterns else {}
        
        return {
            "topic": self.topic,
            "teams": self.teams,
            "finalized": self.finalized,
            
            # Conversation analysis
            "conversation": {
                "total_turns": conversation_flow["total_turns"],
                "duration_seconds": conversation_flow["duration_seconds"],
                "status": conversation_flow["status"],
                "convergence": conversation_flow["convergence_analysis"],
                "turn_breakdown": conversation_flow["turn_breakdown"],
                "team_participation": self.conversation.get_team_participation()
            },
            
            # Feedback analysis
            "feedback": {
                "total_challenges": feedback_metrics["total_challenges"],
                "improvements_achieved": feedback_metrics["improvements_achieved"],
                "improvement_rate": feedback_metrics["improvement_rate"],
                "most_productive_challenge_type": feedback_metrics.get("most_productive_challenge_type"),
                "by_challenge_type": feedback_metrics.get("by_challenge_type", {})
            },
            
            # Decision evolution
            "evolution": evolution_summary if evolution_summary else {"message": "No decision versions tracked"},
            
            # Consensus analysis
            "consensus": {
                "score": consensus_score,
                "team_alignment": self.consensus.get_team_alignment(),
                "common_ground": self.consensus.find_common_ground() if len(self.consensus.positions) >= 2 else {},
                "agreement_breakdown": self.consensus.get_agreement_breakdown()
            },
            
            # Pattern recognition
            "patterns": best_practices if best_practices else {"message": "Not enough patterns"},
            
            # Overall insights
            "insights": self._generate_insights(
                conversation_flow, feedback_metrics,
                evolution_summary, consensus_score
            )
        }
    
    def _generate_insights(
        self,
        conversation: Dict,
        feedback: Dict,
        evolution: Dict,
        consensus_score: float
    ) -> Dict:
        """Generate high-level insights"""
        insights = {
            "collaboration_quality": "unknown",
            "key_strengths": [],
            "areas_for_improvement": [],
            "overall_assessment": ""
        }
        
        # Assess quality
        if consensus_score >= 0.8 and feedback.get("improvement_rate", 0) >= 0.7:
            insights["collaboration_quality"] = "excellent"
        elif consensus_score >= 0.6 and feedback.get("improvement_rate", 0) >= 0.5:
            insights["collaboration_quality"] = "good"
        elif consensus_score >= 0.4:
            insights["collaboration_quality"] = "moderate"
        else:
            insights["collaboration_quality"] = "needs_improvement"
        
        # Identify strengths
        if feedback.get("improvement_rate", 0) >= 0.7:
            insights["key_strengths"].append("High improvement rate from challenges")
        
        if consensus_score >= 0.7:
            insights["key_strengths"].append("Strong consensus achieved")
        
        if conversation["status"] == "converged":
            insights["key_strengths"].append("Successfully converged to agreement")
        
        if evolution and evolution.get("confidence_improvement", 0) > 0.2:
            insights["key_strengths"].append("Significant confidence improvement")
        
        # Identify areas for improvement
        if conversation["total_turns"] > 8:
            insights["areas_for_improvement"].append("Consider breaking down complex topics")
        
        if feedback.get("improvement_rate", 0) < 0.5:
            insights["areas_for_improvement"].append("More constructive challenges needed")
        
        if consensus_score < 0.5:
            insights["areas_for_improvement"].append("Work on building common ground earlier")
        
        # Overall assessment
        quality = insights["collaboration_quality"]
        turns = conversation["total_turns"]
        insights["overall_assessment"] = f"{quality.title()} collaboration in {turns} turns"
        
        return insights
    
    def to_dict(self) -> Dict:
        """Export complete system state"""
        return {
            "topic": self.topic,
            "teams": self.teams,
            "finalized": self.finalized,
            "complete_analysis": self.get_complete_analysis()
        }
    
    def to_json(self, filepath: Optional[str] = None) -> str:
        """
        Export to JSON
        
        Args:
            filepath: Optional file path to save to
            
        Returns:
            JSON string
        """
        data = self.to_dict()
        json_str = json.dumps(data, indent=2, default=str)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str
    
    def __repr__(self) -> str:
        turns = len(self.conversation.turns)
        status = "finalized" if self.finalized else "active"
        return f"<EnhancedCrossTeamCollaboration topic='{self.topic}' turns={turns} status='{status}'>"


# Quick test
if __name__ == "__main__":
    print("🚀 Enhanced Cross-Team Collaboration - Integrated System\n")
    
    # Create system
    collab = EnhancedCrossTeamCollaboration(
        topic="Test Collaboration",
        teams=["analytical", "technical"]
    )
    
    # Turn 1: Proposal
    collab.add_turn(1, "analytical", "Lucas", "Propose solution A", "proposal")
    collab.register_team_position("analytical", "Solution A", ["Fast", "Accurate"])
    collab.add_decision_version(1, "Solution A", "Initial proposal", "Lucas", "analytical", 0.7)
    
    # Turn 2: Challenge
    collab.add_turn(2, "technical", "Tomasz", "Challenge: too complex", "challenge")
    loop_id = collab.track_challenge("Tomasz", "technical", "Solution A", "complexity", "Solution A", "Too complex")
    collab.register_team_position("technical", "Simpler solution", ["Simple", "Fast"])
    
    # Turn 3: Agreement
    collab.add_turn(3, "analytical", "Sofia", "Agreed, use solution B", "agreement")
    collab.track_response(loop_id, "Sofia", "accept", "Good point", "Solution B")
    collab.add_decision_version(2, "Solution B", "Simpler version", "Sofia", "analytical", 0.9, "Simplified")
    collab.track_agreement(["analytical", "technical"], "Use solution B", "Simpler and faster")
    
    # Finalize
    analysis = collab.finalize(outcome_quality=0.9)
    
    print(f"Turns: {analysis['conversation']['total_turns']}")
    print(f"Consensus: {analysis['consensus']['score']:.0%}")
    print(f"Improvement rate: {analysis['feedback']['improvement_rate']:.0%}")
    print(f"Quality: {analysis['insights']['collaboration_quality']}")
    
    print("\n✅ Integrated System working!")
