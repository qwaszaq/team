"""
Live Team Session with Easy Model Switching
Alex orchestrates, you switch models in Cursor when needed
"""

from model_config import (
    TEAM_MODEL_ASSIGNMENTS, 
    get_model_for_agent, 
    set_model_for_agent,
    show_model_assignments,
    show_available_models
)
from agent_contexts import AGENT_CONTEXTS, update_agent_context, get_agent_context


class LiveTeamOrchestrator:
    """
    Alex Morgan - Real Orchestrator
    Routes messages and tells you which model to switch to
    """
    
    def __init__(self):
        self.current_project = None
        
    def route_message(self, user_message: str) -> str:
        """
        Route message to appropriate team member
        Returns instruction on which model to switch to
        """
        message_lower = user_message.lower()
        
        # Detect which agent should handle this
        if any(word in message_lower for word in ['user', 'who', 'what', 'problem', 'feature', 'requirements']):
            agent = "Magdalena Kowalska"
            role = "Product Manager"
        
        elif any(word in message_lower for word in ['architecture', 'tech', 'stack', 'database', 'design']):
            agent = "Katarzyna Wiśniewska"
            role = "Architect"
        
        elif any(word in message_lower for word in ['code', 'implement', 'build', 'write', 'develop']):
            agent = "Tomasz Zieliński"
            role = "Developer"
        
        elif any(word in message_lower for word in ['test', 'bug', 'quality', 'qa']):
            agent = "Anna Nowakowska"
            role = "QA Engineer"
        
        elif any(word in message_lower for word in ['deploy', 'host', 'server', 'infrastructure', 'devops']):
            agent = "Piotr Szymański"
            role = "DevOps Engineer"
        
        elif any(word in message_lower for word in ['security', 'safe', 'secure', 'protection']):
            agent = "Michał Dąbrowski"
            role = "Security Specialist"
        
        elif any(word in message_lower for word in ['data', 'ml', 'machine learning', 'dataset', 'analytics']):
            agent = "Dr. Joanna Wójcik"
            role = "Data Scientist"
        
        else:
            agent = "Aleksander Nowak"
            role = "Orchestrator"
        
        # Get assigned model for this agent
        model = get_model_for_agent(agent)
        
        # Update agent's context
        update_agent_context(agent, "user", user_message)
        
        # Return routing instruction
        return f"""
🎯 ALEX MORGAN (Orchestrator):
   'Routing to {agent} ({role})'
   
   📌 PLEASE SWITCH TO: {model}
   
   [Once you've switched, I'll respond as {agent} using {model}]
   
   Current context for {agent}:
   • Conversation messages: {len(get_agent_context(agent).get('conversation_history', []))}
   • Model: {model}
"""

    def show_current_assignments(self):
        """Show current model assignments"""
        show_model_assignments()

# Example usage functions
def change_model(agent_name: str, new_model: str):
    """Easy function to change an agent's model"""
    set_model_for_agent(agent_name, new_model)
    print(f"\n✅ {agent_name} will now use {new_model}")
    print(f"   When routing to {agent_name}, switch to {new_model} in Cursor\n")

def show_team():
    """Show team and their models"""
    show_model_assignments()
