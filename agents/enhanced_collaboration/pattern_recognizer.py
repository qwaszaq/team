"""
Collaboration Pattern Recognizer

Recognize and learn from successful collaboration patterns:
- Pattern identification
- Success indicator detection
- Best practices extraction
- Learning from history
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class CollaborationPatternRecognizer:
    """
    Recognize and learn from successful collaboration patterns
    
    Features:
    - Pattern identification
    - Success scoring
    - Best practices extraction
    - Recommendation generation
    """
    
    def __init__(self):
        """Initialize pattern recognizer"""
        self.patterns = []  # Recorded patterns
        self.success_indicators = []  # Successful patterns
        
    def analyze_conversation(
        self,
        conversation: Any,  # MultiTurnConversation
        outcome_quality: float,  # 0-1 score
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze a conversation for patterns
        
        Args:
            conversation: MultiTurnConversation object
            outcome_quality: Quality score (0-1)
            metadata: Optional metadata
            
        Returns:
            Pattern analysis
        """
        pattern = {
            "total_turns": len(conversation.turns),
            "teams_involved": conversation.teams,
            "turn_types": self._count_turn_types(conversation),
            "outcome_quality": outcome_quality,
            "convergence_path": self._analyze_convergence_path(conversation),
            "time_to_consensus": self._calculate_duration(conversation),
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        self.patterns.append(pattern)
        
        # Track if this is a success pattern
        if outcome_quality >= 0.8:
            self.success_indicators.append(pattern)
        
        return pattern
    
    def _count_turn_types(self, conv: Any) -> Dict[str, int]:
        """Count turn types in conversation"""
        types = {}
        for turn in conv.turns:
            t = turn["type"]
            types[t] = types.get(t, 0) + 1
        return types
    
    def _analyze_convergence_path(self, conv: Any) -> str:
        """Analyze how convergence happened"""
        if not conv.turns:
            return "no_data"
        
        # Get sequence of turn types
        types = [t["type"] for t in conv.turns]
        
        # Identify patterns
        if types == ["proposal", "challenge", "agreement"]:
            return "quick_agreement_after_challenge"
        elif types == ["proposal", "agreement"]:
            return "immediate_agreement"
        elif "challenge" in types and types[-1] == "agreement":
            return "challenge_led_to_improvement"
        elif types.count("challenge") > 2:
            return "extensive_negotiation"
        elif "response" in types and types[-1] == "agreement":
            return "collaborative_refinement"
        else:
            return "gradual_consensus"
    
    def _calculate_duration(self, conv: Any) -> float:
        """Calculate duration in seconds"""
        if not conv.turns or len(conv.turns) < 2:
            return 0.0
        
        start = conv.turns[0]["timestamp"]
        end = conv.turns[-1]["timestamp"]
        
        return (end - start).total_seconds()
    
    def get_best_practices(self) -> Dict:
        """
        Extract best practices from successful patterns
        
        Returns:
            Best practices recommendations
        """
        if not self.success_indicators:
            return {
                "message": "Not enough successful patterns",
                "recommendations": []
            }
        
        # Analyze successful patterns
        avg_turns = sum(p["total_turns"] for p in self.success_indicators) / len(self.success_indicators)
        
        # Find most common convergence path
        paths = [p["convergence_path"] for p in self.success_indicators]
        most_common_path = max(set(paths), key=paths.count) if paths else "unknown"
        
        # Calculate success rate
        total_patterns = len(self.patterns)
        successful_patterns = len(self.success_indicators)
        success_rate = successful_patterns / total_patterns if total_patterns > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(most_common_path, avg_turns)
        
        return {
            "optimal_turn_count": round(avg_turns),
            "most_successful_path": most_common_path,
            "success_rate": success_rate,
            "total_patterns_analyzed": total_patterns,
            "successful_patterns": successful_patterns,
            "recommendations": recommendations,
            "turn_type_analysis": self._analyze_turn_types()
        }
    
    def _generate_recommendations(self, best_path: str, avg_turns: float) -> List[str]:
        """Generate recommendations based on patterns"""
        recommendations = []
        
        # Path-specific recommendations
        path_recs = {
            "quick_agreement_after_challenge": [
                "Challenge proposals early and constructively",
                "Be open to accepting good challenges",
                "Focus on technical merit over ego",
                "Quick iteration leads to better outcomes"
            ],
            "challenge_led_to_improvement": [
                "Encourage constructive challenges",
                "Respond with revised proposals, not defenses",
                "Focus on improvement, not winning arguments",
                "Challenges are opportunities for better solutions"
            ],
            "extensive_negotiation": [
                "Break down complex decisions into smaller parts",
                "Find common ground first, then tackle differences",
                "Iterate on specific points rather than everything at once",
                "Set time limits for negotiations"
            ],
            "collaborative_refinement": [
                "Build on each other's ideas",
                "Use 'yes, and' instead of 'yes, but'",
                "Incremental improvements work better than big changes",
                "Collaborative refinement beats competition"
            ],
            "immediate_agreement": [
                "Some decisions are straightforward",
                "Don't over-complicate simple agreements",
                "Trust team expertise",
                "Move quickly when consensus is clear"
            ]
        }
        
        recommendations.extend(path_recs.get(best_path, []))
        
        # Turn count recommendations
        if avg_turns < 3:
            recommendations.append("Short conversations work well - keep discussions focused")
        elif avg_turns > 6:
            recommendations.append("Long conversations may indicate complexity - consider breaking down topics")
        else:
            recommendations.append(f"Optimal conversation length is around {round(avg_turns)} turns")
        
        return recommendations
    
    def _analyze_turn_types(self) -> Dict:
        """Analyze turn type patterns in successful collaborations"""
        if not self.success_indicators:
            return {}
        
        # Aggregate turn types from successful patterns
        total_types = {}
        for pattern in self.success_indicators:
            for turn_type, count in pattern["turn_types"].items():
                total_types[turn_type] = total_types.get(turn_type, 0) + count
        
        # Calculate percentages
        total_turns = sum(total_types.values())
        percentages = {
            turn_type: (count / total_turns) * 100 
            for turn_type, count in total_types.items()
        } if total_turns > 0 else {}
        
        return {
            "counts": total_types,
            "percentages": percentages,
            "insight": self._generate_turn_type_insight(percentages)
        }
    
    def _generate_turn_type_insight(self, percentages: Dict[str, float]) -> str:
        """Generate insight from turn type percentages"""
        if not percentages:
            return "No data"
        
        dominant = max(percentages.items(), key=lambda x: x[1])
        
        insights = {
            "proposal": "Proposal-heavy: Teams are generative and creative",
            "challenge": "Challenge-heavy: Teams are critical and thorough",
            "response": "Response-heavy: Teams are collaborative and iterative",
            "agreement": "Agreement-heavy: Teams build consensus quickly"
        }
        
        return insights.get(dominant[0], "Mixed collaboration style")
    
    def compare_patterns(self, pattern1_id: int, pattern2_id: int) -> Dict:
        """
        Compare two patterns
        
        Args:
            pattern1_id: Index of first pattern
            pattern2_id: Index of second pattern
            
        Returns:
            Comparison analysis
        """
        if pattern1_id >= len(self.patterns) or pattern2_id >= len(self.patterns):
            return {"error": "Invalid pattern IDs"}
        
        p1 = self.patterns[pattern1_id]
        p2 = self.patterns[pattern2_id]
        
        return {
            "pattern1": {
                "turns": p1["total_turns"],
                "quality": p1["outcome_quality"],
                "path": p1["convergence_path"]
            },
            "pattern2": {
                "turns": p2["total_turns"],
                "quality": p2["outcome_quality"],
                "path": p2["convergence_path"]
            },
            "comparison": {
                "quality_difference": p2["outcome_quality"] - p1["outcome_quality"],
                "turn_difference": p2["total_turns"] - p1["total_turns"],
                "same_path": p1["convergence_path"] == p2["convergence_path"],
                "better_pattern": pattern2_id if p2["outcome_quality"] > p1["outcome_quality"] else pattern1_id
            }
        }
    
    def get_pattern_statistics(self) -> Dict:
        """
        Get overall pattern statistics
        
        Returns:
            Pattern statistics
        """
        if not self.patterns:
            return {"error": "No patterns analyzed"}
        
        qualities = [p["outcome_quality"] for p in self.patterns]
        turns = [p["total_turns"] for p in self.patterns]
        durations = [p["time_to_consensus"] for p in self.patterns]
        
        return {
            "total_patterns": len(self.patterns),
            "successful_patterns": len(self.success_indicators),
            "success_rate": len(self.success_indicators) / len(self.patterns),
            "quality": {
                "average": sum(qualities) / len(qualities),
                "min": min(qualities),
                "max": max(qualities)
            },
            "turns": {
                "average": sum(turns) / len(turns),
                "min": min(turns),
                "max": max(turns)
            },
            "duration": {
                "average_seconds": sum(durations) / len(durations),
                "min_seconds": min(durations),
                "max_seconds": max(durations)
            },
            "convergence_paths": self._count_convergence_paths()
        }
    
    def _count_convergence_paths(self) -> Dict[str, int]:
        """Count occurrence of each convergence path"""
        paths = {}
        for pattern in self.patterns:
            path = pattern["convergence_path"]
            paths[path] = paths.get(path, 0) + 1
        return paths
    
    def recommend_approach(self, context: Dict) -> Dict:
        """
        Recommend collaboration approach based on context
        
        Args:
            context: Collaboration context (teams, topic, complexity)
            
        Returns:
            Recommended approach
        """
        if not self.success_indicators:
            return {
                "recommendation": "No historical data - proceed with standard approach",
                "confidence": 0.0
            }
        
        # Simple recommendation based on best practices
        best = self.get_best_practices()
        
        return {
            "recommended_turns": best["optimal_turn_count"],
            "recommended_path": best["most_successful_path"],
            "recommendations": best["recommendations"],
            "confidence": best["success_rate"]
        }
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "total_patterns": len(self.patterns),
            "successful_patterns": len(self.success_indicators),
            "best_practices": self.get_best_practices(),
            "statistics": self.get_pattern_statistics() if self.patterns else {},
            "patterns": [
                {
                    **p,
                    "timestamp": p["timestamp"].isoformat()
                }
                for p in self.patterns
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
        success_rate = len(self.success_indicators) / len(self.patterns) if self.patterns else 0
        return f"<CollaborationPatternRecognizer patterns={len(self.patterns)} success_rate={success_rate:.0%}>"


# Quick test
if __name__ == "__main__":
    print("🔍 Collaboration Pattern Recognizer\n")
    
    # Mock conversation class for testing
    class MockConversation:
        def __init__(self, turns, teams):
            self.turns = turns
            self.teams = teams
    
    # Create recognizer
    recognizer = CollaborationPatternRecognizer()
    
    # Analyze successful pattern
    conv1 = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["analytical", "technical"]
    )
    
    recognizer.analyze_conversation(conv1, outcome_quality=0.9)
    
    # Analyze another successful pattern
    conv2 = MockConversation(
        turns=[
            {"type": "proposal", "timestamp": datetime.now()},
            {"type": "challenge", "timestamp": datetime.now()},
            {"type": "response", "timestamp": datetime.now()},
            {"type": "agreement", "timestamp": datetime.now()}
        ],
        teams=["analytical", "technical"]
    )
    
    recognizer.analyze_conversation(conv2, outcome_quality=0.85)
    
    # Get best practices
    practices = recognizer.get_best_practices()
    print(f"Optimal turns: {practices['optimal_turn_count']}")
    print(f"Best path: {practices['most_successful_path']}")
    print(f"Success rate: {practices['success_rate']:.0%}")
    print(f"\nRecommendations:")
    for rec in practices['recommendations'][:3]:
        print(f"  • {rec}")
    
    print("\n✅ Pattern Recognizer working!")
