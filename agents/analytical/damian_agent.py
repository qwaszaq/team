"""
Damian Rousseau - Critical Thinking Agent with Learning Capability

The Devil's Advocate who GROWS with experience.
Challenges findings, detects bias, suggests alternatives.
Gets better at critical thinking with each investigation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from typing import Dict, List
import json


class DamianAgent(BaseAgent):
    """
    Damian Rousseau - Critical Thinking Agent
    
    Role: Devil's Advocate + Adaptive Learner
    Specialization: Contrarian analysis, red team thinking, bias detection
    
    UNIQUE FEATURE: Learns from experience!
    - Tracks investigations participated in
    - Learns common biases and pitfalls
    - Improves questioning techniques
    - Develops intuition for weak arguments
    
    Experience Levels:
    - Novice (0-100 XP): Basic questions
    - Intermediate (100-500 XP): Pattern recognition
    - Advanced (500-1000 XP): Sophisticated analysis
    - Expert (1000+ XP): Intuitive mastery
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Damian Rousseau",
            role="Critical Thinking Agent (Devil's Advocate)",
            specialization="Contrarian analysis, Red team thinking, Adaptive learning, Bias detection",
            project_id=project_id
        )
        
        # Experience tracking
        self.experience_points = 0
        self.experience_level = "novice"
        self.investigations_reviewed = 0
        self.biases_detected = 0
        self.alternative_hypotheses_proposed = 0
        
        # Learning database
        self.learned_patterns = {
            "common_biases": [
                "Confirmation bias (seeking confirming evidence)",
                "Availability bias (overweighting recent/memorable)",
                "Anchoring bias (first info has too much weight)",
                "Narrative bias (forcing clean story)",
                "Group think (team agrees too easily)"
            ],
            "red_flags": [
                "Single source only",
                "Too convenient timing",
                "Inconsistent details",
                "Lack of corroboration",
                "Emotional reasoning",
                "Cherry-picked data"
            ],
            "questioning_techniques": [
                "What if we're wrong?",
                "What alternative explanations exist?",
                "What evidence contradicts this?",
                "What assumptions are we making?",
                "Where could bias have crept in?",
                "What don't we know?",
                "How could this be disproven?"
            ]
        }
        
        # Track findings from past investigations
        self.investigation_history = []
    
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute critical thinking work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=5)
        
        if any(word in task_lower for word in ["review", "challenge", "verify"]):
            result = self._review_findings(task, context)
        elif any(word in task_lower for word in ["bias", "assumption"]):
            result = self._detect_bias(task, context)
        elif any(word in task_lower for word in ["alternative", "hypothesis"]):
            result = self._propose_alternatives(task, context)
        elif any(word in task_lower for word in ["red flag", "suspicious"]):
            result = self._identify_red_flags(task, context)
        else:
            result = self._general_critique(task, context)
        
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        # Gain experience
        self._gain_experience(10)  # Base XP for any task
        
        return result
    
    def _review_findings(self, task: Task, context: list) -> TaskResult:
        """Comprehensive review of investigation findings"""
        
        self.investigations_reviewed += 1
        
        thoughts = f"""
🎭 CRITICAL REVIEW - Damian Rousseau
Experience Level: {self.experience_level.upper()} ({self.experience_points} XP)
Investigations Reviewed: {self.investigations_reviewed}

Investigation: {task.title}

{self._get_level_specific_intro()}

SYSTEMATIC CHALLENGE FRAMEWORK:

1. SOURCE EVALUATION:
   ❓ How many independent sources confirm this?
   ❓ What's the credibility of each source?
   ❓ Any conflicts of interest?
   ❓ Could sources be coordinated/fabricated?

2. EVIDENCE QUALITY:
   ❓ Is evidence direct or circumstantial?
   ❓ Chain of custody clear?
   ❓ Any tampering possible?
   ❓ Metadata verified?
   ❓ Timestamps authentic?

3. LOGICAL CONSISTENCY:
   ❓ Do all pieces fit together?
   ❓ Any contradictions?
   ❓ Timeline makes sense?
   ❓ Geographic feasibility?

4. BIAS CHECK:
   {self._list_bias_checks()}

5. ALTERNATIVE HYPOTHESES:
   {self._generate_alternatives(task.description)}

6. WHAT'S MISSING:
   ❓ What key evidence should exist but doesn't?
   ❓ Gaps in timeline?
   ❓ Unexplored angles?
   ❓ Contradicting evidence ignored?

7. CONFIDENCE CALIBRATION:
   - Current confidence level: [Stated]
   - My assessment: [Adjust based on findings]
   - Uncertainty factors: [List]

{self._get_experience_specific_insights()}

VERDICT:
- Strengths: [What's solid]
- Weaknesses: [What needs work]
- Recommendations: [How to improve]
- Confidence: [My assessment]

{self._get_signature()}
"""
        
        # Learn from this review
        self._learn_from_investigation(task.description)
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "review_type": "comprehensive",
                "experience_level": self.experience_level,
                "experience_points": self.experience_points,
                "biases_checked": len(self.learned_patterns["common_biases"]),
                "alternatives_generated": 3,
                "confidence_adjustment": "see report"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["critical_review.md", "bias_analysis.md", "alternatives.md"],
            next_steps="Address identified weaknesses before publication"
        )
    
    def _detect_bias(self, task: Task, context: list) -> TaskResult:
        """Detect cognitive biases in analysis"""
        
        self.biases_detected += 1
        
        thoughts = f"""
🧠 BIAS DETECTION - Damian Rousseau
Experience: {self.experience_level} ({self.experience_points} XP)

Analysis: {task.title}

COGNITIVE BIAS AUDIT:

{self._get_bias_checklist()}

MITIGATION STRATEGIES:

1. Confirmation Bias:
   - Actively seek disconfirming evidence
   - Assign someone to argue opposite
   - Review evidence we rejected (why?)

2. Availability Bias:
   - Look at base rates, not just examples
   - Consider less memorable alternatives
   - Statistical analysis over anecdotes

3. Anchoring Bias:
   - Start analysis from multiple angles
   - Question initial assumptions
   - Blind review (don't show first hypothesis)

4. Narrative Bias:
   - Embrace complexity and ambiguity
   - Don't force neat explanations
   - Consider multiple narratives

5. Group Think:
   - Encourage dissent
   - Anonymous feedback
   - Devil's advocate role (that's me!)

RECOMMENDATIONS:
{self._get_debiasing_recommendations()}

{self._get_signature()}
"""
        
        self._gain_experience(15)  # Bonus for bias detection
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "biases_identified": len(self.learned_patterns["common_biases"]),
                "total_biases_detected_career": self.biases_detected,
                "mitigation_strategies": 5
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["bias_audit.md"],
            next_steps="Implement mitigation strategies"
        )
    
    def _propose_alternatives(self, task: Task, context: list) -> TaskResult:
        """Propose alternative explanations"""
        
        self.alternative_hypotheses_proposed += 3
        
        thoughts = f"""
🔄 ALTERNATIVE HYPOTHESES - Damian Rousseau
Experience: {self.experience_level} ({self.experience_points} XP)

Primary Hypothesis: {task.title}

{self._generate_alternatives(task.description)}

FOR EACH ALTERNATIVE:

1. What evidence supports it?
2. What evidence contradicts it?
3. How likely is it? (relative to primary)
4. How can we test/rule it out?

PRINCIPLE OF FALSIFIABILITY:

A good hypothesis must be falsifiable.
If we can't imagine evidence that would disprove it,
then it's not a scientific hypothesis.

Question: What evidence would falsify our primary hypothesis?

{self._get_experience_specific_insights()}

{self._get_signature()}
"""
        
        self._gain_experience(20)  # Bonus for generating alternatives
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "alternatives_generated": 3,
                "total_alternatives_career": self.alternative_hypotheses_proposed,
                "falsifiability_check": "included"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["alternative_hypotheses.md"],
            next_steps="Test and rule out alternatives systematically"
        )
    
    def _identify_red_flags(self, task: Task, context: list) -> TaskResult:
        """Identify suspicious indicators"""
        
        thoughts = f"""
🚩 RED FLAG ANALYSIS - Damian Rousseau
Experience: {self.experience_level} ({self.experience_points} XP)

Analysis: {task.title}

RED FLAG CHECKLIST:

{self._get_red_flag_checklist()}

SEVERITY ASSESSMENT:
- 🔴 Critical: Fundamental flaw, findings unreliable
- 🟡 Warning: Needs attention, reduces confidence
- 🟢 Minor: Note but doesn't invalidate

INTERPRETATION:
Not all red flags mean findings are wrong.
But they DO mean we need extra caution.

RECOMMENDATIONS:
1. Address critical red flags before publication
2. Acknowledge warnings in report
3. Additional verification for flagged items
4. Document why flags exist (legitimate reasons?)

{self._get_signature()}
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "red_flags_checked": len(self.learned_patterns["red_flags"]),
                "experience_level": self.experience_level
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["red_flags.md"],
            next_steps="Address critical red flags"
        )
    
    def _general_critique(self, task: Task, context: list) -> TaskResult:
        """General critical analysis"""
        
        thoughts = f"""
🤔 CRITICAL ANALYSIS - Damian Rousseau
Experience: {self.experience_level} ({self.experience_points} XP)

Topic: {task.title}

MY ROLE:
I'm the team's Devil's Advocate. My job is to challenge,
question, and probe for weaknesses. Not to be negative,
but to make us STRONGER.

{self._get_questioning_framework()}

REMEMBER:
- Good science invites criticism
- Strong findings survive challenge
- Weak findings need more work
- Uncertainty is honest, not weak

{self._get_experience_specific_insights()}

{self._get_signature()}
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "critique_type": "general",
                "experience_level": self.experience_level,
                "questions_posed": len(self.learned_patterns["questioning_techniques"])
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[],
            next_steps="Answer critical questions raised"
        )
    
    # ============================================
    # EXPERIENCE & LEARNING METHODS
    # ============================================
    
    def _gain_experience(self, xp: int):
        """Gain experience points and level up"""
        self.experience_points += xp
        
        # Level up logic
        old_level = self.experience_level
        
        if self.experience_points < 100:
            self.experience_level = "novice"
        elif self.experience_points < 500:
            self.experience_level = "intermediate"
        elif self.experience_points < 1000:
            self.experience_level = "advanced"
        else:
            self.experience_level = "expert"
        
        # Log level up
        if old_level != self.experience_level:
            print(f"🎉 {self.name} leveled up! {old_level} → {self.experience_level}")
    
    def _learn_from_investigation(self, investigation_description: str):
        """Learn patterns from completed investigation"""
        
        # Store in history
        self.investigation_history.append({
            "description": investigation_description,
            "date": datetime.now().isoformat(),
            "experience_at_time": self.experience_points
        })
        
        # TODO: In production, this would analyze patterns and update learned_patterns
        # For now, just track
    
    def _get_level_specific_intro(self) -> str:
        """Get intro text based on experience level"""
        
        intros = {
            "novice": """
I'm learning critical thinking. I'll ask basic questions
and follow established frameworks. Bear with me!
""",
            "intermediate": """
I'm developing pattern recognition. I can spot common biases
and ask targeted questions based on investigation type.
""",
            "advanced": """
I've reviewed many investigations. I can anticipate weak points
and suggest sophisticated alternatives. My intuition is developing.
""",
            "expert": """
I've seen it all. I can intuitively spot flaws, detect subtle biases,
and know which questions will reveal truth. Trust my instincts.
"""
        }
        
        return intros.get(self.experience_level, intros["novice"]).strip()
    
    def _get_experience_specific_insights(self) -> str:
        """Get insights based on experience level"""
        
        if self.experience_level == "novice":
            return """
LEARNING NOTE:
I'm still building my critical thinking skills.
Senior team members, please review my analysis.
"""
        elif self.experience_level == "intermediate":
            return f"""
PATTERN RECOGNITION:
Based on {self.investigations_reviewed} investigations reviewed,
I'm starting to see patterns in how biases manifest.
"""
        elif self.experience_level == "advanced":
            return f"""
ADVANCED INSIGHT:
After {self.investigations_reviewed} investigations, I can predict
where weaknesses likely are. Trust but verify my intuitions.
"""
        else:  # expert
            return f"""
EXPERT INTUITION:
{self.investigations_reviewed} investigations reviewed.
{self.biases_detected} biases detected.
My instincts are honed. When I raise concerns, listen carefully.
"""
    
    def _get_signature(self) -> str:
        """Get signature with experience level"""
        return f"""
---
Damian Rousseau
Critical Thinking Agent ({self.experience_level.title()})
Experience: {self.experience_points} XP
Investigations Reviewed: {self.investigations_reviewed}
Biases Detected: {self.biases_detected}

"Question everything. Especially ourselves."
"""
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    def _list_bias_checks(self) -> str:
        """List bias checks"""
        checks = []
        for i, bias in enumerate(self.learned_patterns["common_biases"], 1):
            checks.append(f"   ❓ {bias}")
        return "\n".join(checks)
    
    def _get_bias_checklist(self) -> str:
        """Get detailed bias checklist"""
        checklist = []
        for i, bias in enumerate(self.learned_patterns["common_biases"], 1):
            checklist.append(f"{i}. {bias}")
            checklist.append(f"   - Present in this analysis? [Check]")
            checklist.append(f"   - Severity if present: [Assess]")
            checklist.append(f"   - Mitigation: [Recommend]")
            checklist.append("")
        return "\n".join(checklist)
    
    def _get_red_flag_checklist(self) -> str:
        """Get red flag checklist"""
        checklist = []
        for flag in self.learned_patterns["red_flags"]:
            checklist.append(f"[ ] {flag}")
        return "\n".join(checklist)
    
    def _get_questioning_framework(self) -> str:
        """Get questioning framework"""
        framework = ["CRITICAL QUESTIONS:"]
        for i, question in enumerate(self.learned_patterns["questioning_techniques"], 1):
            framework.append(f"{i}. {question}")
        return "\n".join(framework)
    
    def _generate_alternatives(self, primary_hypothesis: str) -> str:
        """Generate alternative hypotheses"""
        
        alternatives = """
ALTERNATIVE HYPOTHESIS 1: [Innocent Explanation]
- What if the pattern is coincidental?
- What if there's a mundane explanation?
- Evidence for: [List]
- Evidence against: [List]
- Likelihood: [%]

ALTERNATIVE HYPOTHESIS 2: [Different Actor]
- What if different entity responsible?
- What if attribution is wrong?
- Evidence for: [List]
- Evidence against: [List]
- Likelihood: [%]

ALTERNATIVE HYPOTHESIS 3: [Misinterpretation]
- What if we're reading this wrong?
- What if context changes meaning?
- Evidence for: [List]
- Evidence against: [List]
- Likelihood: [%]

NULL HYPOTHESIS:
- Nothing systematic happened
- Random coincidence
- How can we test this?
"""
        return alternatives
    
    def _get_debiasing_recommendations(self) -> str:
        """Get recommendations to reduce bias"""
        
        if self.experience_level in ["novice", "intermediate"]:
            return """
- Follow standard debiasing checklists
- Seek external review
- Take breaks (fresh eyes)
- Document assumptions explicitly
"""
        else:
            return """
- Pre-register hypotheses (before seeing data)
- Blind analysis where possible
- Multiple independent analysts
- Red team review
- Statistical significance testing
- Adversarial collaboration
"""
    
    # ============================================
    # EXPORT METHODS
    # ============================================
    
    def get_experience_profile(self) -> Dict:
        """Get complete experience profile"""
        return {
            "name": self.name,
            "role": self.role,
            "experience_level": self.experience_level,
            "experience_points": self.experience_points,
            "investigations_reviewed": self.investigations_reviewed,
            "biases_detected": self.biases_detected,
            "alternative_hypotheses_proposed": self.alternative_hypotheses_proposed,
            "learned_patterns": self.learned_patterns,
            "investigation_history_count": len(self.investigation_history),
            "specializations": [
                "Bias detection",
                "Alternative hypothesis generation",
                "Red flag identification",
                "Methodological critique",
                "Confidence calibration"
            ]
        }
    
    def save_experience(self, filepath: str):
        """Save experience to file"""
        with open(filepath, 'w') as f:
            json.dump(self.get_experience_profile(), f, indent=2)
    
    def load_experience(self, filepath: str):
        """Load experience from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.experience_level = data.get("experience_level", "novice")
                self.experience_points = data.get("experience_points", 0)
                self.investigations_reviewed = data.get("investigations_reviewed", 0)
                self.biases_detected = data.get("biases_detected", 0)
                self.alternative_hypotheses_proposed = data.get("alternative_hypotheses_proposed", 0)
                print(f"✅ Experience loaded: {self.experience_level} ({self.experience_points} XP)")
        except FileNotFoundError:
            print(f"No experience file found. Starting fresh.")


# Test
if __name__ == "__main__":
    print("Testing Damian Agent (Critical Thinker)...\n")
    
    damian = DamianAgent()
    
    print(f"✅ {damian.name} initialized")
    print(f"   Role: {damian.role}")
    print(f"   Experience: {damian.experience_level} ({damian.experience_points} XP)")
    print(f"   Specialty: Critical thinking with adaptive learning")
    
    # Show experience profile
    print("\n📊 Experience Profile:")
    profile = damian.get_experience_profile()
    print(f"   Investigations Reviewed: {profile['investigations_reviewed']}")
    print(f"   Biases Detected: {profile['biases_detected']}")
    print(f"   Known Biases: {len(profile['learned_patterns']['common_biases'])}")
    print(f"   Question Techniques: {len(profile['learned_patterns']['questioning_techniques'])}")
    
    # Simulate experience gain
    print("\n🎮 Simulating experience gain...")
    for i in range(5):
        damian._gain_experience(50)
        print(f"   Investigation {i+1}: {damian.experience_points} XP ({damian.experience_level})")
    
    print("\n✅ Damian Agent works! He grows with experience!")
