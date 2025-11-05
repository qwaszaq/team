"""
Claude Supervision Module - Progressive Autonomy Pattern
Aleksander Nowak
2025-11-05
"""

import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class SupervisionMode(Enum):
    """Supervision modes"""
    SUPERVISED = "supervised"      # Claude reviews every task
    SPOT_CHECK = "spot_check"      # Claude reviews sample tasks
    AUTONOMOUS = "autonomous"      # No review (agents trusted)


class QualityGrade(Enum):
    """Quality grades"""
    A_EXCELLENT = "A"
    B_GOOD = "B"
    C_ACCEPTABLE = "C"
    D_NEEDS_WORK = "D"
    F_UNACCEPTABLE = "F"


@dataclass
class QualityReview:
    """Quality review result"""
    task_id: str
    reviewer: str
    grade: QualityGrade
    quality_score: float  # 0.0 - 1.0
    strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    approved: bool
    requires_retry: bool
    context_analysis: Optional[Dict[str, Any]] = None


class ClaudeSupervisor:
    """
    Claude supervision system for local agent quality assurance
    
    Progressive Autonomy Pattern:
    1. SUPERVISED: All tasks reviewed post-execution
    2. SPOT_CHECK: Sample tasks reviewed (agents proving themselves)
    3. AUTONOMOUS: No review (agents fully trusted)
    
    Key Principle: Review happens AFTER task completion
    - Local agent completes work
    - Claude reviews quality
    - Feedback provided for improvement
    - Agent can retry if needed
    
    44k vs 200k Context:
    - Local agents: 44k tokens (good for focused analysis)
    - Claude: 200k tokens (excellent for cross-document connections)
    - Claude's advantage: Finding contradictions, patterns across documents
    """
    
    def __init__(self, initial_mode: SupervisionMode = SupervisionMode.SUPERVISED):
        """
        Initialize Claude supervisor
        
        Args:
            initial_mode: Starting supervision mode
        """
        self.mode = initial_mode
        self.review_history: List[QualityReview] = []
        
        # Quality thresholds for mode transitions
        self.AUTONOMOUS_THRESHOLD = 0.85  # 85% avg quality for autonomous
        self.SPOT_CHECK_THRESHOLD = 0.75  # 75% for spot checks
        self.MIN_REVIEWS_FOR_TRANSITION = 10  # Need 10 reviews before upgrading
        
        # Statistics
        self.total_reviews = 0
        self.approved_count = 0
        self.retry_count = 0
        
        print(f"✅ Claude Supervisor initialized: {self.mode.value} mode")
    
    def should_review(self, task_id: str) -> bool:
        """
        Determine if task should be reviewed
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if should review
        """
        if self.mode == SupervisionMode.SUPERVISED:
            return True  # Review everything
        
        elif self.mode == SupervisionMode.SPOT_CHECK:
            # Review every 5th task
            return self.total_reviews % 5 == 0
        
        elif self.mode == SupervisionMode.AUTONOMOUS:
            return False  # No review
        
        return True
    
    def review_task(
        self,
        task_id: str,
        agent_name: str,
        agent_role: str,
        task_description: str,
        agent_output: Dict[str, Any],
        confidence: float,
        full_context: Optional[str] = None
    ) -> QualityReview:
        """
        Review agent's completed work
        
        NOTE: This is a SIMULATION - in production, this would call Claude API
        
        Args:
            task_id: Task identifier
            agent_name: Agent name
            agent_role: Agent role
            task_description: Task description
            agent_output: Agent's output
            confidence: Agent's confidence score
            full_context: Optional full context (for Claude's 200k window)
            
        Returns:
            QualityReview with feedback
        """
        # SIMULATION: In production, this would be Claude API call
        # For now, we use rule-based simulation
        
        review = self._simulate_claude_review(
            task_id=task_id,
            agent_name=agent_name,
            agent_role=agent_role,
            task_description=task_description,
            agent_output=agent_output,
            confidence=confidence,
            full_context=full_context
        )
        
        # Update statistics
        self.total_reviews += 1
        self.review_history.append(review)
        
        if review.approved:
            self.approved_count += 1
        
        if review.requires_retry:
            self.retry_count += 1
        
        # Check for mode transition
        self._check_mode_transition()
        
        return review
    
    def _simulate_claude_review(
        self,
        task_id: str,
        agent_name: str,
        agent_role: str,
        task_description: str,
        agent_output: Dict[str, Any],
        confidence: float,
        full_context: Optional[str] = None
    ) -> QualityReview:
        """
        Simulate Claude's review (placeholder for actual Claude API)
        
        In production, this would:
        1. Send task + output + context to Claude
        2. Ask Claude to assess quality
        3. Return Claude's feedback
        
        For now: Rule-based simulation
        """
        # Simulate quality assessment based on confidence
        quality_score = confidence
        
        # Determine grade
        if quality_score >= 0.90:
            grade = QualityGrade.A_EXCELLENT
        elif quality_score >= 0.80:
            grade = QualityGrade.B_GOOD
        elif quality_score >= 0.70:
            grade = QualityGrade.C_ACCEPTABLE
        elif quality_score >= 0.60:
            grade = QualityGrade.D_NEEDS_WORK
        else:
            grade = QualityGrade.F_UNACCEPTABLE
        
        # Simulate strengths/gaps
        strengths = self._identify_strengths(agent_output, confidence)
        gaps = self._identify_gaps(agent_output, confidence)
        suggestions = self._generate_suggestions(agent_role, gaps)
        
        # Context analysis (Claude's 200k advantage)
        context_analysis = None
        if full_context:
            context_analysis = self._analyze_context_usage(full_context)
        
        # Approval decision
        approved = quality_score >= 0.70
        requires_retry = quality_score < 0.60
        
        return QualityReview(
            task_id=task_id,
            reviewer="claude",
            grade=grade,
            quality_score=quality_score,
            strengths=strengths,
            gaps=gaps,
            suggestions=suggestions,
            approved=approved,
            requires_retry=requires_retry,
            context_analysis=context_analysis
        )
    
    def _identify_strengths(
        self,
        agent_output: Dict[str, Any],
        confidence: float
    ) -> List[str]:
        """Identify strengths in agent's work"""
        strengths = []
        
        if confidence >= 0.80:
            strengths.append("High confidence in analysis")
        
        if agent_output.get('key_findings'):
            strengths.append(f"Identified {len(agent_output['key_findings'])} key findings")
        
        if agent_output.get('recommendations'):
            strengths.append("Provided actionable recommendations")
        
        if agent_output.get('summary'):
            strengths.append("Clear executive summary")
        
        return strengths or ["Completed analysis"]
    
    def _identify_gaps(
        self,
        agent_output: Dict[str, Any],
        confidence: float
    ) -> List[str]:
        """Identify gaps in agent's work"""
        gaps = []
        
        if confidence < 0.70:
            gaps.append("Low confidence - may need more context")
        
        if not agent_output.get('key_findings'):
            gaps.append("Missing key findings section")
        
        if not agent_output.get('recommendations'):
            gaps.append("No recommendations provided")
        
        return gaps
    
    def _generate_suggestions(
        self,
        agent_role: str,
        gaps: List[str]
    ) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if "Low confidence" in str(gaps):
            suggestions.append("Request additional context or documents")
        
        if "Missing key findings" in str(gaps):
            suggestions.append("Structure analysis with clear findings section")
        
        if "No recommendations" in str(gaps):
            suggestions.append("Include actionable next steps")
        
        # Role-specific suggestions
        if agent_role == "financial":
            suggestions.append("Include quantitative metrics and ratios")
        elif agent_role == "legal":
            suggestions.append("Reference specific regulations or statutes")
        elif agent_role == "risk":
            suggestions.append("Quantify risk levels (high/medium/low)")
        
        return suggestions or ["Continue current approach"]
    
    def _analyze_context_usage(self, full_context: str) -> Dict[str, Any]:
        """
        Analyze context usage (Claude's 200k advantage)
        
        This is where Claude can spot things local agents might miss:
        - Cross-document contradictions
        - Patterns across many documents
        - Missing connections between entities
        """
        # Simulation of Claude's broader context analysis
        return {
            "context_length": len(full_context),
            "cross_document_insights": [
                "Potential contradiction detected between documents",
                "Related entity mentioned in 3 different documents"
            ],
            "broader_patterns": [
                "Similar pattern seen in historical cases"
            ],
            "recommended_focus": "Review section 4.2 for potential inconsistencies"
        }
    
    def _check_mode_transition(self):
        """Check if supervision mode should change"""
        if len(self.review_history) < self.MIN_REVIEWS_FOR_TRANSITION:
            return  # Not enough data
        
        # Calculate recent average quality
        recent_reviews = self.review_history[-self.MIN_REVIEWS_FOR_TRANSITION:]
        avg_quality = sum(r.quality_score for r in recent_reviews) / len(recent_reviews)
        
        # Transition logic
        current_mode = self.mode
        
        if avg_quality >= self.AUTONOMOUS_THRESHOLD:
            self.mode = SupervisionMode.AUTONOMOUS
        elif avg_quality >= self.SPOT_CHECK_THRESHOLD:
            self.mode = SupervisionMode.SPOT_CHECK
        else:
            self.mode = SupervisionMode.SUPERVISED
        
        if self.mode != current_mode:
            print(f"🔄 Supervision mode changed: {current_mode.value} → {self.mode.value}")
            print(f"   Avg quality: {avg_quality:.2f}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get supervision statistics"""
        avg_quality = (
            sum(r.quality_score for r in self.review_history) / len(self.review_history)
            if self.review_history else 0
        )
        
        return {
            "mode": self.mode.value,
            "total_reviews": self.total_reviews,
            "approved_count": self.approved_count,
            "retry_count": self.retry_count,
            "average_quality": avg_quality,
            "approval_rate": self.approved_count / self.total_reviews if self.total_reviews > 0 else 0
        }
    
    def format_review_feedback(self, review: QualityReview) -> str:
        """Format review feedback for agent"""
        feedback = f"""
╔════════════════════════════════════════════════════════════════╗
║  CLAUDE QUALITY REVIEW                                         ║
╚════════════════════════════════════════════════════════════════╝

Task: {review.task_id}
Grade: {review.grade.value}
Quality Score: {review.quality_score:.2f}
Status: {"✅ APPROVED" if review.approved else "⚠️ NEEDS IMPROVEMENT"}

STRENGTHS:
"""
        for strength in review.strengths:
            feedback += f"  ✅ {strength}\n"
        
        if review.gaps:
            feedback += "\nGAPS IDENTIFIED:\n"
            for gap in review.gaps:
                feedback += f"  ⚠️  {gap}\n"
        
        if review.suggestions:
            feedback += "\nSUGGESTIONS FOR IMPROVEMENT:\n"
            for suggestion in review.suggestions:
                feedback += f"  💡 {suggestion}\n"
        
        if review.context_analysis:
            feedback += f"\nCONTEXT ANALYSIS (Claude's 200k advantage):\n"
            for insight in review.context_analysis.get('cross_document_insights', []):
                feedback += f"  🔍 {insight}\n"
        
        if review.requires_retry:
            feedback += "\n❌ RETRY REQUIRED: Quality below acceptable threshold\n"
        
        feedback += "═" * 66 + "\n"
        
        return feedback


def test_claude_supervisor():
    """Test Claude supervision system"""
    print("🧪 Testing Claude Supervision System...\n")
    
    # Initialize supervisor
    print("1. Initializing supervisor...")
    supervisor = ClaudeSupervisor(initial_mode=SupervisionMode.SUPERVISED)
    
    # Simulate agent tasks
    print("\n2. Simulating agent tasks...")
    
    test_tasks = [
        {
            "task_id": "task_001",
            "agent_name": "Financial Analyst",
            "agent_role": "financial",
            "description": "Analyze Q4 financials",
            "output": {
                "summary": "Revenue up 20%",
                "key_findings": ["Strong growth", "Margin improvement"],
                "recommendations": ["Maintain trajectory"]
            },
            "confidence": 0.85
        },
        {
            "task_id": "task_002",
            "agent_name": "Legal Analyst",
            "agent_role": "legal",
            "description": "Review contracts",
            "output": {
                "summary": "Contracts reviewed"
            },
            "confidence": 0.55
        },
        {
            "task_id": "task_003",
            "agent_name": "Risk Analyst",
            "agent_role": "risk",
            "description": "Risk assessment",
            "output": {
                "summary": "Low risk profile",
                "key_findings": ["No major risks", "Controls adequate"],
                "recommendations": ["Continue monitoring"]
            },
            "confidence": 0.90
        }
    ]
    
    for task in test_tasks:
        should_review = supervisor.should_review(task['task_id'])
        print(f"\n   Task: {task['task_id']}")
        print(f"   Should review: {should_review}")
        
        if should_review:
            review = supervisor.review_task(
                task_id=task['task_id'],
                agent_name=task['agent_name'],
                agent_role=task['agent_role'],
                task_description=task['description'],
                agent_output=task['output'],
                confidence=task['confidence']
            )
            
            print(f"   Grade: {review.grade.value}")
            print(f"   Quality: {review.quality_score:.2f}")
            print(f"   Approved: {review.approved}")
    
    # Show statistics
    print("\n3. Supervision statistics...")
    stats = supervisor.get_statistics()
    print(f"   Mode: {stats['mode']}")
    print(f"   Total reviews: {stats['total_reviews']}")
    print(f"   Approved: {stats['approved_count']}")
    print(f"   Avg quality: {stats['average_quality']:.2f}")
    print(f"   Approval rate: {stats['approval_rate']:.1%}")
    
    # Show detailed feedback
    print("\n4. Sample review feedback...")
    if supervisor.review_history:
        feedback = supervisor.format_review_feedback(supervisor.review_history[0])
        print(feedback)
    
    print("\n✅ Claude supervision tests complete!")


if __name__ == "__main__":
    test_claude_supervisor()
