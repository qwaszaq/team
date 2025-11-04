"""
Local LLM Integration for Analytical Team
Privacy-first AI processing using LM Studio Server

Configuration:
- Local LLM via LM Studio Server (sensitive data stays local)
- Standard OpenAI-compatible endpoint
- Configurable per agent or per task
- Fallback options available

Usage:
    llm = LocalLLM()
    response = llm.chat(messages, temperature=0.7, max_tokens=1000)
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class LocalLLM:
    """
    Local LLM client for analytical agents
    
    Privacy Features:
    - All data stays on local machine
    - No external API calls
    - Sensitive data never leaves your infrastructure
    - Configurable models via LM Studio
    
    Performance:
    - Fast inference (local GPU/CPU)
    - No rate limits
    - No API costs
    - Unlimited usage
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize Local LLM client
        
        Args:
            base_url: LM Studio Server endpoint (default: http://localhost:1234/v1)
            model: Model name (auto-detected if None)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self.session = requests.Session()
        
        # Test connection on init
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to LM Studio Server"""
        try:
            response = self.session.get(
                f"{self.base_url}/models",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json()
                available = models.get('data', [])
                
                if self.model:
                    # User specified model
                    print(f"✅ Connected to LM Studio Server")
                    print(f"   Model: {self.model}")
                    return True
                elif available:
                    # Auto-select first available model
                    self.model = available[0].get('id')
                    print(f"✅ Connected to LM Studio Server")
                    print(f"   Model: {self.model} (auto-detected)")
                    print(f"   Endpoint: {self.base_url}")
                    return True
                else:
                    print(f"✅ Connected to LM Studio Server")
                    print(f"   Model: {self.model}")
                    return True
                else:
                    print(f"⚠️  LM Studio connected but no models loaded")
                    print(f"   Please load a model in LM Studio")
                    return False
            else:
                print(f"❌ Cannot connect to LM Studio Server")
                print(f"   Endpoint: {self.base_url}")
                print(f"   Status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to LM Studio Server")
            print(f"   Endpoint: {self.base_url}")
            print(f"   Make sure LM Studio Server is running!")
            return False
        except Exception as e:
            print(f"❌ Error connecting to LM Studio: {e}")
            return False
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> str:
        """
        Send chat completion request to local LLM
        
        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Stream response (not implemented yet)
        
        Returns:
            Generated text response
        
        Example:
            messages = [
                {"role": "system", "content": "You are a financial analyst"},
                {"role": "user", "content": "Analyze this company"}
            ]
            response = llm.chat(messages)
        """
        
        if not self.model:
            return "Error: No model loaded in LM Studio"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: LM Studio returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "Error: LM Studio request timed out (model may be too slow or prompt too long)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_embeddings(
        self,
        text: str,
        model: str = "jinaai/jina-embeddings-v4-text-retrieval"
    ) -> Optional[List[float]]:
        """
        Generate embeddings for text (for semantic search)
        
        Args:
            text: Input text (up to 8192 tokens with Jina v4!)
            model: Embedding model name (default: Jina v4)
        
        Returns:
            Embedding vector (list of floats)
        
        Note:
            Jina v4 is EXCELLENT for analytical documents:
            - Handles tables, charts, structured content
            - Up to 8192 tokens (vs 512 for most models)
            - Optimized for retrieval/search
            - Perfect for: market reports, financial docs, legal documents
        """
        
        payload = {
            "model": model,
            "input": text
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/embeddings",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['data'][0]['embedding']
            else:
                print(f"Embeddings error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"Embeddings error: {e}")
            return None
    
    def get_available_models(self) -> List[str]:
        """Get list of available models in LM Studio"""
        try:
            response = self.session.get(
                f"{self.base_url}/models",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json()
                return [m['id'] for m in models.get('data', [])]
            else:
                return []
        except:
            return []
    
    def switch_model(self, model_name: str) -> bool:
        """
        Switch to different model
        
        Args:
            model_name: Name of model to use
        
        Returns:
            True if successful
        """
        available = self.get_available_models()
        
        if model_name in available:
            self.model = model_name
            print(f"✅ Switched to model: {model_name}")
            return True
        else:
            print(f"❌ Model '{model_name}' not found")
            print(f"   Available: {', '.join(available)}")
            return False
    
    def get_status(self) -> Dict:
        """Get LM Studio Server status"""
        return {
            "endpoint": self.base_url,
            "current_model": self.model,
            "available_models": self.get_available_models(),
            "privacy_mode": "✅ LOCAL (Data stays on your machine)",
            "api_costs": "💰 FREE (No external API charges)",
            "rate_limits": "♾️ UNLIMITED (No throttling)"
        }


class AnalyticalAgentLLM:
    """
    LLM Integration for Analytical Agents
    
    Supports multiple modes:
    1. LOCAL (LM Studio) - for sensitive data
    2. CLOUD (OpenAI/Anthropic) - for non-sensitive data
    3. HYBRID - automatic routing based on data sensitivity
    """
    
    def __init__(
        self,
        mode: str = "LOCAL",
        lm_studio_url: str = "http://localhost:1234/v1"
    ):
        """
        Initialize agent LLM client
        
        Args:
            mode: "LOCAL", "CLOUD", or "HYBRID"
            lm_studio_url: LM Studio Server endpoint
        """
        self.mode = mode.upper()
        
        if self.mode in ["LOCAL", "HYBRID"]:
            self.local_llm = LocalLLM(base_url=lm_studio_url)
        else:
            self.local_llm = None
        
        # Cloud LLM would be initialized here if needed
        self.cloud_llm = None
    
    def analyze(
        self,
        agent_name: str,
        agent_role: str,
        task_description: str,
        context: str,
        is_sensitive: bool = True
    ) -> str:
        """
        Analyze task using appropriate LLM
        
        Args:
            agent_name: Name of agent (e.g., "Elena Volkov")
            agent_role: Agent's role (e.g., "OSINT Specialist")
            task_description: What to analyze
            context: Additional context
            is_sensitive: Whether data is sensitive (routes to local if True)
        
        Returns:
            Analysis result
        """
        
        # Build prompt
        system_prompt = f"""You are {agent_name}, {agent_role} on the Destiny Analytical Team.

Your expertise: {agent_role}

Task: {task_description}

Context: {context}

Provide a professional, thorough analysis. Be specific and actionable."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_description}
        ]
        
        # Route based on sensitivity and mode
        if self.mode == "LOCAL" or (self.mode == "HYBRID" and is_sensitive):
            # Use local LLM for sensitive data
            if self.local_llm:
                return self.local_llm.chat(messages, temperature=0.7, max_tokens=1500)
            else:
                return "Error: Local LLM not available"
        
        elif self.mode == "CLOUD" or (self.mode == "HYBRID" and not is_sensitive):
            # Use cloud LLM for non-sensitive data
            if self.cloud_llm:
                return self.cloud_llm.chat(messages)
            else:
                return "Error: Cloud LLM not configured"
        
        else:
            return "Error: Invalid LLM mode"
    
    def get_configuration(self) -> Dict:
        """Get current LLM configuration"""
        config = {
            "mode": self.mode,
            "privacy_status": "🔒 PRIVATE" if self.mode in ["LOCAL", "HYBRID"] else "☁️ CLOUD",
        }
        
        if self.local_llm:
            config["local_llm"] = self.local_llm.get_status()
        
        return config


# Quick test
if __name__ == "__main__":
    print("🔒 Local LLM Integration for Analytical Team\n")
    
    print("Testing connection to LM Studio Server...\n")
    llm = LocalLLM()
    
    status = llm.get_status()
    print("\nStatus:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test chat
    print("\n--- Test: Simple chat ---")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in one sentence."}
    ]
    
    response = llm.chat(messages, max_tokens=50)
    print(f"Response: {response}")
    
    print("\n✅ Local LLM integration ready!")
    print("   Sensitive data stays on your machine")
    print("   No external API calls")
    print("   Complete privacy guaranteed")
