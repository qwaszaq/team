"""
LMStudio LLM Client - Core Integration
Aleksander Nowak & Tomasz Zieliński
2025-11-05
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import urllib.request
import urllib.error


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    tokens_used: Dict[str, int]
    time_taken: float
    success: bool
    error: Optional[str] = None


class LMStudioLLMClient:
    """
    Client for LMStudio local LLM
    
    Tested and verified working with:
    - openai/gpt-oss-20b (quality, 44k context)
    - gemma-3-12b-it (speed, 44k context)
    
    Server: 192.168.200.226:1234
    """
    
    def __init__(
        self,
        base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        timeout: int = 120
    ):
        """
        Initialize LMStudio client
        
        Args:
            base_url: LMStudio API endpoint
            model: Model to use (openai/gpt-oss-20b or gemma-3-12b-it)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        # Model registry
        self.models = {
            "default": "openai/gpt-oss-20b",      # Quality
            "fast": "gemma-3-12b-it",             # Speed
            "quality": "openai/gpt-oss-20b",      # Alias
            "speed": "gemma-3-12b-it"             # Alias
        }
        
        # Context limits
        self.context_limits = {
            "openai/gpt-oss-20b": 44000,
            "gemma-3-12b-it": 44000
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None
    ) -> LLMResponse:
        """
        Send chat completion request to LMStudio
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            model: Override default model
            
        Returns:
            LLMResponse with content and metadata
        """
        url = f"{self.base_url}/chat/completions"
        
        # Use provided or default values
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        model_name = model if model is not None else self.model
        
        # Resolve model aliases
        if model_name in self.models:
            model_name = self.models[model_name]
        
        # Build request
        data = {
            "model": model_name,
            "messages": messages,
            "temperature": temp,
            "max_tokens": tokens
        }
        
        try:
            start_time = time.time()
            
            # Make request
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                elapsed = time.time() - start_time
                
                # Parse response
                content = result['choices'][0]['message']['content']
                usage = result.get('usage', {})
                
                return LLMResponse(
                    content=content,
                    model=model_name,
                    tokens_used={
                        'prompt': usage.get('prompt_tokens', 0),
                        'completion': usage.get('completion_tokens', 0),
                        'total': usage.get('total_tokens', 0)
                    },
                    time_taken=elapsed,
                    success=True
                )
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return LLMResponse(
                content="",
                model=model_name,
                tokens_used={},
                time_taken=0,
                success=False,
                error=f"HTTP {e.code}: {error_body}"
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                model=model_name,
                tokens_used={},
                time_taken=0,
                success=False,
                error=str(e)
            )
    
    def simple_prompt(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Simple single-turn prompt (convenience method)
        
        Args:
            prompt: User prompt
            model: Optional model override
            
        Returns:
            Response content as string
        """
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages, model=model)
        return response.content if response.success else f"Error: {response.error}"
    
    def analyze_document(
        self,
        document: str,
        analysis_type: str,
        context: Optional[str] = None
    ) -> LLMResponse:
        """
        Analyze document with specific analysis type
        
        Args:
            document: Document text to analyze
            analysis_type: Type of analysis (financial, legal, risk, etc.)
            context: Optional additional context
            
        Returns:
            LLMResponse with analysis
        """
        system_prompts = {
            "financial": "You are a financial analyst. Analyze documents for financial insights, risks, and patterns.",
            "legal": "You are a legal expert. Analyze documents for legal implications, compliance issues, and risks.",
            "risk": "You are a risk analyst. Identify and assess risks in the provided documents.",
            "general": "You are a helpful analyst. Provide comprehensive analysis of the document."
        }
        
        system_prompt = system_prompts.get(analysis_type, system_prompts["general"])
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Context: {context}\n\nDocument to analyze:\n{document}"
            })
        else:
            messages.append({
                "role": "user",
                "content": f"Analyze this document:\n\n{document}"
            })
        
        return self.chat_completion(messages)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (4 chars ≈ 1 token)
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def check_context_limit(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Check if messages fit in context window
        
        Args:
            messages: Messages to check
            
        Returns:
            Dict with fit status and token info
        """
        total_text = " ".join(msg["content"] for msg in messages)
        estimated_tokens = self.estimate_tokens(total_text)
        limit = self.context_limits.get(self.model, 44000)
        
        return {
            "fits": estimated_tokens < limit,
            "estimated_tokens": estimated_tokens,
            "limit": limit,
            "usage_percent": (estimated_tokens / limit) * 100
        }
    
    def health_check(self) -> bool:
        """
        Check if LMStudio server is responding
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            response = self.simple_prompt("test")
            return len(response) > 0
        except:
            return False


# Convenience function for quick usage
def quick_analyze(text: str, analysis_type: str = "general") -> str:
    """
    Quick one-liner for analysis
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis
        
    Returns:
        Analysis result
    """
    client = LMStudioLLMClient()
    response = client.analyze_document(text, analysis_type)
    return response.content if response.success else f"Error: {response.error}"


if __name__ == "__main__":
    # Test the client
    print("🧪 Testing LMStudio Client...")
    
    client = LMStudioLLMClient()
    
    # Health check
    print("\n1. Health check...")
    healthy = client.health_check()
    print(f"   {'✅' if healthy else '❌'} LMStudio: {'Healthy' if healthy else 'Down'}")
    
    if healthy:
        # Simple test
        print("\n2. Simple prompt test...")
        response = client.simple_prompt("What is 2+2? Answer briefly.")
        print(f"   Response: {response}")
        
        # Document analysis test
        print("\n3. Document analysis test...")
        test_doc = "Revenue increased 23% to $4.2M. Operating expenses rose 18%. Margins improved to 32%."
        analysis = client.analyze_document(test_doc, "financial")
        print(f"   Analysis: {analysis.content[:200]}...")
        print(f"   Tokens: {analysis.tokens_used}")
        print(f"   Time: {analysis.time_taken:.2f}s")
    
    print("\n✅ Tests complete!")
