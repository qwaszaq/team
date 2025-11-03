#!/usr/bin/env python3
"""
Complete Workflow Example - Session Management

Pokazuje pełny workflow z automatycznym briefingiem dla orchestratora.
"""

from datetime import datetime
import time

from postgres_context_store import PostgresContextStore
from neo4j_integration import Neo4jKnowledgeGraph
from orchestrator_briefing import (
    OrchestratorBriefingGenerator,
    OrchestratorStartupRoutine,
    SessionManager
)


def simulate_full_project_session():
    """
    Symuluje pełną sesję projektu:
    1. START: Orchestrator czyta briefing
    2. WORK: Zespół pracuje, robi decyzje
    3. END: Helena generuje updated briefing
    """
    
    print("\n" + "🌟 "*25)
    print("  COMPLETE PROJECT SESSION WORKFLOW")
    print("🌟 "*25)
    
    # Initialize storage
    postgres = PostgresContextStore(
        "dbname=destiny_team user=user password=password host=localhost port=5432"
    )
    
    neo4j = Neo4jKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    
    project_id = "demo-project"
    project_dir = "/Users/artur/coursor-agents-destiny-folder"
    
    # Create project if doesn't exist
    postgres.create_project(
        project_id=project_id,
        project_name="E-commerce Platform Demo",
        description="Demo project showing session management"
    )
    
    neo4j.create_project_node(
        project_id=project_id,
        name="E-commerce Platform Demo",
        description="Demo project"
    )
    
    # ===== SESSION START =====
    
    print("\n" + "🌅 "*25)
    print("  PORANEK: Rozpoczęcie Sesji")
    print("🌅 "*25)
    
    session = SessionManager(
        project_id=project_id,
        project_directory=project_dir,
        postgres_store=postgres,
        neo4j_graph=neo4j
    )
    
    # Orchestrator czyta briefing
    context = session.start_session()
    
    input("\nPress Enter to simulate work during the day...")
    
    # ===== WORK SIMULATION =====
    
    print("\n" + "💼 "*25)
    print("  DZIEŃ: Praca Zespołu")
    print("💼 "*25)
    print()
    
    # Simulate team messages
    messages_today = [
        {
            "sender": "Magdalena Kowalska",
            "content": "Zespół, musimy doprecyzować wymagania dotyczące płatności",
            "type": "REQUEST",
            "importance": 0.7
        },
        {
            "sender": "Katarzyna Wiśniewska",
            "content": "Decyzja: Będziemy używać Stripe API dla płatności",
            "type": "DECISION",
            "importance": 0.9
        },
        {
            "sender": "Tomasz Zieliński",
            "content": "Implementuję integrację z Stripe",
            "type": "UPDATE",
            "importance": 0.6
        },
        {
            "sender": "Michał Dąbrowski",
            "content": "Stripe jest bezpieczny, ale musimy dodać rate limiting",
            "type": "REQUIREMENT",
            "importance": 0.8
        },
        {
            "sender": "Tomasz Zieliński",
            "content": "Ukończyłem podstawową integrację Stripe",
            "type": "UPDATE",
            "importance": 0.7
        }
    ]
    
    print("📨 Wiadomości dzisiejszej sesji:\n")
    
    for i, msg in enumerate(messages_today, 1):
        # Store message
        from postgres_context_store import StoredMessage
        stored_msg = StoredMessage(
            id=f"msg-{i}",
            project_id=project_id,
            sender=msg['sender'],
            recipient=None,
            message_type=msg['type'],
            content=msg['content'],
            context={},
            timestamp=datetime.now(),
            importance=msg['importance']
        )
        
        postgres.store_message(stored_msg)
        
        # Display
        icon = "📝" if msg['type'] == "REQUEST" else "✅" if msg['type'] == "DECISION" else "🔄"
        print(f"  {icon} {msg['sender']}: {msg['content']}")
        
        time.sleep(0.3)  # Simulate time passing
    
    print()
    print(f"✅ Dzisiaj: {len(messages_today)} wiadomości")
    print()
    
    # Add some tasks to work queue
    with postgres.conn.cursor() as cur:
        cur.execute("""
            INSERT INTO agent_work_queue (agent_name, project_id, task, status, priority)
            VALUES 
                ('Tomasz Zieliński', %s, 'Implement Stripe integration', 'completed', 8),
                ('Tomasz Zieliński', %s, 'Add rate limiting', 'in_progress', 7),
                ('Anna Nowakowska', %s, 'Test payment flow', 'pending', 6)
        """, (project_id, project_id, project_id))
        postgres.conn.commit()
    
    # Add decision to decisions table
    with postgres.conn.cursor() as cur:
        cur.execute("""
            INSERT INTO decisions (project_id, decision_text, made_by, timestamp)
            VALUES (%s, %s, %s, NOW())
        """, (
            project_id,
            "Stripe API chosen for payment processing",
            "Katarzyna Wiśniewska"
        ))
        postgres.conn.commit()
    
    input("\nPress Enter to end session and generate briefing...")
    
    # ===== SESSION END =====
    
    session.end_session()
    
    # ===== SHOW GENERATED BRIEFING =====
    
    print("\n" + "📄 "*25)
    print("  GENERATED PROJECT_STATUS.MD")
    print("📄 "*25)
    print()
    
    # Read and display generated file
    try:
        with open(f"{project_dir}/PROJECT_STATUS.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(content)
        
    except FileNotFoundError:
        print("⚠️  File not yet generated")
    
    # ===== NEXT SESSION SIMULATION =====
    
    input("\n\nPress Enter to simulate NEXT DAY session start...")
    
    print("\n" + "🌅 "*25)
    print("  NASTĘPNY DZIEŃ: Nowa Sesja")
    print("🌅 "*25)
    
    # New session manager
    new_session = SessionManager(
        project_id=project_id,
        project_directory=project_dir,
        postgres_store=postgres,
        neo4j_graph=neo4j
    )
    
    # Orchestrator czyta wczorajszy briefing
    context = new_session.start_session()
    
    print("\n✅ Aleksander ma pełen kontekst z wczoraj!")
    print("   - Wie że Stripe został wybrany")
    print("   - Wie że Tomasz implementuje")
    print("   - Wie że są 3 zadania")
    print("   - Wie że jest 1 blocker (OAuth)")
    print()
    print("Może natychmiast kontynuować koordynację! 🎯")
    
    # Cleanup
    postgres.close()
    neo4j.close()
    
    print("\n" + "="*70)
    print("  ✅ WORKFLOW DEMO COMPLETE!")
    print("="*70)
    print()
    print("📝 Key Takeaway:")
    print("   - Każda sesja kończy się briefingiem")
    print("   - Następna sesja zaczyna od przeczytania briefingu")
    print("   - Orchestrator zawsze ma kontekst")
    print("   - Zero czasu na 'przypominanie sobie'")
    print()


if __name__ == "__main__":
    simulate_full_project_session()
