# 🚀 Quick Start: Transparency System

**5-minute guide to using the new orchestration tools**

---

## ⚡ Instant Demo

```bash
cd /Users/artur/coursor-agents-destiny-folder/orchestration
python3 test_transparency_integration.py
```

**This runs a complete simulation** showing:
- User request
- Team briefing
- Task assignment
- Progress tracking
- Cross-team handoff
- Final delivery

**Takes ~10 seconds, shows everything! 🎯**

---

## 🎯 Common Use Cases

### **Use Case 1: "I need research from Analytical Team"**

```python
from orchestration.orchestration_dashboard import OrchestrationDashboard
from orchestration.team_briefing_generator import BriefingPriority, TeamMember

dashboard = OrchestrationDashboard()

# 1. Check if team is available
dashboard.show_team_status()
# See: "Analytical Team: 4/6 available"

# 2. Create briefing
briefing = dashboard.briefing_gen.create_briefing(
    task_id="RESEARCH-XYZ",
    title="Research competitor product X",
    description="Need complete competitive analysis...",
    team_name="Analytical Team",
    team_lead="Viktor Kovalenko",
    requester="Artur",
    priority=BriefingPriority.HIGH,
    objectives=["Research X", "Compare with our product"],
    deliverables=["Research report", "Recommendations"],
    team_members=[
        TeamMember("Elena Volkov", "OSINT", ["Web research"]),
        TeamMember("Sofia Martinez", "Market", ["Competitive analysis"])
    ]
)

# 3. Print briefing (team sees this)
dashboard.briefing_gen.print_briefing(briefing)

# 4. Assign specific tasks
dashboard.tracker.assign_task("Elena Volkov", "OSINT-XYZ", "OSINT on product X")
dashboard.tracker.assign_task("Sofia Martinez", "MARKET-XYZ", "Market analysis")

# 5. Start work
dashboard.tracker.start_task("OSINT-XYZ")

# 6. Monitor progress anytime
dashboard.show_complete_status()
```

---

### **Use Case 2: "Show me what everyone is doing"**

```python
from orchestration.orchestration_dashboard import OrchestrationDashboard

dashboard = OrchestrationDashboard()

# One command shows everything
dashboard.show_complete_status()
```

**Output:**
```
🎯 DESTINY ORCHESTRATION DASHBOARD
═══════════════════════════════════

Core Team:
  Capacity: ███░░░░░░░ 30%
  Working:
    • Tomasz (2 tasks)
    • Anna (1 task)

Analytical Team:
  Capacity: ████████░░ 80%
  Working:
    • Elena (1 task) - OSINT research (65%)
    • Sofia (2 tasks) - Market analysis (40%)

Active Handoffs:
  🔄 HANDOFF-001: Analytical → Core
     Title: Research ready for validation
     Status: in_progress
```

---

### **Use Case 3: "Track handoff between teams"**

```python
from orchestration.orchestration_dashboard import OrchestrationDashboard
from orchestration.cross_team_handoff import HandoffType

dashboard = OrchestrationDashboard()

# Analytical Team delivers results
handoff_id = dashboard.handoff_mgr.initiate_handoff(
    handoff_type=HandoffType.DELIVERY,
    from_team="Analytical Team",
    from_lead="Viktor Kovalenko",
    to_team="Core Team",
    to_lead="Aleksander Nowak",
    title="Research Complete - Ready for Technical Review",
    description="We've completed the research. Please validate.",
    deliverables=["Research report", "Feature comparison"],
    checklist_items=[
        "Review findings",
        "Validate accuracy",
        "Assess feasibility"
    ]
)

print(f"✅ Handoff created: {handoff_id}")

# You accept
dashboard.handoff_mgr.accept_handoff(handoff_id, "Aleksander Nowak")

# Assign to Tomasz for validation
dashboard.tracker.assign_task("Tomasz Kamiński", "VALIDATE-001", "Validate research")

# Track progress
dashboard.handoff_mgr.update_progress(handoff_id, "Tomasz reviewing...")
dashboard.handoff_mgr.check_item(handoff_id, 0)  # Review done

# Complete
dashboard.handoff_mgr.complete_handoff(handoff_id)

# View complete handoff
dashboard.handoff_mgr.print_handoff(handoff_id)
```

---

## 🎨 Visual Dashboard Output

The dashboard shows beautiful formatted output:

```
======================================================================
🎯 DESTINY TEAM - REAL-TIME STATUS DASHBOARD
======================================================================

──────────────────────────────────────────────────────────────────────
👥 Core Team
──────────────────────────────────────────────────────────────────────
   Active Tasks: 3 | Completed Today: 5
   Capacity: 40% | Available: 4/7 agents

   🟡 Tomasz Kamiński
      Senior Developer | Workload: 2 tasks
      ├─ [in_progress] Implement feature X
      │  ████████░░ 80%
      └─ [queued] Code review for PR #123

   🟢 Anna Lewandowska
      QA Engineer | Workload: 0 tasks
      └─ Available for work

──────────────────────────────────────────────────────────────────────
👥 Analytical Team
──────────────────────────────────────────────────────────────────────
   Active Tasks: 2 | Completed Today: 3
   Capacity: 33% | Available: 4/6 agents

   🟡 Elena Volkov
      OSINT Specialist | Workload: 1 tasks
      ├─ [in_progress] OSINT research
      │  ██████░░░░ 65%
```

---

## 💡 Pro Tips

### **1. Run Dashboard in Background Terminal**
```bash
# Terminal 1: Work here
cd /Users/artur/coursor-agents-destiny-folder

# Terminal 2: Monitor dashboard
cd orchestration
watch -n 5 python3 orchestration_dashboard.py
# Updates every 5 seconds!
```

### **2. Save Briefings for Documentation**
```python
briefing = dashboard.briefing_gen.create_briefing(...)
markdown = dashboard.briefing_gen.to_markdown(briefing)

# Save to docs/ → Helena will auto-index!
with open(f"docs/briefings/BRIEF-{task_id}.md", "w") as f:
    f.write(markdown)
```

### **3. Export Status as JSON**
```python
status = dashboard.tracker.get_all_status()
# Returns JSON - can save to DB or send via API
```

---

## 📚 Next Steps

1. **Read full documentation:** `docs/orchestration/TRANSPARENCY_SYSTEM.md`
2. **Run the demo:** `python3 test_transparency_integration.py`
3. **Try it yourself:** Start using in your orchestration!

---

**Status:** ✅ Ready to use  
**Questions?** Check TRANSPARENCY_SYSTEM.md for details
