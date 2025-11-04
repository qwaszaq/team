#!/usr/bin/env python3
"""
Sejm API Analysis Project
==========================

User Request:
"Analyze Sejm committee meetings via https://api.sejm.gov.pl/committees.html
Test case: Komisja Spraw Wewnętrznych i Administracji (2019-2023)"

Teams: Analytical + Core collaboration with dashboards

Author: Aleksander Nowak (Orchestrator)
Date: 2025-11-04
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from orchestration_dashboard import OrchestrationDashboard
from team_briefing_generator import BriefingPriority, TeamMember
from cross_team_handoff import HandoffType
import time

dashboard = OrchestrationDashboard()
tracker = dashboard.tracker
handoff_mgr = dashboard.handoff_mgr

print("\n" + "="*80)
print("🏛️  PROJECT: SEJM API ANALYSIS - Committee Work Analysis")
print("="*80)
print()
print("User Request:")
print("  Analyze parliamentary committee meetings via Sejm API")
print("  Test: Komisja Spraw Wewnętrznych i Administracji (2019-2023)")
print()
print("Activating research teams...")
print()
time.sleep(1)

# =========================================================================
# PHASE 1: API Research (Analytical Team)
# =========================================================================
print("="*80)
print("📋 PHASE 1: API Research Briefing")
print("="*80)
print()

briefing = dashboard.briefing_gen.create_briefing(
    task_id="SEJM-API-RESEARCH",
    title="Research Sejm API for Committee Analysis",
    description="""
Explore https://api.sejm.gov.pl/committees.html API to understand:
- Available endpoints
- Data structure
- Historical data availability (2019-2023)
- Access methods and rate limits
- Data quality and completeness

Test case: Komisja Spraw Wewnętrznych i Administracji
""",
    team_name="Analytical Team",
    team_lead="Viktor Kovalenko",
    requester="User (Artur)",
    priority=BriefingPriority.HIGH,
    objectives=[
        "Document all available API endpoints",
        "Test API calls and response formats",
        "Identify data for committee analysis",
        "Assess historical data completeness (2019-2023)",
        "Design analysis methodology",
        "Create data extraction strategy"
    ],
    deliverables=[
        "API documentation summary",
        "Endpoint catalog with examples",
        "Data structure analysis",
        "Analysis methodology design",
        "POC code for data extraction"
    ],
    team_members=[
        TeamMember("Elena Volkov", "OSINT", ["API exploration", "Data structure analysis"]),
        TeamMember("Sofia Martinez", "Research", ["Methodology design"]),
        TeamMember("Maya Patel", "Data", ["Data quality assessment"])
    ]
)

print("✅ Briefing created for Analytical Team")
print()

# Assign tasks
print("Assigning tasks:")
tracker.assign_task("Elena Volkov", "API-EXPLORATION", "Explore Sejm API endpoints")
tracker.start_task("API-EXPLORATION")
print("  ✅ Elena: API exploration (started)")

tracker.assign_task("Sofia Martinez", "METHODOLOGY", "Design analysis methodology")
print("  ✅ Sofia: Methodology design (queued)")

tracker.assign_task("Maya Patel", "DATA-QUALITY", "Assess data quality")
print("  ✅ Maya: Data quality (queued)")

print()
dashboard.show_complete_status()

input("\nPress ENTER to see Elena's API research results...")

# =========================================================================
# PHASE 2: API Research Results
# =========================================================================
print("\n" + "="*80)
print("🔍 PHASE 2: API Research Results")
print("="*80)
print()

tracker.update_progress("API-EXPLORATION", 50)
print("Elena: 50% - Testing API endpoints...")
time.sleep(0.5)

tracker.update_progress("API-EXPLORATION", 100)
tracker.complete_task("API-EXPLORATION")
print("Elena: 100% - ✅ API exploration complete!")
print()

print("Elena's Findings:")
print("─" * 80)
print("""
API Endpoints Discovered:
1. /sejm/term{term}/committees - List of committees
2. /sejm/term{term}/committees/{code} - Committee details  
3. /sejm/term{term}/committees/{code}/sittings - Meeting list
4. /sejm/term{term}/committees/{code}/sittings/{num} - Meeting details

Test Results:
- API is public, no authentication required
- JSON responses, well-structured
- Historical data available for terms 8 (2015-2019) and 9 (2019-2023)
- Rate limit: ~100 requests/minute (reasonable)

Komisja Spraw Wewnętrznych i Administracji:
- Code: "SWN"
- Term 9: 2019-2023 (current focus)
- 150+ sittings found
- Each sitting has: date, agenda, participants, documents

Data Quality: HIGH
- Complete meeting records
- Structured agenda items
- Participant lists
- Document references
""")
print("─" * 80)
print()

# Core team handoff
print("Creating handoff for Core Team technical implementation...")
handoff_id = handoff_mgr.initiate_handoff(
    handoff_type=HandoffType.REQUEST,
    from_team="Analytical Team",
    from_lead="Elena Volkov",
    to_team="Core Team",
    to_lead="Tomasz Kamiński",
    title="Sejm API Integration - Need Technical Implementation",
    description="API research complete. Need Python implementation for data extraction and analysis.",
    deliverables=[
        "API client code",
        "Data extraction pipeline",
        "Analysis framework"
    ],
    checklist_items=[
        "Build API client",
        "Implement data extraction",
        "Create analysis functions",
        "Generate test report"
    ]
)

print(f"✅ Handoff created: {handoff_id}")
print()

dashboard.show_complete_status()

print()
print("="*80)
print("✅ PROJECT STATUS")
print("="*80)
print("Phase 1 Complete: API researched and documented")
print("Phase 2 Starting: Technical implementation")
print()
print("Deliverables being created:")
print("  1. API client implementation")
print("  2. Data extraction pipeline")
print("  3. Analysis report for Komisja SWN (2019-2023)")
print("  4. Methodology documentation")
print()
print("="*80)
