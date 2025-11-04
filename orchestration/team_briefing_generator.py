"""
Team Briefing Generator
=======================

Generates professional briefings when tasks are delegated to teams.
Shows team members what they need to know to start work.

Author: Aleksander Nowak (Orchestrator)
Date: 2025-11-04
Sprint: Transparency Tools + Cross-Team Improvements
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum


class BriefingPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TeamMember:
    """Team member assignment"""
    name: str
    role: str
    responsibilities: List[str]
    status: str = "assigned"


@dataclass
class TaskBriefing:
    """Complete task briefing for a team"""
    # Basic info
    task_id: str
    title: str
    description: str
    requester: str
    priority: BriefingPriority
    
    # Team info
    team_name: str
    team_lead: str
    team_members: List[TeamMember]
    
    # Requirements
    objectives: List[str]
    deliverables: List[str]
    constraints: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None
    
    # Timeline
    deadline: Optional[datetime] = None
    estimated_duration: Optional[str] = None
    
    # Context
    background: Optional[str] = None
    success_criteria: Optional[List[str]] = None
    
    # Metadata
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class TeamBriefingGenerator:
    """
    Generates professional team briefings.
    
    Usage:
        generator = TeamBriefingGenerator()
        
        briefing = generator.create_briefing(
            task_id="TASK-001",
            title="Analyze Claude SDK competitors",
            team_name="Analytical Team",
            requester="User (Artur)",
            ...
        )
        
        # Print briefing
        generator.print_briefing(briefing)
        
        # Or get markdown
        markdown = generator.to_markdown(briefing)
    """
    
    def create_briefing(
        self,
        task_id: str,
        title: str,
        description: str,
        team_name: str,
        team_lead: str,
        requester: str = "User",
        priority: BriefingPriority = BriefingPriority.MEDIUM,
        objectives: Optional[List[str]] = None,
        deliverables: Optional[List[str]] = None,
        team_members: Optional[List[TeamMember]] = None,
        deadline: Optional[datetime] = None,
        estimated_duration: Optional[str] = None,
        background: Optional[str] = None,
        success_criteria: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None
    ) -> TaskBriefing:
        """Create a complete task briefing"""
        
        return TaskBriefing(
            task_id=task_id,
            title=title,
            description=description,
            requester=requester,
            priority=priority,
            team_name=team_name,
            team_lead=team_lead,
            team_members=team_members or [],
            objectives=objectives or [],
            deliverables=deliverables or [],
            constraints=constraints,
            dependencies=dependencies,
            deadline=deadline,
            estimated_duration=estimated_duration,
            background=background,
            success_criteria=success_criteria
        )
    
    def print_briefing(self, briefing: TaskBriefing):
        """Print a formatted briefing to console"""
        
        priority_emoji = {
            BriefingPriority.LOW: "🔵",
            BriefingPriority.MEDIUM: "🟡",
            BriefingPriority.HIGH: "🟠",
            BriefingPriority.CRITICAL: "🔴"
        }
        
        print("\n" + "="*70)
        print(f"📋 {briefing.team_name.upper()} BRIEFING")
        print("="*70)
        print()
        
        # Header
        print(f"Task ID: {briefing.task_id}")
        print(f"Title: {briefing.title}")
        print(f"Priority: {priority_emoji[briefing.priority]} {briefing.priority.value.upper()}")
        print(f"Requester: {briefing.requester}")
        print(f"Assigned: {briefing.created_at.strftime('%Y-%m-%d %H:%M')}")
        if briefing.deadline:
            print(f"Deadline: {briefing.deadline.strftime('%Y-%m-%d %H:%M')}")
        if briefing.estimated_duration:
            print(f"Est. Duration: {briefing.estimated_duration}")
        print()
        
        # Description
        print("─"*70)
        print("📝 DESCRIPTION")
        print("─"*70)
        print(briefing.description)
        print()
        
        # Background (if provided)
        if briefing.background:
            print("─"*70)
            print("📚 BACKGROUND")
            print("─"*70)
            print(briefing.background)
            print()
        
        # Objectives
        if briefing.objectives:
            print("─"*70)
            print("🎯 OBJECTIVES")
            print("─"*70)
            for i, obj in enumerate(briefing.objectives, 1):
                print(f"  {i}. {obj}")
            print()
        
        # Deliverables
        if briefing.deliverables:
            print("─"*70)
            print("📦 EXPECTED DELIVERABLES")
            print("─"*70)
            for i, deliv in enumerate(briefing.deliverables, 1):
                print(f"  {i}. {deliv}")
            print()
        
        # Team Composition
        print("─"*70)
        print("👥 TEAM COMPOSITION")
        print("─"*70)
        print(f"Lead: {briefing.team_lead}")
        print()
        if briefing.team_members:
            print("Members:")
            for member in briefing.team_members:
                print(f"  • {member.name} ({member.role})")
                if member.responsibilities:
                    for resp in member.responsibilities:
                        print(f"    - {resp}")
        print()
        
        # Success Criteria
        if briefing.success_criteria:
            print("─"*70)
            print("✅ SUCCESS CRITERIA")
            print("─"*70)
            for i, criteria in enumerate(briefing.success_criteria, 1):
                print(f"  {i}. {criteria}")
            print()
        
        # Constraints
        if briefing.constraints:
            print("─"*70)
            print("⚠️  CONSTRAINTS")
            print("─"*70)
            for constraint in briefing.constraints:
                print(f"  • {constraint}")
            print()
        
        # Dependencies
        if briefing.dependencies:
            print("─"*70)
            print("🔗 DEPENDENCIES")
            print("─"*70)
            for dep in briefing.dependencies:
                print(f"  • {dep}")
            print()
        
        # Footer
        print("="*70)
        print("Status: 🟢 READY TO START")
        print("="*70)
        print()
    
    def to_markdown(self, briefing: TaskBriefing) -> str:
        """Convert briefing to markdown format"""
        
        priority_emoji = {
            BriefingPriority.LOW: "🔵",
            BriefingPriority.MEDIUM: "🟡",
            BriefingPriority.HIGH: "🟠",
            BriefingPriority.CRITICAL: "🔴"
        }
        
        md = []
        md.append(f"# {briefing.team_name} Briefing")
        md.append("")
        md.append(f"**Task ID:** `{briefing.task_id}`  ")
        md.append(f"**Title:** {briefing.title}  ")
        md.append(f"**Priority:** {priority_emoji[briefing.priority]} {briefing.priority.value.upper()}  ")
        md.append(f"**Requester:** {briefing.requester}  ")
        md.append(f"**Assigned:** {briefing.created_at.strftime('%Y-%m-%d %H:%M')}  ")
        
        if briefing.deadline:
            md.append(f"**Deadline:** {briefing.deadline.strftime('%Y-%m-%d %H:%M')}  ")
        if briefing.estimated_duration:
            md.append(f"**Est. Duration:** {briefing.estimated_duration}  ")
        
        md.append("")
        md.append("---")
        md.append("")
        
        # Description
        md.append("## 📝 Description")
        md.append("")
        md.append(briefing.description)
        md.append("")
        
        # Background
        if briefing.background:
            md.append("## 📚 Background")
            md.append("")
            md.append(briefing.background)
            md.append("")
        
        # Objectives
        if briefing.objectives:
            md.append("## 🎯 Objectives")
            md.append("")
            for i, obj in enumerate(briefing.objectives, 1):
                md.append(f"{i}. {obj}")
            md.append("")
        
        # Deliverables
        if briefing.deliverables:
            md.append("## 📦 Expected Deliverables")
            md.append("")
            for i, deliv in enumerate(briefing.deliverables, 1):
                md.append(f"{i}. {deliv}")
            md.append("")
        
        # Team
        md.append("## 👥 Team Composition")
        md.append("")
        md.append(f"**Lead:** {briefing.team_lead}")
        md.append("")
        if briefing.team_members:
            md.append("**Members:**")
            for member in briefing.team_members:
                md.append(f"- **{member.name}** ({member.role})")
                if member.responsibilities:
                    for resp in member.responsibilities:
                        md.append(f"  - {resp}")
            md.append("")
        
        # Success Criteria
        if briefing.success_criteria:
            md.append("## ✅ Success Criteria")
            md.append("")
            for i, criteria in enumerate(briefing.success_criteria, 1):
                md.append(f"{i}. {criteria}")
            md.append("")
        
        # Constraints
        if briefing.constraints:
            md.append("## ⚠️ Constraints")
            md.append("")
            for constraint in briefing.constraints:
                md.append(f"- {constraint}")
            md.append("")
        
        # Dependencies
        if briefing.dependencies:
            md.append("## 🔗 Dependencies")
            md.append("")
            for dep in briefing.dependencies:
                md.append(f"- {dep}")
            md.append("")
        
        md.append("---")
        md.append("")
        md.append("**Status:** 🟢 READY TO START")
        
        return "\n".join(md)


if __name__ == "__main__":
    # Demo: Create a sample briefing
    generator = TeamBriefingGenerator()
    
    briefing = generator.create_briefing(
        task_id="TASK-SDK-001",
        title="Analyze Claude Code SDK competitors",
        description="Conduct comprehensive analysis of Claude Code Multiagent SDK and competing frameworks. Identify features, strengths, weaknesses, and recommendations for Destiny Framework.",
        team_name="Analytical Team",
        team_lead="Viktor Kovalenko",
        requester="User (Artur)",
        priority=BriefingPriority.HIGH,
        objectives=[
            "Research Claude SDK capabilities and architecture",
            "Identify real competitors (Claude-Flow, Mastra)",
            "Compare features with Destiny Framework",
            "Provide actionable recommendations"
        ],
        deliverables=[
            "Verified sources document with URLs",
            "Feature comparison matrix",
            "Critical analysis with Devil's Advocate review",
            "Final recommendations report"
        ],
        team_members=[
            TeamMember(
                name="Elena Volkov",
                role="OSINT Specialist",
                responsibilities=["Web research", "Source verification", "Intelligence gathering"]
            ),
            TeamMember(
                name="Sofia Martinez",
                role="Market Research Analyst",
                responsibilities=["Competitive analysis", "Market positioning", "Trend identification"]
            ),
            TeamMember(
                name="Maya Patel",
                role="Data Analyst",
                responsibilities=["Feature comparison", "Data synthesis", "Metrics analysis"]
            ),
            TeamMember(
                name="Damian Rousseau",
                role="Devil's Advocate",
                responsibilities=["Critical review", "Risk identification", "Challenge assumptions"]
            ),
            TeamMember(
                name="Lucas Rivera",
                role="Report Synthesizer",
                responsibilities=["Report writing", "Documentation", "Final synthesis"]
            )
        ],
        estimated_duration="4-6 hours",
        background="User wants to understand if Destiny Framework should adopt features from Claude SDK or competitors.",
        success_criteria=[
            "All sources verified and accessible",
            "Feature matrix covers 10+ key capabilities",
            "Recommendations are specific and actionable",
            "Technical team validates findings"
        ],
        constraints=[
            "Use only publicly available information",
            "No speculation - verify all claims",
            "Focus on architectural decisions, not marketing"
        ]
    )
    
    # Print briefing
    generator.print_briefing(briefing)
    
    # Save as markdown
    print("\n📄 Saving as markdown...")
    markdown = generator.to_markdown(briefing)
    with open("/tmp/briefing_demo.md", "w") as f:
        f.write(markdown)
    print("✅ Saved to /tmp/briefing_demo.md")
