"""
Orchestrator Briefing System

Generuje i czyta PROJECT_STATUS.md - plik przypominający dla orchestratora
przy każdym ponownym uruchomieniu projektu.

Helena (Knowledge Manager) generuje ten plik automatycznie.
Aleksander (Orchestrator) czyta go na starcie każdej sesji.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class ProjectBriefing:
    """Complete project briefing for orchestrator"""
    project_id: str
    project_name: str
    current_phase: str
    last_updated: datetime
    
    # Team status
    team_roles: Dict[str, str]
    active_agents: List[str]
    
    # Work status
    completed_tasks: List[str]
    in_progress_tasks: List[str]
    pending_tasks: List[str]
    blockers: List[str]
    
    # Key decisions
    recent_decisions: List[Dict[str, Any]]
    
    # Plans
    immediate_next_steps: List[str]
    this_week_goals: List[str]
    this_phase_objectives: List[str]
    
    # Context
    last_session_summary: str
    important_notes: List[str]


class OrchestratorBriefingGenerator:
    """
    Generates PROJECT_STATUS.md for orchestrator.
    
    This is part of Knowledge Manager's responsibilities.
    """
    
    def __init__(self, postgres_store, neo4j_graph):
        self.postgres = postgres_store
        self.neo4j = neo4j_graph
    
    def generate_briefing(
        self,
        project_id: str,
        output_path: str = "PROJECT_STATUS.md"
    ) -> ProjectBriefing:
        """
        Generate complete briefing for orchestrator.
        
        This is what orchestrator reads on startup.
        """
        # Gather all information
        project_info = self._get_project_info(project_id)
        team_status = self._get_team_status(project_id)
        work_status = self._get_work_status(project_id)
        decisions = self._get_recent_decisions(project_id, days=7)
        plans = self._get_plans(project_id)
        last_session = self._get_last_session_summary(project_id)
        
        # Create briefing object
        briefing = ProjectBriefing(
            project_id=project_id,
            project_name=project_info['name'],
            current_phase=project_info['phase'],
            last_updated=datetime.now(),
            team_roles=team_status['roles'],
            active_agents=team_status['active'],
            completed_tasks=work_status['completed'],
            in_progress_tasks=work_status['in_progress'],
            pending_tasks=work_status['pending'],
            blockers=work_status['blockers'],
            recent_decisions=decisions,
            immediate_next_steps=plans['immediate'],
            this_week_goals=plans['weekly'],
            this_phase_objectives=plans['phase'],
            last_session_summary=last_session,
            important_notes=self._get_important_notes(project_id)
        )
        
        # Generate markdown
        markdown = self._generate_markdown(briefing)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"📝 Briefing saved to: {output_path}")
        
        return briefing
    
    def _generate_markdown(self, briefing: ProjectBriefing) -> str:
        """Generate markdown document"""
        md = f"""# 🎯 PROJECT STATUS BRIEFING

**Projekt:** {briefing.project_name}  
**ID:** {briefing.project_id}  
**Faza:** {briefing.current_phase}  
**Ostatnia aktualizacja:** {briefing.last_updated.strftime('%Y-%m-%d %H:%M')}

---

## 👥 ZESPÓŁ

### Role i Odpowiedzialności
"""
        
        for agent, role in briefing.team_roles.items():
            active = "🟢" if agent in briefing.active_agents else "⚪"
            md += f"\n{active} **{agent}** - {role}"
        
        md += f"""

**Aktywni agenci:** {len(briefing.active_agents)}/{len(briefing.team_roles)}

---

## 📊 STATUS PRAC

### ✅ Ukończone Zadania ({len(briefing.completed_tasks)})
"""
        
        for task in briefing.completed_tasks[-10:]:  # Last 10
            md += f"\n- ✅ {task}"
        
        md += f"\n\n### 🔄 W Trakcie ({len(briefing.in_progress_tasks)})\n"
        
        for task in briefing.in_progress_tasks:
            md += f"\n- 🔄 {task}"
        
        md += f"\n\n### ⏳ Do Zrobienia ({len(briefing.pending_tasks)})\n"
        
        for task in briefing.pending_tasks[:5]:  # Top 5
            md += f"\n- ⏳ {task}"
        
        if briefing.blockers:
            md += f"\n\n### 🚧 Blokery ({len(briefing.blockers)})\n"
            for blocker in briefing.blockers:
                md += f"\n- 🚧 **UWAGA:** {blocker}"
        
        md += "\n\n---\n\n## 🎯 KLUCZOWE DECYZJE (Ostatnie 7 Dni)\n"
        
        for decision in briefing.recent_decisions[:5]:
            date = decision.get('date', 'N/A')
            text = decision.get('text', 'N/A')
            by = decision.get('decided_by', 'Team')
            
            md += f"\n### {date}: {text}\n"
            md += f"**Decided by:** {by}\n"
            
            if 'reasoning' in decision:
                md += f"**Reasoning:** {', '.join(decision['reasoning'])}\n"
        
        md += "\n---\n\n## 📅 PLANY\n"
        md += "\n### 🔥 Natychmiastowe Następne Kroki\n"
        
        for step in briefing.immediate_next_steps:
            md += f"\n1. {step}"
        
        md += "\n\n### 📆 Cele Na Ten Tydzień\n"
        
        for goal in briefing.this_week_goals:
            md += f"\n- {goal}"
        
        md += "\n\n### 🎯 Cele Tej Fazy\n"
        
        for objective in briefing.this_phase_objectives:
            md += f"\n- {objective}"
        
        md += f"\n\n---\n\n## 📝 OSTATNIA SESJA\n\n{briefing.last_session_summary}\n"
        
        if briefing.important_notes:
            md += "\n---\n\n## ⚠️ WAŻNE NOTATKI\n"
            for note in briefing.important_notes:
                md += f"\n- ⚠️ {note}"
        
        md += f"""

---

## 🔍 JAK UŻYWAĆ TEGO DOKUMENTU

**Aleksander (Orchestrator), na początku sesji:**

1. **Przeczytaj ten plik** (5 minut)
2. **Zrozum status:** Gdzie jesteśmy, co zrobiono, co dalej
3. **Sprawdź blokery:** Czy coś wymaga natychmiastowej uwagi
4. **Review recent decisions:** Kontekst ostatnich wyborów
5. **Plan today:** Na podstawie "Natychmiastowe Następne Kroki"

**To daje Ci:**
- ✅ Pełny kontekst w 5 minut
- ✅ Jasne priorytety
- ✅ Świadomość problemów
- ✅ Ciągłość między sesjami

**Helena aktualizuje ten plik automatycznie:**
- Po każdej ważnej decyzji
- Na koniec dnia
- Po zakończeniu zadania
- Gdy zmienia się status

---

*Wygenerowane przez: Dr. Helena Kowalczyk (Knowledge Manager)*  
*System: Destiny Team Multi-Layer Memory*
"""
        
        return md
    
    def _get_project_info(self, project_id: str) -> Dict:
        """Get basic project info"""
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT project_name, current_phase, metadata
                FROM projects
                WHERE project_id = %s
            """, (project_id,))
            
            row = cur.fetchone()
            if row:
                return {
                    'name': row[0],
                    'phase': row[1] or 'Discovery',
                    'metadata': row[2] or {}
                }
        
        return {'name': 'Unknown', 'phase': 'Unknown', 'metadata': {}}
    
    def _get_team_status(self, project_id: str) -> Dict:
        """Get team status"""
        # Get all agents from messages
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT sender
                FROM messages
                WHERE project_id = %s
                  AND timestamp > NOW() - INTERVAL '7 days'
            """, (project_id,))
            
            active_agents = [row[0] for row in cur.fetchall()]
        
        # Defined roles
        roles = {
            "Aleksander Nowak": "Orchestrator",
            "Magdalena Kowalska": "Product Manager",
            "Katarzyna Wiśniewska": "Architect",
            "Tomasz Zieliński": "Developer",
            "Anna Nowakowska": "QA Engineer",
            "Piotr Szymański": "DevOps Engineer",
            "Michał Dąbrowski": "Security Specialist",
            "Dr. Joanna Wójcik": "Data Scientist",
            "Dr. Helena Kowalczyk": "Knowledge Manager"
        }
        
        return {
            'roles': roles,
            'active': active_agents
        }
    
    def _get_work_status(self, project_id: str) -> Dict:
        """Get work/task status"""
        with self.postgres.conn.cursor() as cur:
            # Get tasks from work queue
            cur.execute("""
                SELECT task, status, agent_name
                FROM agent_work_queue
                WHERE project_id = %s
                ORDER BY priority DESC, created_at DESC
            """, (project_id,))
            
            tasks = cur.fetchall()
        
        completed = [t[0] for t in tasks if t[1] == 'completed']
        in_progress = [f"{t[0]} (@{t[2]})" for t in tasks if t[1] == 'in_progress']
        pending = [t[0] for t in tasks if t[1] == 'pending']
        
        # Get blockers from messages
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT content
                FROM messages
                WHERE project_id = %s
                  AND (content ILIKE '%blocker%' OR content ILIKE '%blocked%')
                  AND timestamp > NOW() - INTERVAL '3 days'
                ORDER BY timestamp DESC
                LIMIT 5
            """, (project_id,))
            
            blockers = [row[0][:100] for row in cur.fetchall()]
        
        return {
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'blockers': blockers
        }
    
    def _get_recent_decisions(self, project_id: str, days: int = 7) -> List[Dict]:
        """Get recent decisions"""
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT decision_text, made_by, timestamp, context
                FROM decisions
                WHERE project_id = %s
                  AND timestamp > NOW() - INTERVAL '%s days'
                ORDER BY timestamp DESC
            """, (project_id, days))
            
            decisions = []
            for row in cur.fetchall():
                decisions.append({
                    'text': row[0],
                    'decided_by': row[1],
                    'date': row[2].strftime('%Y-%m-%d'),
                    'context': row[3]
                })
            
            return decisions
    
    def _get_plans(self, project_id: str) -> Dict:
        """Get plans and goals"""
        # Get from agent contexts (where plans are stored)
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT context_key, context_value
                FROM agent_contexts
                WHERE project_id = %s
                  AND agent_name = 'Aleksander Nowak'
                  AND context_key LIKE 'plan_%'
                ORDER BY updated_at DESC
            """, (project_id,))
            
            plans = {'immediate': [], 'weekly': [], 'phase': []}
            
            for row in cur.fetchall():
                key, value = row
                if 'immediate' in key:
                    plans['immediate'] = value if isinstance(value, list) else [value]
                elif 'weekly' in key:
                    plans['weekly'] = value if isinstance(value, list) else [value]
                elif 'phase' in key:
                    plans['phase'] = value if isinstance(value, list) else [value]
        
        # Default plans if none found
        if not plans['immediate']:
            plans['immediate'] = ["Continue with current phase", "Address any blockers"]
        
        return plans
    
    def _get_last_session_summary(self, project_id: str) -> str:
        """Get summary of last work session"""
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT context_value
                FROM agent_contexts
                WHERE project_id = %s
                  AND agent_name = 'Dr. Helena Kowalczyk'
                  AND context_key LIKE 'summary_daily_%'
                ORDER BY updated_at DESC
                LIMIT 1
            """, (project_id,))
            
            row = cur.fetchone()
            if row and isinstance(row[0], dict):
                return row[0].get('executive_summary', 'No summary available')
        
        return "First session - no previous summary"
    
    def _get_important_notes(self, project_id: str) -> List[str]:
        """Get important notes/reminders"""
        notes = []
        
        # Check for high-importance unresolved items
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT content
                FROM messages
                WHERE project_id = %s
                  AND importance > 0.8
                  AND requires_response = true
                  AND response_to IS NULL
                ORDER BY timestamp DESC
                LIMIT 3
            """, (project_id,))
            
            for row in cur.fetchall():
                notes.append(f"Awaiting response: {row[0][:80]}...")
        
        return notes


class OrchestratorStartupRoutine:
    """
    Orchestrator's startup routine.
    
    Reads PROJECT_STATUS.md and loads context into orchestrator's memory.
    """
    
    def __init__(self, project_directory: str = "."):
        self.project_dir = project_directory
    
    def startup(self, project_id: str) -> Dict[str, Any]:
        """
        Orchestrator startup routine.
        
        Returns loaded context for orchestrator.
        """
        print("\n" + "="*70)
        print("  🎯 ORCHESTRATOR STARTUP - Loading Context")
        print("="*70)
        print()
        
        # Read PROJECT_STATUS.md
        status_file = f"{self.project_dir}/PROJECT_STATUS.md"
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ Loaded PROJECT_STATUS.md")
            print()
            
            # Parse briefing
            briefing = self._parse_briefing(content)
            
            # Display key info
            print("📋 Quick Overview:")
            print(f"  Projekt: {briefing.get('project_name', 'N/A')}")
            print(f"  Faza: {briefing.get('current_phase', 'N/A')}")
            print(f"  Aktywni agenci: {briefing.get('active_agents', 0)}")
            print(f"  W trakcie: {briefing.get('in_progress_count', 0)} zadań")
            print(f"  Blokery: {briefing.get('blockers_count', 0)}")
            print()
            
            if briefing.get('blockers_count', 0) > 0:
                print("⚠️  UWAGA: Są blokery! Wymagają uwagi.")
                print()
            
            print("✅ Orchestrator ready to work!")
            print()
            
            return briefing
            
        except FileNotFoundError:
            print(f"⚠️  PROJECT_STATUS.md not found")
            print(f"   This appears to be first session.")
            print(f"   Helena will create it at end of session.")
            print()
            return {}
    
    def _parse_briefing(self, content: str) -> Dict[str, Any]:
        """Parse briefing from markdown"""
        # Simple parsing (extract key numbers)
        briefing = {}
        
        # Extract project name
        if "**Projekt:**" in content:
            line = [l for l in content.split('\n') if "**Projekt:**" in l][0]
            briefing['project_name'] = line.split('**Projekt:**')[1].strip()
        
        # Extract phase
        if "**Faza:**" in content:
            line = [l for l in content.split('\n') if "**Faza:**" in l][0]
            briefing['current_phase'] = line.split('**Faza:**')[1].strip()
        
        # Count tasks
        briefing['in_progress_count'] = content.count('🔄')
        briefing['blockers_count'] = content.count('🚧')
        briefing['completed_count'] = content.count('✅') - 2  # Minus checkmarks in text
        
        # Active agents
        if "**Aktywni agenci:**" in content:
            line = [l for l in content.split('\n') if "**Aktywni agenci:**" in l][0]
            counts = line.split('**Aktywni agenci:**')[1].strip()
            briefing['active_agents'] = int(counts.split('/')[0])
        
        return briefing


# ==================== INTEGRATED WORKFLOW ====================

class SessionManager:
    """
    Manages project sessions with automatic briefing generation.
    
    Workflow:
    - Session START: Orchestrator reads PROJECT_STATUS.md
    - Session END: Helena generates updated PROJECT_STATUS.md
    """
    
    def __init__(
        self,
        project_id: str,
        project_directory: str,
        postgres_store,
        neo4j_graph
    ):
        self.project_id = project_id
        self.project_dir = project_directory
        self.briefing_gen = OrchestratorBriefingGenerator(postgres_store, neo4j_graph)
        self.startup_routine = OrchestratorStartupRoutine(project_directory)
    
    def start_session(self) -> Dict[str, Any]:
        """
        Start work session.
        
        Orchestrator reads PROJECT_STATUS.md to get context.
        """
        print("🚀 Starting work session...")
        print()
        
        # Load briefing
        context = self.startup_routine.startup(self.project_id)
        
        print("="*70)
        print("  SESSION STARTED")
        print("="*70)
        print()
        print("Aleksander (Orchestrator) has full context!")
        print("Ready to coordinate team work.")
        print()
        
        return context
    
    def end_session(self):
        """
        End work session.
        
        Helena generates updated PROJECT_STATUS.md for next session.
        """
        print("\n" + "="*70)
        print("  📝 Ending Session - Generating Briefing")
        print("="*70)
        print()
        
        # Generate briefing
        briefing = self.briefing_gen.generate_briefing(
            project_id=self.project_id,
            output_path=f"{self.project_dir}/PROJECT_STATUS.md"
        )
        
        print()
        print("✅ PROJECT_STATUS.md updated")
        print()
        print("Next session:")
        print("  1. Orchestrator will read PROJECT_STATUS.md")
        print("  2. Full context loaded in 5 minutes")
        print("  3. Ready to continue work")
        print()
        print("="*70)
        print("  SESSION ENDED")
        print("="*70)


# ==================== EXAMPLE ====================

def example_session_workflow():
    """Example showing complete session workflow"""
    from postgres_context_store import PostgresContextStore
    from neo4j_integration import Neo4jKnowledgeGraph
    
    print("=" * 70)
    print("  📚 SESSION MANAGEMENT DEMO")
    print("=" * 70)
    print()
    
    # Initialize
    postgres = PostgresContextStore(
        "dbname=destiny_team user=user password=password host=localhost port=5432"
    )
    
    neo4j = Neo4jKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    
    # Session manager
    session = SessionManager(
        project_id="test-project",
        project_directory="/Users/artur/coursor-agents-destiny-folder",
        postgres_store=postgres,
        neo4j_graph=neo4j
    )
    
    # START SESSION
    print("\n" + "🌅 "*20)
    print("  MORNING: Starting New Session")
    print("🌅 "*20)
    
    context = session.start_session()
    
    # Simulate work...
    print("\n[Simulating work during day...]")
    print("  - Messages exchanged")
    print("  - Decisions made")
    print("  - Tasks completed")
    print()
    
    # END SESSION
    print("\n" + "🌙 "*20)
    print("  EVENING: Ending Session")
    print("🌙 "*20)
    
    session.end_session()
    
    # Cleanup
    postgres.close()
    neo4j.close()
    
    print()
    print("=" * 70)
    print("  ✅ DEMO COMPLETE")
    print("=" * 70)
    print()
    print("📄 Check PROJECT_STATUS.md to see what was generated!")


if __name__ == "__main__":
    example_session_workflow()
