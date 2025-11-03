#!/usr/bin/env python3
"""
Session Workflow - Automatyczny workflow dla sesji projektu

START sesji: Aleksander czyta PROJECT_STATUS.md
END sesji: Helena generuje updated PROJECT_STATUS.md

Użycie:
  python session_workflow.py start <project_id>
  ... work ...
  python session_workflow.py end <project_id>
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

from postgres_context_store import PostgresContextStore
from neo4j_integration import Neo4jKnowledgeGraph
from orchestrator_briefing import (
    OrchestratorBriefingGenerator,
    OrchestratorStartupRoutine,
    SessionManager
)


def get_project_directory():
    """Get project directory"""
    return Path(__file__).parent


def start_session(project_id: str):
    """
    Start work session.
    
    Aleksander (Orchestrator) czyta PROJECT_STATUS.md
    """
    print("\n" + "🌅 "*30)
    print("  ROZPOCZĘCIE SESJI ROBOCZEJ")
    print("🌅 "*30)
    print()
    
    project_dir = get_project_directory()
    
    # Check if PROJECT_STATUS.md exists
    status_file = project_dir / "PROJECT_STATUS.md"
    
    if not status_file.exists():
        print("📝 Pierwsza sesja tego projektu.")
        print("   PROJECT_STATUS.md zostanie utworzony na końcu sesji.")
        print()
        print("🎯 Aleksander (Orchestrator):")
        print("   - Starting fresh")
        print("   - No previous context")
        print("   - Will coordinate team from scratch")
        print()
    else:
        print("📄 Znaleziono PROJECT_STATUS.md")
        print()
        print("🎯 Aleksander (Orchestrator) czyta briefing...")
        print()
        
        # Orchestrator reads briefing
        routine = OrchestratorStartupRoutine(str(project_dir))
        context = routine.startup(project_id)
        
        print()
        print("✅ Aleksander ma pełen kontekst!")
        print()
        
        # Show file location
        print(f"📍 Briefing location: {status_file}")
        print()
        
        # Show quick stats
        if context:
            print("📊 Quick Stats:")
            if 'in_progress_count' in context:
                print(f"   W trakcie: {context['in_progress_count']} zadań")
            if 'blockers_count' in context:
                if context['blockers_count'] > 0:
                    print(f"   ⚠️  Blokery: {context['blockers_count']}")
            print()
    
    print("="*70)
    print("  🚀 SESJA ROZPOCZĘTA")
    print("="*70)
    print()
    print("Aleksander koordynuje zespół.")
    print("Helena monitoruje i dokumentuje.")
    print()
    print("Aby zakończyć sesję:")
    print(f"  python session_workflow.py end {project_id}")
    print()


def end_session(project_id: str):
    """
    End work session.
    
    Helena (Knowledge Manager) generuje updated PROJECT_STATUS.md
    """
    print("\n" + "🌙 "*30)
    print("  ZAKOŃCZENIE SESJI ROBOCZEJ")
    print("🌙 "*30)
    print()
    
    project_dir = get_project_directory()
    
    # Initialize storage
    print("📦 Connecting to storage layers...")
    
    try:
        postgres = PostgresContextStore(
            "dbname=destiny_team user=user password=password host=localhost port=5432"
        )
        print("  ✓ PostgreSQL")
    except Exception as e:
        print(f"  ✗ PostgreSQL: {e}")
        return
    
    try:
        neo4j = Neo4jKnowledgeGraph(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="password"
        )
        print("  ✓ Neo4j")
    except Exception as e:
        print(f"  ✗ Neo4j: {e}")
        neo4j = None
    
    print()
    
    # Helena generates briefing
    print("📝 Dr. Helena Kowalczyk (Knowledge Manager):")
    print("   Analyzing today's work...")
    print()
    
    generator = OrchestratorBriefingGenerator(postgres, neo4j)
    
    briefing = generator.generate_briefing(
        project_id=project_id,
        output_path=str(project_dir / "PROJECT_STATUS.md")
    )
    
    print()
    print("✅ PROJECT_STATUS.md updated!")
    print()
    
    # Summary of what was generated
    print("📊 Briefing zawiera:")
    print(f"   - Status zespołu: {len(briefing.team_roles)} agentów")
    print(f"   - Ukończone: {len(briefing.completed_tasks)} zadań")
    print(f"   - W trakcie: {len(briefing.in_progress_tasks)} zadań")
    print(f"   - Do zrobienia: {len(briefing.pending_tasks)} zadań")
    print(f"   - Recent decisions: {len(briefing.recent_decisions)}")
    print(f"   - Next steps: {len(briefing.immediate_next_steps)}")
    
    if briefing.blockers:
        print(f"   - ⚠️  Blokery: {len(briefing.blockers)}")
    
    print()
    print("="*70)
    print("  🌙 SESJA ZAKOŃCZONA")
    print("="*70)
    print()
    print("Następna sesja:")
    print(f"  python session_workflow.py start {project_id}")
    print()
    print("Aleksander przeczyta briefing i będzie gotowy do pracy! 🎯")
    print()
    
    # Cleanup
    postgres.close()
    if neo4j:
        neo4j.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Session workflow management for Destiny Team"
    )
    
    parser.add_argument(
        'action',
        choices=['start', 'end'],
        help="Action: start or end session"
    )
    
    parser.add_argument(
        'project_id',
        nargs='?',
        default='destiny-team-core',
        help="Project ID (default: destiny-team-core)"
    )
    
    args = parser.parse_args()
    
    if args.action == 'start':
        start_session(args.project_id)
    elif args.action == 'end':
        end_session(args.project_id)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - show help
        print("\n" + "="*70)
        print("  📚 SESSION WORKFLOW MANAGER")
        print("="*70)
        print()
        print("Usage:")
        print("  python session_workflow.py start [project_id]  # Start session")
        print("  python session_workflow.py end [project_id]    # End session")
        print()
        print("What it does:")
        print()
        print("START session:")
        print("  1. Aleksander reads PROJECT_STATUS.md")
        print("  2. Loads full context (5 minutes)")
        print("  3. Ready to coordinate team")
        print()
        print("END session:")
        print("  1. Helena analyzes today's work")
        print("  2. Generates updated PROJECT_STATUS.md")
        print("  3. Ready for next session")
        print()
        print("Example:")
        print("  python session_workflow.py start destiny-team-core")
        print("  # ... work ...")
        print("  python session_workflow.py end destiny-team-core")
        print()
        print("="*70)
        print()
    else:
        main()
