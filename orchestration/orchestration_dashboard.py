"""
Orchestration Dashboard
=======================

Unified dashboard that integrates:
- Team Status Tracker
- Team Briefing Generator
- Cross-Team Handoff Manager

Provides single interface for orchestrator to see everything happening.

Author: Aleksander Nowak (Orchestrator)
Date: 2025-11-04
Sprint: Transparency Tools + Cross-Team Improvements
"""

from datetime import datetime
from typing import Optional, List
from team_status_tracker import get_tracker, AgentStatus, TaskStatus
from team_briefing_generator import TeamBriefingGenerator, BriefingPriority, TeamMember
from cross_team_handoff import get_handoff_manager, HandoffType, HandoffStatus


class OrchestrationDashboard:
    """
    Unified dashboard for orchestration.
    
    Usage:
        dashboard = OrchestrationDashboard()
        
        # View everything
        dashboard.show_complete_status()
        
        # Or specific views
        dashboard.show_team_status()
        dashboard.show_active_handoffs()
        dashboard.show_recent_activity()
    """
    
    def __init__(self):
        self.tracker = get_tracker()
        self.briefing_gen = TeamBriefingGenerator()
        self.handoff_mgr = get_handoff_manager()
    
    def show_complete_status(self):
        """Show complete system status"""
        print("\n" + "="*80)
        print("🎯 DESTINY ORCHESTRATION DASHBOARD - COMPLETE STATUS")
        print("="*80)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Teams Overview
        self._show_teams_overview()
        
        # Active Handoffs
        self._show_active_handoffs_summary()
        
        # Recent Activity
        self._show_recent_activity()
        
        print("="*80)
        print()
    
    def _show_teams_overview(self):
        """Show overview of both teams"""
        print("─"*80)
        print("👥 TEAMS OVERVIEW")
        print("─"*80)
        
        for team_name in ["Core Team", "Analytical Team"]:
            team_status = self.tracker.get_team_status(team_name)
            
            capacity = team_status['team_capacity'] * 100
            capacity_bar = "█" * int(capacity / 10) + "░" * (10 - int(capacity / 10))
            
            print(f"\n{team_name}:")
            print(f"  Capacity: {capacity_bar} {capacity:.0f}%")
            print(f"  Active: {team_status['active_tasks']} tasks | Completed today: {team_status['completed_today']}")
            print(f"  Available: {team_status['available_agents']}/{len(team_status['agents'])} agents")
            
            # Show busy agents
            busy = [a for a in team_status['agents'] if a['workload'] > 0]
            if busy:
                print(f"  Working:")
                for agent in busy[:3]:  # Show top 3
                    print(f"    • {agent['name']} ({agent['workload']} tasks)")
        
        print()
    
    def _show_active_handoffs_summary(self):
        """Show active handoffs summary"""
        print("─"*80)
        print("🔄 ACTIVE HANDOFFS")
        print("─"*80)
        
        active_handoffs = self.handoff_mgr.get_active_handoffs()
        
        if not active_handoffs:
            print("  No active handoffs")
        else:
            for handoff in active_handoffs:
                status_emoji = {
                    HandoffStatus.INITIATED: "🆕",
                    HandoffStatus.ACCEPTED: "✅",
                    HandoffStatus.IN_PROGRESS: "🔄",
                }
                emoji = status_emoji.get(handoff.status, "")
                
                print(f"\n  {emoji} {handoff.handoff_id}")
                print(f"     {handoff.from_team} → {handoff.to_team}")
                print(f"     {handoff.title}")
                print(f"     Status: {handoff.status.value}")
                
                if handoff.checklist:
                    pct = handoff.checklist.completion_percentage
                    print(f"     Progress: {pct}%")
        
        print()
    
    def _show_recent_activity(self):
        """Show recent activity across system"""
        print("─"*80)
        print("📊 RECENT ACTIVITY (Last 24h)")
        print("─"*80)
        
        # Get stats
        all_status = self.tracker.get_all_status()
        
        total_completed = sum(
            team['completed_today'] 
            for team in all_status['teams'].values()
        )
        
        total_active = sum(
            team['active_tasks'] 
            for team in all_status['teams'].values()
        )
        
        print(f"  Tasks completed today: {total_completed}")
        print(f"  Tasks currently active: {total_active}")
        print(f"  Active handoffs: {len(self.handoff_mgr.get_active_handoffs())}")
        print()
    
    def show_team_status(self, team_name: Optional[str] = None):
        """Show detailed team status"""
        if team_name:
            self.tracker.print_status_dashboard()
        else:
            # Show both teams
            self.tracker.print_status_dashboard()
    
    def show_active_handoffs(self):
        """Show all active handoffs"""
        print("\n" + "="*80)
        print("🔄 ACTIVE HANDOFFS - DETAILED VIEW")
        print("="*80)
        print()
        
        active = self.handoff_mgr.get_active_handoffs()
        
        if not active:
            print("No active handoffs\n")
            return
        
        for handoff in active:
            self.handoff_mgr.print_handoff(handoff.handoff_id)
    
    def create_team_briefing_for_handoff(self, handoff_id: str) -> str:
        """Generate team briefing from handoff"""
        handoff = self.handoff_mgr.get_handoff(handoff_id)
        
        # Convert handoff to briefing
        briefing = self.briefing_gen.create_briefing(
            task_id=handoff.handoff_id,
            title=handoff.title,
            description=handoff.description,
            team_name=handoff.to_team,
            team_lead=handoff.to_lead,
            requester=f"{handoff.from_team} ({handoff.from_lead})",
            priority=BriefingPriority.HIGH,
            objectives=["Process handoff request", "Deliver specified artifacts"],
            deliverables=handoff.deliverables,
            background=handoff.context,
            success_criteria=handoff.acceptance_criteria,
            deadline=handoff.deadline
        )
        
        return self.briefing_gen.to_markdown(briefing)
    
    def show_agent_workload(self, agent_name: Optional[str] = None):
        """Show agent workload"""
        print("\n" + "="*80)
        print("👤 AGENT WORKLOAD")
        print("="*80)
        print()
        
        if agent_name:
            # Show specific agent
            status = self.tracker.get_agent_status(agent_name)
            self._print_agent_detail(status)
        else:
            # Show all agents sorted by workload
            all_status = self.tracker.get_all_status()
            all_agents = []
            for team in all_status['teams'].values():
                all_agents.extend(team['agents'])
            
            # Sort by workload
            all_agents.sort(key=lambda a: a['workload'], reverse=True)
            
            for agent in all_agents:
                workload_emoji = "🔴" if agent['workload'] > 2 else "🟡" if agent['workload'] > 0 else "🟢"
                print(f"{workload_emoji} {agent['name']}")
                print(f"   {agent['role']} | Workload: {agent['workload']} tasks")
                
                if agent['current_tasks']:
                    for task in agent['current_tasks']:
                        print(f"   ├─ {task['title']} ({task['progress_pct']}%)")
                print()
        
        print("="*80)
        print()
    
    def _print_agent_detail(self, agent_status: dict):
        """Print detailed agent status"""
        print(f"Name: {agent_status['name']}")
        print(f"Role: {agent_status['role']}")
        print(f"Team: {agent_status['team']}")
        print(f"Status: {agent_status['status']}")
        print(f"Workload: {agent_status['workload']} active tasks")
        print(f"Completed today: {agent_status['completed_today']}")
        print()
        
        if agent_status['current_tasks']:
            print("Current Tasks:")
            for task in agent_status['current_tasks']:
                print(f"  • {task['title']}")
                print(f"    Status: {task['status']} | Progress: {task['progress_pct']}%")
                if task['description']:
                    print(f"    {task['description']}")
                print()
    
    def get_recommendations(self) -> List[str]:
        """Get orchestration recommendations based on current state"""
        recommendations = []
        
        all_status = self.tracker.get_all_status()
        
        for team_name, team in all_status['teams'].items():
            # Check team capacity
            if team['team_capacity'] > 0.8:
                recommendations.append(
                    f"⚠️  {team_name} at {team['team_capacity']*100:.0f}% capacity - consider load balancing"
                )
            
            # Check for available agents in overloaded team
            overloaded = [a for a in team['agents'] if a['workload'] > 3]
            available = [a for a in team['agents'] if a['workload'] == 0]
            
            if overloaded and available:
                recommendations.append(
                    f"💡 {team_name}: {len(overloaded)} overloaded agents, {len(available)} available - redistribute?"
                )
        
        # Check for stale handoffs
        active_handoffs = self.handoff_mgr.get_active_handoffs()
        for handoff in active_handoffs:
            if handoff.status == HandoffStatus.INITIATED:
                hours_since = (datetime.now() - handoff.initiated_at).total_seconds() / 3600
                if hours_since > 24:
                    recommendations.append(
                        f"⏰ Handoff {handoff.handoff_id} not accepted for {hours_since:.0f}h - follow up?"
                    )
        
        return recommendations
    
    def show_recommendations(self):
        """Show orchestration recommendations"""
        print("\n" + "="*80)
        print("💡 ORCHESTRATION RECOMMENDATIONS")
        print("="*80)
        print()
        
        recommendations = self.get_recommendations()
        
        if not recommendations:
            print("✅ No recommendations - system running smoothly")
        else:
            for rec in recommendations:
                print(f"  {rec}")
        
        print()
        print("="*80)
        print()


if __name__ == "__main__":
    # Demo: Create orchestration dashboard
    dashboard = OrchestrationDashboard()
    
    # Add some demo data
    tracker = dashboard.tracker
    
    # Assign tasks to Core Team
    tracker.assign_task(
        "Tomasz Kamiński",
        "CORE-001",
        "Implement transparency dashboard"
    )
    tracker.start_task("CORE-001")
    tracker.update_progress("CORE-001", 65)
    
    tracker.assign_task(
        "Anna Lewandowska",
        "CORE-002",
        "Test new handoff protocol"
    )
    tracker.start_task("CORE-002")
    tracker.update_progress("CORE-002", 30)
    
    # Assign tasks to Analytical Team
    tracker.assign_task(
        "Elena Volkov",
        "ANAL-001",
        "OSINT research on competitors"
    )
    tracker.start_task("ANAL-001")
    tracker.update_progress("ANAL-001", 80)
    
    # Create a handoff
    handoff_mgr = dashboard.handoff_mgr
    handoff_id = handoff_mgr.initiate_handoff(
        handoff_type=HandoffType.REQUEST,
        from_team="Core Team",
        from_lead="Aleksander Nowak",
        to_team="Analytical Team",
        to_lead="Viktor Kovalenko",
        title="Market research on SDK competitors",
        description="Need competitive analysis of multiagent SDKs",
        deliverables=["Research report", "Feature comparison"],
        checklist_items=["Research", "Analysis", "Report"]
    )
    handoff_mgr.accept_handoff(handoff_id, "Viktor Kovalenko")
    handoff_mgr.start_work(handoff_id)
    handoff_mgr.check_item(handoff_id, 0)
    handoff_mgr.update_progress(handoff_id, "Research 50% complete")
    
    # Show complete dashboard
    dashboard.show_complete_status()
    
    # Show recommendations
    dashboard.show_recommendations()
