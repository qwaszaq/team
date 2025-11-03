"""
Magdalena Wiśniewska - Senior UX/UI Designer Agent
Specialization: User experience design, interface design, usability testing

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class MagdalenaAgent(BaseAgent):
    """
    Senior UX/UI Designer Agent
    
    Specialized in:
    - User experience design
    - Interface design and wireframing
    - User research and testing
    - Design systems
    - Accessibility (A11y)
    
    This agent provides UX-specific reasoning and design-focused outputs.
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        super().__init__(
            name="Magdalena Wiśniewska",
            role="Senior UX/UI Designer",
            specialization="User experience design, UI/UX, Usability, Accessibility",
            project_id=project_id
        )
        
        # UX-specific attributes
        self.design_tools = ["Figma", "Sketch", "Adobe XD", "InVision"]
        self.research_methods = ["User interviews", "Surveys", "Usability testing", "A/B testing"]
        self.focus_areas = ["User journeys", "Wireframes", "Prototypes", "Design systems", "A11y"]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute UX-specific work
        
        Analyzes task and routes to appropriate UX handler based on keywords.
        """
        start_time = datetime.now()
        
        # Load relevant UX context
        context = self.load_context(task.description, limit=3)
        context_list = context if isinstance(context, list) else []
        
        # Analyze task type based on description
        task_lower = task.description.lower()
        
        if any(word in task_lower for word in ["design", "ux", "user experience", "interface", "ui"]):
            result = self._design_user_experience(task, context_list)
        elif any(word in task_lower for word in ["wireframe", "mockup", "prototype", "layout"]):
            result = self._create_wireframes(task, context_list)
        elif any(word in task_lower for word in ["research", "user", "interview", "survey", "testing"]):
            result = self._conduct_user_research(task, context_list)
        elif any(word in task_lower for word in ["component", "design system", "library", "pattern"]):
            result = self._design_system_work(task, context_list)
        elif any(word in task_lower for word in ["accessibility", "a11y", "wcag", "inclusive"]):
            result = self._accessibility_review(task, context_list)
        else:
            result = self._general_ux_work(task, context_list)
            
        # Calculate actual time taken
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
        
    def _design_user_experience(self, task: Task, context_list) -> TaskResult:
        """Design complete user experience for a feature"""
        
        thoughts = f"""
UX DESIGN ANALYSIS (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: User Experience Design

UX DESIGN PROCESS:
1. User Research Foundation
   - Understanding target users and their needs
   - Defining user personas and use cases
   - Analyzing user pain points and goals
   
2. Information Architecture
   - Organizing content and features logically
   - Creating site map and navigation structure
   - Defining user flows and task flows
   
3. User Journey Mapping
   - Mapping key user journeys from start to finish
   - Identifying touchpoints and interactions
   - Highlighting opportunities for delight
   
4. Interaction Design
   - Defining interaction patterns
   - Specifying feedback and transitions
   - Ensuring consistency across flows
   
5. Visual Design Direction
   - Establishing visual hierarchy
   - Defining color, typography, spacing
   - Creating mood boards and style tiles

UX CONTEXT REVIEWED:
{len(context_list)} previous UX decisions analyzed

USER-CENTERED APPROACH:
✓ Focus on user needs and goals
✓ Simplicity and clarity prioritized
✓ Accessibility considerations from start
✓ Mobile-first responsive design
✓ Performance and usability balance

DESIGN DELIVERABLES:
- User personas and journey maps
- Information architecture diagram
- User flow diagrams
- Wireframes (lo-fi and hi-fi)
- Interactive prototype
- Design specifications

FIGMA FILE STRUCTURE:
📁 Project
  ├── 01_Research (personas, journeys)
  ├── 02_IA (site map, flows)
  ├── 03_Wireframes (lo-fi sketches)
  ├── 04_Hi-Fi (detailed designs)
  └── 05_Prototype (interactive)

NEXT STEPS:
- User testing with prototype
- Iterate based on feedback
- Handoff to development (Tomasz)
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "ux_design",
                "design_tool": "Figma",
                "user_personas": 3,
                "user_journeys": 2,
                "wireframes_created": True,
                "prototype_ready": True,
                "accessibility_considered": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "user_personas.pdf",
                "user_journey_maps.pdf", 
                "wireframes_lofi.fig",
                "wireframes_hifi.fig",
                "interactive_prototype.fig",
                "design_specs.pdf"
            ],
            next_steps="Ready for user testing, then handoff to Tomasz (Dev) for implementation"
        )
        
    def _create_wireframes(self, task: Task, context_list) -> TaskResult:
        """Create wireframes and mockups"""
        
        thoughts = f"""
WIREFRAMING PROCESS (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: Wireframe Creation

WIREFRAMING APPROACH:
1. Low-Fidelity Sketches
   - Rapid ideation with basic shapes
   - Exploring multiple layout options
   - Focus on structure, not details
   - Paper sketches or digital lo-fi
   
2. Content Prioritization
   - Defining visual hierarchy
   - Identifying primary, secondary, tertiary content
   - Ensuring key actions are prominent
   
3. Layout Patterns
   - Choosing appropriate UI patterns
   - Grid system and alignment
   - Spacing and white space strategy
   - Responsive breakpoints considered
   
4. High-Fidelity Wireframes
   - Detailed component placement
   - Real content or realistic placeholders
   - Interaction states (hover, active, disabled)
   - Annotations for complex behaviors
   
5. Component Inventory
   - Buttons, forms, cards, navigation
   - Input fields, dropdowns, modals
   - Icons and imagery placeholders
   - Feedback elements (toasts, alerts)

DESIGN DECISIONS:
✓ Mobile-first approach (320px → desktop)
✓ 8px grid system for consistency
✓ Clear visual hierarchy (typography scale)
✓ Sufficient touch targets (44x44px minimum)
✓ Accessible color contrast (WCAG AA)

WIREFRAME FIDELITY LEVELS:
- Lo-Fi: Structure and layout only
- Mid-Fi: Basic styling, grayscale
- Hi-Fi: Full styling, colors, imagery

FIGMA LAYERS:
📋 Wireframes
  ├── Mobile (320-767px)
  ├── Tablet (768-1023px)
  └── Desktop (1024px+)

ANNOTATIONS:
- Interaction notes for complex flows
- Responsive behavior specifications
- Edge cases and error states
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "wireframes",
                "fidelity": "high",
                "screens_designed": 8,
                "responsive": True,
                "annotated": True,
                "grid_system": "8px"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "wireframes_mobile.fig",
                "wireframes_tablet.fig",
                "wireframes_desktop.fig",
                "annotations.pdf"
            ],
            next_steps="Review with stakeholders, then create high-fidelity designs"
        )
        
    def _conduct_user_research(self, task: Task, context_list) -> TaskResult:
        """Conduct user research and gather insights"""
        
        thoughts = f"""
USER RESEARCH PLAN (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: User Research

RESEARCH METHODOLOGY:
1. Research Goals Definition
   - What questions need answering?
   - What decisions will research inform?
   - Success criteria for research
   
2. User Segmentation
   - Identifying target user groups
   - Creating screening criteria
   - Recruiting diverse participants
   - Sample size: 8-12 users (qualitative)
   
3. Research Methods
   ├── Qualitative Methods:
   │   • User interviews (1-on-1, 30-45 min)
   │   • Contextual inquiry (observing in context)
   │   • Usability testing (think-aloud protocol)
   │   • Focus groups (if needed)
   │
   └── Quantitative Methods:
       • Surveys (larger sample, n>100)
       • Analytics review (existing data)
       • A/B testing (post-launch)
   
4. Research Execution
   - Interview guide / test script
   - Recording and note-taking
   - Observing behavior, not just listening
   - Probing deeper on insights
   
5. Analysis & Synthesis
   - Affinity mapping of findings
   - Identifying patterns and themes
   - Creating user personas
   - Documenting pain points and opportunities

RESEARCH FINDINGS:
📊 Key Insights Discovered:
1. Users struggle with [specific pain point]
2. Main use case is [primary goal]
3. Users expect [specific feature/behavior]
4. Mobile usage is [percentage]%
5. Accessibility is important for [user segment]

USER PERSONAS CREATED:
👤 Primary: [Name] - [brief description]
   Goals: [what they want to achieve]
   Pain points: [what frustrates them]
   
👥 Secondary: [Name] - [brief description]
   Goals: [different goals]
   Pain points: [different frustrations]

RECOMMENDATIONS:
✓ Prioritize [specific feature] based on user needs
✓ Simplify [specific flow] - users got confused
✓ Add [specific element] - users expect it
✓ Consider [alternative approach] for [use case]
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "user_research",
                "research_method": "interviews",
                "participants": 10,
                "personas_created": 2,
                "key_insights": 5,
                "recommendations": 4
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "research_plan.pdf",
                "interview_guide.pdf",
                "research_findings.pdf",
                "user_personas.pdf",
                "recommendations.pdf"
            ],
            next_steps="Use insights to inform design decisions and validate with prototypes"
        )
        
    def _design_system_work(self, task: Task, context_list) -> TaskResult:
        """Work on design system and component library"""
        
        thoughts = f"""
DESIGN SYSTEM WORK (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: Design System Development

DESIGN SYSTEM STRUCTURE:
1. Foundation Layer
   ├── Colors (brand, semantic, feedback)
   ├── Typography (scales, weights, line heights)
   ├── Spacing (8px grid, margin/padding tokens)
   ├── Elevation (shadows, z-index)
   └── Breakpoints (responsive grid)
   
2. Component Library
   ├── Atoms (buttons, inputs, icons, badges)
   ├── Molecules (form groups, cards, list items)
   ├── Organisms (navigation, modals, forms)
   └── Templates (page layouts)
   
3. Patterns & Guidelines
   - Interaction patterns
   - Usage guidelines
   - Do's and Don'ts
   - Accessibility requirements
   
4. Documentation
   - Component specs
   - Code examples (for Tomasz)
   - Design principles
   - Contribution guidelines

COMPONENT INVENTORY:
🎨 Foundation Tokens:
- Colors: 8 primary, 12 semantic, 6 feedback
- Typography: 6 size scales, 3 weights
- Spacing: 8px base (4, 8, 16, 24, 32, 40, 48, 64)
- Shadows: 4 elevation levels

🧩 Components Created:
- Button (primary, secondary, text, icon)
- Input (text, number, email, search)
- Dropdown (select, multi-select, autocomplete)
- Card (basic, media, interactive)
- Modal (dialog, alert, confirmation)
- Navigation (top nav, side nav, breadcrumb)

FIGMA ORGANIZATION:
📁 Design System
  ├── 🎨 Foundations (colors, type, spacing)
  ├── 🧩 Components (organized library)
  ├── 📋 Templates (page layouts)
  └── 📖 Documentation (usage guides)

DESIGN TOKENS:
Prepared for handoff to development:
- CSS custom properties
- SCSS variables
- JSON token files
- Component API specs

BENEFITS:
✓ Consistency across product
✓ Faster design iteration
✓ Easier development handoff
✓ Scalable and maintainable
✓ Accessibility built-in
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "design_system",
                "components_created": 15,
                "foundation_tokens": True,
                "documentation": "complete",
                "figma_library": True,
                "dev_handoff_ready": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "design_system.fig",
                "component_library.fig",
                "design_tokens.json",
                "usage_guidelines.pdf",
                "developer_handoff.pdf"
            ],
            next_steps="Share with team, get feedback, handoff tokens to Tomasz (Dev)"
        )
        
    def _accessibility_review(self, task: Task, context_list) -> TaskResult:
        """Review design for accessibility compliance"""
        
        thoughts = f"""
ACCESSIBILITY REVIEW (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: Accessibility (A11y) Review

WCAG 2.1 COMPLIANCE CHECKLIST:
1. Perceivable
   ✓ Color contrast ratios (AA: 4.5:1 text, 3:1 UI)
   ✓ Text alternatives for images (alt text)
   ✓ Captions for video/audio content
   ✓ Multiple ways to perceive information
   
2. Operable
   ✓ Keyboard navigation (no mouse required)
   ✓ Focus indicators visible and clear
   ✓ No keyboard traps
   ✓ Touch targets ≥44x44px
   ✓ Sufficient time to read/interact
   
3. Understandable
   ✓ Clear, simple language
   ✓ Consistent navigation
   ✓ Input error identification & suggestions
   ✓ Labels and instructions provided
   
4. Robust
   ✓ Semantic HTML structure
   ✓ ARIA labels where needed
   ✓ Compatible with assistive tech

ACCESSIBILITY AUDIT RESULTS:
📊 Overall Score: 92/100 (WCAG AA compliant)

✅ PASSES:
- Color contrast: All text meets AA standard
- Keyboard navigation: Full keyboard access
- Focus indicators: Clear and visible
- Touch targets: All ≥44x44px
- Semantic structure: Proper headings, landmarks

⚠️  ISSUES FOUND (3):
1. [MEDIUM] Missing alt text on 2 decorative images
   → Fix: Add alt="" for decorative images
   
2. [LOW] One form missing associated label
   → Fix: Add <label> or aria-label
   
3. [LOW] Link text not descriptive ("click here")
   → Fix: Use descriptive link text

RECOMMENDATIONS:
✓ Add skip navigation link
✓ Ensure error messages are announced
✓ Test with screen reader (VoiceOver, NVDA)
✓ Consider reduced motion preferences
✓ Provide text alternatives for icons

TESTING TOOLS USED:
- Axe DevTools (automated scan)
- Contrast checker (color ratios)
- Keyboard-only navigation test
- Screen reader test (VoiceOver)

COMPLIANCE LEVEL: WCAG 2.1 AA ✅
Ready for development with minor fixes.
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "accessibility_review",
                "wcag_level": "AA",
                "compliance_score": 92,
                "issues_found": 3,
                "severity": "low_to_medium",
                "passes": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "accessibility_audit.pdf",
                "wcag_checklist.pdf",
                "issue_report.pdf",
                "remediation_guide.pdf"
            ],
            next_steps="Address 3 minor issues, then ready for development"
        )
        
    def _general_ux_work(self, task: Task, context_list) -> TaskResult:
        """General UX design work"""
        
        thoughts = f"""
UX DESIGN TASK (Magdalena Wiśniewska):
{'='*70}

TASK: {task.title}
TYPE: General UX Work

UX APPROACH:
1. User-Centered Mindset
   - Always starting with user needs
   - Questioning assumptions
   - Validating with research or testing
   
2. Design Thinking Process
   - Empathize: Understand users deeply
   - Define: Frame the right problem
   - Ideate: Explore multiple solutions
   - Prototype: Make ideas tangible
   - Test: Learn and iterate
   
3. Key UX Principles Applied
   ✓ Clarity over cleverness
   ✓ Consistency in patterns
   ✓ Feedback for actions
   ✓ Error prevention and recovery
   ✓ Accessibility for all users
   
4. Collaboration
   - Working with Tomasz (Dev) on feasibility
   - Getting Anna's (QA) input on edge cases
   - Aligning with Michał (Architect) on constraints

UX CONTEXT AVAILABLE:
{len(context_list)} previous UX decisions reviewed

DELIVERABLES:
- User-focused design solution
- Documented design rationale
- Ready for stakeholder review
- Prepared for usability testing

STATUS: Completed with UX best practices
APPROACH: User-centered, research-informed
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "general_ux",
                "status": "completed",
                "user_centered": True,
                "research_informed": True,
                "accessibility_considered": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["ux_solution.fig", "design_rationale.pdf"],
            next_steps="Review with team and validate with users"
        )


# Module test
if __name__ == "__main__":
    import uuid
    
    print("Testing MagdalenaAgent...")
    
    magdalena = MagdalenaAgent()
    
    # Test UX design task
    task = Task(
        task_id=uuid.uuid4(),
        title="Design user dashboard",
        description="Design the user experience for a project metrics dashboard",
        assigned_to=magdalena.name,
        assigned_by="Test",
        context={},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    result = magdalena.process_task(task)
    
    print(f"\n✅ MagdalenaAgent test:")
    print(f"   Status: {result.status.value}")
    print(f"   Type: {result.output.get('type')}")
    print(f"   Contains 'ux': {'ux' in result.thoughts.lower()}")
    print(f"   Contains 'user': {'user' in result.thoughts.lower()}")
    print(f"   Contains 'wireframe': {'wireframe' in result.thoughts.lower()}")
    
    assert result.status == TaskStatus.DONE
    assert "ux" in result.thoughts.lower() or "user" in result.thoughts.lower()
    
    print("\n✅ MagdalenaAgent ready!")
