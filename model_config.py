"""
Easy Model Configuration System
Change any team member's model assignment easily - just edit this file!
"""

# ============================================
# MODEL ASSIGNMENTS - CHANGE HERE!
# ============================================
# Simply change the model name next to any agent

TEAM_MODEL_ASSIGNMENTS = {
    "Aleksander Nowak": "claude-sonnet-4.5",  # Orchestrator
    "Magdalena Kowalska": "gpt-5",  # Product Manager
    "Katarzyna Wiśniewska": "gpt-5",  # Architect
    "Tomasz Zieliński": "claude-codex",  # Developer
    "Anna Nowakowska": "gemini-pro-2.5",  # QA Engineer
    "Piotr Szymański": "gpt-5",  # DevOps Engineer
    "Michał Dąbrowski": "claude-sonnet-4.5",  # Security Specialist
    "Dr. Joanna Wójcik": "gemini-pro-2.5"  # Data Scientist - CHANGE THIS TO ANY MODEL BELOW!
}

# Available Models in Cursor (you can switch to these)
AVAILABLE_MODELS = [
    "gpt-5",
    "gpt-5-high",
    "claude-sonnet-4.5",
    "claude-codex",
    "gemini-pro-2.5"
]

def get_model_for_agent(agent_name: str) -> str:
    """Get the assigned model for an agent"""
    return TEAM_MODEL_ASSIGNMENTS.get(agent_name, "gpt-5")

def set_model_for_agent(agent_name: str, model: str):
    """Change an agent's model assignment - SUPER EASY!"""
    if model not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model} not available. Choose from: {AVAILABLE_MODELS}")
    
    if agent_name not in TEAM_MODEL_ASSIGNMENTS:
        raise ValueError(f"Agent {agent_name} not found")
    
    old_model = TEAM_MODEL_ASSIGNMENTS[agent_name]
    TEAM_MODEL_ASSIGNMENTS[agent_name] = model
    print(f"✅ {agent_name} changed from {old_model} → {model}")

def show_model_assignments():
    """Show current model assignments"""
    print("\n" + "=" * 70)
    print("CURRENT MODEL ASSIGNMENTS")
    print("=" * 70)
    print()
    for agent, model in TEAM_MODEL_ASSIGNMENTS.items():
        print(f"  {agent:30s} → {model}")
    print("\n💡 To change a model, edit model_config.py or use:")
    print("   set_model_for_agent('Agent Name', 'model-name')\n")

def show_available_models():
    """Show available models"""
    print("\n" + "=" * 70)
    print("AVAILABLE MODELS")
    print("=" * 70)
    print()
    for model in AVAILABLE_MODELS:
        print(f"  • {model}")
    print()

# Quick change functions for common scenarios
def set_data_scientist_to_gemini():
    """Quick function: Set Data Scientist to Gemini Pro 2.5"""
    set_model_for_agent("Dr. Joanna Wójcik", "gemini-pro-2.5")

def set_data_scientist_to_gpt5():
    """Quick function: Set Data Scientist to GPT-5"""
    set_model_for_agent("Dr. Joanna Wójcik", "gpt-5")

def set_data_scientist_to_gpt5_high():
    """Quick function: Set Data Scientist to GPT-5 High"""
    set_model_for_agent("Dr. Joanna Wójcik", "gpt-5-high")
