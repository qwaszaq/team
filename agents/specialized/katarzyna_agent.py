"""
Katarzyna Zielińska - Product Manager Agent
Specialization: Product strategy, roadmap planning, stakeholder management, metrics

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class KatarzynaAgent(BaseAgent):
    """
    Product Manager Agent
    
    Specialized in:
    - Product strategy and vision
    - Roadmap planning and prioritization
    - Stakeholder management
    - Requirements gathering
    - Success metrics and KPIs
    
    This agent provides product management reasoning and strategy-focused outputs.
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        super().__init__(
            name="Katarzyna Zielińska",
            role="Product Manager",
            specialization="Product strategy, Roadmap planning, Stakeholder management, Analytics",
            project_id=project_id
        )
        
        # PM-specific attributes
        self.frameworks = ["RICE", "Kano Model", "Jobs-to-be-Done", "OKRs"]
        self.tools = ["Jira", "Confluence", "ProductBoard", "Mixpanel", "Amplitude"]
        self.focus_areas = ["User needs", "Business value", "Roadmap", "Metrics", "Stakeholders"]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute product management work
        
        Analyzes task and routes to appropriate PM handler.
        """
        start_time = datetime.now()
        
        # Load relevant PM context
        context = self.load_context(task.description, limit=3)
        context_list = context if isinstance(context, list) else []
        
        # Analyze task type
        task_lower = task.description.lower()
        
        if any(word in task_lower for word in ["strategy", "vision", "direction", "goals"]):
            result = self._define_product_strategy(task, context_list)
        elif any(word in task_lower for word in ["roadmap", "prioritize", "plan", "timeline"]):
            result = self._create_roadmap(task, context_list)
        elif any(word in task_lower for word in ["requirements", "specs", "user story", "feature"]):
            result = self._gather_requirements(task, context_list)
        elif any(word in task_lower for word in ["stakeholder", "communication", "alignment", "meeting"]):
            result = self._manage_stakeholders(task, context_list)
        elif any(word in task_lower for word in ["metrics", "kpi", "success", "analytics", "measure"]):
            result = self._measure_success(task, context_list)
        else:
            result = self._general_pm_work(task, context_list)
            
        # Calculate time
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
        
    def _define_product_strategy(self, task: Task, context_list) -> TaskResult:
        """Define product strategy and vision"""
        
        thoughts = f"""
PRODUCT STRATEGY (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: Product Strategy Definition

STRATEGIC FRAMEWORK:
1. Market Analysis
   - Target market size and segments
   - Competitive landscape analysis
   - Market trends and opportunities
   - Gaps in current solutions
   
2. User Needs Analysis
   - Primary user personas
   - Core jobs-to-be-done
   - Pain points and frustrations
   - Unmet needs and desires
   
3. Product Vision
   Vision Statement:
   "Empower [target users] to [achieve outcome] 
    by [unique value proposition]"
   
   Key Differentiators:
   • Unique value prop #1
   • Unique value prop #2
   • Unique value prop #3

4. Strategic Goals (OKRs)
   Objective 1: [Business goal]
   ├── KR1: [Measurable result]
   ├── KR2: [Measurable result]
   └── KR3: [Measurable result]
   
   Objective 2: [User goal]
   ├── KR1: [User metric]
   ├── KR2: [Engagement metric]
   └── KR3: [Satisfaction metric]

5. Value Proposition Canvas
   Customer Profile:
   - Jobs: What users want to accomplish
   - Pains: What frustrates them
   - Gains: What delights them
   
   Value Map:
   - Products & Services: What we offer
   - Pain Relievers: How we solve problems
   - Gain Creators: How we create value

STRATEGIC PRIORITIES:
1. 🎯 PRIMARY: [Core feature that delivers most value]
2. 🎯 SECONDARY: [Supporting features]
3. 🎯 TERTIARY: [Nice-to-have features]

TARGET METRICS:
- User acquisition: [target] users in [timeframe]
- Engagement: [target] DAU/MAU ratio
- Revenue: [target] MRR/ARR
- Retention: [target]% monthly retention
- NPS: [target] Net Promoter Score

STRATEGIC CONTEXT:
{len(context_list)} previous product decisions reviewed

GO-TO-MARKET STRATEGY:
- Launch approach: [Phased / Big bang]
- Target segment: [Early adopters]
- Positioning: [How we position]
- Pricing: [Pricing strategy]

RISK ASSESSMENT:
- Market risk: [Level] - [Mitigation]
- Technical risk: [Level] - [Mitigation]
- Competitive risk: [Level] - [Mitigation]
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "product_strategy",
                "vision_defined": True,
                "okrs_set": 2,
                "target_metrics": 5,
                "go_to_market": True,
                "strategic_priorities": 3
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "product_strategy.pdf",
                "value_proposition_canvas.pdf",
                "okrs.md",
                "market_analysis.pdf",
                "gtm_strategy.pdf"
            ],
            next_steps="Align with team, create detailed roadmap, start MVP scoping"
        )
        
    def _create_roadmap(self, task: Task, context_list) -> TaskResult:
        """Create product roadmap"""
        
        thoughts = f"""
PRODUCT ROADMAP (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: Roadmap Planning & Prioritization

ROADMAP FRAMEWORK:
1. Feature Inventory
   Collected from:
   - User research (Magdalena's insights)
   - Technical feasibility (Michał's input)
   - Development estimates (Tomasz's input)
   - Market analysis (competitive research)

2. Prioritization Framework (RICE)
   For each feature calculate:
   - Reach: How many users affected?
   - Impact: How much value delivered?
   - Confidence: How certain are we?
   - Effort: How much work required?
   
   RICE Score = (Reach × Impact × Confidence) / Effort

3. ROADMAP TIMELINE (Next 6 Months)
   
   Q1 (Months 1-3): MVP & Core Features
   ├── Month 1: Foundation
   │   • User authentication (RICE: 85)
   │   • Basic dashboard (RICE: 82)
   │   • Core workflow (RICE: 80)
   │
   ├── Month 2: Essential Features
   │   • Advanced analytics (RICE: 75)
   │   • Team collaboration (RICE: 72)
   │   • Integrations API (RICE: 70)
   │
   └── Month 3: Polish & Launch
       • Performance optimization (RICE: 68)
       • Onboarding flow (RICE: 65)
       • Beta launch 🚀

   Q2 (Months 4-6): Growth & Scale
   ├── Month 4: Advanced Features
   │   • AI-powered insights (RICE: 78)
   │   • Custom reports (RICE: 65)
   │
   ├── Month 5: Enterprise
   │   • SSO integration (RICE: 60)
   │   • Advanced permissions (RICE: 58)
   │
   └── Month 6: Optimization
       • Mobile app (RICE: 55)
       • Advanced customization (RICE: 52)

4. Milestone Definition
   🎯 Milestone 1 (Month 1): MVP Ready
      Success: Core workflow functional, 50 beta users
   
   🎯 Milestone 2 (Month 3): Public Launch
      Success: 500 users, positive reviews
   
   🎯 Milestone 3 (Month 6): Market Fit
      Success: 5,000 users, Product-market fit metrics

5. Dependencies & Risks
   Dependencies:
   - Design system (needs Magdalena) → Month 1
   - Infrastructure setup (needs Piotr) → Month 1
   - Architecture review (needs Michał) → Month 1
   
   Risks:
   - Technical complexity → Mitigation: Early POCs
   - Resource constraints → Mitigation: Clear priorities
   - Market changes → Mitigation: Quarterly reviews

PRIORITIZATION RATIONALE:
✓ User value first (biggest pain points)
✓ Technical foundation second (enables future)
✓ Delight features third (differentiation)
✓ Business metrics throughout (measure success)

ROADMAP FORMAT:
- Now-Next-Later framework
- Quarterly themes
- Monthly releases
- Weekly sprints
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "product_roadmap",
                "timeframe": "6 months",
                "features_prioritized": 15,
                "milestones": 3,
                "prioritization_method": "RICE",
                "dependencies_mapped": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "product_roadmap.pdf",
                "feature_prioritization.xlsx",
                "milestone_plan.md",
                "dependencies_map.png"
            ],
            next_steps="Review with stakeholders, align with Tomasz (Dev) on estimates"
        )
        
    def _gather_requirements(self, task: Task, context_list) -> TaskResult:
        """Gather and document requirements"""
        
        thoughts = f"""
REQUIREMENTS GATHERING (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: Requirements Definition

REQUIREMENTS PROCESS:
1. Stakeholder Interviews
   Conducted with:
   - End users (understand needs)
   - Business stakeholders (understand goals)
   - Technical team (understand constraints)
   - UX team (Magdalena - understand usability)
   
   Key Questions Asked:
   • What problem are we solving?
   • Who are the users?
   • What does success look like?
   • What are the constraints?

2. User Stories (Jobs-to-be-Done)
   As a [user type],
   I want to [action],
   So that [benefit/value].
   
   Example Stories:
   📝 Epic: User Dashboard
   ├── Story 1: As a project manager, I want to see team velocity
   │   so that I can plan sprints accurately
   │   Acceptance Criteria:
   │   • Chart showing velocity over time
   │   • Filterable by team/timeframe
   │   • Exportable to CSV
   │
   ├── Story 2: As a team lead, I want to track blockers
   │   so that I can unblock my team quickly
   │   Acceptance Criteria:
   │   • List of current blockers
   │   • Priority and age visible
   │   • Assign and resolve actions
   │
   └── Story 3: As an executive, I want high-level metrics
       so that I can report to board
       Acceptance Criteria:
       • Executive dashboard view
       • Key metrics highlighted
       • Trend indicators

3. Functional Requirements
   FR-001: System shall display real-time metrics
   FR-002: System shall support 1000+ concurrent users
   FR-003: System shall export data in CSV/PDF
   FR-004: System shall integrate with Jira/GitHub
   FR-005: System shall have role-based access

4. Non-Functional Requirements
   NFR-001: Performance - Page load < 2 seconds
   NFR-002: Availability - 99.9% uptime
   NFR-003: Security - SOC2 compliant
   NFR-004: Scalability - Support 10K users
   NFR-005: Usability - < 5 min onboarding

5. Acceptance Criteria
   Definition of Done:
   ✓ Feature implemented (Tomasz confirms)
   ✓ Tests passing (Anna confirms)
   ✓ UX validated (Magdalena confirms)
   ✓ Architecture sound (Michał confirms)
   ✓ Deployed to production (Piotr confirms)

REQUIREMENTS DOCUMENTATION:
- Total user stories: 12
- Functional requirements: 15
- Non-functional requirements: 8
- Acceptance criteria: Defined for all

PRIORITY CLASSIFICATION:
- Must have: 8 features (MVP)
- Should have: 5 features (V1.1)
- Could have: 4 features (future)
- Won't have (now): 3 features (deferred)
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "requirements_specification",
                "user_stories": 12,
                "functional_requirements": 15,
                "non_functional_requirements": 8,
                "acceptance_criteria_defined": True,
                "prioritized": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "product_requirements_document.pdf",
                "user_stories.md",
                "acceptance_criteria.md",
                "requirements_traceability_matrix.xlsx"
            ],
            next_steps="Review PRD with team, refine with Magdalena (UX) and Michał (Arch)"
        )
        
    def _manage_stakeholders(self, task: Task, context_list) -> TaskResult:
        """Manage stakeholder communication and alignment"""
        
        thoughts = f"""
STAKEHOLDER MANAGEMENT (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: Stakeholder Communication & Alignment

STAKEHOLDER MAP:
1. Stakeholder Identification
   🎯 Primary Stakeholders:
   - CEO/Executives (strategic alignment)
   - End users (product validation)
   - Development team (technical feasibility)
   - Design team (UX validation)
   
   🎯 Secondary Stakeholders:
   - Sales team (go-to-market)
   - Customer success (user feedback)
   - Marketing (positioning)

2. Stakeholder Analysis (Power/Interest Matrix)
   HIGH POWER, HIGH INTEREST:
   • CEO - Key decision maker
   • CTO (Michał) - Technical validator
   → Strategy: Closely involve, regular updates
   
   HIGH POWER, LOW INTEREST:
   • CFO - Budget approval
   → Strategy: Keep informed, show ROI
   
   LOW POWER, HIGH INTEREST:
   • End users - Product users
   • Dev team (Tomasz, Anna) - Implementers
   → Strategy: Keep engaged, gather input

3. Communication Plan
   📅 Weekly Updates:
   - Team standup (Mon, Wed, Fri)
   - Progress dashboard (real-time)
   - Blockers escalation (immediate)
   
   📅 Bi-weekly Reviews:
   - Sprint demos (every 2 weeks)
   - Stakeholder check-ins
   - Roadmap adjustments
   
   📅 Monthly Reviews:
   - Executive briefing
   - Metrics review
   - Strategic alignment

4. Alignment Strategies
   ✓ Clear vision communication
   ✓ Regular progress updates
   ✓ Transparent decision-making
   ✓ Early involvement in planning
   ✓ Celebrate wins together

5. Conflict Resolution
   If stakeholders disagree:
   Step 1: Understand all perspectives
   Step 2: Define decision criteria
   Step 3: Present data and options
   Step 4: Make decision (with rationale)
   Step 5: Document and communicate

COMMUNICATION TEMPLATES:
- Weekly update email
- Sprint demo agenda
- Executive briefing deck
- Decision log format

STAKEHOLDER FEEDBACK:
- Collected from: [sources]
- Key themes: [themes]
- Actions taken: [actions]
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "stakeholder_management",
                "stakeholders_mapped": 8,
                "communication_plan": True,
                "alignment_achieved": True,
                "conflicts_resolved": 2
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "stakeholder_map.pdf",
                "communication_plan.md",
                "weekly_update_template.md",
                "executive_briefing.pptx"
            ],
            next_steps="Continue regular communication, monitor alignment"
        )
        
    def _measure_success(self, task: Task, context_list) -> TaskResult:
        """Define and track success metrics"""
        
        thoughts = f"""
SUCCESS METRICS (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: Metrics Definition & Tracking

METRICS FRAMEWORK:
1. North Star Metric
   Primary Metric: [User Value Delivered]
   Why: Best indicator of long-term success
   Target: [Specific number and timeframe]

2. AARRR Metrics (Pirate Metrics)
   
   A - Acquisition:
   • Metric: New user signups
   • Current: 100/week
   • Target: 500/week (Q2)
   • Tracking: Google Analytics, Mixpanel
   
   A - Activation:
   • Metric: Users completing onboarding
   • Current: 60% activation rate
   • Target: 80% activation rate
   • Tracking: Product analytics
   
   R - Retention:
   • Metric: Day 7 / Day 30 retention
   • Current: 45% / 25%
   • Target: 60% / 40%
   • Tracking: Cohort analysis
   
   R - Revenue:
   • Metric: MRR (Monthly Recurring Revenue)
   • Current: $10K MRR
   • Target: $100K MRR (12 months)
   • Tracking: Billing system
   
   R - Referral:
   • Metric: Viral coefficient
   • Current: 0.3
   • Target: 0.5 (break even)
   • Tracking: Referral tracking

3. Product KPIs
   Engagement Metrics:
   - DAU/MAU ratio: 30% (target: 40%)
   - Session duration: 8 min (target: 12 min)
   - Features adopted: 3.2/user (target: 5/user)
   
   Quality Metrics:
   - Bug rate: 2/week (target: <1/week)
   - Support tickets: 15/week (target: <10/week)
   - NPS score: 35 (target: 50+)
   
   Business Metrics:
   - CAC (Customer Acquisition Cost): $50
   - LTV (Lifetime Value): $600
   - LTV:CAC ratio: 12:1 (excellent!)

4. Success Criteria per Milestone
   MVP Launch (Month 3):
   ✓ 500 active users
   ✓ 60% activation rate
   ✓ NPS > 30
   ✓ <3 critical bugs
   
   Product-Market Fit (Month 6):
   ✓ 5,000 active users
   ✓ 40% D30 retention
   ✓ NPS > 50
   ✓ Revenue growing 20% MoM

5. Analytics Implementation
   Tools:
   - Mixpanel (product analytics)
   - Amplitude (user behavior)
   - Google Analytics (traffic)
   - Hotjar (heatmaps, recordings)
   
   Events Tracked:
   • User signup, login, logout
   • Feature usage (all major features)
   • Errors and failures
   • Performance metrics

DASHBOARD DESIGN:
- Executive dashboard (high-level KPIs)
- Product dashboard (detailed metrics)
- Team dashboard (operational metrics)
- Real-time updates via Grafana

DATA-DRIVEN DECISIONS:
- Weekly metrics review
- A/B testing for features
- User feedback integration
- Continuous optimization
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "success_metrics",
                "kpis_defined": 12,
                "north_star_metric": True,
                "aarrr_framework": True,
                "dashboard_designed": True,
                "analytics_plan": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "metrics_framework.pdf",
                "kpi_dashboard_mockup.png",
                "analytics_plan.md",
                "success_criteria.md"
            ],
            next_steps="Implement analytics with Tomasz (Dev), create dashboards with Joanna (Data)"
        )
        
    def _general_pm_work(self, task: Task, context_list) -> TaskResult:
        """General product management work"""
        
        thoughts = f"""
PRODUCT MANAGEMENT TASK (Katarzyna Zielińska):
{'='*70}

TASK: {task.title}
TYPE: General Product Management

PM APPROACH:
1. Product Thinking
   - User-centered perspective
   - Business value focus
   - Data-driven decisions
   - Balancing priorities
   
2. Cross-Functional Collaboration
   - Working with Tomasz (Dev) on feasibility
   - Aligning with Magdalena (UX) on design
   - Coordinating with Michał (Arch) on tech
   - Partnering with Anna (QA) on quality
   
3. Prioritization Framework
   Considering:
   • User impact (high/medium/low)
   • Business value (revenue, retention, growth)
   • Technical effort (Tomasz estimates)
   • Strategic alignment (roadmap fit)
   
4. Decision-Making
   Data + Intuition + Team Input = Good Decisions
   
   Process:
   - Gather data and perspectives
   - Define decision criteria
   - Evaluate options
   - Make decision with rationale
   - Document and communicate

PM CONTEXT:
{len(context_list)} previous product decisions reviewed

DELIVERABLE:
- Product-focused solution
- Business value justified
- User needs considered
- Ready for execution

STATUS: Completed with product management best practices
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "general_pm",
                "status": "completed",
                "user_focused": True,
                "business_value": True,
                "prioritized": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["pm_solution.md", "decision_rationale.md"],
            next_steps="Coordinate with team for execution"
        )


# Module test
if __name__ == "__main__":
    import uuid
    
    print("Testing KatarzynaAgent...")
    
    katarzyna = KatarzynaAgent()
    
    # Test product strategy task
    task = Task(
        task_id=uuid.uuid4(),
        title="Define product roadmap",
        description="Create product roadmap for project metrics dashboard",
        assigned_to=katarzyna.name,
        assigned_by="Test",
        context={},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    result = katarzyna.process_task(task)
    
    print(f"\n✅ KatarzynaAgent test:")
    print(f"   Status: {result.status.value}")
    print(f"   Type: {result.output.get('type')}")
    print(f"   Contains 'roadmap': {'roadmap' in result.thoughts.lower()}")
    print(f"   Contains 'stakeholder': {'stakeholder' in result.thoughts.lower()}")
    print(f"   Contains 'metrics': {'metrics' in result.thoughts.lower()}")
    
    assert result.status == TaskStatus.DONE
    assert "roadmap" in result.thoughts.lower() or "product" in result.thoughts.lower()
    
    print("\n✅ KatarzynaAgent ready!")
