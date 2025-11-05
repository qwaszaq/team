"""
Base Agent Framework - Sequential Multi-Agent Pattern
Katarzyna Wiśniewska & Tomasz Zieliński
2025-11-05
"""

import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.llm.lmstudio_client import LMStudioLLMClient, LLMResponse
from src.data.embedding_pipeline import DualEmbeddingSystem


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Task for agent"""
    task_id: str
    title: str
    description: str
    task_type: str
    data: Dict[str, Any]
    created_at: datetime
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class TaskResult:
    """Result from agent"""
    task_id: str
    agent_name: str
    agent_role: str
    status: TaskStatus
    output: Dict[str, Any]
    reasoning: str
    confidence: float
    time_taken: float
    tokens_used: Dict[str, int]
    artifacts: List[str]
    suggestions: Optional[List[str]] = None


class BaseAgent:
    """
    Base class for all analytical agents
    
    Sequential multi-agent pattern:
    - One LLM, multiple personas
    - Agents work sequentially
    - Context passed like a baton
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        specialization: str,
        llm_model: str = "openai/gpt-oss-20b"
    ):
        """
        Initialize agent
        
        Args:
            name: Agent name
            role: Agent role (financial, legal, risk, etc.)
            specialization: Area of expertise
            llm_model: LLM model to use
        """
        self.name = name
        self.role = role
        self.specialization = specialization
        self.llm_model = llm_model
        
        # Clients
        self.llm = LMStudioLLMClient(model=llm_model)
        self.embeddings = DualEmbeddingSystem()
        
        # Performance tracking
        self.tasks_completed = 0
        self.total_time = 0
        self.quality_scores = []
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt for this agent
        
        Returns:
            System prompt string
        """
        return f"""You are {self.name}, a {self.role} specialist.

Your expertise: {self.specialization}

Your approach:
1. Analyze thoroughly and systematically
2. Identify key patterns and insights
3. Highlight risks and opportunities
4. Provide actionable recommendations
5. Support conclusions with evidence

Be concise but comprehensive. Focus on what matters most."""
    
    def format_context(self, context: List[Dict[str, Any]]) -> str:
        """
        Format context from previous agents
        
        Args:
            context: List of previous task results
            
        Returns:
            Formatted context string
        """
        if not context:
            return "No previous context."
        
        formatted = "## Previous Analysis:\n\n"
        for item in context:
            formatted += f"**{item.get('agent_role', 'Unknown')}:**\n"
            formatted += f"{item.get('output', {}).get('summary', 'No summary')}\n\n"
        
        return formatted
    
    def execute(self, task: Task, context: Optional[List[Dict[str, Any]]] = None) -> TaskResult:
        """
        Execute task
        
        Args:
            task: Task to execute
            context: Optional context from previous agents
            
        Returns:
            TaskResult with analysis
        """
        import time
        start_time = time.time()
        
        # Build messages
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Add context if available
        if context:
            context_str = self.format_context(context)
            messages.append({
                "role": "user",
                "content": f"Previous analysis:\n{context_str}"
            })
        
        # Add task
        task_prompt = f"""## Task: {task.title}

{task.description}

## Data:
{self._format_task_data(task.data)}

Provide your analysis in the following structure:
1. Executive Summary
2. Key Findings
3. Risks & Concerns
4. Recommendations
5. Next Steps"""
        
        messages.append({"role": "user", "content": task_prompt})
        
        # Execute with LLM
        response = self.llm.chat_completion(messages)
        
        elapsed = time.time() - start_time
        
        # Parse response
        if response.success:
            output = self._parse_analysis(response.content)
            status = TaskStatus.COMPLETED
            confidence = self._assess_confidence(response.content)
        else:
            output = {"error": response.error}
            status = TaskStatus.FAILED
            confidence = 0.0
        
        # Update stats
        self.tasks_completed += 1
        self.total_time += elapsed
        
        return TaskResult(
            task_id=task.task_id,
            agent_name=self.name,
            agent_role=self.role,
            status=status,
            output=output,
            reasoning=response.content,
            confidence=confidence,
            time_taken=elapsed,
            tokens_used=response.tokens_used,
            artifacts=self._identify_artifacts(response.content),
            suggestions=self._extract_suggestions(response.content)
        )
    
    def _format_task_data(self, data: Dict[str, Any]) -> str:
        """Format task data for prompt"""
        formatted = ""
        for key, value in data.items():
            formatted += f"**{key}:** {value}\n"
        return formatted
    
    def _parse_analysis(self, content: str) -> Dict[str, Any]:
        """Parse LLM analysis into structured output"""
        return {
            "full_analysis": content,
            "summary": self._extract_summary(content),
            "key_findings": self._extract_section(content, "Key Findings"),
            "recommendations": self._extract_section(content, "Recommendations")
        }
    
    def _extract_summary(self, content: str) -> str:
        """Extract executive summary"""
        lines = content.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if "executive summary" in line.lower() or "summary" in line.lower():
                in_summary = True
                continue
            if in_summary:
                if line.startswith('#') or "key findings" in line.lower():
                    break
                if line.strip():
                    summary_lines.append(line.strip())
        
        return " ".join(summary_lines[:3]) if summary_lines else content[:200]
    
    def _extract_section(self, content: str, section_name: str) -> List[str]:
        """Extract specific section"""
        lines = content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_name.lower() in line.lower():
                in_section = True
                continue
            if in_section:
                if line.startswith('#'):
                    break
                if line.strip() and (line.strip().startswith('-') or line.strip().startswith('*')):
                    section_lines.append(line.strip())
        
        return section_lines
    
    def _assess_confidence(self, content: str) -> float:
        """Assess confidence in analysis"""
        # Simple heuristic based on content
        confidence_indicators = [
            "clearly", "definitely", "evidence shows", "data indicates",
            "consistent with", "strongly suggests"
        ]
        
        uncertainty_indicators = [
            "unclear", "possibly", "might", "could be", "uncertain",
            "insufficient data", "need more information"
        ]
        
        content_lower = content.lower()
        confidence_count = sum(1 for indicator in confidence_indicators if indicator in content_lower)
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in content_lower)
        
        base_confidence = 0.7
        confidence = base_confidence + (confidence_count * 0.05) - (uncertainty_count * 0.1)
        
        return max(0.0, min(1.0, confidence))
    
    def _identify_artifacts(self, content: str) -> List[str]:
        """Identify artifacts mentioned in analysis"""
        artifacts = []
        if "report" in content.lower():
            artifacts.append("analysis_report.md")
        if "findings" in content.lower():
            artifacts.append("key_findings.json")
        return artifacts
    
    def _extract_suggestions(self, content: str) -> List[str]:
        """Extract next step suggestions"""
        return self._extract_section(content, "Next Steps")


class FinancialAnalystAgent(BaseAgent):
    """Financial analysis specialist"""
    
    def __init__(self):
        super().__init__(
            name="Financial Analyst",
            role="financial",
            specialization="Financial analysis, revenue patterns, profitability, cash flow"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Financial Analyst specialist.

Expertise: Financial statement analysis, revenue patterns, profitability metrics, 
cash flow analysis, financial ratios, trend analysis.

Your analysis should focus on:
- Revenue trends and drivers
- Profitability and margins
- Cash flow patterns
- Financial health indicators
- Key financial ratios
- Red flags or concerns

Be quantitative, precise, and highlight financial risks."""


class LegalAnalystAgent(BaseAgent):
    """Legal analysis specialist"""
    
    def __init__(self):
        super().__init__(
            name="Legal Analyst",
            role="legal",
            specialization="Legal compliance, contracts, regulatory issues"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Legal Analyst specialist.

Expertise: Legal compliance, contract analysis, regulatory requirements,
risk assessment, liability identification.

Your analysis should focus on:
- Legal compliance issues
- Contractual obligations
- Regulatory risks
- Liability concerns
- Documentation gaps
- Legal recommendations

Be thorough and highlight legal risks clearly."""


class RiskAnalystAgent(BaseAgent):
    """Risk analysis specialist"""
    
    def __init__(self):
        super().__init__(
            name="Risk Analyst",
            role="risk",
            specialization="Risk assessment, threat identification, mitigation strategies"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Risk Analyst specialist.

Expertise: Risk identification, threat assessment, vulnerability analysis,
mitigation strategies, risk quantification.

Your analysis should focus on:
- Key risks identified
- Risk severity (high/medium/low)
- Potential impact
- Likelihood assessment
- Mitigation recommendations
- Monitoring suggestions

Be systematic and prioritize risks by severity."""


def test_agents():
    """Test agent framework"""
    print("🧪 Testing Agent Framework...\n")
    
    # Create task
    task = Task(
        task_id="task_001",
        title="Analyze Financial Performance",
        description="Analyze the company's Q4 financial performance",
        task_type="financial_analysis",
        data={
            "revenue": "$4.2M",
            "growth": "23% YoY",
            "expenses": "18% increase",
            "margin": "32%",
            "period": "Q4 2024"
        },
        created_at=datetime.now()
    )
    
    # Test financial agent
    print("1. Financial Agent Analysis:")
    financial_agent = FinancialAnalystAgent()
    result1 = financial_agent.execute(task)
    
    print(f"   Status: {result1.status.value}")
    print(f"   Confidence: {result1.confidence:.2f}")
    print(f"   Time: {result1.time_taken:.2f}s")
    print(f"   Tokens: {result1.tokens_used['total']}")
    print(f"   Summary: {result1.output['summary'][:150]}...")
    
    # Test legal agent with context
    print("\n2. Legal Agent Analysis (with context):")
    legal_agent = LegalAnalystAgent()
    context = [result1.__dict__]
    result2 = legal_agent.execute(task, context)
    
    print(f"   Status: {result2.status.value}")
    print(f"   Confidence: {result2.confidence:.2f}")
    print(f"   Time: {result2.time_taken:.2f}s")
    print(f"   Summary: {result2.output['summary'][:150]}...")
    
    print("\n✅ Agent tests complete!")


if __name__ == "__main__":
    test_agents()
