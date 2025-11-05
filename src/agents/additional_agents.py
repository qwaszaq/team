"""
Additional Specialized Agents
Team Destiny
2025-11-05
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.base_agent import BaseAgent


class DataScienceAgent(BaseAgent):
    """Data Science & Analytics specialist"""
    
    def __init__(self):
        super().__init__(
            name="Data Science Agent",
            role="data_science",
            specialization="Statistical analysis, ML insights, data patterns, predictive analytics"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Data Science & Analytics specialist.

Expertise: Statistical analysis, machine learning insights, data patterns,
predictive analytics, quantitative methods, hypothesis testing.

Your analysis should focus on:
- Statistical significance and trends
- Data patterns and correlations
- Predictive insights
- Model recommendations
- Data quality assessment
- Quantitative evidence

Be data-driven, rigorous, and highlight statistical confidence."""


class DevOpsAgent(BaseAgent):
    """DevOps & Infrastructure specialist"""
    
    def __init__(self):
        super().__init__(
            name="DevOps Agent",
            role="devops",
            specialization="Infrastructure, deployment, scalability, monitoring, automation"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a DevOps & Infrastructure specialist.

Expertise: Infrastructure design, deployment strategies, scalability,
monitoring, automation, CI/CD, system reliability.

Your analysis should focus on:
- Infrastructure requirements
- Scalability considerations
- Deployment strategies
- Monitoring recommendations
- Performance optimization
- Reliability concerns

Be practical, focused on operational excellence."""


class SecurityAgent(BaseAgent):
    """Security & Compliance specialist"""
    
    def __init__(self):
        super().__init__(
            name="Security Agent",
            role="security",
            specialization="Security vulnerabilities, compliance, data protection, threat analysis"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Security & Compliance specialist.

Expertise: Security vulnerabilities, compliance requirements, data protection,
threat analysis, access control, encryption, audit trails.

Your analysis should focus on:
- Security vulnerabilities
- Compliance gaps (GDPR, SOC2, etc.)
- Data protection measures
- Access control issues
- Threat assessment
- Security recommendations

Be thorough, paranoid (in a good way), and highlight risks."""


class ProductAgent(BaseAgent):
    """Product Management specialist"""
    
    def __init__(self):
        super().__init__(
            name="Product Agent",
            role="product",
            specialization="User needs, market fit, feature prioritization, product strategy"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Product Management specialist.

Expertise: User needs analysis, market fit, feature prioritization,
product strategy, user experience, competitive analysis.

Your analysis should focus on:
- User needs and pain points
- Market opportunities
- Feature priorities
- Product-market fit
- User experience issues
- Competitive positioning

Be user-centric, strategic, and focus on value delivery."""


class QualityAssuranceAgent(BaseAgent):
    """QA & Testing specialist"""
    
    def __init__(self):
        super().__init__(
            name="QA Agent",
            role="qa",
            specialization="Testing strategies, quality metrics, bug detection, test coverage"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Quality Assurance & Testing specialist.

Expertise: Testing strategies, quality metrics, bug detection, test coverage,
automation, regression testing, quality standards.

Your analysis should focus on:
- Test coverage gaps
- Quality metrics
- Potential bugs or edge cases
- Testing strategies
- Quality standards
- Automation opportunities

Be meticulous, thorough, and quality-focused."""


class ArchitectAgent(BaseAgent):
    """Architecture & Design specialist"""
    
    def __init__(self):
        super().__init__(
            name="Architecture Agent",
            role="architecture",
            specialization="System design, architectural patterns, scalability, technical debt"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Software Architecture specialist.

Expertise: System design, architectural patterns, scalability, technical debt,
design principles, technology selection, integration patterns.

Your analysis should focus on:
- Architectural soundness
- Design patterns usage
- Scalability considerations
- Technical debt assessment
- Technology choices
- Integration approaches

Be strategic, forward-thinking, and focus on long-term sustainability."""


class DocumentationAgent(BaseAgent):
    """Documentation & Knowledge Management specialist"""
    
    def __init__(self):
        super().__init__(
            name="Documentation Agent",
            role="documentation",
            specialization="Documentation quality, knowledge management, clarity, completeness"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Documentation & Knowledge Management specialist.

Expertise: Documentation quality, knowledge management, technical writing,
clarity, completeness, user guides, API documentation.

Your analysis should focus on:
- Documentation completeness
- Clarity and readability
- Examples and use cases
- Knowledge gaps
- User-facing documentation
- Developer documentation

Be clear, thorough, and user-focused."""


# Registry of all available agents
AGENT_REGISTRY = {
    "financial": "FinancialAnalystAgent",
    "legal": "LegalAnalystAgent",
    "risk": "RiskAnalystAgent",
    "data_science": DataScienceAgent,
    "devops": DevOpsAgent,
    "security": SecurityAgent,
    "product": ProductAgent,
    "qa": QualityAssuranceAgent,
    "architecture": ArchitectAgent,
    "documentation": DocumentationAgent
}


def get_agent(agent_type: str) -> BaseAgent:
    """
    Get agent by type
    
    Args:
        agent_type: Agent type identifier
        
    Returns:
        Agent instance
    """
    if agent_type in AGENT_REGISTRY:
        agent_class = AGENT_REGISTRY[agent_type]
        if isinstance(agent_class, str):
            # Import from base_agent
            from src.agents.base_agent import FinancialAnalystAgent, LegalAnalystAgent, RiskAnalystAgent
            if agent_class == "FinancialAnalystAgent":
                return FinancialAnalystAgent()
            elif agent_class == "LegalAnalystAgent":
                return LegalAnalystAgent()
            elif agent_class == "RiskAnalystAgent":
                return RiskAnalystAgent()
        else:
            return agent_class()
    
    raise ValueError(f"Unknown agent type: {agent_type}")


def test_additional_agents():
    """Test additional agents"""
    print("🧪 Testing Additional Agents...\n")
    
    from src.agents.base_agent import Task
    from datetime import datetime
    
    # Test task
    task = Task(
        task_id="test_additional",
        title="System Analysis",
        description="Analyze the system from your specialty perspective",
        task_type="general",
        data={
            "system": "Multi-agent analytical platform",
            "components": ["LLM", "Embeddings", "Agents", "Databases"],
            "users": "Enterprise analysts"
        },
        created_at=datetime.now()
    )
    
    # Test each agent
    agents_to_test = [
        DataScienceAgent(),
        DevOpsAgent(),
        SecurityAgent(),
        ProductAgent(),
        QualityAssuranceAgent(),
        ArchitectAgent(),
        DocumentationAgent()
    ]
    
    for agent in agents_to_test:
        print(f"Testing: {agent.name}")
        result = agent.execute(task)
        print(f"  Status: {result.status.value}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Time: {result.time_taken:.2f}s")
        print(f"  Summary: {result.output['summary'][:100]}...")
        print()
    
    print("✅ All additional agents tested!")


if __name__ == "__main__":
    test_additional_agents()
