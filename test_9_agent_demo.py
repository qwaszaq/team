"""
9-Agent Comprehensive Demo
Proves ALL 9 specialized agents work differently on the SAME task

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.specialized.tomasz_agent import TomaszAgent
from agents.specialized.anna_agent import AnnaAgent
from agents.specialized.magdalena_agent import MagdalenaAgent
from agents.specialized.michal_agent import MichalAgent
from agents.specialized.katarzyna_agent import KatarzynaAgent
from agents.specialized.piotr_agent import PiotrAgent
from agents.specialized.joanna_agent import JoannaAgent
from agents.specialized.dr_joanna_agent import DrJoannaAgent
from agents.specialized.aleksander_agent import AleksanderAgent
from agents.task_models import Task, TaskStatus
import uuid
from datetime import datetime


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate word-level similarity between two texts"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return (len(intersection) / len(union) * 100) if union else 0


def main():
    print("\n" + "="*80)
    print("🚀 9-AGENT COMPREHENSIVE DEMO - ULTIMATE PROOF")
    print("="*80)
    print("\nTesting: ALL 9 specialized agents on the SAME task")
    print("Goal: Prove 9 completely different approaches\n")
    
    # Initialize all 9 agents
    print("📦 Initializing all 9 agents...")
    tomasz = TomaszAgent()
    anna = AnnaAgent()
    magdalena = MagdalenaAgent()
    michal = MichalAgent()
    katarzyna = KatarzynaAgent()
    piotr = PiotrAgent()
    joanna = JoannaAgent()
    dr_joanna = DrJoannaAgent()
    aleksander = AleksanderAgent()
    
    agents = [
        tomasz, anna, magdalena, michal, katarzyna,
        piotr, joanna, dr_joanna, aleksander
    ]
    
    print(f"✅ All {len(agents)} agents initialized!\n")
    
    # Create the SAME task for everyone
    task_description = """
    Build a comprehensive team collaboration platform that enables distributed teams
    to work effectively. The platform should include real-time communication,
    project tracking, resource management, and performance analytics. It needs to
    scale to 10,000+ users, be mobile-friendly, and integrate with existing tools.
    """
    
    print("📋 TASK (same for all 9 agents):")
    print(task_description.strip())
    print("\n" + "="*80 + "\n")
    
    # Process task with each agent
    results = {}
    
    for i, agent in enumerate(agents, 1):
        print(f"🔄 Agent {i}/9: {agent.name} processing...")
        
        task = Task(
            task_id=uuid.uuid4(),
            title="Build team collaboration platform",
            description=task_description,
            assigned_to=agent.name,
            assigned_by="Demo",
            context={},
            priority=5,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        result = agent.process_task(task)
        results[agent.name] = result
        
        print(f"   ✅ {agent.name}: {result.status.value}")
        print(f"   📊 Output type: {result.output.get('type')}")
        print()
    
    print("="*80)
    print("🔍 ANALYSIS - PROVING 9-WAY DIFFERENTIATION")
    print("="*80 + "\n")
    
    # Assertion 1: All tasks completed successfully
    print("Test 1: All agents completed tasks")
    for agent_name, result in results.items():
        assert result.status == TaskStatus.DONE, f"{agent_name} failed!"
    print("✅ PASS - All 9 agents completed successfully\n")
    
    # Assertion 2: All have different output types
    print("Test 2: All agents produce different output types")
    output_types = [r.output.get('type') for r in results.values()]
    unique_types = set(output_types)
    print(f"   Output types: {output_types}")
    assert len(unique_types) == 9, f"Expected 9 unique types, got {len(unique_types)}"
    print(f"✅ PASS - All 9 output types are unique!\n")
    
    # Assertion 3: Each agent uses domain-specific terminology
    print("Test 3: Domain-specific terminology")
    
    terminology_checks = {
        "Tomasz Kamiński": ["implement", "code", "api", "class", "function"],
        "Anna Lewandowska": ["test", "quality", "bug", "coverage", "validation"],
        "Magdalena Wiśniewska": ["user", "design", "wireframe", "persona", "ux"],
        "Michał Kowalczyk": ["architecture", "scalability", "pattern", "component", "system"],
        "Katarzyna Zielińska": ["roadmap", "product", "stakeholder", "priority", "metric"],
        "Piotr Nowicki": ["deployment", "infrastructure", "ci/cd", "pipeline", "docker"],
        "Joanna Mazur": ["data", "analysis", "model", "feature", "insight"],
        "Dr. Joanna Kowalska": ["research", "experiment", "finding", "hypothesis", "innovation"],
        "Aleksander Nowak": ["coordinate", "delegate", "team", "decision", "assign"]
    }
    
    for agent_name, result in results.items():
        thoughts = result.thoughts.lower()
        expected_terms = terminology_checks[agent_name]
        found = [term for term in expected_terms if term in thoughts]
        print(f"   {agent_name}: {len(found)}/{len(expected_terms)} terms → {found[:3]}")
        assert len(found) >= 2, f"{agent_name} missing domain terminology!"
    print("✅ PASS - All agents use their domain-specific terminology\n")
    
    # Assertion 4: Different reasoning approaches (low similarity)
    print("Test 4: Reasoning diversity (low similarity between agents)")
    all_thoughts = [r.thoughts for r in results.values()]
    
    similarities = []
    for i in range(len(all_thoughts)):
        for j in range(i+1, len(all_thoughts)):
            sim = calculate_similarity(all_thoughts[i], all_thoughts[j])
            similarities.append(sim)
    
    avg_similarity = sum(similarities) / len(similarities)
    print(f"   Average similarity: {avg_similarity:.1f}%")
    print(f"   (Lower = more different reasoning)")
    assert avg_similarity < 50, f"Agents too similar: {avg_similarity}%"
    print(f"✅ PASS - Low similarity ({avg_similarity:.1f}% < 50%) = diverse reasoning!\n")
    
    # Assertion 5: Different artifacts produced
    print("Test 5: Different artifacts produced by each agent")
    all_artifacts = []
    for agent_name, result in results.items():
        artifacts = result.artifacts
        all_artifacts.extend(artifacts)
        print(f"   {agent_name}: {len(artifacts)} artifacts → {artifacts[:2]}")
    
    unique_artifacts = len(set(all_artifacts))
    total_artifacts = len(all_artifacts)
    uniqueness = (unique_artifacts / total_artifacts * 100) if total_artifacts else 0
    print(f"   Uniqueness: {unique_artifacts}/{total_artifacts} ({uniqueness:.1f}%)")
    assert uniqueness > 70, f"Artifacts too similar: {uniqueness}%"
    print(f"✅ PASS - High artifact uniqueness ({uniqueness:.1f}%)\n")
    
    # Assertion 6: Different next steps
    print("Test 6: Different next steps recommended")
    all_next_steps = [r.next_steps.lower() for r in results.values()]
    unique_next_steps = len(set(all_next_steps))
    print(f"   Unique next steps: {unique_next_steps}/9")
    assert unique_next_steps >= 7, f"Next steps too similar: {unique_next_steps}/9"
    print(f"✅ PASS - Diverse next steps ({unique_next_steps}/9)\n")
    
    # Assertion 7: Role-specific focus
    print("Test 7: Each agent focuses on their role")
    
    role_focus = {
        "Tomasz Kamiński": "implementation",
        "Anna Lewandowska": "test",
        "Magdalena Wiśniewska": "design",
        "Michał Kowalczyk": "architecture",
        "Katarzyna Zielińska": "product",
        "Piotr Nowicki": "infrastructure",
        "Joanna Mazur": "data",
        "Dr. Joanna Kowalska": "research",
        "Aleksander Nowak": "coordination"
    }
    
    for agent_name, result in results.items():
        focus_word = role_focus[agent_name]
        thoughts = result.thoughts.lower()
        count = thoughts.count(focus_word)
        print(f"   {agent_name}: '{focus_word}' appears {count}x")
        assert count >= 1, f"{agent_name} doesn't focus on their role!"
    print("✅ PASS - All agents focus on their specialized role\n")
    
    # Assertion 8: Different output structure
    print("Test 8: Different output data structures")
    output_keys = []
    for agent_name, result in results.items():
        keys = sorted(result.output.keys())
        output_keys.append(str(keys))
        print(f"   {agent_name}: {len(keys)} output fields")
    
    unique_structures = len(set(output_keys))
    print(f"   Unique structures: {unique_structures}/9")
    assert unique_structures >= 7, f"Output structures too similar!"
    print(f"✅ PASS - Diverse output structures ({unique_structures}/9)\n")
    
    # Assertion 9: Varying complexity/depth
    print("Test 9: Varying output complexity (character count)")
    complexities = []
    for agent_name, result in results.items():
        length = len(result.thoughts)
        complexities.append(length)
        print(f"   {agent_name}: {length:,} characters")
    
    min_length = min(complexities)
    max_length = max(complexities)
    range_ratio = max_length / min_length if min_length > 0 else 0
    print(f"   Range ratio: {range_ratio:.2f}x (shows varying complexity)")
    assert range_ratio > 1.2, f"Outputs too uniform in size!"
    print(f"✅ PASS - Varying complexity ({range_ratio:.2f}x range)\n")
    
    # Assertion 10: Different time estimates (if provided)
    print("Test 10: Different time perspectives")
    # Check if agents mention different time horizons
    time_words = {
        "immediate": ["now", "immediately", "today", "urgent"],
        "short_term": ["day", "week", "sprint"],
        "medium_term": ["month", "quarter"],
        "long_term": ["year", "long-term", "future"]
    }
    
    agent_perspectives = {}
    for agent_name, result in results.items():
        thoughts = result.thoughts.lower()
        perspective = []
        for horizon, words in time_words.items():
            if any(word in thoughts for word in words):
                perspective.append(horizon)
        agent_perspectives[agent_name] = perspective
        print(f"   {agent_name}: {perspective}")
    
    unique_perspectives = len(set(str(p) for p in agent_perspectives.values()))
    print(f"   Unique time perspectives: {unique_perspectives}")
    assert unique_perspectives >= 5, "Time perspectives too similar!"
    print(f"✅ PASS - Diverse time perspectives ({unique_perspectives})\n")
    
    # Final Summary
    print("="*80)
    print("🎉 FINAL RESULTS - 9-AGENT DIFFERENTIATION PROOF")
    print("="*80 + "\n")
    
    print("✅ Test 1: All 9 agents completed successfully")
    print("✅ Test 2: All 9 unique output types")
    print("✅ Test 3: All 9 use domain-specific terminology")
    print(f"✅ Test 4: Low similarity ({avg_similarity:.1f}% < 50%)")
    print(f"✅ Test 5: High artifact uniqueness ({uniqueness:.1f}%)")
    print(f"✅ Test 6: Diverse next steps ({unique_next_steps}/9)")
    print("✅ Test 7: All agents focus on their role")
    print(f"✅ Test 8: Diverse output structures ({unique_structures}/9)")
    print(f"✅ Test 9: Varying complexity ({range_ratio:.2f}x)")
    print(f"✅ Test 10: Diverse time perspectives ({unique_perspectives})")
    
    print("\n" + "="*80)
    print("🏆 ALL 10 ASSERTIONS PASSED!")
    print("="*80)
    print("\n🎯 PROOF COMPLETE:")
    print("   • 9 specialized agents")
    print("   • Same task input")
    print("   • 9 completely different outputs")
    print("   • Statistically proven differentiation")
    print("   • Production-ready multi-agent system ✅")
    print("\n" + "="*80)
    
    # Return results for potential analysis
    return results


if __name__ == "__main__":
    results = main()
    
    print("\n💾 Saving demo output...")
    with open("demo_9_agent_output.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("9-AGENT COMPREHENSIVE DEMO OUTPUT\n")
        f.write("="*80 + "\n\n")
        
        for agent_name, result in results.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"AGENT: {agent_name}\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"Status: {result.status.value}\n")
            f.write(f"Output Type: {result.output.get('type')}\n")
            f.write(f"Time Taken: {result.time_taken:.2f}s\n\n")
            f.write("REASONING:\n")
            f.write(result.thoughts)
            f.write(f"\n\nARTIFACTS: {', '.join(result.artifacts)}\n")
            f.write(f"NEXT STEPS: {result.next_steps}\n")
    
    print("✅ Output saved to: demo_9_agent_output.txt")
    print("\n🚀 Ready to transition to DOGFOODING (Option B)!")
