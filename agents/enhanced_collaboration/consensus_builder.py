"""
Consensus Builder

Build consensus between teams through structured agreement tracking:
- Team position tracking
- Common ground detection
- Compromise proposals
- Consensus measurement
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class ConsensusBuilder:
    """
    Build consensus between teams through structured agreement tracking
    
    Features:
    - Team position registration
    - Common ground detection
    - Compromise proposals
    - Consensus scoring
    - Agreement tracking
    """
    
    def __init__(self, topic: str, teams: List[str]):
        """
        Initialize consensus builder
        
        Args:
            topic: Topic for consensus building
            teams: List of participating teams
        """
        self.topic = topic
        self.teams = teams
        self.positions = {}  # Team positions
        self.agreements = []  # Tracked agreements
        self.disagreements = []  # Tracked disagreements
        
    def register_position(
        self,
        team: str,
        position: str,
        key_points: List[str],
        non_negotiables: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Register a team's position
        
        Args:
            team: Team name
            position: Team's position statement
            key_points: Key points of the position
            non_negotiables: Non-negotiable requirements
            metadata: Optional metadata
            
        Returns:
            Position object
        """
        if team not in self.teams:
            raise ValueError(f"Team '{team}' not in consensus teams: {self.teams}")
        
        position_obj = {
            "team": team,
            "position": position,
            "key_points": key_points,
            "non_negotiables": non_negotiables or [],
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        self.positions[team] = position_obj
        
        return position_obj
    
    def find_common_ground(self) -> Dict:
        """
        Find areas of agreement between teams
        
        Returns:
            Common ground analysis
        """
        if len(self.positions) < 2:
            return {"error": "Need at least 2 team positions"}
        
        # Collect all key points from all teams
        all_points = []
        for team, pos in self.positions.items():
            for point in pos["key_points"]:
                all_points.append({
                    "team": team,
                    "point": point,
                    "point_lower": point.lower()
                })
        
        # Find overlaps (simple keyword-based matching)
        common = []
        seen_points = set()
        
        for i, item1 in enumerate(all_points):
            if item1["point_lower"] in seen_points:
                continue
                
            matching_teams = [item1["team"]]
            
            for item2 in all_points[i+1:]:
                if item2["team"] in matching_teams:
                    continue
                
                # Check for keyword overlap
                if self._points_similar(item1["point_lower"], item2["point_lower"]):
                    matching_teams.append(item2["team"])
            
            if len(matching_teams) >= 2:
                common.append({
                    "point": item1["point"],
                    "teams_agreeing": matching_teams,
                    "agreement_strength": len(matching_teams) / len(self.teams)
                })
                seen_points.add(item1["point_lower"])
        
        # Find unique positions (potential conflicts)
        conflicts = self._find_conflicts()
        
        return {
            "common_ground": common,
            "unique_positions": self._find_unique_positions(),
            "conflicts": conflicts,
            "agreement_areas": len(common),
            "conflict_areas": len(conflicts)
        }
    
    def _points_similar(self, point1: str, point2: str) -> bool:
        """Check if two points are similar"""
        # Simple keyword overlap
        words1 = set(point1.split())
        words2 = set(point2.split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        words1 = words1 - common_words
        words2 = words2 - common_words
        
        if not words1 or not words2:
            return False
        
        # Check overlap
        overlap = len(words1 & words2)
        min_length = min(len(words1), len(words2))
        
        # Consider similar if >50% overlap
        return overlap / min_length > 0.5
    
    def _find_unique_positions(self) -> Dict[str, List[str]]:
        """Find unique positions per team"""
        unique = {}
        
        for team, pos in self.positions.items():
            unique_points = []
            
            for point in pos["key_points"]:
                # Check if this point is shared
                is_shared = False
                point_lower = point.lower()
                
                for other_team, other_pos in self.positions.items():
                    if other_team == team:
                        continue
                    
                    for other_point in other_pos["key_points"]:
                        if self._points_similar(point_lower, other_point.lower()):
                            is_shared = True
                            break
                    
                    if is_shared:
                        break
                
                if not is_shared:
                    unique_points.append(point)
            
            if unique_points:
                unique[team] = unique_points
        
        return unique
    
    def _find_conflicts(self) -> List[Dict]:
        """Find conflicting positions"""
        conflicts = []
        
        # Check non-negotiables for conflicts
        for team1, pos1 in self.positions.items():
            for non_neg in pos1["non_negotiables"]:
                # Check if contradicted by other teams
                for team2, pos2 in self.positions.items():
                    if team1 == team2:
                        continue
                    
                    # Simple contradiction detection
                    non_neg_lower = non_neg.lower()
                    
                    for point in pos2["key_points"]:
                        point_lower = point.lower()
                        
                        # Check for negation words near similar concepts
                        if self._indicates_conflict(non_neg_lower, point_lower):
                            conflicts.append({
                                "team1": team1,
                                "position1": non_neg,
                                "team2": team2,
                                "position2": point,
                                "conflict_type": "non_negotiable_conflict"
                            })
        
        return conflicts
    
    def _indicates_conflict(self, text1: str, text2: str) -> bool:
        """Check if two texts indicate conflict"""
        negation_words = ["no", "not", "never", "avoid", "reject", "against"]
        
        # Check if one has negation and they share keywords
        has_negation1 = any(neg in text1 for neg in negation_words)
        has_negation2 = any(neg in text2 for neg in negation_words)
        
        if has_negation1 != has_negation2:
            # One has negation, other doesn't
            # Check if they talk about same thing
            words1 = set(text1.split()) - {"no", "not", "never", "avoid", "reject", "against"}
            words2 = set(text2.split()) - {"no", "not", "never", "avoid", "reject", "against"}
            
            overlap = len(words1 & words2)
            if overlap >= 2:  # At least 2 shared keywords
                return True
        
        return False
    
    def propose_compromise(self) -> Dict:
        """
        Propose compromise solutions
        
        Returns:
            Compromise proposals
        """
        common = self.find_common_ground()
        
        compromise = {
            "agreed_points": common["common_ground"],
            "compromise_proposals": [],
            "areas_for_discussion": common["conflicts"]
        }
        
        # Generate compromise proposals for conflicts
        for conflict in common["conflicts"]:
            proposal = self._generate_compromise_proposal(conflict)
            if proposal:
                compromise["compromise_proposals"].append(proposal)
        
        # For unique positions, suggest optional features
        unique = common["unique_positions"]
        if unique:
            compromise["optional_features"] = {
                "description": "Team-specific features that could be optional",
                "suggestions": []
            }
            
            for team, points in unique.items():
                for point in points:
                    compromise["optional_features"]["suggestions"].append({
                        "feature": point,
                        "team": team,
                        "status": "optional"
                    })
        
        return compromise
    
    def _generate_compromise_proposal(self, conflict: Dict) -> Optional[Dict]:
        """Generate compromise proposal for a conflict"""
        # Simple heuristic-based compromise generation
        
        return {
            "conflict": f"{conflict['team1']} vs {conflict['team2']}",
            "proposal": "Find middle ground or make feature optional",
            "rationale": "Both teams have valid concerns",
            "requires_discussion": True
        }
    
    def track_agreement(
        self,
        teams_agreeing: List[str],
        agreed_point: str,
        rationale: str,
        metadata: Optional[Dict] = None
    ):
        """
        Track when teams reach agreement
        
        Args:
            teams_agreeing: List of teams in agreement
            agreed_point: What was agreed upon
            rationale: Why this agreement was reached
            metadata: Optional metadata
        """
        agreement = {
            "teams": teams_agreeing,
            "point": agreed_point,
            "rationale": rationale,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        self.agreements.append(agreement)
    
    def track_disagreement(
        self,
        teams_disagreeing: List[str],
        disagreement_point: str,
        reason: str,
        metadata: Optional[Dict] = None
    ):
        """
        Track disagreements
        
        Args:
            teams_disagreeing: Teams in disagreement
            disagreement_point: Point of disagreement
            reason: Reason for disagreement
            metadata: Optional metadata
        """
        disagreement = {
            "teams": teams_disagreeing,
            "point": disagreement_point,
            "reason": reason,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        self.disagreements.append(disagreement)
    
    def get_consensus_score(self) -> float:
        """
        Calculate consensus score (0-1)
        
        Returns:
            Consensus score
        """
        if not self.positions:
            return 0.0
        
        # Count total points across all teams
        total_points = sum(
            len(pos["key_points"]) 
            for pos in self.positions.values()
        )
        
        if total_points == 0:
            return 0.0
        
        # Agreements contribute positively
        agreed_points = len(self.agreements)
        
        # Common ground also contributes
        common = self.find_common_ground()
        common_points = len(common.get("common_ground", []))
        
        # Calculate score
        consensus_items = agreed_points + common_points
        
        return min(1.0, consensus_items / total_points)
    
    def get_agreement_breakdown(self) -> Dict:
        """Get breakdown of agreements and disagreements"""
        return {
            "total_agreements": len(self.agreements),
            "total_disagreements": len(self.disagreements),
            "agreement_rate": len(self.agreements) / (len(self.agreements) + len(self.disagreements)) if (len(self.agreements) + len(self.disagreements)) > 0 else 0.0,
            "agreements": self.agreements,
            "disagreements": self.disagreements
        }
    
    def get_team_alignment(self) -> Dict[str, float]:
        """
        Get alignment score for each team
        
        Returns:
            Alignment scores per team
        """
        if len(self.positions) < 2:
            return {}
        
        alignment = {}
        
        for team in self.teams:
            if team not in self.positions:
                alignment[team] = 0.0
                continue
            
            # Count how many agreements this team is part of
            team_agreements = sum(
                1 for agr in self.agreements 
                if team in agr["teams"]
            )
            
            # Calculate alignment
            if len(self.agreements) > 0:
                alignment[team] = team_agreements / len(self.agreements)
            else:
                alignment[team] = 0.0
        
        return alignment
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "topic": self.topic,
            "teams": self.teams,
            "positions": {
                team: {
                    **pos,
                    "timestamp": pos["timestamp"].isoformat()
                }
                for team, pos in self.positions.items()
            },
            "consensus_score": self.get_consensus_score(),
            "common_ground": self.find_common_ground(),
            "agreement_breakdown": self.get_agreement_breakdown(),
            "team_alignment": self.get_team_alignment(),
            "compromise": self.propose_compromise()
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
        
        # Make timestamps JSON serializable
        if "agreement_breakdown" in data:
            for agr in data["agreement_breakdown"].get("agreements", []):
                if "timestamp" in agr:
                    agr["timestamp"] = agr["timestamp"].isoformat()
            for disagr in data["agreement_breakdown"].get("disagreements", []):
                if "timestamp" in disagr:
                    disagr["timestamp"] = disagr["timestamp"].isoformat()
        
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str
    
    def __repr__(self) -> str:
        score = self.get_consensus_score()
        return f"<ConsensusBuilder topic='{self.topic}' teams={len(self.teams)} consensus={score:.0%}>"


# Quick test
if __name__ == "__main__":
    print("🤝 Consensus Builder\n")
    
    # Create builder
    builder = ConsensusBuilder(
        topic="Skills Routing Implementation",
        teams=["analytical", "technical"]
    )
    
    # Register positions
    builder.register_position(
        team="analytical",
        position="Need accurate intent detection",
        key_points=[
            "User-friendly natural language",
            "High accuracy (>80%)",
            "Fast response"
        ],
        non_negotiables=["High accuracy"]
    )
    
    builder.register_position(
        team="technical",
        position="Prefer simple, maintainable solution",
        key_points=[
            "No complex dependencies",
            "Very fast response",
            "Easy to debug"
        ],
        non_negotiables=["Simple implementation"]
    )
    
    # Find common ground
    common = builder.find_common_ground()
    print(f"Common ground areas: {len(common['common_ground'])}")
    print(f"Conflicts: {len(common['conflicts'])}")
    
    # Track agreement
    builder.track_agreement(
        teams_agreeing=["analytical", "technical"],
        agreed_point="Use keyword matching with <10ms target",
        rationale="Meets both speed and simplicity requirements"
    )
    
    # Get consensus score
    score = builder.get_consensus_score()
    print(f"Consensus score: {score:.1%}")
    
    print("\n✅ Consensus Builder working!")
