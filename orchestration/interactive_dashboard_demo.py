#!/usr/bin/env python3
"""
Interactive Dashboard Demo
==========================

Shows all dashboard features in action!

Run this to see what you have!

Author: Aleksander Nowak
Date: 2025-11-04
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from orchestration_dashboard import OrchestrationDashboard
from team_briefing_generator import BriefingPriority, TeamMember
from cross_team_handoff import HandoffType
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(message="Press ENTER to continue..."):
    input(f"\n{message}")

def main():
    dashboard = OrchestrationDashboard()
    tracker = dashboard.tracker
    handoff_mgr = dashboard.handoff_mgr
    
    clear_screen()
    print("="*80)
    print("🎨 INTERACTIVE DASHBOARD DEMO")
    print("="*80)
    print()
    print("This demo shows all the transparency tools you have!")
    print()
    print("You'll see:")
    print("  1. Team Status Dashboard (real-time)")
    print("  2. Team Briefing Generator")
    print("  3. Cross-Team Handoff System")
    print("  4. Complete Orchestration Dashboard")
    print()
    pause()
    
    # =========================================================================
    # DEMO 1: Empty Dashboard
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 1: Dashboard (Empty State)")
    print("="*80)
    print()
    print("This is what dashboard looks like when no work is happening:")
    print()
    
    dashboard.show_complete_status()
    
    print("Notice:")
    print("  • Both teams at 0% capacity")
    print("  • All agents available")
    print("  • No active handoffs")
    print()
    pause()
    
    # =========================================================================
    # DEMO 2: Assigning Work
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 2: Assigning Work to Analytical Team")
    print("="*80)
    print()
    print("Simulating: User asks for research...")
    print()
    time.sleep(1)
    
    # Assign tasks
    print("Assigning tasks:")
    tracker.assign_task(
        "Elena Volkov",
        "DEMO-OSINT",
        "OSINT research on competitors"
    )
    tracker.start_task("DEMO-OSINT")
    print("  ✅ Elena Volkov: OSINT research (started)")
    time.sleep(0.5)
    
    tracker.assign_task(
        "Sofia Martinez",
        "DEMO-MARKET",
        "Market analysis"
    )
    print("  ✅ Sofia Martinez: Market analysis (queued)")
    time.sleep(0.5)
    
    tracker.assign_task(
        "Maya Patel",
        "DEMO-DATA",
        "Data analysis"
    )
    print("  ✅ Maya Patel: Data analysis (queued)")
    print()
    pause()
    
    # Show updated dashboard
    clear_screen()
    print("="*80)
    print("DEMO 2: Dashboard With Active Work")
    print("="*80)
    print()
    
    dashboard.show_complete_status()
    
    print("Notice the changes:")
    print("  • Analytical Team now at 50% capacity")
    print("  • 3 tasks active")
    print("  • Available agents: 3/6")
    print()
    pause()
    
    # =========================================================================
    # DEMO 3: Progress Tracking
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 3: Real-Time Progress Tracking")
    print("="*80)
    print()
    print("Watch as Elena makes progress on her task...")
    print()
    
    for progress in [25, 50, 75]:
        tracker.update_progress("DEMO-OSINT", progress)
        print(f"  Elena: {progress}% " + "█" * (progress // 10) + "░" * (10 - progress // 10))
        time.sleep(0.5)
    
    tracker.update_progress("DEMO-OSINT", 100)
    print(f"  Elena: 100% " + "█" * 10)
    print()
    time.sleep(0.5)
    
    tracker.complete_task("DEMO-OSINT")
    print("  ✅ Elena completed her task!")
    print()
    pause()
    
    # Show updated dashboard
    dashboard.show_complete_status()
    
    print("Notice:")
    print("  • Elena now available")
    print("  • Completed today: 1")
    print("  • Active tasks: 2")
    print()
    pause()
    
    # =========================================================================
    # DEMO 4: Team Briefing
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 4: Professional Team Briefing")
    print("="*80)
    print()
    print("This is what teams see when assigned work:")
    print()
    pause()
    
    briefing = dashboard.briefing_gen.create_briefing(
        task_id="DEMO-RESEARCH",
        title="Research AI Tools",
        description="Comprehensive analysis of AI development tools",
        team_name="Analytical Team",
        team_lead="Viktor Kovalenko",
        requester="User (Demo)",
        priority=BriefingPriority.HIGH,
        objectives=[
            "Identify top AI tools",
            "Analyze features",
            "Compare pricing"
        ],
        deliverables=[
            "Research report",
            "Comparison matrix"
        ],
        team_members=[
            TeamMember("Elena Volkov", "OSINT", ["Research", "Verify sources"]),
            TeamMember("Sofia Martinez", "Market", ["Competitive analysis"])
        ],
        success_criteria=[
            "All sources verified",
            "10+ tools compared"
        ]
    )
    
    dashboard.briefing_gen.print_briefing(briefing)
    
    print("Notice:")
    print("  • Clear objectives")
    print("  • Defined deliverables")
    print("  • Team composition")
    print("  • Success criteria")
    print()
    pause()
    
    # =========================================================================
    # DEMO 5: Cross-Team Handoff
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 5: Cross-Team Handoff")
    print("="*80)
    print()
    print("Simulating: Analytical Team delivers results to Core Team...")
    print()
    time.sleep(1)
    
    handoff_id = handoff_mgr.initiate_handoff(
        handoff_type=HandoffType.DELIVERY,
        from_team="Analytical Team",
        from_lead="Viktor Kovalenko",
        to_team="Core Team",
        to_lead="Maria Wiśniewska",
        title="Research Complete - Ready for Review",
        description="Analysis finished. Need technical validation.",
        deliverables=[
            "Research report",
            "Recommendations"
        ],
        checklist_items=[
            "Review findings",
            "Validate accuracy",
            "Approve recommendations"
        ]
    )
    
    print(f"✅ Handoff created: {handoff_id}")
    print()
    
    handoff_mgr.accept_handoff(handoff_id, "Maria Wiśniewska")
    print("✅ Maria Wiśniewska accepted the handoff")
    print()
    
    handoff_mgr.start_work(handoff_id)
    print("✅ Work started")
    print()
    pause()
    
    # Show handoff details
    handoff_mgr.print_handoff(handoff_id)
    
    print("Notice:")
    print("  • Clear handoff protocol")
    print("  • Deliverables tracked")
    print("  • Checklist for completion")
    print("  • Activity log maintained")
    print()
    pause()
    
    # Complete some checklist items
    clear_screen()
    print("="*80)
    print("DEMO 5: Handoff Progress")
    print("="*80)
    print()
    print("Simulating work progress...")
    print()
    
    for i in range(3):
        handoff_mgr.check_item(handoff_id, i)
        handoff_mgr.update_progress(handoff_id, f"Completed item {i+1}")
        print(f"  ✅ Checklist item {i+1} complete")
        time.sleep(0.5)
    
    print()
    handoff_mgr.complete_handoff(handoff_id)
    print("  ✅ Handoff completed!")
    print()
    pause()
    
    # Show final handoff
    handoff_mgr.print_handoff(handoff_id)
    pause()
    
    # =========================================================================
    # DEMO 6: Complete Dashboard
    # =========================================================================
    clear_screen()
    print("="*80)
    print("DEMO 6: Complete Dashboard View")
    print("="*80)
    print()
    print("Final state - everything in one view:")
    print()
    
    dashboard.show_complete_status()
    
    print()
    print("="*80)
    print("🎉 DEMO COMPLETE!")
    print("="*80)
    print()
    print("You've seen:")
    print("  ✅ Real-time team status tracking")
    print("  ✅ Progress bars and capacity metrics")
    print("  ✅ Professional team briefings")
    print("  ✅ Cross-team handoff protocol")
    print("  ✅ Complete orchestration dashboard")
    print()
    print("This is what you have available!")
    print()
    print("📚 Read more:")
    print("  - docs/orchestration/TRANSPARENCY_SYSTEM.md (complete guide)")
    print("  - docs/orchestration/QUICK_START.md (quick tutorial)")
    print("  - DASHBOARD_DEMO.md (this demo explained)")
    print()
    print("🚀 Next time you delegate work, you'll see this in action!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. You can run it again anytime!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
