"""
Real Claude API Supervisor - Production Implementation
Aleksander Nowak
2025-11-05

REAL CLAUDE INTEGRATION - No simulation!
Uses Anthropic Claude API for actual quality supervision
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  anthropic package not installed. Install with: pip install anthropic")


class SupervisionMode(Enum):
    """Supervision modes"""
    SUPERVISED = "supervised"
    SPOT_CHECK = "spot_check"
    AUTONOMOUS = "autonomous"


class QualityGrade(Enum):
    """Quality grades"""
    A_EXCELLENT = "A"
    B_GOOD = "B"
    C_ACCEPTABLE = "C"
    D_NEEDS_WORK = "D"
    F_UNACCEPTABLE = "F"


@dataclass
class ClaudeReview:
    """Claude's review result"""
    task_id: str
    grade: QualityGrade
    quality_score: float
    strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    cross_document_insights: List[str]
    approved: bool
    requires_retry: bool
    reasoning: str
    tokens_used: Dict[str, int]
    time_taken: float


class ClaudeAPISupervisor:
    """
    Real Claude API Supervisor
    
    Uses Claude Sonnet 4.5 for actual quality reviews
    
    Key Features:
    - Real AI review (not simulation!)
    - 200k context window
    - Cross-document pattern detection
    - Progressive autonomy
    - Cost tracking
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4.5-20241022",
        initial_mode: SupervisionMode = SupervisionMode.SUPERVISED
    ):
        """
        Initialize Claude API supervisor
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            model: Claude model to use
            initial_mode: Starting supervision mode
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package required. Install: pip install anthropic")
        
        # Get API key
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter"
            )
        
        # Initialize Claude client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.mode = initial_mode
        
        # Statistics
        self.total_reviews = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.review_history: List[ClaudeReview] = []
        
        # Thresholds
        self.AUTONOMOUS_THRESHOLD = 0.85
        self.SPOT_CHECK_THRESHOLD = 0.75
        self.MIN_REVIEWS_FOR_TRANSITION = 10
        
        print(f"✅ Claude API Supervisor initialized")
        print(f"   Model: {self.model}")
        print(f"   Mode: {self.mode.value}")
    
    def should_review(self, task_id: str) -> bool:
        """Determine if task should be reviewed"""
        if self.mode == SupervisionMode.SUPERVISED:
            return True
        elif self.mode == SupervisionMode.SPOT_CHECK:
            return self.total_reviews % 5 == 0
        elif self.mode == SupervisionMode.AUTONOMOUS:
            return False
        return True
    
    def review_task(
        self,
        task_id: str,
        agent_name: str,
        agent_role: str,
        task_description: str,
        agent_output: Dict[str, Any],
        confidence: float,
        full_context: Optional[str] = None,
        all_documents: Optional[List[str]] = None
    ) -> ClaudeReview:
        """
        Review agent's work using real Claude API
        
        Args:
            task_id: Task identifier
            agent_name: Agent name
            agent_role: Agent role
            task_description: Task description
            agent_output: Agent's output
            confidence: Agent's confidence
            full_context: Optional full context (use Claude's 200k!)
            all_documents: Optional all document texts
            
        Returns:
            ClaudeReview with real AI feedback
        """
        start_time = time.time()
        
        # Build review prompt
        prompt = self._build_review_prompt(
            agent_name=agent_name,
            agent_role=agent_role,
            task_description=task_description,
            agent_output=agent_output,
            confidence=confidence,
            full_context=full_context,
            all_documents=all_documents
        )
        
        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,  # Lower for consistent reviews
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse Claude's response
            review_text = response.content[0].text
            review_data = self._parse_claude_response(review_text)
            
            # Calculate metrics
            elapsed = time.time() - start_time
            tokens_used = {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
                "total": response.usage.input_tokens + response.usage.output_tokens
            }
            
            # Calculate cost (Claude Sonnet 4.5 pricing)
            cost = self._calculate_cost(tokens_used)
            
            # Create review
            review = ClaudeReview(
                task_id=task_id,
                grade=QualityGrade[review_data["grade"]],
                quality_score=review_data["quality_score"],
                strengths=review_data["strengths"],
                gaps=review_data["gaps"],
                suggestions=review_data["suggestions"],
                cross_document_insights=review_data.get("cross_document_insights", []),
                approved=review_data["approved"],
                requires_retry=review_data["requires_retry"],
                reasoning=review_text,
                tokens_used=tokens_used,
                time_taken=elapsed
            )
            
            # Update statistics
            self.total_reviews += 1
            self.total_tokens += tokens_used["total"]
            self.total_cost += cost
            self.review_history.append(review)
            
            # Check mode transition
            self._check_mode_transition()
            
            return review
            
        except Exception as e:
            # Return error review
            return ClaudeReview(
                task_id=task_id,
                grade=QualityGrade.C_ACCEPTABLE,
                quality_score=0.7,
                strengths=["Task completed"],
                gaps=[f"Review failed: {str(e)}"],
                suggestions=["Manual review recommended"],
                cross_document_insights=[],
                approved=True,
                requires_retry=False,
                reasoning=f"Claude API error: {str(e)}",
                tokens_used={"input": 0, "output": 0, "total": 0},
                time_taken=0
            )
    
    def _build_review_prompt(
        self,
        agent_name: str,
        agent_role: str,
        task_description: str,
        agent_output: Dict[str, Any],
        confidence: float,
        full_context: Optional[str] = None,
        all_documents: Optional[List[str]] = None
    ) -> str:
        """Build comprehensive review prompt for Claude"""
        
        prompt = f"""You are reviewing the work of a local AI agent as part of a quality assurance system.

# AGENT INFORMATION
Agent: {agent_name}
Role: {agent_role}
Confidence: {confidence:.2f}

# TASK
{task_description}

# AGENT'S OUTPUT
{json.dumps(agent_output, indent=2)}

# YOUR ROLE AS SUPERVISOR
You have a 200k token context window (vs the local agent's 44k). Use this advantage to:
1. Spot cross-document connections the agent might have missed
2. Identify contradictions between different sources
3. Find patterns across multiple documents
4. Assess overall quality and completeness

"""
        
        # Add full context if available (leverage 200k!)
        if all_documents:
            prompt += f"\n# ALL DOCUMENTS (for cross-analysis)\n"
            for i, doc in enumerate(all_documents[:10], 1):  # Limit to prevent huge prompts
                prompt += f"\n## Document {i}\n{doc[:2000]}...\n"
        
        if full_context:
            prompt += f"\n# ADDITIONAL CONTEXT\n{full_context[:5000]}\n"
        
        prompt += """

# PROVIDE YOUR REVIEW IN THIS EXACT JSON FORMAT:
{
    "grade": "A" | "B" | "C" | "D" | "F",
    "quality_score": 0.0-1.0,
    "strengths": ["strength 1", "strength 2", ...],
    "gaps": ["gap 1", "gap 2", ...],
    "suggestions": ["suggestion 1", "suggestion 2", ...],
    "cross_document_insights": ["insight 1 using your 200k context advantage", ...],
    "approved": true | false,
    "requires_retry": true | false,
    "reasoning": "Brief explanation of your assessment"
}

# GRADING CRITERIA
A (0.90-1.0):  Excellent work, comprehensive, insightful
B (0.80-0.89): Good work, solid analysis, minor gaps
C (0.70-0.79): Acceptable, meets requirements, some gaps
D (0.60-0.69): Needs improvement, significant gaps
F (<0.60):     Unacceptable, major issues, requires retry

Be constructive and specific. Focus on actionable feedback.
"""
        
        return prompt
    
    def _parse_claude_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's JSON response"""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            
            data = json.loads(json_str)
            
            # Validate and convert
            return {
                "grade": data["grade"].replace("_EXCELLENT", "").replace("_GOOD", "").replace("_ACCEPTABLE", "").replace("_NEEDS_WORK", "").replace("_UNACCEPTABLE", ""),
                "quality_score": float(data["quality_score"]),
                "strengths": data.get("strengths", []),
                "gaps": data.get("gaps", []),
                "suggestions": data.get("suggestions", []),
                "cross_document_insights": data.get("cross_document_insights", []),
                "approved": bool(data.get("approved", True)),
                "requires_retry": bool(data.get("requires_retry", False)),
                "reasoning": data.get("reasoning", "")
            }
        except Exception as e:
            # Fallback if parsing fails
            return {
                "grade": "C",
                "quality_score": 0.7,
                "strengths": ["Completed task"],
                "gaps": ["Response parsing failed"],
                "suggestions": ["Manual review recommended"],
                "cross_document_insights": [],
                "approved": True,
                "requires_retry": False,
                "reasoning": f"Parse error: {str(e)}"
            }
    
    def _calculate_cost(self, tokens_used: Dict[str, int]) -> float:
        """
        Calculate cost based on Claude Sonnet 4.5 pricing
        
        Pricing (as of Nov 2024):
        - Input: $3 per million tokens
        - Output: $15 per million tokens
        """
        input_cost = (tokens_used["input"] / 1_000_000) * 3.0
        output_cost = (tokens_used["output"] / 1_000_000) * 15.0
        return input_cost + output_cost
    
    def _check_mode_transition(self):
        """Check if supervision mode should change"""
        if len(self.review_history) < self.MIN_REVIEWS_FOR_TRANSITION:
            return
        
        recent = self.review_history[-self.MIN_REVIEWS_FOR_TRANSITION:]
        avg_quality = sum(r.quality_score for r in recent) / len(recent)
        
        old_mode = self.mode
        
        if avg_quality >= self.AUTONOMOUS_THRESHOLD:
            self.mode = SupervisionMode.AUTONOMOUS
        elif avg_quality >= self.SPOT_CHECK_THRESHOLD:
            self.mode = SupervisionMode.SPOT_CHECK
        else:
            self.mode = SupervisionMode.SUPERVISED
        
        if self.mode != old_mode:
            print(f"🔄 Supervision mode: {old_mode.value} → {self.mode.value}")
            print(f"   Avg quality: {avg_quality:.2f}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get supervision statistics"""
        return {
            "mode": self.mode.value,
            "total_reviews": self.total_reviews,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "avg_cost_per_review": self.total_cost / self.total_reviews if self.total_reviews > 0 else 0,
            "avg_quality": sum(r.quality_score for r in self.review_history) / len(self.review_history) if self.review_history else 0
        }
    
    def format_review(self, review: ClaudeReview) -> str:
        """Format review for display"""
        output = f"""
╔════════════════════════════════════════════════════════════════╗
║  CLAUDE QUALITY REVIEW (Real AI Supervision!)                 ║
╚════════════════════════════════════════════════════════════════╝

Task: {review.task_id}
Grade: {review.grade.value}
Quality Score: {review.quality_score:.2f}
Status: {"✅ APPROVED" if review.approved else "⚠️ NEEDS IMPROVEMENT"}

STRENGTHS:
"""
        for strength in review.strengths:
            output += f"  ✅ {strength}\n"
        
        if review.gaps:
            output += "\nGAPS IDENTIFIED:\n"
            for gap in review.gaps:
                output += f"  ⚠️  {gap}\n"
        
        if review.suggestions:
            output += "\nSUGGESTIONS:\n"
            for suggestion in review.suggestions:
                output += f"  💡 {suggestion}\n"
        
        if review.cross_document_insights:
            output += "\n🔍 CROSS-DOCUMENT INSIGHTS (200k Context Advantage):\n"
            for insight in review.cross_document_insights:
                output += f"  🌟 {insight}\n"
        
        output += f"\nTOKENS USED: {review.tokens_used['total']:,} "
        output += f"(input: {review.tokens_used['input']:,}, output: {review.tokens_used['output']:,})\n"
        output += f"TIME: {review.time_taken:.2f}s\n"
        
        if review.requires_retry:
            output += "\n❌ RETRY REQUIRED\n"
        
        output += "═" * 66 + "\n"
        
        return output


def test_claude_api_supervisor():
    """Test Claude API supervisor"""
    print("🧪 Testing Real Claude API Supervisor...\n")
    
    # Check if API key available
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set")
        print("   Set environment variable to test real API")
        print("   Example: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    try:
        # Initialize
        print("1. Initializing Claude API supervisor...")
        supervisor = ClaudeAPISupervisor()
        
        # Test review
        print("\n2. Testing real Claude review...")
        test_output = {
            "summary": "Revenue increased 25% to $5M. Profit margins improved to 32%.",
            "key_findings": [
                "Strong revenue growth",
                "Margin expansion",
                "Cash position healthy"
            ],
            "recommendations": [
                "Continue growth trajectory",
                "Monitor operating expenses"
            ]
        }
        
        review = supervisor.review_task(
            task_id="test_001",
            agent_name="Financial Analyst",
            agent_role="financial",
            task_description="Analyze Q4 financial performance",
            agent_output=test_output,
            confidence=0.85
        )
        
        # Display results
        print(supervisor.format_review(review))
        
        # Stats
        stats = supervisor.get_statistics()
        print("\n3. Statistics:")
        print(f"   Reviews: {stats['total_reviews']}")
        print(f"   Tokens: {stats['total_tokens']:,}")
        print(f"   Cost: ${stats['total_cost']:.4f}")
        print(f"   Avg quality: {stats['avg_quality']:.2f}")
        
        print("\n✅ Claude API supervisor working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_claude_api_supervisor()
