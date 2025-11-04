"""
Feedback Loop Tracker

Tracks challenge-response-improvement cycles in multi-turn collaboration:
- Challenge tracking
- Response tracking
- Improvement measurement
- Resolution analysis
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class FeedbackLoopTracker:
    """
    Track challenge-response-improvement cycles
    
    Features:
    - Challenge tracking with classification
    - Response tracking (accept/counter/defend)
    - Improvement detection
    - Resolution metrics
    - Productivity analysis
    """
    
    def __init__(self):
        """Initialize feedback loop tracker"""
        self.loops = []  # List of feedback loop objects
        self.loop_id_counter = 0
        
    def track_challenge(
        self,
        challenger: str,
        challenger_team: str,
        target: str,
        challenge_type: str,  # "technical", "cost", "complexity", "risk", "time"
        original_proposal: str,
        challenge_reason: str,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Track a challenge
        
        Args:
            challenger: Name of person challenging
            challenger_team: Team of challenger
            target: What/who is being challenged
            challenge_type: Type of challenge
            original_proposal: Original proposal being challenged
            challenge_reason: Reason for challenge
            metadata: Optional metadata
            
        Returns:
            Loop ID for tracking responses
        """
        self.loop_id_counter += 1
        
        loop = {
            "id": self.loop_id_counter,
            "challenger": challenger,
            "challenger_team": challenger_team,
            "target": target,
            "type": challenge_type,
            "original_proposal": original_proposal,
            "challenge_reason": challenge_reason,
            "timestamp": datetime.now(),
            "responses": [],
            "resolution": None,  # "improved", "original_maintained", "unresolved"
            "improvement_achieved": False,
            "metadata": metadata or {}
        }
        
        self.loops.append(loop)
        return loop["id"]
    
    def track_response(
        self,
        loop_id: int,
        responder: str,
        response_type: str,  # "accept", "counter", "defend", "compromise"
        response_content: str,
        revised_proposal: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Track response to challenge
        
        Args:
            loop_id: Loop ID from track_challenge
            responder: Person responding
            response_type: Type of response
            response_content: Response content
            revised_proposal: Revised proposal if any
            metadata: Optional metadata
            
        Returns:
            True if response tracked successfully
        """
        loop = self._find_loop(loop_id)
        
        if not loop:
            return False
        
        response = {
            "responder": responder,
            "type": response_type,
            "content": response_content,
            "revised_proposal": revised_proposal,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        loop["responses"].append(response)
        
        # Analyze resolution
        self._update_resolution(loop, response_type, revised_proposal)
        
        return True
    
    def _find_loop(self, loop_id: int) -> Optional[Dict]:
        """Find loop by ID"""
        for loop in self.loops:
            if loop["id"] == loop_id:
                return loop
        return None
    
    def _update_resolution(
        self,
        loop: Dict,
        response_type: str,
        revised_proposal: Optional[str]
    ):
        """Update resolution status based on response"""
        if response_type == "accept" and revised_proposal:
            loop["resolution"] = "improved"
            loop["improvement_achieved"] = True
        elif response_type == "accept" and not revised_proposal:
            loop["resolution"] = "improved"
            loop["improvement_achieved"] = True
        elif response_type == "compromise":
            loop["resolution"] = "improved"
            loop["improvement_achieved"] = True
        elif response_type == "defend":
            loop["resolution"] = "original_maintained"
            loop["improvement_achieved"] = False
        elif response_type == "counter":
            # Counter-challenge, resolution still pending
            loop["resolution"] = "unresolved"
    
    def get_loop(self, loop_id: int) -> Optional[Dict]:
        """
        Get loop details
        
        Args:
            loop_id: Loop ID
            
        Returns:
            Loop details or None
        """
        return self._find_loop(loop_id)
    
    def get_improvement_metrics(self) -> Dict:
        """
        Get metrics on improvements from challenges
        
        Returns:
            Dictionary with improvement metrics
        """
        total_loops = len(self.loops)
        
        if total_loops == 0:
            return {
                "total_challenges": 0,
                "improvements_achieved": 0,
                "improvement_rate": 0.0,
                "by_challenge_type": {},
                "most_productive_challenge_type": None
            }
        
        improved = sum(1 for l in self.loops if l["improvement_achieved"])
        
        # Break down by challenge type
        by_type = {}
        for loop in self.loops:
            type_ = loop["type"]
            if type_ not in by_type:
                by_type[type_] = {"total": 0, "improved": 0}
            by_type[type_]["total"] += 1
            if loop["improvement_achieved"]:
                by_type[type_]["improved"] += 1
        
        # Calculate improvement rates per type
        for type_ in by_type:
            total = by_type[type_]["total"]
            improved_count = by_type[type_]["improved"]
            by_type[type_]["improvement_rate"] = improved_count / total if total > 0 else 0.0
        
        # Find most productive challenge type
        most_productive = None
        if by_type:
            most_productive = max(
                by_type.items(),
                key=lambda x: x[1]["improvement_rate"]
            )[0]
        
        return {
            "total_challenges": total_loops,
            "improvements_achieved": improved,
            "improvement_rate": improved / total_loops,
            "by_challenge_type": by_type,
            "most_productive_challenge_type": most_productive,
            "resolved_loops": sum(1 for l in self.loops if l["resolution"] is not None),
            "unresolved_loops": sum(1 for l in self.loops if l["resolution"] is None)
        }
    
    def get_challenge_breakdown(self) -> Dict[str, int]:
        """Get breakdown of challenges by type"""
        breakdown = {}
        for loop in self.loops:
            type_ = loop["type"]
            breakdown[type_] = breakdown.get(type_, 0) + 1
        return breakdown
    
    def get_resolution_breakdown(self) -> Dict[str, int]:
        """Get breakdown of resolutions"""
        breakdown = {}
        for loop in self.loops:
            resolution = loop["resolution"] or "unresolved"
            breakdown[resolution] = breakdown.get(resolution, 0) + 1
        return breakdown
    
    def get_loops_by_type(self, challenge_type: str) -> List[Dict]:
        """
        Get all loops of a specific type
        
        Args:
            challenge_type: Type to filter by
            
        Returns:
            List of matching loops
        """
        return [loop for loop in self.loops if loop["type"] == challenge_type]
    
    def get_loops_by_challenger(self, challenger: str) -> List[Dict]:
        """
        Get all loops by specific challenger
        
        Args:
            challenger: Challenger name
            
        Returns:
            List of loops from this challenger
        """
        return [loop for loop in self.loops if loop["challenger"] == challenger]
    
    def get_team_challenge_stats(self, team: str) -> Dict:
        """
        Get challenge statistics for a team
        
        Args:
            team: Team name
            
        Returns:
            Team statistics
        """
        team_loops = [l for l in self.loops if l["challenger_team"] == team]
        
        if not team_loops:
            return {
                "team": team,
                "total_challenges": 0,
                "improvements_from_challenges": 0,
                "success_rate": 0.0
            }
        
        improvements = sum(1 for l in team_loops if l["improvement_achieved"])
        
        return {
            "team": team,
            "total_challenges": len(team_loops),
            "improvements_from_challenges": improvements,
            "success_rate": improvements / len(team_loops),
            "challenge_breakdown": self._count_types(team_loops)
        }
    
    def _count_types(self, loops: List[Dict]) -> Dict[str, int]:
        """Count challenge types in loop list"""
        counts = {}
        for loop in loops:
            type_ = loop["type"]
            counts[type_] = counts.get(type_, 0) + 1
        return counts
    
    def get_top_challengers(self, limit: int = 5) -> List[Dict]:
        """
        Get top challengers by impact
        
        Args:
            limit: Number of top challengers to return
            
        Returns:
            List of top challengers with stats
        """
        challenger_stats = {}
        
        for loop in self.loops:
            challenger = loop["challenger"]
            if challenger not in challenger_stats:
                challenger_stats[challenger] = {
                    "name": challenger,
                    "total_challenges": 0,
                    "improvements_achieved": 0
                }
            
            challenger_stats[challenger]["total_challenges"] += 1
            if loop["improvement_achieved"]:
                challenger_stats[challenger]["improvements_achieved"] += 1
        
        # Calculate impact scores
        for stats in challenger_stats.values():
            total = stats["total_challenges"]
            improved = stats["improvements_achieved"]
            stats["impact_score"] = improved / total if total > 0 else 0.0
        
        # Sort by impact score
        sorted_challengers = sorted(
            challenger_stats.values(),
            key=lambda x: x["impact_score"],
            reverse=True
        )
        
        return sorted_challengers[:limit]
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "total_loops": len(self.loops),
            "improvement_metrics": self.get_improvement_metrics(),
            "challenge_breakdown": self.get_challenge_breakdown(),
            "resolution_breakdown": self.get_resolution_breakdown(),
            "loops": [
                {
                    **loop,
                    "timestamp": loop["timestamp"].isoformat(),
                    "responses": [
                        {
                            **r,
                            "timestamp": r["timestamp"].isoformat()
                        }
                        for r in loop["responses"]
                    ]
                }
                for loop in self.loops
            ]
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
        metrics = self.get_improvement_metrics()
        return f"<FeedbackLoopTracker loops={len(self.loops)} improvements={metrics['improvements_achieved']} rate={metrics['improvement_rate']:.2%}>"


# Quick test
if __name__ == "__main__":
    print("🔄 Feedback Loop Tracker\n")
    
    # Create tracker
    tracker = FeedbackLoopTracker()
    
    # Track challenge
    loop_id = tracker.track_challenge(
        challenger="Tomasz Kamiński",
        challenger_team="technical",
        target="Analytical proposal",
        challenge_type="complexity",
        original_proposal="Use spaCy for NLP",
        challenge_reason="Too complex, 100MB+ dependency"
    )
    
    # Track response
    tracker.track_response(
        loop_id=loop_id,
        responder="Sofia Martinez",
        response_type="accept",
        response_content="You're right, let's simplify",
        revised_proposal="Use simple keyword matching"
    )
    
    # Get metrics
    metrics = tracker.get_improvement_metrics()
    print(f"Total challenges: {metrics['total_challenges']}")
    print(f"Improvements achieved: {metrics['improvements_achieved']}")
    print(f"Improvement rate: {metrics['improvement_rate']:.1%}")
    print(f"By type: {metrics['by_challenge_type']}")
    
    print("\n✅ Feedback Loop Tracker working!")
