"""
Automatic Team Orchestration - CLI Version
Aleksander (Orchestrator) automatically responds as team members
No need to switch models - everything happens through orchestrator
"""

from model_config import TEAM_MODEL_ASSIGNMENTS, get_model_for_agent
from agent_contexts import AGENT_CONTEXTS, update_agent_context, get_agent_context
import json


class AutoTeamOrchestrator:
    """
    Aleksander Nowak - Automatic Orchestrator (CLI Version)
    Automatically responds as team members without requiring model switching
    """
    
    def __init__(self):
        self.conversation_history = []
        
    def process_message(self, user_message: str) -> str:
        """
        Process message and automatically route to appropriate team member
        Responds as that team member immediately - no model switching needed
        """
        message_lower = user_message.lower()
        
        # Detect which agent should handle this
        if any(word in message_lower for word in ['user', 'who', 'what', 'problem', 'feature', 'requirements']):
            return self._respond_as_agent("Magdalena Kowalska", "Product Manager", user_message)
        
        elif any(word in message_lower for word in ['architecture', 'tech', 'stack', 'database', 'design']):
            return self._respond_as_agent("Katarzyna Wiśniewska", "Architect", user_message)
        
        elif any(word in message_lower for word in ['code', 'implement', 'build', 'write', 'develop']):
            return self._respond_as_agent("Tomasz Zieliński", "Developer", user_message)
        
        elif any(word in message_lower for word in ['test', 'bug', 'quality', 'qa']):
            return self._respond_as_agent("Anna Nowakowska", "QA Engineer", user_message)
        
        elif any(word in message_lower for word in ['deploy', 'host', 'server', 'infrastructure', 'devops']):
            return self._respond_as_agent("Piotr Szymański", "DevOps Engineer", user_message)
        
        elif any(word in message_lower for word in ['security', 'safe', 'secure', 'protection']):
            return self._respond_as_agent("Michał Dąbrowski", "Security Specialist", user_message)
        
        elif any(word in message_lower for word in ['data', 'ml', 'machine learning', 'dataset', 'analytics']):
            return self._respond_as_agent("Dr. Joanna Wójcik", "Data Scientist", user_message)
        
        else:
            return self._respond_as_orchestrator(user_message)
    
    def _respond_as_agent(self, agent_name: str, role: str, user_message: str) -> str:
        """Respond as a specific team member"""
        
        # Get agent's assigned model
        model = get_model_for_agent(agent_name)
        
        # Update agent's context
        update_agent_context(agent_name, "user", user_message)
        
        # Get agent's conversation history
        agent_context = get_agent_context(agent_name)
        conversation_count = len(agent_context.get('conversation_history', []))
        
        # Build response header
        response = f"""
🎯 ALEKSANDER NOWAK (Orchestrator):
   'Przekierowuję do {agent_name} ({role})'
   'Przypisany model: {model}'
   'Kontekst: {conversation_count} wiadomości w historii'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 {agent_name.upper()} ({role}):
   [Odpowiadam jako {agent_name} używając charakterystyki modelu {model}]
   
"""
        
        # Add agent-specific response based on their role and model characteristics
        response += self._generate_agent_response(agent_name, role, model, user_message, agent_context)
        
        # Update agent's conversation history
        update_agent_context(agent_name, "assistant", "Response generated")
        
        return response
    
    def _generate_agent_response(self, agent_name: str, role: str, model: str, query: str, context: dict) -> str:
        """Generate response based on agent's role and model characteristics"""
        
        # This is where the actual response would be generated
        # For now, return a structured response that shows agent is responding
        
        if role == "Product Manager":
            return f"""   Analizuję Twoje pytanie z perspektywy Product Managera:
   
   '{query}'
   
   Z mojej perspektywy (używając {model}), ważne są:
   • Potrzeby użytkowników
   • Wartość biznesowa
   • Priorytetyzacja funkcji
   • Doświadczenie użytkownika
   
   Mogę zadać kilka pytań, żeby lepiej zrozumieć wymagania..."""
        
        elif role == "Architect":
            return f"""   Patrzę na to z perspektywy architekta (używając {model}):
   
   '{query}'
   
   Moja analiza techniczna:
   • Wybór odpowiedniego stacku technologicznego
   • Skalowalność rozwiązania
   • Bezpieczeństwo architektury
   • Wydajność systemu
   
   Mogę zaproponować konkretną architekturę..."""
        
        elif role == "Developer":
            return f"""   Jako developer (używając {model}), myślę o implementacji:
   
   '{query}'
   
   Moje podejście:
   • Praktyczna implementacja
   • Jakość kodu
   • Wydajność
   • Maintainability
   
   Mogę zaproponować konkretne rozwiązanie..."""
        
        elif role == "QA Engineer":
            return f"""   Z perspektywy QA (używając {model}), analizuję:
   
   '{query}'
   
   Moje podejście:
   • Testy jednostkowe i integracyjne
   • Edge cases
   • Jakość i niezawodność
   • Proces testowania
   
   Mogę stworzyć plan testów..."""
        
        elif role == "DevOps Engineer":
            return f"""   Jako DevOps (używając {model}), myślę o deploymentzie:
   
   '{query}'
   
   Moje podejście:
   • CI/CD pipeline
   • Infrastruktura
   • Monitoring
   • Automatyzacja
   
   Mogę zaproponować rozwiązanie deployment..."""
        
        elif role == "Security Specialist":
            return f"""   Z perspektywy Security (używając {model}), analizuję:
   
   '{query}'
   
   Moje podejście:
   • Bezpieczeństwo
   • Compliance
   • Weryfikacja bezpieczeństwa
   • Best practices
   
   Mogę stworzyć checklist bezpieczeństwa..."""
        
        elif role == "Data Scientist":
            return f"""   Jako Data Scientist (używając {model}), analizuję:
   
   '{query}'
   
   Moje podejście:
   • Analiza danych
   • Modele ML
   • Statystyka
   • Wizualizacja danych
   
   Mogę zaproponować podejście do analizy danych..."""
        
        else:
            return f"   Odpowiadam jako {agent_name} ({role}) używając {model}"
    
    def _respond_as_orchestrator(self, user_message: str) -> str:
        """Respond as orchestrator"""
        return f"""
🎯 ALEKSANDER NOWAK (Orchestrator):
   'Rozumiem Twoje pytanie. Przekierowuję do odpowiedniego członka zespołu...'
   
   '{user_message}'
   
   [Automatycznie rozpoznaję najlepszego członka zespołu do odpowiedzi]
"""

# Global orchestrator instance
orchestrator = AutoTeamOrchestrator()

def ask_team(question: str) -> str:
    """Ask the team a question - automatic routing"""
    return orchestrator.process_message(question)
