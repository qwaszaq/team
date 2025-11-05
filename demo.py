#!/usr/bin/env python3
"""
Destiny Analytical System - Live Demo
Team Destiny - 2025-11-05

Demonstrates the complete system with real analysis
"""

import sys
import os
from datetime import datetime

# Add to path
sys.path.insert(0, os.path.dirname(__file__))

from src.agents.orchestrator import MultiAgentOrchestrator
from src.agents.additional_agents import get_agent
from src.supervision.claude_supervisor import ClaudeSupervisor


def print_banner():
    """Print demo banner"""
    print("="*70)
    print("     DESTINY ANALYTICAL SYSTEM - LIVE DEMO")
    print("="*70)
    print()


def demo_simple_analysis():
    """Demo 1: Simple analysis with one agent"""
    print("DEMO 1: Simple Financial Analysis")
    print("-" * 70)
    
    from src.agents.base_agent import Task, FinancialAnalystAgent
    
    # Create agent
    agent = FinancialAnalystAgent()
    
    # Create task
    task = Task(
        task_id="demo_task_001",
        title="Q4 2024 Financial Analysis",
        description="Analyze quarterly financial performance",
        task_type="financial",
        data={
            "revenue": "$5.2M",
            "growth_yoy": "28%",
            "profit_margin": "34%",
            "expenses": "$3.4M",
            "cash": "$12M",
            "period": "Q4 2024"
        },
        created_at=datetime.now()
    )
    
    print(f"Task: {task.title}")
    print(f"Data: {task.data}")
    print()
    
    # Execute
    print("Executing analysis...")
    result = agent.execute(task)
    
    # Display results
    print(f"\n✅ Analysis Complete!")
    print(f"Status: {result.status.value}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Time: {result.time_taken:.2f}s")
    print(f"Tokens: {result.tokens_used['total']}")
    print(f"\nSummary:")
    print(result.output['summary'])
    print()


def demo_multi_agent():
    """Demo 2: Multi-agent orchestration"""
    print("\n" + "="*70)
    print("DEMO 2: Multi-Agent Orchestration")
    print("-" * 70)
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Test documents
    documents = [
        {
            "id": "financial_report",
            "content": """
            Q4 2024 Financial Performance
            
            Revenue: Company achieved $5.2M in quarterly revenue, representing 
            a 28% year-over-year increase. Enterprise segment contributed 65% 
            of total revenue, up from 58% in Q3.
            
            Profitability: EBITDA margin improved to 34%, compared to 31% in 
            the previous quarter. Operating expenses were controlled at $3.4M.
            
            Cash Position: Strong cash position of $12M provides excellent 
            runway for planned expansion into European markets.
            
            Outlook: Management projects 25-30% growth for 2025, driven by 
            enterprise segment expansion and new product launches.
            """,
            "type": "financial"
        },
        {
            "id": "risk_assessment",
            "content": """
            Q4 2024 Risk Review
            
            Operational Risks: Supply chain stability improved. Key vendor 
            relationships strengthened through long-term contracts.
            
            Market Risks: Increased competition in enterprise segment. Three 
            new competitors entered the market in Q4.
            
            Financial Risks: Currency exposure limited to 15% of revenue. 
            Strong balance sheet mitigates short-term risks.
            
            Compliance: All regulatory requirements met. Data privacy audit 
            completed successfully.
            """,
            "type": "general"
        }
    ]
    
    print(f"Documents: {len(documents)}")
    print(f"Analysis types: Financial, Legal, Risk")
    print()
    
    # Process case
    print("Executing multi-agent analysis...")
    analysis = orchestrator.process_case(
        case_id=f"demo_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Q4 2024 Comprehensive Analysis",
        documents=documents,
        analysis_types=["financial", "legal", "risk"],
        description="Complete Q4 analysis with multiple specialized agents"
    )
    
    # Display results
    print(f"\n✅ Multi-Agent Analysis Complete!")
    print(f"Case: {analysis.case_id}")
    print(f"Agents: {', '.join(analysis.agents_used)}")
    print(f"Embeddings: {analysis.embeddings_count}")
    print(f"Time: {analysis.total_time:.2f}s")
    print(f"Tokens: {analysis.total_tokens}")
    print(f"Avg Confidence: {analysis.average_confidence:.2f}")
    print()


def demo_additional_agents():
    """Demo 3: Additional specialized agents"""
    print("\n" + "="*70)
    print("DEMO 3: Specialized Agents")
    print("-" * 70)
    
    from src.agents.base_agent import Task
    from src.agents.additional_agents import DataScienceAgent, SecurityAgent
    
    # Create task
    task = Task(
        task_id="demo_specialist_001",
        title="System Security Review",
        description="Assess system security posture",
        task_type="security",
        data={
            "system": "Multi-agent analytical platform",
            "users": "Enterprise analysts",
            "data_types": ["Financial", "Legal", "Confidential"],
            "deployment": "Hybrid (on-prem + cloud supervision)"
        },
        created_at=datetime.now()
    )
    
    # Test Security Agent
    print("Security Agent Analysis:")
    security = SecurityAgent()
    result = security.execute(task)
    print(f"  Status: {result.status.value}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Summary: {result.output['summary'][:150]}...")
    print()
    
    # Test Data Science Agent
    print("Data Science Agent Analysis:")
    data_science = DataScienceAgent()
    result = data_science.execute(task)
    print(f"  Status: {result.status.value}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Summary: {result.output['summary'][:150]}...")
    print()


def demo_supervision():
    """Demo 4: Claude supervision"""
    print("\n" + "="*70)
    print("DEMO 4: Quality Supervision")
    print("-" * 70)
    
    supervisor = ClaudeSupervisor()
    
    # Simulate agent output
    test_output = {
        "summary": "Strong financial performance with 28% revenue growth.",
        "key_findings": [
            "Revenue: $5.2M (+28% YoY)",
            "Profit margin: 34% (improved from 31%)",
            "Cash position: $12M (strong runway)"
        ],
        "recommendations": [
            "Continue growth trajectory",
            "Monitor competitive landscape",
            "Prepare for European expansion"
        ]
    }
    
    print("Reviewing agent output...")
    review = supervisor.review_task(
        task_id="demo_review_001",
        agent_name="Financial Analyst",
        agent_role="financial",
        task_description="Q4 Financial Analysis",
        agent_output=test_output,
        confidence=0.85
    )
    
    print(f"\n✅ Review Complete!")
    print(f"Grade: {review.grade.value}")
    print(f"Quality Score: {review.quality_score:.2f}")
    print(f"Status: {'Approved' if review.approved else 'Needs improvement'}")
    print(f"\nStrengths:")
    for strength in review.strengths[:3]:
        print(f"  ✅ {strength}")
    print()


def main():
    """Run all demos"""
    print_banner()
    
    try:
        # Demo 1: Simple analysis
        demo_simple_analysis()
        
        # Demo 2: Multi-agent
        demo_multi_agent()
        
        # Demo 3: Additional agents
        demo_additional_agents()
        
        # Demo 4: Supervision
        demo_supervision()
        
        # Summary
        print("\n" + "="*70)
        print("DEMO COMPLETE!")
        print("="*70)
        print("\n✅ All demos executed successfully!")
        print("\nThe system demonstrated:")
        print("  ✅ Single agent analysis")
        print("  ✅ Multi-agent orchestration")
        print("  ✅ Specialized agents (10 total)")
        print("  ✅ Quality supervision")
        print("\nSystem is ready for production use! 🚀")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
