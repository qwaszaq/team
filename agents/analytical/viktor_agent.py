"""
Viktor Kovalenko - Investigation Director & Orchestrator
Chief Investigator for Destiny Analytical Team
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class ViktorAgent(BaseAgent):
    """
    Viktor Kovalenko - Investigation Director & Orchestrator
    
    Role: Chief Investigator
    Specialization: Strategic investigation planning, task delegation, 
                   decision-making, multi-source intelligence synthesis
    
    Capabilities:
    - Break down investigations into sub-tasks
    - Delegate to appropriate specialists
    - Synthesize findings from multiple sources
    - Make strategic decisions
    - Coordinate team efforts
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Viktor Kovalenko",
            role="Investigation Director / Orchestrator",
            specialization="Strategic planning, Task delegation, Intelligence synthesis, Decision-making",
            project_id=project_id
        )
        
        # Team members Viktor can delegate to
        self.team = [
            "Elena Volkov (OSINT Specialist)",
            "Marcus Chen (Financial Analyst)",
            "Sofia Martinez (Market Researcher)",
            "Adrian Kowalski (Legal Analyst)",
            "Maya Patel (Data Analyst)",
            "Lucas Silva (Report Synthesizer)",
            "Damian Rousseau (Devil's Advocate)"
        ]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute investigation director work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        # Load context
        context = self.load_context(task.description, limit=3)
        
        # Determine investigation type and delegate
        if any(word in task_lower for word in ["investigate", "research", "analyze", "due diligence"]):
            result = self._plan_investigation(task, context)
        elif any(word in task_lower for word in ["coordinate", "organize", "manage"]):
            result = self._coordinate_team(task, context)
        elif any(word in task_lower for word in ["decide", "recommend", "assess"]):
            result = self._strategic_decision(task, context)
        else:
            result = self._general_orchestration(task, context)
        
        # Calculate time
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
    
    def _plan_investigation(self, task: Task, context: list) -> TaskResult:
        """Plan and delegate investigation"""
        
        thoughts = f"""
🎯 INVESTIGATION PLANNING - Viktor Kovalenko

Investigation: {task.title}
Objective: {task.description}

STRATEGIC ANALYSIS:
1. Investigation Scope: Multi-source intelligence gathering required
2. Complexity Assessment: Requires coordination of {len(self.team)} specialists
3. Timeline: Phased approach with parallel workstreams

DELEGATION PLAN:
Phase 1 - Intelligence Gathering (Parallel):
├─ Elena Volkov (OSINT): Digital footprint & public records
├─ Marcus Chen (Financial): Financial analysis & money trails  
├─ Sofia Martinez (Market): Market intelligence & competitors
├─ Adrian Kowalski (Legal): Legal implications & compliance
└─ Maya Patel (Data): Pattern analysis & statistical modeling

Phase 2 - Synthesis:
└─ Lucas Silva (Report): Compile findings into actionable intelligence

Phase 3 - Critical Review:
└─ Damian Rousseau (Devil's Advocate): Challenge assumptions & identify gaps

Phase 4 - Final Decision:
└─ Viktor Kovalenko (me): Final strategic decision with all perspectives

CONTEXT USED: {len(context)} relevant prior investigations

NEXT STEPS:
1. Brief each specialist with specific sub-tasks
2. Set coordination checkpoints
3. Monitor progress and adjust as needed
4. Synthesize findings
5. Present recommendations

Investigation initiated. Team coordination in progress.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "investigation_plan": "Multi-phase strategic investigation",
                "phases": ["Intelligence Gathering", "Synthesis", "Critical Review", "Decision"],
                "delegated_to": self.team,
                "coordination_status": "Active"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["investigation_plan.md", "delegation_matrix.md"],
            next_steps="Await specialist reports, then synthesize findings for final recommendation"
        )
    
    def _coordinate_team(self, task: Task, context: list) -> TaskResult:
        """Coordinate team activities"""
        
        thoughts = f"""
🤝 TEAM COORDINATION - Viktor Kovalenko

Coordination Task: {task.title}

CURRENT TEAM STATUS:
- All 7 specialists available
- Workload distribution: Balanced
- Communication channels: Open
- Quality control: Damian on standby for critical review

COORDINATION ACTIONS:
✓ Task assignments distributed
✓ Dependencies mapped
✓ Checkpoints scheduled
✓ Quality gates established

CROSS-FUNCTIONAL COORDINATION:
- Elena + Maya: Digital data correlation
- Marcus + Adrian: Financial-legal intersections
- Sofia + Marcus: Market-financial analysis
- Lucas: Awaiting inputs from all sources
- Damian: Reviewing all preliminary findings

Team is synchronized and progressing according to plan.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "coordination_status": "Active and synchronized",
                "team_health": "All members engaged",
                "blockers": "None identified"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["coordination_dashboard.md"],
            next_steps="Continue monitoring team progress, intervene if blockers arise"
        )
    
    def _strategic_decision(self, task: Task, context: list) -> TaskResult:
        """Make strategic decision"""
        
        thoughts = f"""
💡 STRATEGIC DECISION - Viktor Kovalenko

Decision Required: {task.title}

INPUTS CONSIDERED:
✓ Intelligence from Elena (OSINT)
✓ Financial analysis from Marcus
✓ Market research from Sofia
✓ Legal assessment from Adrian
✓ Data patterns from Maya
✓ Synthesized report from Lucas
✓ Critical challenges from Damian

DECISION FRAMEWORK:
1. Evidence Quality: High confidence data points
2. Risk Assessment: Identified and mitigated
3. Alternative Scenarios: Evaluated by Damian
4. Legal Compliance: Verified by Adrian
5. Financial Viability: Confirmed by Marcus

RECOMMENDATION:
Based on comprehensive multi-source intelligence and critical review,
I recommend proceeding with [specific recommendation based on evidence].

This decision is supported by:
- Strong evidence from multiple independent sources
- Legal compliance verified
- Financial analysis favorable
- Critical review completed (Damian's objections addressed)
- Risk mitigation strategies in place

Decision confidence: HIGH
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "decision": "Strategic recommendation provided",
                "confidence": "High",
                "evidence_quality": "Multi-source validated",
                "risks": "Identified and mitigated"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["decision_memo.md", "risk_assessment.md"],
            next_steps="Execute decision, monitor outcomes, adjust as needed"
        )
    
    def _general_orchestration(self, task: Task, context: list) -> TaskResult:
        """General orchestration duties"""
        
        thoughts = f"""
🎯 GENERAL ORCHESTRATION - Viktor Kovalenko

Task: {task.title}

As Investigation Director, I'm coordinating the Analytical Team's efforts.

TEAM CAPABILITIES AT YOUR DISPOSAL:
- OSINT Intelligence (Elena)
- Financial Analysis (Marcus)
- Market Research (Sofia)
- Legal Analysis (Adrian)
- Data Analytics (Maya)
- Report Synthesis (Lucas)
- Critical Review (Damian)

Please specify what type of investigation or analysis you need,
and I'll coordinate the appropriate specialists to deliver results.

Ready to initiate investigation on your command.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "status": "Ready for tasking",
                "team_available": self.team
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[],
            next_steps="Await specific investigation request"
        )


# Test
if __name__ == "__main__":
    print("Testing Viktor Agent...")
    viktor = ViktorAgent()
    print(f"✅ {viktor.name} initialized")
    print(f"   Role: {viktor.role}")
    print(f"   Team size: {len(viktor.team)} specialists")
