"""
Cross-Team Handoff Protocol
============================

Manages handoffs between Core Team and Analytical Team.
Ensures clean transitions, no information loss, and accountability.

Author: Aleksander Nowak (Orchestrator)  
Date: 2025-11-04
Sprint: Transparency Tools + Cross-Team Improvements
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Literal
from enum import Enum
import json


class HandoffType(Enum):
    """Type of handoff"""
    REQUEST = "request"  # Core → Analytical (requesting research)
    DELIVERY = "delivery"  # Analytical → Core (delivering results)
    FEEDBACK = "feedback"  # Core → Analytical (requesting changes)
    CLARIFICATION = "clarification"  # Either direction (asking questions)


class HandoffStatus(Enum):
    """Status of handoff"""
    INITIATED = "initiated"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass
class HandoffArtifact:
    """Artifact being transferred"""
    name: str
    type: str  # "document", "data", "code", "decision"
    location: str  # File path or location
    description: Optional[str] = None
    size: Optional[str] = None


@dataclass
class HandoffChecklist:
    """Checklist for handoff completion"""
    items: List[str] = field(default_factory=list)
    completed: List[bool] = field(default_factory=list)
    
    @property
    def is_complete(self) -> bool:
        return all(self.completed) if self.completed else False
    
    @property
    def completion_percentage(self) -> int:
        if not self.items:
            return 100
        return int((sum(self.completed) / len(self.items)) * 100)


@dataclass
class TeamHandoff:
    """
    Complete handoff record between teams.
    
    Tracks:
    - Who is handing off to whom
    - What is being handed off
    - Why the handoff is happening
    - Status and progress
    - Acceptance criteria
    """
    
    # Identity
    handoff_id: str
    handoff_type: HandoffType
    
    # Teams
    from_team: str  # "Core Team" or "Analytical Team"
    from_lead: str  # Team lead name
    to_team: str
    to_lead: str
    
    # Content
    title: str
    description: str
    context: Optional[str] = None
    artifacts: List[HandoffArtifact] = field(default_factory=list)
    
    # Requirements
    deliverables: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    checklist: Optional[HandoffChecklist] = None
    
    # Timeline
    initiated_at: datetime = None
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    
    # Status
    status: HandoffStatus = HandoffStatus.INITIATED
    notes: List[str] = field(default_factory=list)
    
    # Accountability
    initiated_by: str = ""
    accepted_by: Optional[str] = None
    
    def __post_init__(self):
        if self.initiated_at is None:
            self.initiated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "handoff_id": self.handoff_id,
            "handoff_type": self.handoff_type.value,
            "from_team": self.from_team,
            "from_lead": self.from_lead,
            "to_team": self.to_team,
            "to_lead": self.to_lead,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "initiated_at": self.initiated_at.isoformat(),
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "checklist_complete": self.checklist.is_complete if self.checklist else True,
            "artifacts": [{"name": a.name, "type": a.type, "location": a.location} for a in self.artifacts]
        }


class CrossTeamHandoffManager:
    """
    Manages all cross-team handoffs.
    
    Usage:
        manager = CrossTeamHandoffManager()
        
        # Core Team requests research from Analytical
        handoff_id = manager.initiate_handoff(
            handoff_type=HandoffType.REQUEST,
            from_team="Core Team",
            from_lead="Aleksander Nowak",
            to_team="Analytical Team",
            to_lead="Viktor Kovalenko",
            title="Research Claude SDK competitors",
            description="Need comprehensive competitive analysis...",
            deliverables=["Research report", "Feature comparison"]
        )
        
        # Analytical Team accepts
        manager.accept_handoff(handoff_id, "Viktor Kovalenko")
        
        # Work happens...
        manager.update_progress(handoff_id, "Research 50% complete")
        
        # Analytical Team delivers
        manager.complete_handoff(handoff_id, ["docs/research_report.md"])
        
        # View handoff
        manager.print_handoff(handoff_id)
    """
    
    def __init__(self):
        self.handoffs: Dict[str, TeamHandoff] = {}
        self.handoff_counter = 0
    
    def _generate_handoff_id(self) -> str:
        """Generate unique handoff ID"""
        self.handoff_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"HANDOFF-{timestamp}-{self.handoff_counter:03d}"
    
    def initiate_handoff(
        self,
        handoff_type: HandoffType,
        from_team: str,
        from_lead: str,
        to_team: str,
        to_lead: str,
        title: str,
        description: str,
        initiated_by: str = "",
        context: Optional[str] = None,
        deliverables: Optional[List[str]] = None,
        acceptance_criteria: Optional[List[str]] = None,
        checklist_items: Optional[List[str]] = None,
        deadline: Optional[datetime] = None
    ) -> str:
        """Initiate a new cross-team handoff"""
        
        handoff_id = self._generate_handoff_id()
        
        checklist = None
        if checklist_items:
            checklist = HandoffChecklist(
                items=checklist_items,
                completed=[False] * len(checklist_items)
            )
        
        handoff = TeamHandoff(
            handoff_id=handoff_id,
            handoff_type=handoff_type,
            from_team=from_team,
            from_lead=from_lead,
            to_team=to_team,
            to_lead=to_lead,
            title=title,
            description=description,
            context=context,
            deliverables=deliverables or [],
            acceptance_criteria=acceptance_criteria or [],
            checklist=checklist,
            deadline=deadline,
            initiated_by=initiated_by or from_lead
        )
        
        self.handoffs[handoff_id] = handoff
        return handoff_id
    
    def accept_handoff(self, handoff_id: str, accepted_by: str):
        """Accept a handoff"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        handoff.status = HandoffStatus.ACCEPTED
        handoff.accepted_at = datetime.now()
        handoff.accepted_by = accepted_by
        handoff.notes.append(f"Accepted by {accepted_by} at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def start_work(self, handoff_id: str):
        """Mark handoff as in progress"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        handoff.status = HandoffStatus.IN_PROGRESS
        handoff.notes.append(f"Work started at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def update_progress(self, handoff_id: str, note: str):
        """Add progress note"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        handoff.notes.append(f"[{timestamp}] {note}")
    
    def check_item(self, handoff_id: str, item_index: int):
        """Check off a checklist item"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        if handoff.checklist and item_index < len(handoff.checklist.items):
            handoff.checklist.completed[item_index] = True
            item_name = handoff.checklist.items[item_index]
            handoff.notes.append(f"✅ Completed: {item_name}")
    
    def add_artifact(
        self,
        handoff_id: str,
        name: str,
        artifact_type: str,
        location: str,
        description: Optional[str] = None
    ):
        """Add an artifact to the handoff"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        artifact = HandoffArtifact(
            name=name,
            type=artifact_type,
            location=location,
            description=description
        )
        
        self.handoffs[handoff_id].artifacts.append(artifact)
        self.handoffs[handoff_id].notes.append(f"📎 Added artifact: {name} ({artifact_type})")
    
    def complete_handoff(self, handoff_id: str, artifacts: Optional[List[str]] = None):
        """Complete a handoff"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        handoff.status = HandoffStatus.COMPLETED
        handoff.completed_at = datetime.now()
        
        if artifacts:
            for artifact in artifacts:
                handoff.notes.append(f"📦 Delivered: {artifact}")
        
        handoff.notes.append(f"✅ Handoff completed at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def block_handoff(self, handoff_id: str, reason: str):
        """Block a handoff"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        handoff.status = HandoffStatus.BLOCKED
        handoff.notes.append(f"🚫 BLOCKED: {reason}")
    
    def reject_handoff(self, handoff_id: str, reason: str, rejected_by: str):
        """Reject a handoff"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        
        handoff = self.handoffs[handoff_id]
        handoff.status = HandoffStatus.REJECTED
        handoff.notes.append(f"❌ REJECTED by {rejected_by}: {reason}")
    
    def get_handoff(self, handoff_id: str) -> TeamHandoff:
        """Get handoff details"""
        if handoff_id not in self.handoffs:
            raise ValueError(f"Handoff {handoff_id} not found")
        return self.handoffs[handoff_id]
    
    def get_active_handoffs(self, team: Optional[str] = None) -> List[TeamHandoff]:
        """Get all active handoffs"""
        active = [h for h in self.handoffs.values() 
                 if h.status in [HandoffStatus.INITIATED, HandoffStatus.ACCEPTED, HandoffStatus.IN_PROGRESS]]
        
        if team:
            active = [h for h in active if h.to_team == team or h.from_team == team]
        
        return active
    
    def print_handoff(self, handoff_id: str):
        """Print formatted handoff details"""
        handoff = self.get_handoff(handoff_id)
        
        status_emoji = {
            HandoffStatus.INITIATED: "🆕",
            HandoffStatus.ACCEPTED: "✅",
            HandoffStatus.IN_PROGRESS: "🔄",
            HandoffStatus.COMPLETED: "✅",
            HandoffStatus.REJECTED: "❌",
            HandoffStatus.BLOCKED: "🚫"
        }
        
        type_emoji = {
            HandoffType.REQUEST: "📨",
            HandoffType.DELIVERY: "📦",
            HandoffType.FEEDBACK: "💬",
            HandoffType.CLARIFICATION: "❓"
        }
        
        print("\n" + "="*70)
        print(f"🔄 CROSS-TEAM HANDOFF: {handoff.handoff_id}")
        print("="*70)
        print()
        
        print(f"Type: {type_emoji[handoff.handoff_type]} {handoff.handoff_type.value.upper()}")
        print(f"Status: {status_emoji[handoff.status]} {handoff.status.value.upper()}")
        print()
        
        print("─"*70)
        print("👥 TEAMS")
        print("─"*70)
        print(f"From: {handoff.from_team} (Lead: {handoff.from_lead})")
        print(f"To:   {handoff.to_team} (Lead: {handoff.to_lead})")
        print()
        
        print("─"*70)
        print("📋 HANDOFF DETAILS")
        print("─"*70)
        print(f"Title: {handoff.title}")
        print(f"Description: {handoff.description}")
        if handoff.context:
            print(f"Context: {handoff.context}")
        print()
        
        if handoff.deliverables:
            print("─"*70)
            print("📦 EXPECTED DELIVERABLES")
            print("─"*70)
            for i, deliv in enumerate(handoff.deliverables, 1):
                print(f"  {i}. {deliv}")
            print()
        
        if handoff.acceptance_criteria:
            print("─"*70)
            print("✅ ACCEPTANCE CRITERIA")
            print("─"*70)
            for i, criteria in enumerate(handoff.acceptance_criteria, 1):
                print(f"  {i}. {criteria}")
            print()
        
        if handoff.checklist:
            print("─"*70)
            print(f"☑️  CHECKLIST ({handoff.checklist.completion_percentage}% complete)")
            print("─"*70)
            for i, (item, done) in enumerate(zip(handoff.checklist.items, handoff.checklist.completed)):
                checkbox = "✅" if done else "⬜"
                print(f"  {checkbox} {item}")
            print()
        
        if handoff.artifacts:
            print("─"*70)
            print("📎 ARTIFACTS")
            print("─"*70)
            for artifact in handoff.artifacts:
                print(f"  • {artifact.name} ({artifact.type})")
                print(f"    Location: {artifact.location}")
                if artifact.description:
                    print(f"    {artifact.description}")
            print()
        
        print("─"*70)
        print("📅 TIMELINE")
        print("─"*70)
        print(f"Initiated: {handoff.initiated_at.strftime('%Y-%m-%d %H:%M')} by {handoff.initiated_by}")
        if handoff.accepted_at:
            print(f"Accepted:  {handoff.accepted_at.strftime('%Y-%m-%d %H:%M')} by {handoff.accepted_by}")
        if handoff.completed_at:
            print(f"Completed: {handoff.completed_at.strftime('%Y-%m-%d %H:%M')}")
        if handoff.deadline:
            print(f"Deadline:  {handoff.deadline.strftime('%Y-%m-%d %H:%M')}")
        print()
        
        if handoff.notes:
            print("─"*70)
            print("📝 ACTIVITY LOG")
            print("─"*70)
            for note in handoff.notes[-10:]:  # Last 10 notes
                print(f"  • {note}")
            print()
        
        print("="*70)
        print()


# Global instance
_handoff_manager = CrossTeamHandoffManager()


def get_handoff_manager() -> CrossTeamHandoffManager:
    """Get the global handoff manager instance"""
    return _handoff_manager


if __name__ == "__main__":
    # Demo: Simulate the Claude SDK analysis handoff
    manager = CrossTeamHandoffManager()
    
    # Core Team requests research from Analytical
    handoff_id = manager.initiate_handoff(
        handoff_type=HandoffType.REQUEST,
        from_team="Core Team",
        from_lead="Aleksander Nowak",
        to_team="Analytical Team",
        to_lead="Viktor Kovalenko",
        title="Analyze Claude Code SDK competitors",
        description="Need comprehensive competitive analysis of Claude SDK and alternatives. Focus on features, architecture, and recommendations for Destiny Framework.",
        initiated_by="Aleksander Nowak",
        context="User wants to understand if we should adopt features from competitors",
        deliverables=[
            "Verified sources document",
            "Feature comparison matrix",
            "Critical analysis report",
            "Technical recommendations"
        ],
        acceptance_criteria=[
            "All sources verified with URLs",
            "Feature matrix covers 10+ capabilities",
            "Recommendations are actionable",
            "Technical team validates findings"
        ],
        checklist_items=[
            "Research Claude SDK",
            "Identify real competitors",
            "Feature comparison",
            "Critical review",
            "Technical validation",
            "Final report"
        ]
    )
    
    print(f"✅ Handoff initiated: {handoff_id}\n")
    
    # Analytical accepts
    manager.accept_handoff(handoff_id, "Viktor Kovalenko")
    manager.start_work(handoff_id)
    
    # Progress updates
    manager.update_progress(handoff_id, "Elena starting OSINT research")
    manager.check_item(handoff_id, 0)  # Research Claude SDK
    
    manager.update_progress(handoff_id, "Identified Claude-Flow and Mastra as competitors")
    manager.check_item(handoff_id, 1)  # Identify competitors
    
    manager.add_artifact(
        handoff_id,
        "ELENA_OSINT_SOURCES_VERIFIED.md",
        "document",
        "docs/general/ELENA_OSINT_SOURCES_VERIFIED.md",
        "Verified sources with URLs and accessibility"
    )
    
    manager.update_progress(handoff_id, "Maya completing feature comparison matrix")
    manager.check_item(handoff_id, 2)  # Feature comparison
    
    manager.update_progress(handoff_id, "Damian performing critical review")
    manager.check_item(handoff_id, 3)  # Critical review
    
    manager.add_artifact(
        handoff_id,
        "ANALYTICAL_TEAM_RESEARCH_CLAUDE_SDK.md",
        "document",
        "docs/team/ANALYTICAL_TEAM_RESEARCH_CLAUDE_SDK.md",
        "Complete research report with recommendations"
    )
    
    # Handoff to Technical for validation
    manager.update_progress(handoff_id, "Handed off to Technical Team for validation")
    manager.check_item(handoff_id, 4)  # Technical validation
    
    manager.update_progress(handoff_id, "Technical validation complete - recommendations approved")
    manager.check_item(handoff_id, 5)  # Final report
    
    # Complete handoff
    manager.complete_handoff(
        handoff_id,
        artifacts=[
            "docs/general/ELENA_OSINT_SOURCES_VERIFIED.md",
            "docs/team/ANALYTICAL_TEAM_RESEARCH_CLAUDE_SDK.md",
            "docs/team/TECHNICAL_TEAM_ANALYSIS_FINAL.md"
        ]
    )
    
    # Print final handoff
    manager.print_handoff(handoff_id)
