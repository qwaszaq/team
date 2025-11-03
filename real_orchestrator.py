"""
Live Real Multi-Model Team Session
Alex (Orchestrator) routes to actual team members with their assigned models
Each agent maintains independent context and uses their specific AI model
"""

from destiny_team import DestinyTeam, MessageType, ProjectPhase
from typing import Dict
import json


class RealTeamOrchestrator:
    """
    Alex Morgan - Real Orchestrator
    Routes messages to team members who use their actual assigned AI models
    """
    
    def __init__(self):
        self.team = DestinyTeam()
        self.project_state = None
        self.agent_contexts = {}  # Track each agent's independent context
        
        # Initialize contexts for each agent
        for name, agent in self.team.message_bus.agents.items():
            self.agent_contexts[name] = {
                "conversation_history": [],
                "personal_knowledge": {},
                "shared_knowledge": []
            }
    
    def route_to_agent(self, agent_name: str, query: str, include_context: bool = True) -> str:
        """
        Route a query to a specific agent with their independent context
        In production, this would call the actual AI model API
        """
        
        agent = self.team.message_bus.agents.get(agent_name)
        if not agent:
            return f"Agent {agent_name} not found"
        
        # Build context from this agent's independent conversation history
        context = self._build_agent_context(agent_name, include_context)
        
        # In production, this would call:
        # response = call_ai_model(agent.model_name, context, query)
        # For now, we'll use a structured approach that shows real model routing
        
        # Update agent's conversation history
        self.agent_contexts[agent_name]["conversation_history"].append({
            "role": "user",
            "content": query
        })
        
        # Generate response based on agent's model and personality
        response = self._get_agent_response(agent, query, context)
        
        # Store response in agent's conversation history
        self.agent_contexts[agent_name]["conversation_history"].append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _build_agent_context(self, agent_name: str, include_shared: bool) -> str:
        """Build context from agent's independent conversation history"""
        agent = self.team.message_bus.agents[agent_name]
        context = self.agent_contexts[agent_name]
        
        parts = []
        parts.append(f"Agent: {agent.name} ({agent.role})")
        parts.append(f"Model: {agent.model_name}")
        parts.append(f"Personality: {', '.join(agent.personality.traits)}")
        
        # Add agent's personal conversation history
        if context["conversation_history"]:
            parts.append("\nPrevious conversation:")
            for msg in context["conversation_history"][-5:]:  # Last 5 messages
                parts.append(f"{msg['role']}: {msg['content']}")
        
        # Add personal knowledge
        if context["personal_knowledge"]:
            parts.append(f"\nPersonal knowledge: {json.dumps(context['personal_knowledge'], indent=2)}")
        
        # Optionally include shared knowledge
        if include_shared and context["shared_knowledge"]:
            parts.append("\nInformation from team:")
            for msg in context["shared_knowledge"][-3:]:
                parts.append(f"{msg['from']}: {msg['content']}")
        
        return "\n".join(parts)
    
    def _get_agent_response(self, agent, query: str, context: str) -> str:
        """
        Get response from agent's assigned AI model
        This is where we'd call the actual API
        """
        
        # For now, return a response that indicates the model that would be used
        # In production, replace with actual API call:
        # 
        # if agent.model_name == "gpt-5":
        #     return call_openai_gpt5(context, query)
        # elif agent.model_name == "claude-sonnet-4.5":
        #     return call_anthropic_claude(context, query)
        # elif agent.model_name == "claude-codex":
        #     return call_anthropic_codex(context, query)
        # elif agent.model_name == "gemini-pro-2.5":
        #     return call_google_gemini(context, query)
        
        # Placeholder that shows which model would be called
        return f"[{agent.model_name} response for {agent.name} would be generated here]"
    
    def get_agent_context_status(self, agent_name: str) -> Dict:
        """Get status of agent's independent context"""
        agent = self.team.message_bus.agents.get(agent_name)
        if not agent:
            return {}
        
        context = self.agent_contexts[agent_name]
        return {
            "name": agent.name,
            "role": agent.role,
            "model": agent.model_name,
            "conversation_messages": len(context["conversation_history"]),
            "personal_knowledge_items": len(context["personal_knowledge"]),
            "shared_knowledge_messages": len(context["shared_knowledge"])
        }
