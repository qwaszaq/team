"""
4-Agent Demo: Proving Real Multi-Agent Specialization

This demo shows 4 specialized agents handling the SAME task DIFFERENTLY.

Agents:
- Tomasz (Developer)
- Anna (QA Engineer)
- Magdalena (UX Designer)
- Michał (Architect)

Usage:
    python3 test_4_agent_demo.py

Expected: All 10 assertions pass, proving 4-way differentiation.
"""

import uuid
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.specialized.tomasz_agent import TomaszAgent
from agents.specialized.anna_agent import AnnaAgent
from agents.specialized.magdalena_agent import MagdalenaAgent
from agents.specialized.michal_agent import MichalAgent
from agents.task_models import Task, TaskStatus


def main():
    print("\n" + "="*80)
    print("🎬 4-AGENT DEMO: Real Multi-Agent Specialization")
    print("="*80)
    print()
    print("Demonstrating 4 specialized agents handling the SAME task DIFFERENTLY.")
    print()
    
    # Initialize all 4 agents
    print("━" * 80)
    print("📋 INITIALIZING 4 SPECIALIZED AGENTS")
    print("━" * 80)
    
    tomasz = TomaszAgent()
    anna = AnnaAgent()
    magdalena = MagdalenaAgent()
    michal = MichalAgent()
    
    print(f"✅ {tomasz.name} ({tomasz.role})")
    print(f"✅ {anna.name} ({anna.role})")
    print(f"✅ {magdalena.name} ({magdalena.role})")
    print(f"✅ {michal.name} ({michal.role})")
    print()
    
    # Create THE SAME task for all 4 agents
    print("━" * 80)
    print("📝 CREATING IDENTICAL TASK FOR ALL 4 AGENTS")
    print("━" * 80)
    
    task_description = "Build and design a user dashboard for tracking project metrics and team performance"
    
    task_tomasz = Task(
        task_id=uuid.uuid4(),
        title="Project metrics dashboard",
        description=task_description,
        assigned_to=tomasz.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    task_anna = Task(
        task_id=uuid.uuid4(),
        title="Project metrics dashboard",
        description=task_description,
        assigned_to=anna.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    task_magdalena = Task(
        task_id=uuid.uuid4(),
        title="Project metrics dashboard",
        description=task_description,
        assigned_to=magdalena.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    task_michal = Task(
        task_id=uuid.uuid4(),
        title="Project metrics dashboard",
        description=task_description,
        assigned_to=michal.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    print(f"Task: '{task_tomasz.title}'")
    print(f"Description: '{task_description}'")
    print()
    print("⚠️  NOTE: All 4 tasks are IDENTICAL - same title, same description!")
    print()
    
    # Process with each agent
    print("━" * 80)
    print("👨‍💻 TOMASZ (DEVELOPER) PROCESSES THE TASK")
    print("━" * 80)
    print()
    
    result_tomasz = tomasz.process_task(task_tomasz)
    
    print(f"Status: {result_tomasz.status.value}")
    print(f"Output type: {result_tomasz.output.get('type')}")
    print()
    print("Tomasz's approach (first 300 chars):")
    print("-" * 80)
    print(result_tomasz.thoughts[:300] + "...")
    print("-" * 80)
    print()
    
    print("━" * 80)
    print("👩‍💼 ANNA (QA ENGINEER) PROCESSES THE SAME TASK")
    print("━" * 80)
    print()
    
    result_anna = anna.process_task(task_anna)
    
    print(f"Status: {result_anna.status.value}")
    print(f"Output type: {result_anna.output.get('type')}")
    print()
    print("Anna's approach (first 300 chars):")
    print("-" * 80)
    print(result_anna.thoughts[:300] + "...")
    print("-" * 80)
    print()
    
    print("━" * 80)
    print("🎨 MAGDALENA (UX DESIGNER) PROCESSES THE SAME TASK")
    print("━" * 80)
    print()
    
    result_magdalena = magdalena.process_task(task_magdalena)
    
    print(f"Status: {result_magdalena.status.value}")
    print(f"Output type: {result_magdalena.output.get('type')}")
    print()
    print("Magdalena's approach (first 300 chars):")
    print("-" * 80)
    print(result_magdalena.thoughts[:300] + "...")
    print("-" * 80)
    print()
    
    print("━" * 80)
    print("🏗️ MICHAŁ (ARCHITECT) PROCESSES THE SAME TASK")
    print("━" * 80)
    print()
    
    result_michal = michal.process_task(task_michal)
    
    print(f"Status: {result_michal.status.value}")
    print(f"Output type: {result_michal.output.get('type')}")
    print()
    print("Michał's approach (first 300 chars):")
    print("-" * 80)
    print(result_michal.thoughts[:300] + "...")
    print("-" * 80)
    print()
    
    # COMPREHENSIVE VERIFICATION
    print("━" * 80)
    print("🔍 COMPREHENSIVE VERIFICATION: ARE THEY ALL DIFFERENT?")
    print("━" * 80)
    print()
    
    # Assertion 1: All completed
    print("✓ Assertion 1: All agents completed successfully...")
    assert result_tomasz.status == TaskStatus.DONE, "Tomasz failed!"
    assert result_anna.status == TaskStatus.DONE, "Anna failed!"
    assert result_magdalena.status == TaskStatus.DONE, "Magdalena failed!"
    assert result_michal.status == TaskStatus.DONE, "Michał failed!"
    print("  ✅ PASS: All 4 agents completed")
    print()
    
    # Assertion 2: Different output types
    print("✓ Assertion 2: All output types are different...")
    type_tomasz = result_tomasz.output.get('type')
    type_anna = result_anna.output.get('type')
    type_magdalena = result_magdalena.output.get('type')
    type_michal = result_michal.output.get('type')
    
    print(f"  Tomasz: '{type_tomasz}'")
    print(f"  Anna: '{type_anna}'")
    print(f"  Magdalena: '{type_magdalena}'")
    print(f"  Michał: '{type_michal}'")
    
    all_types = [type_tomasz, type_anna, type_magdalena, type_michal]
    assert len(set(all_types)) == 4, f"Types not all different! {all_types}"
    print("  ✅ PASS: All 4 output types are unique")
    print()
    
    # Assertion 3: Tomasz uses developer terms
    print("✓ Assertion 3: Tomasz uses developer terminology...")
    tomasz_lower = result_tomasz.thoughts.lower()
    dev_terms = ["implement", "code", "python", "api", "function", "class"]
    found_dev = [term for term in dev_terms if term in tomasz_lower]
    print(f"  Found developer terms: {found_dev}")
    assert len(found_dev) >= 2, f"Tomasz should use dev terms! Found: {found_dev}"
    print(f"  ✅ PASS: Found {len(found_dev)} developer terms")
    print()
    
    # Assertion 4: Anna uses QA terms
    print("✓ Assertion 4: Anna uses QA terminology...")
    anna_lower = result_anna.thoughts.lower()
    qa_terms = ["test", "qa", "quality", "verify", "coverage", "edge case", "bug"]
    found_qa = [term for term in qa_terms if term in anna_lower]
    print(f"  Found QA terms: {found_qa}")
    assert len(found_qa) >= 2, f"Anna should use QA terms! Found: {found_qa}"
    print(f"  ✅ PASS: Found {len(found_qa)} QA terms")
    print()
    
    # Assertion 5: Magdalena uses UX terms
    print("✓ Assertion 5: Magdalena uses UX terminology...")
    magdalena_lower = result_magdalena.thoughts.lower()
    ux_terms = ["ux", "user", "wireframe", "design", "persona", "journey", "interface"]
    found_ux = [term for term in ux_terms if term in magdalena_lower]
    print(f"  Found UX terms: {found_ux}")
    assert len(found_ux) >= 3, f"Magdalena should use UX terms! Found: {found_ux}"
    print(f"  ✅ PASS: Found {len(found_ux)} UX terms")
    print()
    
    # Assertion 6: Michał uses architecture terms
    print("✓ Assertion 6: Michał uses architecture terminology...")
    michal_lower = result_michal.thoughts.lower()
    arch_terms = ["architecture", "component", "scalability", "pattern", "system", "layer"]
    found_arch = [term for term in arch_terms if term in michal_lower]
    print(f"  Found architecture terms: {found_arch}")
    assert len(found_arch) >= 3, f"Michał should use arch terms! Found: {found_arch}"
    print(f"  ✅ PASS: Found {len(found_arch)} architecture terms")
    print()
    
    # Assertion 7: Reasoning is different (pairwise)
    print("✓ Assertion 7: Reasoning is substantively different...")
    
    def calculate_similarity(text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        common = len(words1 & words2)
        total = len(words1 | words2)
        return (common / total * 100) if total > 0 else 0
    
    sim_t_a = calculate_similarity(result_tomasz.thoughts, result_anna.thoughts)
    sim_t_m = calculate_similarity(result_tomasz.thoughts, result_magdalena.thoughts)
    sim_t_mi = calculate_similarity(result_tomasz.thoughts, result_michal.thoughts)
    sim_a_m = calculate_similarity(result_anna.thoughts, result_magdalena.thoughts)
    sim_a_mi = calculate_similarity(result_anna.thoughts, result_michal.thoughts)
    sim_m_mi = calculate_similarity(result_magdalena.thoughts, result_michal.thoughts)
    
    print(f"  Tomasz ↔ Anna: {sim_t_a:.1f}% similarity")
    print(f"  Tomasz ↔ Magdalena: {sim_t_m:.1f}% similarity")
    print(f"  Tomasz ↔ Michał: {sim_t_mi:.1f}% similarity")
    print(f"  Anna ↔ Magdalena: {sim_a_m:.1f}% similarity")
    print(f"  Anna ↔ Michał: {sim_a_mi:.1f}% similarity")
    print(f"  Magdalena ↔ Michał: {sim_m_mi:.1f}% similarity")
    
    avg_similarity = (sim_t_a + sim_t_m + sim_t_mi + sim_a_m + sim_a_mi + sim_m_mi) / 6
    print(f"  Average similarity: {avg_similarity:.1f}%")
    
    assert avg_similarity < 50, f"Too similar ({avg_similarity:.1f}%)! Might be copy-paste!"
    print(f"  ✅ PASS: Low similarity ({avg_similarity:.1f}%) - genuinely different!")
    print()
    
    # Assertion 8: Different artifacts
    print("✓ Assertion 8: Different artifacts produced...")
    artifacts_tomasz = set(result_tomasz.artifacts)
    artifacts_anna = set(result_anna.artifacts)
    artifacts_magdalena = set(result_magdalena.artifacts)
    artifacts_michal = set(result_michal.artifacts)
    
    print(f"  Tomasz: {artifacts_tomasz}")
    print(f"  Anna: {artifacts_anna}")
    print(f"  Magdalena: {artifacts_magdalena}")
    print(f"  Michał: {artifacts_michal}")
    
    # Check that artifacts are mostly different
    all_artifacts = artifacts_tomasz | artifacts_anna | artifacts_magdalena | artifacts_michal
    unique_count = len(all_artifacts)
    total_count = len(artifacts_tomasz) + len(artifacts_anna) + len(artifacts_magdalena) + len(artifacts_michal)
    uniqueness = (unique_count / total_count * 100) if total_count > 0 else 0
    
    print(f"  Uniqueness: {uniqueness:.1f}% ({unique_count}/{total_count} unique)")
    assert uniqueness > 60, f"Artifacts too similar! {uniqueness:.1f}% unique"
    print(f"  ✅ PASS: {uniqueness:.1f}% unique artifacts")
    print()
    
    # Assertion 9: Different next steps
    print("✓ Assertion 9: Different next steps recommended...")
    next_tomasz = result_tomasz.next_steps.lower() if result_tomasz.next_steps else ""
    next_anna = result_anna.next_steps.lower() if result_anna.next_steps else ""
    next_magdalena = result_magdalena.next_steps.lower() if result_magdalena.next_steps else ""
    next_michal = result_michal.next_steps.lower() if result_michal.next_steps else ""
    
    print(f"  Tomasz: '{result_tomasz.next_steps[:60]}...'")
    print(f"  Anna: '{result_anna.next_steps[:60]}...'")
    print(f"  Magdalena: '{result_magdalena.next_steps[:60]}...'")
    print(f"  Michał: '{result_michal.next_steps[:60]}...'")
    
    # All should have next steps and they should be different
    assert len(next_tomasz) > 0, "Tomasz missing next steps"
    assert len(next_anna) > 0, "Anna missing next steps"
    assert len(next_magdalena) > 0, "Magdalena missing next steps"
    assert len(next_michal) > 0, "Michał missing next steps"
    
    all_next_steps = [next_tomasz, next_anna, next_magdalena, next_michal]
    assert len(set(all_next_steps)) >= 3, "Next steps too similar!"
    print("  ✅ PASS: Different next steps for each agent")
    print()
    
    # Assertion 10: Role-specific focus
    print("✓ Assertion 10: Each agent focuses on their role...")
    
    # Tomasz should focus on implementation
    assert "implement" in tomasz_lower or "code" in tomasz_lower, "Tomasz not focused on implementation"
    print("  ✅ Tomasz focuses on implementation")
    
    # Anna should focus on testing
    assert "test" in anna_lower or "qa" in anna_lower, "Anna not focused on testing"
    print("  ✅ Anna focuses on testing")
    
    # Magdalena should focus on UX
    assert "ux" in magdalena_lower or "user" in magdalena_lower, "Magdalena not focused on UX"
    print("  ✅ Magdalena focuses on UX")
    
    # Michał should focus on architecture
    assert "architecture" in michal_lower or "component" in michal_lower, "Michał not focused on architecture"
    print("  ✅ Michał focuses on architecture")
    
    print("  ✅ PASS: All agents focus on their specialized roles")
    print()
    
    # Final summary
    print("="*80)
    print("🎉 ALL 10 ASSERTIONS PASSED!")
    print("="*80)
    print()
    print("✅ PROOF OF REAL 4-AGENT MULTI-AGENT SYSTEM:")
    print()
    print("  1. ✅ All 4 agents completed same task")
    print("  2. ✅ 4 different output types (implementation, test_plan, ux_design, architecture_design)")
    print("  3. ✅ Tomasz uses developer terminology")
    print("  4. ✅ Anna uses QA terminology")
    print("  5. ✅ Magdalena uses UX terminology")
    print("  6. ✅ Michał uses architecture terminology")
    print(f"  7. ✅ Low similarity ({avg_similarity:.1f}%) - genuinely different reasoning")
    print(f"  8. ✅ {uniqueness:.1f}% unique artifacts")
    print("  9. ✅ Different next steps for each")
    print(" 10. ✅ Each agent focuses on their specialized role")
    print()
    print("="*80)
    print("🚀 THIS IS A REAL 4-AGENT MULTI-AGENT SYSTEM!")
    print("="*80)
    print()
    print("Not theatrical - agents have DIFFERENT behaviors!")
    print("Not copy-paste - agents reason DIFFERENTLY!")
    print("Not fake - agents produce DIFFERENT outputs!")
    print()
    print("✅ Demo complete - 4 agents proven specialized!")
    print()


if __name__ == "__main__":
    try:
        main()
        print("✅ 4-agent demo succeeded!\n")
        exit(0)
    except AssertionError as e:
        print(f"\n❌ DEMO FAILED: {e}\n")
        print("Fix agents to ensure real differences!\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ DEMO ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
