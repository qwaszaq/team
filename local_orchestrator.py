"""
Local LLM Orchestrator - On-Prem Intelligence System
Uses LMStudio local model with local toolkits
Supervised by Aleksander (Claude) for quality assurance

Architecture:
- Local LLM (LMStudio): Executes investigations, uses tools
- Local Toolkits: Scraping, Math, Data Analysis
- Structured Logging: All actions logged for supervisor review
- File-based Communication: Simple, reliable, no network dependencies
"""

import requests
import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging
from pathlib import Path
import sys

# Import local toolkits
try:
    from agents.analytical.tools.scraping_toolkit import ScrapingToolkit
    from agents.analytical.tools.mathematical_toolkit import MathematicalToolkit
    HAS_TOOLKITS = True
except ImportError:
    HAS_TOOLKITS = False
    print("⚠️  Warning: Toolkits not available. Install dependencies or check import paths.")


class LocalLLMOrchestrator:
    """
    Local LLM-based investigation orchestrator
    
    Uses:
    - LMStudio API for local LLM inference (OpenAI-compatible)
    - Local toolkits for scraping, analysis, calculations
    - Structured logging for supervisor (Aleksander) review
    
    Workflow:
    1. Receive task from supervisor
    2. Execute using local LLM + tools
    3. Log all actions (JSONL format)
    4. Save results for review
    5. Supervisor assesses quality
    6. Iterate if needed
    """
    
    def __init__(
        self,
        lmstudio_url: str = "http://localhost:1234/v1",
        model_name: str = "local-model",  # Whatever is loaded in LMStudio
        log_dir: str = "./logs/local_llm",
        workspace_dir: str = "./shared_workspace"
    ):
        """
        Initialize Local LLM Orchestrator
        
        Args:
            lmstudio_url: LMStudio API endpoint
            model_name: Model identifier (for logging)
            log_dir: Where to store investigation logs
            workspace_dir: Shared workspace for supervisor communication
        """
        self.lmstudio_url = lmstudio_url
        self.model_name = model_name
        self.log_dir = Path(log_dir)
        self.workspace_dir = Path(workspace_dir)
        
        # Create directories
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "tasks").mkdir(exist_ok=True)
        (self.workspace_dir / "results").mkdir(exist_ok=True)
        (self.workspace_dir / "guidance").mkdir(exist_ok=True)
        
        # Action log (in-memory + file)
        self.action_log = []
        self.current_log_file = None
        
        # Setup logging
        self.setup_logging()
        
        # Initialize toolkits
        if HAS_TOOLKITS:
            self.scraping = ScrapingToolkit()
            self.math = MathematicalToolkit()
            print("✅ Toolkits initialized: ScrapingToolkit, MathematicalToolkit")
        else:
            self.scraping = None
            self.math = None
            print("⚠️  Toolkits not available - running in limited mode")
        
        # Define available tools
        self.tools = self._initialize_tools()
        
        print(f"✅ LocalLLMOrchestrator initialized")
        print(f"   LMStudio: {self.lmstudio_url}")
        print(f"   Model: {self.model_name}")
        print(f"   Tools: {len(self.tools)} available")
    
    def setup_logging(self):
        """Setup structured logging for Aleksander review"""
        # Console logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
    
    def start_investigation(self, investigation_id: str):
        """Start new investigation logging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = self.log_dir / f"investigation_{investigation_id}_{timestamp}.jsonl"
        self.action_log = []
        
        self.log_action({
            "type": "investigation_start",
            "investigation_id": investigation_id,
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name
        })
    
    def log_action(self, action: Dict):
        """
        Log action in structured format for supervisor review
        Writes to JSONL file (one JSON per line)
        """
        # Add to in-memory log
        self.action_log.append(action)
        
        # Write to file
        if self.current_log_file:
            with open(self.current_log_file, 'a') as f:
                f.write(json.dumps(action) + '\n')
        
        # Also log to console (abridged)
        action_type = action.get("type", "unknown")
        if action_type == "llm_call":
            self.logger.info(f"🤖 LLM Call: {len(action.get('messages', []))} messages")
        elif action_type == "llm_response":
            tokens = action.get("usage", {}).get("total_tokens", 0)
            self.logger.info(f"💬 LLM Response: {tokens} tokens")
        elif action_type == "tool_execution":
            tool = action.get("tool", "unknown")
            self.logger.info(f"🔧 Tool: {tool}")
        elif action_type == "tool_error":
            self.logger.error(f"❌ Tool Error: {action.get('error', '')}")
    
    def _initialize_tools(self) -> List[Dict]:
        """
        Define available tools for LLM function calling
        OpenAI-compatible format (LMStudio supports this)
        """
        tools = []
        
        # Tool 1: Scrape Webpage
        if self.scraping:
            tools.append({
                "type": "function",
                "function": {
                    "name": "scrape_webpage",
                    "description": "Scrape and parse a webpage. Extract text, links, tables, or metadata. Use this to collect information from websites.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to scrape (must include http:// or https://)"
                            },
                            "extract_type": {
                                "type": "string",
                                "enum": ["text", "links", "tables", "metadata", "all"],
                                "description": "What to extract: 'text' (main content), 'links' (all URLs), 'tables' (structured data), 'metadata' (title, description), or 'all' (everything)",
                                "default": "text"
                            }
                        },
                        "required": ["url"]
                    }
                }
            })
        
        # Tool 2: Calculate Statistics
        if self.math:
            tools.append({
                "type": "function",
                "function": {
                    "name": "calculate_statistics",
                    "description": "Calculate statistical measures from numerical data. Use this to analyze numbers, detect outliers, or perform statistical tests.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Array of numbers to analyze"
                            },
                            "analysis_type": {
                                "type": "string",
                                "enum": ["basic_stats", "outliers"],
                                "description": "'basic_stats' (mean, median, std, min, max) or 'outliers' (detect unusual values)",
                                "default": "basic_stats"
                            },
                            "outlier_threshold": {
                                "type": "number",
                                "description": "For outliers: number of standard deviations (typically 2 or 3)",
                                "default": 2
                            }
                        },
                        "required": ["data", "analysis_type"]
                    }
                }
            })
        
        # Tool 3: Archive Source
        if self.scraping:
            tools.append({
                "type": "function",
                "function": {
                    "name": "archive_source",
                    "description": "Archive a webpage locally for future reference. Use this for EVERY source you collect to ensure it's preserved.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to archive"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Source metadata: {title, author, date, credibility, description}",
                                "properties": {
                                    "title": {"type": "string"},
                                    "author": {"type": "string"},
                                    "date": {"type": "string"},
                                    "credibility": {
                                        "type": "string",
                                        "enum": ["high", "medium", "low"],
                                        "description": "Source credibility assessment"
                                    },
                                    "description": {"type": "string"}
                                }
                            }
                        },
                        "required": ["url"]
                    }
                }
            })
        
        return tools
    
    def call_llm(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict:
        """
        Call LMStudio local LLM
        Uses OpenAI-compatible API
        
        Returns:
            {
                "choices": [{
                    "message": {
                        "content": "...",
                        "tool_calls": [...]  # If using tools
                    }
                }],
                "usage": {"total_tokens": N}
            }
        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        # Log the call
        self.log_action({
            "type": "llm_call",
            "timestamp": datetime.now().isoformat(),
            "messages": [{"role": m["role"], "content": m.get("content", "")[:200] + "..."} for m in messages],
            "tools_available": len(tools) if tools else 0,
            "temperature": temperature,
            "max_tokens": max_tokens
        })
        
        try:
            response = requests.post(
                f"{self.lmstudio_url}/chat/completions",
                json=payload,
                timeout=180  # 3 minutes
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Log the response
            message = result.get("choices", [{}])[0].get("message", {})
            self.log_action({
                "type": "llm_response",
                "timestamp": datetime.now().isoformat(),
                "content": message.get("content", "")[:500] + "...",  # Truncate for logging
                "tool_calls": len(message.get("tool_calls", [])),
                "usage": result.get("usage", {})
            })
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.log_action({
                "type": "error",
                "timestamp": datetime.now().isoformat(),
                "error_type": "llm_call_failed",
                "error": str(e),
                "suggestion": "Check if LMStudio is running at " + self.lmstudio_url
            })
            raise RuntimeError(f"LMStudio API call failed: {e}")
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Any:
        """
        Execute a tool call from LLM
        Logs tool usage for supervisor review
        
        Returns:
            Tool result (dict, string, or list)
        """
        self.log_action({
            "type": "tool_execution",
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "arguments": {k: str(v)[:100] for k, v in arguments.items()}  # Truncate for logging
        })
        
        try:
            # Tool 1: Scrape Webpage
            if tool_name == "scrape_webpage":
                url = arguments.get("url")
                extract_type = arguments.get("extract_type", "text")
                
                if not self.scraping:
                    return {"error": "ScrapingToolkit not available"}
                
                # Fetch page
                html = self.scraping.fetch_page(url)
                if not html:
                    return {"error": f"Failed to fetch {url}"}
                
                # Parse
                parsed = self.scraping.parse_html(html)
                
                # Extract based on type
                if extract_type == "text":
                    result = {
                        "url": url,
                        "text": self.scraping.extract_text(parsed)
                    }
                elif extract_type == "links":
                    result = {
                        "url": url,
                        "links": self.scraping.extract_links(parsed, url)
                    }
                elif extract_type == "tables":
                    result = {
                        "url": url,
                        "tables": self.scraping.extract_tables(parsed)
                    }
                elif extract_type == "metadata":
                    result = {
                        "url": url,
                        "metadata": self.scraping.extract_metadata(parsed)
                    }
                else:  # all
                    result = {
                        "url": url,
                        "text": self.scraping.extract_text(parsed),
                        "links": self.scraping.extract_links(parsed, url)[:10],  # Limit
                        "metadata": self.scraping.extract_metadata(parsed)
                    }
                
                return result
            
            # Tool 2: Calculate Statistics
            elif tool_name == "calculate_statistics":
                data = arguments.get("data", [])
                analysis_type = arguments.get("analysis_type", "basic_stats")
                threshold = arguments.get("outlier_threshold", 2)
                
                if not self.math:
                    return {"error": "MathematicalToolkit not available"}
                
                if not data:
                    return {"error": "No data provided"}
                
                if analysis_type == "basic_stats":
                    result = self.math.basic_stats(data)
                elif analysis_type == "outliers":
                    outlier_indices = self.math.detect_outliers(data, threshold=threshold)
                    result = {
                        "data": data,
                        "outlier_indices": outlier_indices,
                        "outliers": [data[i] for i in outlier_indices],
                        "outlier_count": len(outlier_indices)
                    }
                else:
                    result = {"error": f"Unknown analysis type: {analysis_type}"}
                
                return result
            
            # Tool 3: Archive Source
            elif tool_name == "archive_source":
                url = arguments.get("url")
                metadata = arguments.get("metadata", {})
                
                if not self.scraping:
                    return {"error": "ScrapingToolkit not available"}
                
                archived = self.scraping.archive_page(url, metadata)
                return archived
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        
        except Exception as e:
            error_result = {
                "error": str(e),
                "tool": tool_name,
                "arguments": arguments
            }
            
            self.log_action({
                "type": "tool_error",
                "timestamp": datetime.now().isoformat(),
                **error_result
            })
            
            return error_result
    
    def run_investigation(
        self,
        task: str,
        context: Optional[Dict] = None,
        investigation_id: Optional[str] = None,
        max_iterations: int = 10
    ) -> Dict:
        """
        Run investigation using local LLM with tools
        
        Args:
            task: Investigation task description
            context: Additional context (optional)
            investigation_id: ID for this investigation
            max_iterations: Max LLM iterations (tool calls)
        
        Returns:
            {
                "investigation_id": "...",
                "task": "...",
                "result": "Investigation findings...",
                "iterations": N,
                "actions_count": N,
                "status": "complete" | "incomplete",
                "log_file": Path,
                "timestamp": "..."
            }
        """
        
        # Generate investigation ID if not provided
        if not investigation_id:
            investigation_id = f"inv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Start logging
        self.start_investigation(investigation_id)
        
        print(f"\n{'='*60}")
        print(f"🔍 INVESTIGATION: {investigation_id}")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        # System prompt for local LLM
        system_prompt = """You are a professional investigative analyst working on-premises.

Your capabilities:
- Web scraping (collect information from websites)
- Statistical analysis (analyze numerical data)
- Source archiving (preserve evidence)

Your responsibilities:
1. SOURCE ATTRIBUTION: Cite every source with URL, date, and credibility
2. ARCHIVING: Archive ALL sources immediately using archive_source tool
3. MULTI-SOURCE VERIFICATION: Use at least 3 independent sources for key facts
4. STATISTICAL RIGOR: Use calculate_statistics for any numerical analysis
5. TRANSPARENCY: Document your methodology and limitations

Quality standards:
- Your work will be reviewed by a supervisor (Aleksander)
- He will check: tool usage, source quality, analytical rigor, completeness
- Be thorough, professional, and honest about what you found vs. what you couldn't find

Available tools:
- scrape_webpage: Collect information from websites
- calculate_statistics: Analyze numerical data
- archive_source: Preserve sources (MANDATORY for every source)

Instructions:
- Start by planning your approach
- Use tools systematically
- Archive EVERY source
- Summarize findings with proper citations
- Be honest about limitations"""

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Investigation Task:\n{task}\n\n" + 
                          (f"Context:\n{json.dumps(context, indent=2)}\n\n" if context else "") +
                          "Please conduct this investigation using available tools. " +
                          "Remember to archive all sources and provide proper citations."
            }
        ]
        
        iteration = 0
        investigation_complete = False
        final_response = ""
        
        while not investigation_complete and iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{max_iterations} ---")
            
            # Call LLM with tools
            try:
                response = self.call_llm(messages, tools=self.tools if iteration < max_iterations else None)
            except Exception as e:
                print(f"❌ LLM call failed: {e}")
                break
            
            # Get response message
            message = response.get("choices", [{}])[0].get("message", {})
            messages.append(message)
            
            # Check for tool calls
            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                # No more tool calls = investigation complete
                investigation_complete = True
                final_response = message.get("content", "")
                print("✅ Investigation complete (no more tool calls)")
            else:
                # Execute tool calls
                print(f"🔧 Executing {len(tool_calls)} tool(s)...")
                
                for tool_call in tool_calls:
                    function = tool_call.get("function", {})
                    tool_name = function.get("name")
                    
                    try:
                        arguments = json.loads(function.get("arguments", "{}"))
                    except json.JSONDecodeError:
                        arguments = {}
                        print(f"⚠️  Failed to parse arguments for {tool_name}")
                    
                    # Execute tool
                    tool_result = self.execute_tool(tool_name, arguments)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.get("id", f"call_{iteration}"),
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    })
        
        # Finalize
        status = "complete" if investigation_complete else "max_iterations_reached"
        
        # Compile results
        result = {
            "investigation_id": investigation_id,
            "task": task,
            "context": context,
            "result": final_response,
            "iterations": iteration,
            "actions_count": len(self.action_log),
            "status": status,
            "log_file": str(self.current_log_file),
            "timestamp": datetime.now().isoformat()
        }
        
        # Save result for supervisor review
        result_file = self.workspace_dir / "results" / f"result_{investigation_id}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"✅ INVESTIGATION COMPLETE")
        print(f"{'='*60}")
        print(f"Status: {status}")
        print(f"Iterations: {iteration}")
        print(f"Actions logged: {len(self.action_log)}")
        print(f"Result file: {result_file}")
        print(f"Log file: {self.current_log_file}")
        print(f"\n📝 RESULT:\n{final_response[:500]}..." if len(final_response) > 500 else f"\n📝 RESULT:\n{final_response}")
        
        return result


def main():
    """
    Example usage of LocalLLMOrchestrator
    """
    print("🚀 LOCAL LLM ORCHESTRATOR - Proof of Concept")
    print("="*60)
    
    # Initialize
    orchestrator = LocalLLMOrchestrator(
        lmstudio_url="http://localhost:1234/v1",
        model_name="local-model"
    )
    
    # Example investigation
    task = """
    Research the concept of "Central Transportation Hub" (CPK) in Poland.
    
    Find:
    1. What is CPK?
    2. When was it announced?
    3. What are its main components?
    
    Use web scraping to collect information.
    Archive all sources.
    Provide summary with citations.
    """
    
    result = orchestrator.run_investigation(
        task=task,
        investigation_id="test_cpk_research",
        max_iterations=5
    )
    
    print("\n" + "="*60)
    print("🎯 Next Step: Supervisor Review")
    print("="*60)
    print(f"Aleksander (Claude) will now review:")
    print(f"  - Log file: {result['log_file']}")
    print(f"  - Result file: {result.get('investigation_id')}")
    print(f"  - Tool usage quality")
    print(f"  - Source attribution compliance")
    print(f"  - Analytical rigor")


if __name__ == "__main__":
    main()
