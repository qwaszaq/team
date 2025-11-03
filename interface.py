"""
User Interface for interacting with Destiny Development Team
"""

from destiny_team import DestinyTeam, ProjectPhase
import json


class TeamInterface:
    """Interactive interface for Artur to work with the team"""
    
    def __init__(self):
        self.team = DestinyTeam()
        self.project_state = None
    
    def start(self):
        """Start the interactive session"""
        print("=" * 70)
        print("🎯 WELCOME TO THE DESTINY DEVELOPMENT TEAM")
        print("=" * 70)
        print()
        print("Hi Artur! I'm Alex Morgan, your Orchestrator.")
        print("I'll coordinate our team of experts to help you build your project.")
        print()
        print("Our team includes:")
        print("  • Lisa Anderson - Product Manager")
        print("  • Sarah Chen - Architect")
        print("  • Marcus Rodriguez - Developer")
        print("  • Priya Patel - QA Engineer")
        print("  • Jordan Kim - DevOps Engineer")
        print("  • Mike Torres - Security Specialist")
        print()
        
        self._new_project()
        self._interactive_session()
    
    def _new_project(self):
        """Initialize a new project"""
        print("=" * 70)
        print("LET'S START YOUR PROJECT")
        print("=" * 70)
        print()
        
        project_name = input("What would you like to build? (project name): ").strip()
        if not project_name:
            project_name = "My Project"
        
        print()
        print("Tell me about your project:")
        description = input("> ").strip()
        if not description:
            description = "A new application"
        
        print()
        print("🚀 Initializing project...")
        self.project_state = self.team.start_project(project_name, description)
        self.team.message_bus.process_queue()
        
        print()
        print(f"✅ Project '{project_name}' initialized!")
        print()
    
    def _interactive_session(self):
        """Main interactive loop"""
        while True:
            print("=" * 70)
            print("WHAT WOULD YOU LIKE TO DO?")
            print("=" * 70)
            print()
            print("1. Talk to the team (ask questions)")
            print("2. Check project status")
            print("3. See team member status")
            print("4. Review decisions made")
            print("5. Answer questions from team")
            print("6. Start new project")
            print("7. Exit")
            print()
            
            choice = input("Your choice (1-7): ").strip()
            print()
            
            if choice == "1":
                self._talk_to_team()
            elif choice == "2":
                self._show_project_status()
            elif choice == "3":
                self._show_team_status()
            elif choice == "4":
                self._show_decisions()
            elif choice == "5":
                self._answer_questions()
            elif choice == "6":
                self._new_project()
            elif choice == "7":
                print("👋 Goodbye! The team is here whenever you need us.")
                break
            else:
                print("Invalid choice. Please try again.")
            print()
    
    def _talk_to_team(self):
        """Talk to the team"""
        print("Who would you like to talk to?")
        print("1. Alex (Orchestrator) - Project coordination")
        print("2. Lisa (Product Manager) - Requirements & features")
        print("3. Sarah (Architect) - Technical design")
        print("4. Marcus (Developer) - Implementation")
        print("5. Priya (QA) - Testing")
        print("6. Jordan (DevOps) - Deployment")
        print("7. Mike (Security) - Security concerns")
        print("8. Entire team")
        print()
        
        choice = input("Your choice (1-8): ").strip()
        print()
        
        message = input("What would you like to say/ask?\n> ").strip()
        print()
        
        if message:
            # In a real implementation, this would route to the appropriate agent
            print(f"💬 Your message: {message}")
            print()
            print("The team is processing your request...")
            print("(In production, agents would respond here)")
            print()
    
    def _show_project_status(self):
        """Show current project status"""
        if not self.project_state:
            print("No project active.")
            return
        
        print("📊 PROJECT STATUS")
        print("=" * 70)
        print(f"Project: {self.project_state.project_name}")
        print(f"Description: {self.project_state.description}")
        print(f"Phase: {self.project_state.current_phase.value}")
        print(f"Tasks Completed: {len(self.project_state.completed_tasks)}")
        print(f"Active Tasks: {len(self.project_state.active_tasks)}")
        print(f"Blockers: {len(self.project_state.blockers)}")
        print(f"Risks: {len(self.project_state.risks)}")
        print()
    
    def _show_team_status(self):
        """Show status of all team members"""
        print("👥 TEAM STATUS")
        print("=" * 70)
        status = self.team.get_team_status()
        
        for name, info in status.items():
            print(f"\n{name} ({info['role']})")
            print(f"  Tasks in queue: {len(info['work_queue'])}")
            print(f"  Concerns: {len(info['concerns'])}")
            print(f"  Recommendations: {len(info['recommendations'])}")
        print()
    
    def _show_decisions(self):
        """Show decisions made by the team"""
        if not self.project_state:
            print("No project active.")
            return
        
        print("📝 DECISIONS MADE")
        print("=" * 70)
        
        if self.project_state.decisions:
            for i, decision in enumerate(self.project_state.decisions, 1):
                print(f"\n{i}. {decision.get('title', 'Decision')}")
                print(f"   Made by: {decision.get('made_by', 'Team')}")
                print(f"   Reason: {decision.get('reason', 'N/A')}")
        else:
            print("No decisions recorded yet.")
        print()
    
    def _answer_questions(self):
        """Answer questions from team members"""
        print("📋 QUESTIONS FROM THE TEAM")
        print("=" * 70)
        print()
        print("(In production, this would show actual questions from agents)")
        print()
        print("Example questions:")
        print("  • Lisa: 'Who will use this application?'")
        print("  • Sarah: 'Do you prefer speed or scalability?'")
        print("  • Mike: 'Are there any compliance requirements?'")
        print()
        
        answer = input("Would you like to answer a question? (y/n): ").strip().lower()
        if answer == 'y':
            print("(Questions would be displayed here for you to answer)")
        print()


if __name__ == "__main__":
    interface = TeamInterface()
    interface.start()
