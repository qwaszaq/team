#!/usr/bin/env python3
"""
Test script for PostgreSQL unlimited context system.

This demonstrates how agents communicate with unlimited context storage.
"""

import sys
import uuid
from datetime import datetime, timedelta

from postgres_context_store import PostgresContextStore, StoredMessage
from postgres_integration import DestinyTeamWithPostgres
from destiny_team import MessageType, ProjectState


def test_basic_storage():
    """Test 1: Basic message storage and retrieval"""
    print("\n" + "="*70)
    print("TEST 1: Basic Message Storage")
    print("="*70)
    
    # Initialize
    store = PostgresContextStore("dbname=destiny_team user=artur host=localhost")
    project_id = str(uuid.uuid4())
    
    # Create project
    store.create_project(
        project_id=project_id,
        project_name="Test Project",
        description="Testing PostgreSQL storage"
    )
    print("✓ Project created")
    
    # Store messages
    messages_to_store = [
        ("Magdalena Kowalska", "Team", "Let's discuss the requirements"),
        ("Katarzyna Wiśniewska", "Magdalena Kowalska", "I think we need a microservices architecture"),
        ("Tomasz Zieliński", "Katarzyna Wiśniewska", "Let's start with a monolith and split later"),
        ("Michał Dąbrowski", "Team", "We need to consider security from the start"),
    ]
    
    for sender, recipient, content in messages_to_store:
        msg = StoredMessage(
            id=str(uuid.uuid4()),
            project_id=project_id,
            sender=sender,
            recipient=recipient if recipient != "Team" else None,
            message_type="ANNOUNCEMENT",
            content=content,
            context={},
            timestamp=datetime.now(),
            importance=0.7,
            tags=["requirements", "architecture"]
        )
        store.store_message(msg)
    
    print(f"✓ Stored {len(messages_to_store)} messages")
    
    # Retrieve messages
    retrieved = store.get_agent_conversation_history(
        agent_name="Katarzyna Wiśniewska",
        project_id=project_id,
        limit=10
    )
    
    print(f"✓ Retrieved {len(retrieved)} messages for Architect")
    for msg in retrieved:
        print(f"  - {msg.sender}: {msg.content[:50]}...")
    
    store.close()
    return True


def test_context_retrieval():
    """Test 2: Intelligent context retrieval"""
    print("\n" + "="*70)
    print("TEST 2: Intelligent Context Retrieval")
    print("="*70)
    
    store = PostgresContextStore("dbname=destiny_team user=artur host=localhost")
    project_id = str(uuid.uuid4())
    
    # Create project
    store.create_project(project_id=project_id, project_name="E-commerce App", description="")
    
    # Simulate a long conversation (50 messages)
    topics = [
        ("database", ["PostgreSQL chosen", "Need ACID compliance", "Transactions are critical"]),
        ("security", ["Use OAuth 2.0", "Implement rate limiting", "Encrypt sensitive data"]),
        ("architecture", ["Microservices approach", "API gateway needed", "Service mesh later"]),
        ("frontend", ["React for UI", "TypeScript for type safety", "Mobile-first design"]),
    ]
    
    message_count = 0
    for topic, contents in topics:
        for content in contents:
            msg = StoredMessage(
                id=str(uuid.uuid4()),
                project_id=project_id,
                sender="Team Member",
                recipient=None,
                message_type="ANNOUNCEMENT",
                content=content,
                context={},
                timestamp=datetime.now() - timedelta(days=message_count),  # Spread over time
                importance=0.5,
                tags=[topic]
            )
            store.store_message(msg)
            message_count += 1
    
    print(f"✓ Created {message_count} messages across {len(topics)} topics")
    
    # Test relevance-based retrieval
    query = "What database should we use and why?"
    relevant = store.get_relevant_context_for_agent(
        agent_name="Architect",
        project_id=project_id,
        query=query,
        max_messages=5
    )
    
    print(f"\n✓ Query: '{query}'")
    print(f"✓ Retrieved {len(relevant)} most relevant messages:")
    for msg in relevant:
        print(f"  - [{msg.tags}] {msg.content}")
    
    # Should retrieve database-related messages, not frontend
    assert any("database" in str(msg.tags) for msg in relevant), "Should find database messages"
    print("\n✓ Relevance scoring works correctly!")
    
    store.close()
    return True


def test_agent_context():
    """Test 3: Per-agent context storage"""
    print("\n" + "="*70)
    print("TEST 3: Per-Agent Context Storage")
    print("="*70)
    
    store = PostgresContextStore("dbname=destiny_team user=artur host=localhost")
    project_id = str(uuid.uuid4())
    
    store.create_project(project_id=project_id, project_name="Test", description="")
    
    # Each agent stores their own knowledge
    agents_knowledge = {
        "Katarzyna Wiśniewska": {
            "architecture_choice": {"type": "microservices", "reason": "scalability"},
            "tech_stack": {"backend": "Node.js", "database": "PostgreSQL"}
        },
        "Tomasz Zieliński": {
            "coding_patterns": ["MVC", "Repository pattern", "Dependency injection"],
            "preferred_frameworks": ["Express", "TypeORM"]
        },
        "Michał Dąbrowski": {
            "security_requirements": ["OAuth 2.0", "Rate limiting", "SQL injection protection"],
            "compliance": ["GDPR", "PCI-DSS"]
        }
    }
    
    for agent_name, knowledge in agents_knowledge.items():
        for key, value in knowledge.items():
            store.store_agent_context(
                agent_name=agent_name,
                project_id=project_id,
                context_key=key,
                context_value=value,
                importance=0.8
            )
    
    print(f"✓ Stored knowledge for {len(agents_knowledge)} agents")
    
    # Retrieve architect's context
    architect_context = store.get_agent_context(
        agent_name="Katarzyna Wiśniewska",
        project_id=project_id
    )
    
    print(f"\n✓ Architect's knowledge base:")
    for key, data in architect_context.items():
        print(f"  - {key}: {data['value']}")
    
    # Verify architect doesn't see developer's context
    assert "coding_patterns" not in architect_context, "Context should be per-agent"
    print("\n✓ Context isolation works correctly!")
    
    store.close()
    return True


def test_full_integration():
    """Test 4: Full integration with Destiny Team"""
    print("\n" + "="*70)
    print("TEST 4: Full Integration Test")
    print("="*70)
    
    # Initialize team with PostgreSQL
    team = DestinyTeamWithPostgres(
        postgres_connection_string="dbname=destiny_team user=artur host=localhost"
    )
    
    print(f"✓ Team initialized with project ID: {team.project_id}")
    
    # Start project
    team.start_project(
        project_name="Task Management App",
        description="A web app for managing tasks and projects"
    )
    print("✓ Project started")
    
    # Simulate agent conversations
    pm = team.agents['pm']
    architect = team.agents['architect']
    
    # PM asks requirements
    pm.send_message(
        recipient=None,
        message_type=MessageType.REQUEST,
        content="We need to understand the core features. What should users be able to do?"
    )
    print("✓ PM sent requirements question")
    
    # Architect responds
    architect.send_message(
        recipient="Magdalena Kowalska",
        message_type=MessageType.RESPONSE,
        content="Based on the description, users should be able to: 1) Create tasks, 2) Organize into projects, 3) Set deadlines, 4) Track progress"
    )
    print("✓ Architect responded")
    
    # Architect stores design decision
    architect.add_to_context(
        key="architecture_decision",
        value={
            "approach": "Three-tier architecture",
            "frontend": "React",
            "backend": "Node.js + Express",
            "database": "PostgreSQL"
        },
        importance=0.9
    )
    print("✓ Architect stored design decision")
    
    # Get project summary
    summary = team.get_project_summary()
    print(f"\n✓ Project Statistics:")
    print(f"  - Total messages: {summary['project_stats']['total_messages']}")
    print(f"  - Active agents: {summary['project_stats']['active_agents']}")
    
    # Search history
    results = team.search_project_history("features requirements")
    print(f"\n✓ Search found {len(results)} relevant messages")
    
    team.close()
    return True


def test_cross_session_persistence():
    """Test 5: Cross-session persistence"""
    print("\n" + "="*70)
    print("TEST 5: Cross-Session Persistence")
    print("="*70)
    
    # Session 1: Create project and add messages
    print("\n[Session 1] Starting new project...")
    team1 = DestinyTeamWithPostgres(
        postgres_connection_string="dbname=destiny_team user=artur host=localhost"
    )
    
    project_id = team1.start_project(
        project_name="Persistent Project",
        description="Testing cross-session persistence"
    )
    
    architect = team1.agents['architect']
    architect.send_message(
        recipient=None,
        message_type=MessageType.ANNOUNCEMENT,
        content="I've designed the initial architecture"
    )
    
    architect.add_to_context(
        key="session1_decision",
        value={"decision": "Use microservices", "timestamp": datetime.now().isoformat()},
        importance=0.9
    )
    
    print(f"✓ Created project: {project_id}")
    print("✓ Added messages and context")
    team1.close()
    
    # Session 2: Resume same project
    print("\n[Session 2] Resuming project...")
    team2 = DestinyTeamWithPostgres(
        postgres_connection_string="dbname=destiny_team user=artur host=localhost",
        project_id=project_id  # Resume same project
    )
    
    # Check if history is available
    history = team2.search_project_history("architecture")
    print(f"✓ Found {len(history)} messages from previous session")
    
    # Check if architect's context persisted
    architect2 = team2.agents['architect']
    context = architect2.context_store.get_agent_context(
        agent_name="Katarzyna Wiśniewska",
        project_id=project_id
    )
    
    assert "session1_decision" in context, "Context should persist across sessions"
    print(f"✓ Architect's context persisted: {context['session1_decision']['value']}")
    
    print("\n✓ Cross-session persistence works perfectly!")
    team2.close()
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("PostgreSQL Unlimited Context - Test Suite")
    print("="*70)
    print("\nThis will test the unlimited context storage system.")
    print("Make sure PostgreSQL is running and database 'destiny_team' exists.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    tests = [
        ("Basic Storage", test_basic_storage),
        ("Context Retrieval", test_context_retrieval),
        ("Agent Context", test_agent_context),
        ("Full Integration", test_full_integration),
        ("Cross-Session Persistence", test_cross_session_persistence),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed, error in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
        if error:
            print(f"  Error: {error}")
    
    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)
    
    print(f"\n{passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Your unlimited context system is working!")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")


if __name__ == "__main__":
    # Check if PostgreSQL is likely available
    try:
        store = PostgresContextStore("dbname=destiny_team user=artur host=localhost")
        store.close()
        print("✓ PostgreSQL connection successful!")
        run_all_tests()
    except Exception as e:
        print("✗ Cannot connect to PostgreSQL!")
        print(f"  Error: {e}")
        print("\nPlease:")
        print("  1. Install PostgreSQL: brew install postgresql")
        print("  2. Start service: brew services start postgresql")
        print("  3. Create database: createdb destiny_team")
        print("  4. Run this script again")
        sys.exit(1)
