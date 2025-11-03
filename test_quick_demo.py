"""
Quick Demo: Real Multi-Agent Behavior

This demo proves that different agents handle the SAME task DIFFERENTLY.

Usage:
    python3 test_quick_demo.py

Expected: All assertions pass, showing agents behave uniquely.
"""

import uuid
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.specialized.tomasz_agent import TomaszAgent
from agents.specialized.anna_agent import AnnaAgent
from agents.task_models import Task, TaskStatus


def main():
    print("\n" + "="*80)
    print("🎬 QUICK DEMO: Real Multi-Agent System")
    print("="*80)
    print()
    print("Demonstrating that different agents handle the SAME task DIFFERENTLY.")
    print()
    
    # Initialize agents
    print("━" * 80)
    print("📋 INITIALIZING AGENTS")
    print("━" * 80)
    
    tomasz = TomaszAgent()
    anna = AnnaAgent()
    
    print(f"✅ {tomasz.name} ({tomasz.role})")
    print(f"✅ {anna.name} ({anna.role})")
    print()
    
    # Create THE SAME task for both agents
    print("━" * 80)
    print("📝 CREATING IDENTICAL TASK FOR BOTH AGENTS")
    print("━" * 80)
    
    task_for_tomasz = Task(
        task_id=uuid.uuid4(),
        title="Build and test health check endpoint",
        description="Create a health check endpoint for the API and ensure it works correctly",
        assigned_to=tomasz.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    task_for_anna = Task(
        task_id=uuid.uuid4(),
        title="Build and test health check endpoint",
        description="Create a health check endpoint for the API and ensure it works correctly",
        assigned_to=anna.name,
        assigned_by="Demo Script",
        context={"urgency": "high", "complexity": "medium"},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    print(f"Task: '{task_for_tomasz.title}'")
    print(f"Description: '{task_for_tomasz.description}'")
    print()
    print("⚠️  NOTE: Both tasks are IDENTICAL - same title, same description!")
    print()
    
    # Process task with Tomasz (Developer)
    print("━" * 80)
    print("👨‍💻 TOMASZ (DEVELOPER) PROCESSES THE TASK")
    print("━" * 80)
    print()
    
    result_tomasz = tomasz.process_task(task_for_tomasz)
    
    print(f"Status: {result_tomasz.status.value}")
    print(f"Output type: {result_tomasz.output.get('type')}")
    print()
    print("Tomasz's reasoning:")
    print("-" * 80)
    print(result_tomasz.thoughts[:500] + "..." if len(result_tomasz.thoughts) > 500 else result_tomasz.thoughts)
    print("-" * 80)
    print()
    
    # Process task with Anna (QA)
    print("━" * 80)
    print("👩‍💼 ANNA (QA ENGINEER) PROCESSES THE SAME TASK")
    print("━" * 80)
    print()
    
    result_anna = anna.process_task(task_for_anna)
    
    print(f"Status: {result_anna.status.value}")
    print(f"Output type: {result_anna.output.get('type')}")
    print()
    print("Anna's reasoning:")
    print("-" * 80)
    print(result_anna.thoughts[:500] + "..." if len(result_anna.thoughts) > 500 else result_anna.thoughts)
    print("-" * 80)
    print()
    
    # COMPARE AND VERIFY DIFFERENCES
    print("━" * 80)
    print("🔍 VERIFICATION: ARE THEY DIFFERENT?")
    print("━" * 80)
    print()
    
    # Assertion 1: Both completed successfully
    print("✓ Checking: Both agents completed task...")
    assert result_tomasz.status == TaskStatus.DONE, "Tomasz failed!"
    assert result_anna.status == TaskStatus.DONE, "Anna failed!"
    print("  ✅ PASS: Both completed successfully")
    print()
    
    # Assertion 2: Different output types
    print("✓ Checking: Different output types...")
    tomasz_type = result_tomasz.output.get('type')
    anna_type = result_anna.output.get('type')
    print(f"  Tomasz type: '{tomasz_type}'")
    print(f"  Anna type: '{anna_type}'")
    assert tomasz_type != anna_type, "Output types are the same! Not differentiated!"
    print("  ✅ PASS: Different output types")
    print()
    
    # Assertion 3: Tomasz uses developer terminology
    print("✓ Checking: Tomasz uses developer terminology...")
    tomasz_thoughts_lower = result_tomasz.thoughts.lower()
    developer_terms = ["implement", "code", "python", "design", "architecture"]
    found_terms = [term for term in developer_terms if term in tomasz_thoughts_lower]
    print(f"  Found developer terms: {found_terms}")
    assert len(found_terms) >= 2, f"Tomasz should use developer terms! Found only: {found_terms}"
    print(f"  ✅ PASS: Found {len(found_terms)} developer terms")
    print()
    
    # Assertion 4: Anna uses QA terminology
    print("✓ Checking: Anna uses QA terminology...")
    anna_thoughts_lower = result_anna.thoughts.lower()
    qa_terms = ["test", "qa", "quality", "verify", "coverage", "edge case"]
    found_qa_terms = [term for term in qa_terms if term in anna_thoughts_lower]
    print(f"  Found QA terms: {found_qa_terms}")
    assert len(found_qa_terms) >= 2, f"Anna should use QA terms! Found only: {found_qa_terms}"
    print(f"  ✅ PASS: Found {len(found_qa_terms)} QA terms")
    print()
    
    # Assertion 5: Thoughts are ACTUALLY different (not copy-paste)
    print("✓ Checking: Reasoning is ACTUALLY different...")
    thoughts_similarity = len(set(result_tomasz.thoughts.split()) & set(result_anna.thoughts.split()))
    total_words = len(set(result_tomasz.thoughts.split()))
    similarity_percent = (thoughts_similarity / total_words * 100) if total_words > 0 else 0
    print(f"  Similarity: {similarity_percent:.1f}% common words")
    assert similarity_percent < 70, f"Too similar ({similarity_percent:.1f}%)! Might be copy-paste!"
    print(f"  ✅ PASS: Sufficiently different ({similarity_percent:.1f}% common)")
    print()
    
    # Assertion 6: Different artifacts
    print("✓ Checking: Different artifacts produced...")
    tomasz_artifacts = set(result_tomasz.artifacts)
    anna_artifacts = set(result_anna.artifacts)
    print(f"  Tomasz artifacts: {tomasz_artifacts}")
    print(f"  Anna artifacts: {anna_artifacts}")
    assert tomasz_artifacts != anna_artifacts, "Artifacts are identical!"
    print("  ✅ PASS: Different artifacts")
    print()
    
    # Final verification
    print("="*80)
    print("🎉 ALL ASSERTIONS PASSED!")
    print("="*80)
    print()
    print("✅ PROOF OF REAL MULTI-AGENT SYSTEM:")
    print()
    print("  1. ✅ Same task given to both agents")
    print("  2. ✅ Different output types (implementation vs test_plan)")
    print("  3. ✅ Tomasz uses developer terminology")
    print("  4. ✅ Anna uses QA terminology")
    print("  5. ✅ Reasoning is substantively different")
    print("  6. ✅ Different artifacts produced")
    print()
    print("="*80)
    print("🚀 THIS IS A REAL MULTI-AGENT SYSTEM!")
    print("="*80)
    print()
    print("Not theatrical - agents have DIFFERENT behaviors!")
    print("Not copy-paste - agents reason DIFFERENTLY!")
    print("Not fake - agents produce DIFFERENT outputs!")
    print()
    print("✅ Demo complete - ready to present!")
    print()


if __name__ == "__main__":
    try:
        main()
        print("✅ Demo script succeeded!\n")
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
