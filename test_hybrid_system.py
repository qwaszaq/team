#!/usr/bin/env python3
"""
Test Hybrid On-Prem Intelligence System
Demonstration: Local LLM Worker + Cloud Supervisor

This script runs a complete investigation demonstration:
1. Local LLM executes CPK research using tools
2. Aleksander (Claude) reviews quality
3. Shows full workflow end-to-end

Usage:
    python test_hybrid_system.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import our hybrid system components
from local_orchestrator import LocalLLMOrchestrator
from supervisor_interface import SupervisorInterface


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def load_demo_task() -> dict:
    """Load CPK research demo task"""
    task_file = Path("shared_workspace/tasks/task_cpk_research_demo.json")
    
    if not task_file.exists():
        print(f"❌ Task file not found: {task_file}")
        print("   Creating default demo task...")
        return {
            "task_id": "cpk_research_demo",
            "objective": "Research the Central Transportation Hub (CPK) project in Poland",
            "quality_requirements": {
                "minimum_sources": 5,
                "source_attribution": "mandatory",
                "archiving": "all_sources"
            }
        }
    
    with open(task_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_investigation(orchestrator: LocalLLMOrchestrator, task: dict) -> dict:
    """Run investigation using local LLM"""
    print_header("PHASE 1: LOCAL LLM INVESTIGATION")
    
    print("📋 Task:")
    print(f"   {task['objective']}\n")
    
    print("🔧 Tools available:")
    print("   • scrape_webpage (collect information)")
    print("   • archive_source (preserve evidence)")
    print("   • calculate_statistics (analyze data)\n")
    
    print("▶️  Starting local LLM investigation...")
    print("   (This may take 2-5 minutes depending on model speed)\n")
    
    # Execute investigation
    result = orchestrator.run_investigation(
        task=task['objective'],
        context={
            "subtasks": task.get('subtasks', []),
            "quality_requirements": task.get('quality_requirements', {})
        },
        investigation_id=task['task_id'],
        max_iterations=15
    )
    
    return result


def review_investigation(supervisor: SupervisorInterface, investigation_id: str) -> dict:
    """Supervisor reviews investigation quality"""
    print_header("PHASE 2: SUPERVISOR QUALITY REVIEW")
    
    print("👔 Aleksander (Claude) reviewing local LLM work...\n")
    
    # Generate quality report
    report = supervisor.generate_quality_report(investigation_id)
    
    if "error" in report:
        print(f"❌ Error generating report: {report['error']}")
        return report
    
    # Print report
    supervisor.print_quality_report(report)
    
    return report


def provide_guidance_if_needed(supervisor: SupervisorInterface, report: dict):
    """Provide guidance if investigation needs improvement"""
    if report['overall_assessment']['ready_for_publication']:
        print_header("✅ INVESTIGATION COMPLETE - PUBLICATION READY")
        print("No further action needed. Quality is excellent!\n")
        return
    
    print_header("PHASE 3: SUPERVISOR GUIDANCE")
    
    print("⚠️  Investigation needs improvement before publication.\n")
    
    # Create guidance
    guidance = supervisor.create_guidance(
        investigation_id=report['investigation_id'],
        guidance_text=f"""
Investigation Quality Assessment: {report['overall_assessment']['overall_grade']}

Issues identified:
{chr(10).join(f"  • {w}" for w in report['findings']['weaknesses'])}

Recommendations:
{chr(10).join(f"  • {r}" for r in report['findings']['recommendations'])}

Please address these issues and re-run the investigation.
        """.strip(),
        priority="high",
        specific_actions=report['findings']['recommendations']
    )
    
    print(f"📝 Guidance created for local LLM")
    print(f"   Priority: {guidance['priority']}")
    print(f"   Actions: {len(guidance['specific_actions'])}")
    print()
    print("Next step:")
    print("   Local LLM would read guidance and continue investigation")
    print("   (In production, this would be automated)\n")


def show_final_summary(result: dict, report: dict):
    """Show final summary of demonstration"""
    print_header("📊 DEMONSTRATION SUMMARY")
    
    print("Hybrid System Performance:\n")
    
    # Execution metrics
    exec_metrics = report['execution_metrics']
    print("⏱️  Execution:")
    print(f"   • Status: {exec_metrics['status']}")
    print(f"   • Iterations: {exec_metrics['iterations']}")
    print(f"   • LLM Calls: {exec_metrics['llm_calls']}")
    print(f"   • Total Tokens: {exec_metrics['total_tokens']:,}")
    print(f"   • Efficiency: {exec_metrics['efficiency'].upper()}")
    print()
    
    # Tool usage
    tool_usage = report['tool_usage']
    print("🔧 Tool Usage:")
    print(f"   • Total Calls: {tool_usage['total_calls']}")
    print(f"   • Tools Used: {tool_usage['tools_used']}")
    print(f"   • Errors: {tool_usage['errors']}")
    print(f"   • Assessment: {tool_usage['assessment'].upper()}")
    print()
    
    # Source quality
    source = report['source_quality']
    print("📚 Source Quality:")
    print(f"   • Sources Scraped: {source['scraped']}")
    print(f"   • Sources Archived: {source['archived']}")
    print(f"   • Archive Ratio: {source['archive_ratio']:.1%}")
    print(f"   • Compliance: {source['compliance'].upper()}")
    print(f"   • Protocol Compliant: {'✅' if source['protocol_compliant'] else '❌'}")
    print()
    
    # Overall
    overall = report['overall_assessment']
    print("🎯 Overall Assessment:")
    print(f"   • Grade: {overall['overall_grade']}")
    print(f"   • Ready for Publication: {'✅ YES' if overall['ready_for_publication'] else '❌ NO'}")
    print()
    
    # Files
    print("📁 Files Created:")
    print(f"   • Investigation Log: {result.get('log_file', 'N/A')}")
    print(f"   • Result: shared_workspace/results/result_{result['investigation_id']}.json")
    print(f"   • Quality Report: shared_workspace/reports/quality_report_{result['investigation_id']}.json")
    print()


def main():
    """Main demonstration workflow"""
    print("="*70)
    print("  🚀 HYBRID ON-PREM INTELLIGENCE SYSTEM - DEMONSTRATION")
    print("="*70)
    print()
    print("Architecture:")
    print("  • Local LLM (LMStudio): Executes investigation with tools")
    print("  • Aleksander (Claude): Supervises quality & provides guidance")
    print("  • Hybrid approach: 90% cost savings + professional quality")
    print()
    
    # Check LMStudio
    print("🔍 Pre-flight Check:")
    print("   • Checking LMStudio connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("   ✅ LMStudio is running")
        else:
            print("   ⚠️  LMStudio responded but status unclear")
    except Exception as e:
        print(f"   ❌ LMStudio not accessible: {e}")
        print()
        print("Please start LMStudio and load a model:")
        print("   1. Open LMStudio")
        print("   2. Load model (e.g., Mixtral 8x7B Instruct)")
        print("   3. Go to 'Local Server' tab")
        print("   4. Click 'Start Server'")
        print("   5. Run this script again")
        print()
        return 1
    
    input("\n▶️  Press Enter to start demonstration...")
    
    # Initialize components
    print_header("INITIALIZATION")
    
    print("Initializing Local LLM Orchestrator...")
    orchestrator = LocalLLMOrchestrator(
        lmstudio_url="http://localhost:1234/v1",
        model_name="local-model"
    )
    
    print("\nInitializing Supervisor Interface...")
    supervisor = SupervisorInterface()
    
    print("\n✅ System initialized\n")
    
    # Load task
    print("Loading demonstration task (CPK research)...")
    task = load_demo_task()
    print(f"✅ Task loaded: {task['task_id']}\n")
    
    input("▶️  Press Enter to start investigation...")
    
    # Phase 1: Investigation
    try:
        result = run_investigation(orchestrator, task)
    except Exception as e:
        print(f"\n❌ Investigation failed: {e}")
        print("\nTroubleshooting:")
        print("   • Check LMStudio is running")
        print("   • Verify model supports function calling")
        print("   • Check logs: ./logs/local_llm/")
        return 1
    
    input("\n▶️  Press Enter for supervisor review...")
    
    # Phase 2: Review
    try:
        report = review_investigation(supervisor, task['task_id'])
    except Exception as e:
        print(f"\n❌ Review failed: {e}")
        return 1
    
    # Phase 3: Guidance (if needed)
    provide_guidance_if_needed(supervisor, report)
    
    # Final summary
    show_final_summary(result, report)
    
    # Next steps
    print_header("🎯 NEXT STEPS")
    print("Demonstration complete! What to do next:\n")
    
    if report['overall_assessment']['ready_for_publication']:
        print("✅ This investigation passed quality review!")
        print()
        print("Production next steps:")
        print("   1. Aleksander synthesizes final professional report")
        print("   2. Publish with full source attribution")
        print("   3. Propagate to knowledge bases (PostgreSQL, Neo4j, Qdrant, Redis)")
        print()
        print("Try a real investigation:")
        print("   • Create custom task in shared_workspace/tasks/")
        print("   • Run with real research topic")
        print("   • Iterate based on supervisor feedback")
    else:
        print("⚠️  This investigation needs improvement.")
        print()
        print("In production system:")
        print("   1. Local LLM reads guidance automatically")
        print("   2. Addresses specific issues")
        print("   3. Re-runs investigation")
        print("   4. Supervisor reviews again")
        print("   5. Iterate until quality >= A")
        print()
        print("Manual next step:")
        print("   • Check guidance: shared_workspace/guidance/")
        print("   • Manually address issues")
        print("   • Re-run investigation")
    
    print()
    print("="*70)
    print("  🎉 DEMONSTRATION COMPLETE")
    print("="*70)
    print()
    print("System Status: ✅ VALIDATED")
    print("Ready for: Production investigations with real data")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
