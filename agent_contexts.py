"""
ALEX MORGAN - Real Orchestrator Session
Maintaining independent contexts for each team member
"""

# Independent Context Storage for Each Agent
AGENT_CONTEXTS = {
    "Aleksander Nowak": {
        "model": "claude-sonnet-4.5",
        "conversation_history": [],
        "knowledge": {},
        "role": "Orchestrator"
    },
    "Magdalena Kowalska": {
        "model": "gpt-5",
        "conversation_history": [],
        "knowledge": {},
        "role": "Product Manager"
    },
    "Katarzyna Wi?niewska": {
        "model": "gpt-5", 
        "conversation_history": [],
        "knowledge": {},
        "role": "Architect"
    },
    "Tomasz Zieli?ski": {
        "model": "claude-codex",
        "conversation_history": [],
        "knowledge": {},
        "role": "Developer"
    },
    "Anna Nowakowska": {
        "model": "gemini-pro-2.5",
        "conversation_history": [],
        "knowledge": {},
        "role": "QA Engineer"
    },
    "Piotr Szyma?ski": {
        "model": "gpt-5",
        "conversation_history": [],
        "knowledge": {},
        "role": "DevOps Engineer"
    },
    "Micha? D?browski": {
        "model": "claude-sonnet-4.5",
        "conversation_history": [],
        "knowledge": {},
        "role": "Security Specialist"
    },
    "Dr. Joanna W?jcik": {
        "model": "gemini-pro-2.5",
        "conversation_history": [],
        "knowledge": {},
        "role": "Data Scientist"
    }
}

def get_agent_context(agent_name: str) -> dict:
    """Get agent's independent context"""
    return AGENT_CONTEXTS.get(agent_name, {})

def update_agent_context(agent_name: str, role: str, content: str):
    """Update agent's conversation history"""
    if agent_name not in AGENT_CONTEXTS:
        AGENT_CONTEXTS[agent_name] = {
            "conversation_history": [],
            "knowledge": {}
        }
    AGENT_CONTEXTS[agent_name]["conversation_history"].append({
        "role": role,
        "content": content,
        "timestamp": "now"
    })
