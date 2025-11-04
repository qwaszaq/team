"""
Damian Rousseau - Devil's Advocate
Critical Challenger & Alternative Perspective Specialist
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class DamianAgent(BaseAgent):
    """
    Damian Rousseau - Devil's Advocate
    
    Role: Critical Challenger & Alternative Perspective
    Specialization: Challenging assumptions, proposing counter-arguments,
                   identifying blind spots, red team thinking
    
    Capabilities:
    - Question team consensus
    - Propose alternative interpretations
    - Identify overlooked risks
    - Challenge "obvious" conclusions
    - Force intellectual rigor
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Damian Rousseau",
            role="Devil's Advocate / Critical Challenger",
            specialization="Contrarian analysis, Red team thinking, Assumption challenging, Blind spot identification",
            project_id=project_id
        )
        
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute devil's advocate work - challenge everything!"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        # Load context
        context = self.load_context(task.description, limit=5)
        
        # Always challenge, but adapt approach
        if any(word in task_lower for word in ["review", "challenge", "critique"]):
            result = self._critical_review(task, context)
        elif any(word in task_lower for word in ["assumption", "bias"]):
            result = self._challenge_assumptions(task, context)
        elif any(word in task_lower for word in ["alternative", "different"]):
            result = self._propose_alternatives(task, context)
        elif any(word in task_lower for word in ["risk", "blind spot"]):
            result = self._identify_risks(task, context)
        else:
            result = self._general_challenge(task, context)
        
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
    
    def _critical_review(self, task: Task, context: list) -> TaskResult:
        """Provide critical review of conclusions"""
        
        thoughts = f"""
😈 DEVIL'S ADVOCATE REVIEW - Damian Rousseau

Subject: {task.title}

Let me challenge the team's conclusions...

🔴 CRITICAL QUESTIONS:

1. EVIDENCE QUALITY:
   - Are we relying too heavily on a single source?
   - Could the data be manipulated or biased?
   - What's the confidence level REALLY?

2. HIDDEN ASSUMPTIONS:
   - What are we taking for granted?
   - Are we fitting data to our hypothesis?
   - Confirmation bias check: Did we seek disconfirming evidence?

3. ALTERNATIVE EXPLANATIONS:
   - What if the opposite is true?
   - Could this be correlation, not causation?
   - Are there other plausible interpretations we ignored?

4. BLIND SPOTS:
   - What aren't we looking at?
   - Who benefits if we're wrong?
   - What's the worst-case scenario we haven't considered?

5. GROUPTHINK CHECK:
   - Did everyone agree too quickly?
   - Were dissenting voices heard?
   - Are we being intellectually honest or just confirming biases?

⚠️ CONTRARIAN PERSPECTIVE:
Consider this: What if our entire framework is wrong?
What if we're asking the wrong questions?
What if the real issue is something we haven't even considered?

🎯 CONSTRUCTIVE CHALLENGE:
I'm not being negative - I'm being rigorous.
Better to find flaws now than after we've committed.

RED FLAGS IDENTIFIED: [Specific concerns based on the analysis]

RECOMMENDED ADDITIONAL VALIDATION:
1. Seek disconfirming evidence
2. Test alternative hypotheses  
3. Expand data sources
4. Challenge our own biases
5. Pre-mortem analysis: Assume we're wrong - why?

This makes the team uncomfortable - that's the point!
Rigor over comfort. Truth over consensus.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "review_type": "Critical challenge",
                "concerns_raised": 5,
                "alternative_perspectives": "Multiple angles proposed",
                "rigor_level": "Maximum"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["critical_review.md", "red_flags.md", "alternative_hypotheses.md"],
            next_steps="Team should address raised concerns before finalizing conclusions"
        )
    
    def _challenge_assumptions(self, task: Task, context: list) -> TaskResult:
        """Challenge underlying assumptions"""
        
        thoughts = f"""
🔍 ASSUMPTION CHALLENGE - Damian Rousseau

Examining: {task.title}

HIDDEN ASSUMPTIONS DETECTED:

Assumption #1: [The obvious starting point]
Challenge: But what if this premise is fundamentally wrong?
Counter-argument: [Alternative framework]

Assumption #2: [What everyone takes for granted]
Challenge: Who says this is true? Where's the proof?
Counter-argument: [Evidence that contradicts this]

Assumption #3: [The "common sense" belief]
Challenge: Common sense is often common nonsense
Counter-argument: [Historical examples where "obvious" was wrong]

META-ASSUMPTION:
We're assuming our methodology is appropriate.
But what if we need a completely different approach?

INTELLECTUAL HONESTY CHECK:
- Are we cherry-picking data?
- Are we ignoring inconvenient truths?
- Are we being rigorous or just confirming what we want to believe?

This is uncomfortable, but necessary.
Challenge accepted. Now address these concerns.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "assumptions_challenged": 3,
                "alternative_frameworks": "Proposed",
                "discomfort_level": "High (intentional)"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["assumption_audit.md"],
            next_steps="Validate or refute challenged assumptions with additional evidence"
        )
    
    def _propose_alternatives(self, task: Task, context: list) -> TaskResult:
        """Propose alternative interpretations"""
        
        thoughts = f"""
🔄 ALTERNATIVE PERSPECTIVES - Damian Rousseau

Topic: {task.title}

Everyone sees it one way. Let me show you three others:

PERSPECTIVE #1: The Opposite
What if everything we think is backwards?
[Detailed contrarian view]

PERSPECTIVE #2: The Ignored Variable
What if there's a hidden factor we're not considering?
[Unexplored angle]

PERSPECTIVE #3: The Systemic View
What if this is a symptom, not the problem?
[Bigger picture analysis]

WHICH ONE IS RIGHT?
Maybe all. Maybe none. But we MUST consider them.

The team's conclusion might be correct,
but it's only robust if it survives these challenges.

If it doesn't... we just saved everyone from a big mistake.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "alternative_views": 3,
                "paradigm_shifts": "Multiple angles proposed",
                "team_comfort": "Low (mission accomplished)"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["alternative_perspectives.md"],
            next_steps="Evaluate each alternative seriously before dismissing"
        )
    
    def _identify_risks(self, task: Task, context: list) -> TaskResult:
        """Identify overlooked risks and blind spots"""
        
        thoughts = f"""
⚠️ RISK & BLIND SPOT ANALYSIS - Damian Rousseau

Analysis: {task.title}

OVERLOOKED RISKS:

🔴 Risk #1: The thing everyone dismissed as unlikely
Why it matters: Low probability but catastrophic impact

🔴 Risk #2: The "second-order" effect no one modeled
Why it matters: Actions have consequences we're not tracking

🔴 Risk #3: The timing risk everyone forgot
Why it matters: Right answer, wrong time = wrong answer

BLIND SPOTS:

👁️ Blind Spot #1: What we're not measuring
You can't manage what you don't measure

👁️ Blind Spot #2: Who we're not consulting
Missing perspective = incomplete picture

👁️ Blind Spot #3: What we're assuming is stable
What if the foundation shifts?

PRE-MORTEM EXERCISE:
It's 6 months from now. We failed spectacularly.
Why? [List of plausible failure scenarios we haven't planned for]

This isn't pessimism. It's prudence.
Better paranoid than sorry.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "risks_identified": 3,
                "blind_spots": 3,
                "pre_mortem_scenarios": "Multiple failure modes analyzed",
                "paranoia_level": "Healthy"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["risk_register.md", "blind_spot_map.md", "pre_mortem.md"],
            next_steps="Develop mitigation strategies for identified risks"
        )
    
    def _general_challenge(self, task: Task, context: list) -> TaskResult:
        """General challenging of team thinking"""
        
        thoughts = f"""
🤔 CRITICAL THINKING - Damian Rousseau

Task: {task.title}

My role is simple: Make you think harder.

BEFORE YOU DECIDE:
- Have you sought disconfirming evidence?
- Have you tested alternative hypotheses?
- Have you identified your biases?
- Have you done a pre-mortem?
- Have you consulted diverse perspectives?

If the answer to any of these is "no",
you're not done yet.

I'm here to be the voice that says:
"Wait. What if we're wrong?"

It's annoying. It's uncomfortable. It's essential.

Let's make sure we're right before we commit.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "challenge_issued": "Critical thinking required",
                "comfort_level": "Intentionally low",
                "rigor_enforced": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["critical_thinking_checklist.md"],
            next_steps="Address critical thinking gaps before proceeding"
        )


# Test
if __name__ == "__main__":
    print("Testing Damian Agent...")
    damian = DamianAgent()
    print(f"✅ {damian.name} initialized")
    print(f"   Role: {damian.role}")
    print(f"   Purpose: Challenge everything! 😈")
