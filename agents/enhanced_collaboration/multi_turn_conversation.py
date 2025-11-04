"""
Multi-Turn Conversation Tracker

Tracks complete multi-turn conversations between teams, including:
- Turn-by-turn conversation flow
- Convergence analysis
- Timeline tracking
- Status monitoring
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class MultiTurnConversation:
    """
    Track complete multi-turn conversations between teams
    
    Features:
    - Turn-by-turn tracking
    - Convergence analysis
    - Timeline tracking
    - Response threading
    """
    
    def __init__(self, topic: str, teams: List[str]):
        """
        Initialize multi-turn conversation
        
        Args:
            topic: Conversation topic
            teams: List of participating teams
        """
        self.topic = topic
        self.teams = teams
        self.turns = []  # List of turn objects
        self.start_time = datetime.now()
        self.end_time = None
        self.status = "active"  # active, converged, diverged, stalled
        
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
        Add a turn to conversation
        
        Args:
            turn_number: Turn sequence number
            team: Which team is speaking
            agent: Agent name
            content: Turn content
            turn_type: Type of turn
            metadata: Optional metadata
            
        Returns:
            The created turn object
        """
        if team not in self.teams:
            raise ValueError(f"Team '{team}' not in conversation teams: {self.teams}")
            
        turn = {
            "turn": turn_number,
            "team": team,
            "agent": agent,
            "timestamp": datetime.now(),
            "content": content,
            "type": turn_type,
            "metadata": metadata or {},
            "responses_to": self._find_parent_turn(team)
        }
        self.turns.append(turn)
        
        # Update status based on turn type
        self._update_status(turn_type)
        
        return turn
    
    def _find_parent_turn(self, current_team: str) -> Optional[int]:
        """
        Find which turn this is responding to
        
        Args:
            current_team: Current speaking team
            
        Returns:
            Turn number being responded to, or None
        """
        # Find most recent turn from a different team
        for turn in reversed(self.turns):
            if turn["team"] != current_team:
                return turn["turn"]
        return None
    
    def _update_status(self, turn_type: str):
        """Update conversation status based on latest turn"""
        if turn_type == "agreement":
            # Check if we have multiple agreements
            recent_agreements = sum(
                1 for t in self.turns[-3:] 
                if t["type"] == "agreement"
            )
            if recent_agreements >= 2:
                self.status = "converged"
        elif turn_type == "challenge":
            # Check if stuck in challenge loop
            recent_challenges = sum(
                1 for t in self.turns[-4:] 
                if t["type"] == "challenge"
            )
            if recent_challenges >= 3:
                self.status = "diverged"
    
    def get_conversation_flow(self) -> Dict:
        """
        Get complete conversation flow
        
        Returns:
            Dictionary with conversation details
        """
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "topic": self.topic,
            "teams": self.teams,
            "total_turns": len(self.turns),
            "duration_seconds": duration,
            "status": self.status,
            "convergence_analysis": self._analyze_convergence(),
            "turn_breakdown": self._count_turn_types(),
            "turns": [
                {
                    "turn": t["turn"],
                    "team": t["team"],
                    "agent": t["agent"],
                    "type": t["type"],
                    "timestamp": t["timestamp"].isoformat(),
                    "content_preview": t["content"][:100] + "..." if len(t["content"]) > 100 else t["content"]
                }
                for t in self.turns
            ]
        }
    
    def _analyze_convergence(self) -> Dict:
        """
        Analyze convergence status
        
        Returns:
            Convergence analysis
        """
        if not self.turns:
            return {"status": "no_data", "confidence": 0.0}
        
        recent_turns = self.turns[-3:]  # Last 3 turns
        
        agreement_count = sum(1 for t in recent_turns if t["type"] == "agreement")
        challenge_count = sum(1 for t in recent_turns if t["type"] == "challenge")
        response_count = sum(1 for t in recent_turns if t["type"] == "response")
        
        if agreement_count >= 2:
            status = "converging"
            confidence = 0.9
        elif challenge_count >= 2:
            status = "diverging"
            confidence = 0.7
        elif response_count >= 2:
            status = "negotiating"
            confidence = 0.6
        else:
            status = "exploring"
            confidence = 0.5
        
        return {
            "status": status,
            "confidence": confidence,
            "recent_agreements": agreement_count,
            "recent_challenges": challenge_count,
            "recent_responses": response_count
        }
    
    def _count_turn_types(self) -> Dict[str, int]:
        """Count turns by type"""
        types = {}
        for turn in self.turns:
            t = turn["type"]
            types[t] = types.get(t, 0) + 1
        return types
    
    def get_turn_sequence(self) -> List[str]:
        """
        Get sequence of turn types
        
        Returns:
            List of turn types in order
        """
        return [t["type"] for t in self.turns]
    
    def get_team_participation(self) -> Dict[str, int]:
        """
        Get participation count by team
        
        Returns:
            Dictionary with team participation counts
        """
        participation = {team: 0 for team in self.teams}
        for turn in self.turns:
            participation[turn["team"]] += 1
        return participation
    
    def finalize(self):
        """Mark conversation as finalized"""
        self.end_time = datetime.now()
        if self.status == "active":
            # Determine final status
            convergence = self._analyze_convergence()
            if convergence["status"] == "converging":
                self.status = "converged"
            else:
                self.status = "completed"
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "topic": self.topic,
            "teams": self.teams,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "total_turns": len(self.turns),
            "conversation_flow": self.get_conversation_flow(),
            "team_participation": self.get_team_participation()
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
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str
    
    def __repr__(self) -> str:
        return f"<MultiTurnConversation topic='{self.topic}' turns={len(self.turns)} status='{self.status}'>"


# Quick test
if __name__ == "__main__":
    print("🔄 Multi-Turn Conversation Tracker\n")
    
    # Create conversation
    conv = MultiTurnConversation(
        topic="Test Topic",
        teams=["analytical", "technical"]
    )
    
    # Add turns
    conv.add_turn(1, "analytical", "Lucas", "Initial proposal", "proposal")
    conv.add_turn(2, "technical", "Tomasz", "I challenge this", "challenge")
    conv.add_turn(3, "analytical", "Sofia", "Good point, revised", "response")
    conv.add_turn(4, "technical", "Aleksander", "Agreed!", "agreement")
    
    # Get flow
    flow = conv.get_conversation_flow()
    print(f"Topic: {flow['topic']}")
    print(f"Total turns: {flow['total_turns']}")
    print(f"Status: {flow['status']}")
    print(f"Convergence: {flow['convergence_analysis']}")
    print(f"\nTurn breakdown: {flow['turn_breakdown']}")
    
    print("\n✅ Multi-Turn Conversation system working!")
