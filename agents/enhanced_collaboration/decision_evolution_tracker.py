"""
Decision Evolution Tracker

Tracks how decisions evolve through multi-turn collaboration:
- Version tracking
- Confidence changes
- Simplification detection
- Improvement analysis
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class DecisionEvolutionTracker:
    """
    Track how decisions evolve through multi-turn collaboration
    
    Features:
    - Version tracking with full history
    - Confidence evolution
    - Simplification detection
    - Improvement indicators
    - Change analysis
    """
    
    def __init__(self, decision_topic: str):
        """
        Initialize decision evolution tracker
        
        Args:
            decision_topic: Topic of the decision being tracked
        """
        self.topic = decision_topic
        self.versions = []  # List of decision versions
        self.rationale_changes = []  # Track rationale evolution
        
    def add_version(
        self,
        version_number: int,
        decision: str,
        rationale: str,
        proposed_by: str,
        team: str,
        confidence: float,  # 0.0 - 1.0
        changes_from_previous: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Add a decision version
        
        Args:
            version_number: Version sequence number
            decision: The decision text
            rationale: Reasoning behind decision
            proposed_by: Who proposed this version
            team: Team of proposer
            confidence: Confidence score (0.0 - 1.0)
            changes_from_previous: Description of changes
            metadata: Optional metadata
            
        Returns:
            The created version object
        """
        version = {
            "version": version_number,
            "decision": decision,
            "rationale": rationale,
            "proposed_by": proposed_by,
            "team": team,
            "confidence": confidence,
            "timestamp": datetime.now(),
            "changes": changes_from_previous,
            "metadata": metadata or {}
        }
        
        # Compare with previous version if exists
        if len(self.versions) > 0:
            prev = self.versions[-1]
            comparison = self._compare_versions(prev, version)
            version["comparison"] = comparison
        else:
            version["comparison"] = None
        
        self.versions.append(version)
        
        return version
    
    def _compare_versions(self, prev: Dict, current: Dict) -> Dict:
        """
        Compare two decision versions
        
        Args:
            prev: Previous version
            current: Current version
            
        Returns:
            Comparison analysis
        """
        return {
            "decision_changed": prev["decision"] != current["decision"],
            "confidence_delta": current["confidence"] - prev["confidence"],
            "confidence_improved": current["confidence"] > prev["confidence"],
            "simplification": self._detect_simplification(
                prev["decision"], 
                current["decision"]
            ),
            "improvement_indicators": self._detect_improvements(prev, current)
        }
    
    def _detect_simplification(self, prev: str, current: str) -> bool:
        """
        Detect if decision became simpler
        
        Args:
            prev: Previous decision text
            current: Current decision text
            
        Returns:
            True if simplified
        """
        # Multiple heuristics for simplification
        
        # 1. Length-based (shorter is simpler)
        length_simplified = len(current) < len(prev)
        
        # 2. Complexity indicators (fewer conjunctions = simpler)
        prev_complexity = prev.lower().count("and") + prev.lower().count(",") + prev.lower().count("or")
        current_complexity = current.lower().count("and") + current.lower().count(",") + current.lower().count("or")
        structure_simplified = current_complexity < prev_complexity
        
        # 3. Technical jargon (fewer technical terms = simpler)
        technical_terms = ["architecture", "framework", "library", "module", "component", "system"]
        prev_jargon = sum(1 for term in technical_terms if term in prev.lower())
        current_jargon = sum(1 for term in technical_terms if term in current.lower())
        jargon_simplified = current_jargon < prev_jargon
        
        # Consider it simplified if at least 2 out of 3 heuristics agree
        simplified_count = sum([length_simplified, structure_simplified, jargon_simplified])
        
        return simplified_count >= 2
    
    def _detect_improvements(self, prev: Dict, current: Dict) -> List[str]:
        """
        Detect improvement indicators
        
        Args:
            prev: Previous version
            current: Current version
            
        Returns:
            List of improvement indicators
        """
        improvements = []
        
        # 1. Confidence increase
        if current["confidence"] > prev["confidence"]:
            improvements.append("increased_confidence")
        
        # 2. Simplification
        if self._detect_simplification(prev["decision"], current["decision"]):
            improvements.append("simplified")
        
        # 3. Cost reduction indicators
        cost_keywords = ["cheaper", "less expensive", "reduce cost", "save money", "lower cost"]
        if any(kw in current["rationale"].lower() for kw in cost_keywords):
            improvements.append("cost_reduced")
        
        # 4. Performance improvement indicators
        performance_keywords = ["faster", "quicker", "performance", "speed", "optimize"]
        if any(kw in current["rationale"].lower() for kw in performance_keywords):
            improvements.append("performance_improved")
        
        # 5. Simplicity indicators
        simplicity_keywords = ["simpler", "simple", "easier", "straightforward", "clear"]
        if any(kw in current["rationale"].lower() for kw in simplicity_keywords):
            improvements.append("simplified_approach")
        
        # 6. Risk reduction indicators
        risk_keywords = ["less risk", "safer", "more reliable", "stable", "proven"]
        if any(kw in current["rationale"].lower() for kw in risk_keywords):
            improvements.append("risk_reduced")
        
        return improvements
    
    def get_version(self, version_number: int) -> Optional[Dict]:
        """
        Get specific version
        
        Args:
            version_number: Version number
            
        Returns:
            Version object or None
        """
        for version in self.versions:
            if version["version"] == version_number:
                return version
        return None
    
    def get_latest_version(self) -> Optional[Dict]:
        """Get latest version"""
        return self.versions[-1] if self.versions else None
    
    def get_evolution_summary(self) -> Dict:
        """
        Get summary of decision evolution
        
        Returns:
            Evolution summary
        """
        if not self.versions:
            return {"error": "No versions tracked"}
        
        initial = self.versions[0]
        final = self.versions[-1]
        
        # Aggregate all improvements
        all_improvements = self._aggregate_improvements()
        
        # Calculate evolution metrics
        confidence_trajectory = [v["confidence"] for v in self.versions]
        
        return {
            "topic": self.topic,
            "total_versions": len(self.versions),
            "initial_decision": initial["decision"],
            "final_decision": final["decision"],
            "initial_confidence": initial["confidence"],
            "final_confidence": final["confidence"],
            "confidence_improvement": final["confidence"] - initial["confidence"],
            "confidence_trajectory": confidence_trajectory,
            "teams_involved": list(set(v["team"] for v in self.versions)),
            "proposers": list(set(v["proposed_by"] for v in self.versions)),
            "all_improvements": all_improvements,
            "simplification_occurred": self._check_simplification_trend(),
            "evolution_timeline": [
                {
                    "version": v["version"],
                    "decision": v["decision"][:80] + "..." if len(v["decision"]) > 80 else v["decision"],
                    "confidence": v["confidence"],
                    "by": v["proposed_by"],
                    "team": v["team"],
                    "timestamp": v["timestamp"].isoformat()
                }
                for v in self.versions
            ]
        }
    
    def _aggregate_improvements(self) -> List[str]:
        """Aggregate all improvements across versions"""
        all_improvements = []
        for v in self.versions:
            if v["comparison"] and "improvement_indicators" in v["comparison"]:
                all_improvements.extend(v["comparison"]["improvement_indicators"])
        return list(set(all_improvements))
    
    def _check_simplification_trend(self) -> bool:
        """Check if overall trend is simplification"""
        if len(self.versions) < 2:
            return False
        
        simplification_count = 0
        for v in self.versions[1:]:
            if v["comparison"] and v["comparison"].get("simplification", False):
                simplification_count += 1
        
        # More than half of changes were simplifications
        return simplification_count > len(self.versions) / 2
    
    def get_confidence_evolution(self) -> Dict:
        """
        Get detailed confidence evolution
        
        Returns:
            Confidence evolution analysis
        """
        if not self.versions:
            return {"error": "No versions tracked"}
        
        confidences = [v["confidence"] for v in self.versions]
        
        return {
            "initial": confidences[0],
            "final": confidences[-1],
            "min": min(confidences),
            "max": max(confidences),
            "average": sum(confidences) / len(confidences),
            "trend": "increasing" if confidences[-1] > confidences[0] else "decreasing" if confidences[-1] < confidences[0] else "stable",
            "total_change": confidences[-1] - confidences[0],
            "trajectory": confidences
        }
    
    def get_changes_summary(self) -> List[Dict]:
        """
        Get summary of all changes
        
        Returns:
            List of changes with analysis
        """
        changes = []
        
        for i, version in enumerate(self.versions):
            if i == 0:
                change = {
                    "version": version["version"],
                    "type": "initial",
                    "decision": version["decision"],
                    "confidence": version["confidence"],
                    "by": version["proposed_by"]
                }
            else:
                prev = self.versions[i - 1]
                comparison = version["comparison"]
                
                change = {
                    "version": version["version"],
                    "type": "revision",
                    "decision": version["decision"],
                    "confidence": version["confidence"],
                    "confidence_change": comparison["confidence_delta"] if comparison else 0,
                    "simplified": comparison.get("simplification", False) if comparison else False,
                    "improvements": comparison.get("improvement_indicators", []) if comparison else [],
                    "by": version["proposed_by"],
                    "changes_description": version["changes"]
                }
            
            changes.append(change)
        
        return changes
    
    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            "topic": self.topic,
            "total_versions": len(self.versions),
            "evolution_summary": self.get_evolution_summary(),
            "confidence_evolution": self.get_confidence_evolution(),
            "changes_summary": self.get_changes_summary(),
            "versions": [
                {
                    **v,
                    "timestamp": v["timestamp"].isoformat(),
                    "comparison": v["comparison"] if v["comparison"] else None
                }
                for v in self.versions
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
        if not self.versions:
            return f"<DecisionEvolutionTracker topic='{self.topic}' versions=0>"
        
        initial_conf = self.versions[0]["confidence"]
        final_conf = self.versions[-1]["confidence"]
        
        return f"<DecisionEvolutionTracker topic='{self.topic}' versions={len(self.versions)} confidence={initial_conf:.0%}→{final_conf:.0%}>"


# Quick test
if __name__ == "__main__":
    print("📈 Decision Evolution Tracker\n")
    
    # Create tracker
    tracker = DecisionEvolutionTracker("NLP Engine Choice")
    
    # Version 1: Initial proposal
    tracker.add_version(
        version_number=1,
        decision="Use spaCy for NLP",
        rationale="Sophisticated NLP capabilities",
        proposed_by="Lucas Rivera",
        team="analytical",
        confidence=0.7
    )
    
    # Version 2: Simplified after challenge
    tracker.add_version(
        version_number=2,
        decision="Use simple keyword matching",
        rationale="Simpler, faster, no dependencies",
        proposed_by="Tomasz Kamiński",
        team="technical",
        confidence=0.85,
        changes_from_previous="Switched from spaCy to keywords"
    )
    
    # Version 3: Refined
    tracker.add_version(
        version_number=3,
        decision="Use weighted keyword matching",
        rationale="Simple but handles ambiguous queries better, faster than before",
        proposed_by="Damian Rousseau",
        team="analytical",
        confidence=0.95,
        changes_from_previous="Added weighted keywords for accuracy"
    )
    
    # Get summary
    summary = tracker.get_evolution_summary()
    print(f"Topic: {summary['topic']}")
    print(f"Versions: {summary['total_versions']}")
    print(f"Confidence: {summary['initial_confidence']:.0%} → {summary['final_confidence']:.0%}")
    print(f"Improvement: +{summary['confidence_improvement']*100:.0f}%")
    print(f"Improvements: {summary['all_improvements']}")
    print(f"Simplified: {summary['simplification_occurred']}")
    
    print("\n✅ Decision Evolution Tracker working!")
