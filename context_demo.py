"""
Demonstration: Independent Context Windows with Information Exchange
Shows how each agent maintains their own AI model context independently
"""

from destiny_team import DestinyTeam, MessageType
import json


def demonstrate_independent_contexts():
    """Show how each agent has independent context but can exchange information"""
    
    print("=" * 70)
    print("INDEPENDENT CONTEXT WINDOWS WITH INFORMATION EXCHANGE")
    print("=" * 70)
    print()
    
    team = DestinyTeam()
    
    # Initialize project
    project = team.start_project("Demo Project", "Testing independent contexts")
    team.message_bus.process_queue()
    
    print("📋 Project initialized!")
    print()
    
    # Show each agent's independent context window
    print("=" * 70)
    print("INDEPENDENT CONTEXT WINDOWS:")
    print("=" * 70)
    print()
    
    for agent_name, agent in team.message_bus.agents.items():
        status = agent.get_status()
        print(f"👤 {agent_name} ({agent.role})")
        print(f"   AI Model: {status['model']}")
        print(f"   Context Window: {status['context_window']}")
        print(f"   Conversation Messages: {status['conversation_messages']}")
        print(f"   Shared Knowledge (from team): {status['shared_knowledge_count']} messages")
        print()
    
    # Simulate agents thinking (building their own context)
    print("=" * 70)
    print("SIMULATING AGENT THINKING (Building Independent Contexts):")
    print("=" * 70)
    print()
    
    # Each agent thinks independently - builds their own conversation history
    print("💭 Lisa (PM) thinking about requirements...")
    response1 = team.product_manager.think(
        "What questions should I ask about user needs?",
        project
    )
    print(f"   Context built: {len(team.product_manager.ai_conversation_history)} messages")
    print()
    
    print("💭 Sarah (Architect) thinking about architecture...")
    response2 = team.architect.think(
        "What tech stack would work best for a social media app?",
        project
    )
    print(f"   Context built: {len(team.architect.ai_conversation_history)} messages")
    print()
    
    print("💭 Marcus (Developer) thinking about implementation...")
    response3 = team.developer.think(
        "How should I structure the authentication code?",
        project
    )
    print(f"   Context built: {len(team.developer.ai_conversation_history)} messages")
    print()
    
    # Agents exchange information
    print("=" * 70)
    print("INFORMATION EXCHANGE (Through Message Bus):")
    print("=" * 70)
    print()
    
    # Lisa sends information to Sarah
    print("📤 Lisa (PM) → Sarah (Architect):")
    print("   'We need to support 10K users initially'")
    team.product_manager.send_message(
        recipient="Sarah Chen",
        message_type=MessageType.ANNOUNCEMENT,
        content="We need to support 10K users initially",
        context={"user_scale": 10000}
    )
    team.message_bus.process_queue()
    print()
    
    # Check Sarah's shared knowledge (information received)
    print("📥 Sarah received the message:")
    print(f"   Shared knowledge count: {len(team.architect.shared_knowledge)}")
    print(f"   But her AI context is still independent: {len(team.architect.ai_conversation_history)} messages")
    print()
    
    # Sarah can choose to include shared knowledge when thinking
    print("💭 Sarah thinking WITH shared knowledge included:")
    response4 = team.architect.think(
        "Given the user scale, what architecture should I recommend?",
        project,
        include_shared_knowledge=True  # Include info from other agents
    )
    print(f"   Her AI context now: {len(team.architect.ai_conversation_history)} messages")
    print()
    
    print("=" * 70)
    print("KEY POINTS:")
    print("=" * 70)
    print()
    print("✅ Each agent has INDEPENDENT context window:")
    print("   • Lisa: 128,000 tokens (GPT-5)")
    print("   • Sarah: 128,000 tokens (GPT-5)")
    print("   • Marcus: 200,000 tokens (Claude Codex)")
    print("   • Priya: 1,000,000 tokens (Gemini Pro 2.5)")
    print("   • Alex: 200,000 tokens (Claude Sonnet 4.5)")
    print()
    print("✅ Each agent builds their own conversation history:")
    print("   • Their AI model remembers THEIR conversations")
    print("   • Context accumulates independently")
    print("   • Different agents can have different context depths")
    print()
    print("✅ Information exchange through Message Bus:")
    print("   • Agents send messages to share information")
    print("   • Received messages stored in 'shared_knowledge'")
    print("   • Agents CHOOSE when to include shared knowledge")
    print("   • Each agent's AI context remains independent")
    print()
    print("✅ Common Goal:")
    print("   • All agents work on the same project")
    print("   • Shared ProjectState tracks overall progress")
    print("   • But each agent's AI context is separate")
    print()
    print("=" * 70)
    print("RESULT:")
    print("=" * 70)
    print()
    print("Each agent has:")
    print("  • Independent AI model context (their own conversation history)")
    print("  • Independent token budget (their own context window)")
    print("  • Ability to exchange information (through messages)")
    print("  • Choice to include shared knowledge (when needed)")
    print()
    print("This allows:")
    print("  • Long-running conversations per agent")
    print("  • Different context depths per role")
    print("  • Efficient token usage (each agent uses their own budget)")
    print("  • Collaboration without context pollution")
    print()


if __name__ == "__main__":
    demonstrate_independent_contexts()
