"""
LM Studio Chat Integration for Destiny Chat UI
Uses local LLM via LM Studio for real AI responses
"""

import requests
from typing import List, Dict, Optional


class LMStudioChat:
    """
    Client for LM Studio chat completions.
    Compatible with OpenAI API format but uses local model.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "local-model"  # Will use whatever is loaded
    ):
        self.base_url = base_url.rstrip('/')
        self.model = model
        
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 800,
        stream: bool = False
    ) -> str:
        """
        Generate chat completion using LM Studio.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Max tokens to generate
            stream: Whether to stream response
            
        Returns:
            Generated response text
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": stream
                },
                timeout=60
            )
            
            if response.status_code != 200:
                return f"❌ LM Studio error: {response.status_code}"
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            return f"❌ Cannot connect to LM Studio: {e}"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def create_agent_prompt(
        self,
        agent_name: str,
        agent_role: str,
        specialization: str,
        user_message: str
    ) -> List[Dict[str, str]]:
        """
        Create prompt messages for agent with personality.
        
        Args:
            agent_name: Name of the agent
            agent_role: Role/title of the agent
            specialization: What agent specializes in
            user_message: User's message
            
        Returns:
            List of messages for chat completion
        """
        
        # Special handling for Aleksander (Orchestrator)
        if "Orchestrator" in agent_role or "Lead" in agent_role:
            system_prompt = f"""You are {agent_name}, the Technical Lead and Orchestrator of Destiny Team.

Your role: Coordinate team, delegate tasks, make decisions.

CRITICAL RULES:
1. DO NOT introduce yourself every time - user knows who you are
2. When user asks to "do something" or "add feature" - DELEGATE to appropriate agent:
   - Code/Implementation → Tomasz Kamiński (Developer)
   - UI/UX/Colors → Joanna Mazur (Designer)
   - Testing → Anna Lewandowska (QA)
   - Architecture → Katarzyna Zielińska (Architect)
3. Be ACTION-oriented: "I'll assign this to X" not "I can help with..."
4. Polish language only
5. NEVER repeat yourself

Example response format:
"Rozumiem. To zadanie dla [Agent Name]. 
[Agent] zajmie się: [konkretny plan]
Rozpoczynam pracę."

BE BRIEF. NO FLUFF. ACTION ONLY."""
        else:
            system_prompt = f"""You are {agent_name}, a {agent_role} in the Destiny Team.

Specialization: {specialization}

RULES:
1. DO NOT introduce yourself - just answer the question
2. Be ACTIONABLE - give specific steps or solutions
3. Polish language only
4. Be concise (max 150 words)
5. If it's a task - say what you'll do, not what you can do

Example: User asks "change colors" 
BAD: "I can help with colors..."
GOOD: "Zmieniam kolorystykę na: [specific colors]. Poprawiam CSS teraz."

BE DIRECT. TAKE ACTION."""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    
    def test_connection(self) -> bool:
        """Test if LM Studio chat API is available"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json()
                available = models.get('data', [])
                if available:
                    print(f"✅ LM Studio chat available!")
                    print(f"   Loaded model: {available[0]['id']}")
                    return True
                else:
                    print(f"⚠️  LM Studio running but no model loaded")
                    return False
            else:
                print(f"❌ LM Studio returned: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to LM Studio: {e}")
            return False


# Quick test
if __name__ == "__main__":
    chat = LMStudioChat()
    
    print("Testing LM Studio chat connection...")
    if chat.test_connection():
        print("\nTesting chat completion...")
        
        messages = chat.create_agent_prompt(
            agent_name="Tomasz Zieliński",
            agent_role="Senior Developer",
            specialization="Full-stack development, Python, System architecture",
            user_message="Cześć! Jak mogę zbudować REST API?"
        )
        
        response = chat.chat(messages, temperature=0.7, max_tokens=500)
        print("\nResponse:")
        print(response)
    else:
        print("\n⚠️  Make sure LM Studio is running with a model loaded!")
        print("   Open LM Studio → Load a chat model → Start server")
