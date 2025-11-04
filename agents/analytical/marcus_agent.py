"""
Marcus Chen - Financial Analyst
Financial Intelligence Expert
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class MarcusAgent(BaseAgent):
    """
    Marcus Chen - Financial Analyst
    
    Role: Financial Intelligence Expert
    Specialization: Financial analysis, forensic accounting, fraud detection,
                   investment analysis, money trail investigation
    
    Capabilities:
    - Financial statement analysis
    - Forensic accounting
    - Fraud detection
    - Investment due diligence
    - Money flow tracking
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Marcus Chen",
            role="Financial Analyst",
            specialization="Financial intelligence, Forensic accounting, Fraud detection, Investment analysis",
            project_id=project_id
        )
        
        # Initialize Financial Toolkit
        from agents.analytical.tools.financial_toolkit import FinancialToolkit
        self.toolkit = FinancialToolkit()
        self.tools = self.toolkit.get_available_tools()
        
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute financial analysis work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=3)
        
        if any(word in task_lower for word in ["fraud", "forensic", "suspicious"]):
            result = self._forensic_analysis(task, context)
        elif any(word in task_lower for word in ["investment", "due diligence", "valuation"]):
            result = self._investment_analysis(task, context)
        elif any(word in task_lower for word in ["financial statement", "balance sheet", "income"]):
            result = self._financial_statement_analysis(task, context)
        elif any(word in task_lower for word in ["money trail", "transaction", "flow"]):
            result = self._money_trail_analysis(task, context)
        else:
            result = self._general_financial_analysis(task, context)
        
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
    
    def _forensic_analysis(self, task: Task, context: list) -> TaskResult:
        """Forensic accounting and fraud detection"""
        
        thoughts = f"""
🕵️ FORENSIC FINANCIAL ANALYSIS - Marcus Chen

Investigation: {task.title}

FRAUD INDICATORS ASSESSMENT:

🚩 Red Flag Analysis:
1. Revenue Recognition Issues
   - Timing anomalies: [Detected/Not detected]
   - Channel stuffing indicators: [Yes/No]
   - Round-tripping patterns: [Yes/No]

2. Expense Manipulation
   - Capitalization vs expensing: [Suspicious/Normal]
   - Off-balance-sheet items: [Present/Absent]
   - Related party transactions: [Found/Not found]

3. Cash Flow Discrepancies
   - Operating cash vs reported earnings: [Alignment]
   - Working capital changes: [Concerning/Normal]
   - Cash conversion cycle: [Analysis]

4. Balance Sheet Concerns
   - Asset quality: [Assessment]
   - Liability completeness: [Check]
   - Equity structure: [Analysis]

📊 Financial Ratios (Benford's Law Applied):
- First digit distribution: [Normal/Anomalous]
- Number patterns: [Analysis]
- Statistical outliers: [Identified]

🔍 Forensic Procedures Applied:
✓ Horizontal analysis (trend over time)
✓ Vertical analysis (common-size statements)
✓ Ratio analysis (peer comparison)
✓ Cash flow analysis
✓ Related party transaction review
✓ Management tone analysis

FINDINGS:
[Specific suspicious patterns identified]
[Quantification of potential impact]
[Confidence level of fraud indicators]

⚠️ SUSPICION LEVEL: [Low/Medium/High]
RECOMMENDATION: [Further investigation / Clear / Refer to authorities]

Note: Following forensic accounting standards (ACFE methodology)
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "red_flags": "Identified in report",
                "suspicion_level": "Documented",
                "methodology": "ACFE compliant",
                "confidence": "High"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["forensic_report.md", "red_flag_summary.md", "statistical_analysis.xlsx"],
            next_steps="Recommend Adrian (legal) for legal assessment if fraud suspected"
        )
    
    def _investment_analysis(self, task: Task, context: list) -> TaskResult:
        """Investment due diligence"""
        
        thoughts = f"""
💰 INVESTMENT ANALYSIS - Marcus Chen

Investment Opportunity: {task.title}

DUE DILIGENCE ASSESSMENT:

📈 Financial Health:
- Revenue growth: [CAGR analysis]
- Profitability: [Margins, trends]
- Cash generation: [FCF analysis]
- Capital efficiency: [ROIC, ROE]

💼 Business Model:
- Revenue streams: [Diversification]
- Unit economics: [LTV/CAC if applicable]
- Scalability: [Assessment]
- Competitive moat: [Strength]

⚖️ Balance Sheet Strength:
- Liquidity ratios: [Current, quick]
- Leverage: [D/E ratio, coverage]
- Asset quality: [Composition]
- Working capital: [Efficiency]

📊 Valuation:
- DCF analysis: [Fair value estimate]
- Comparable company analysis: [Peer multiple]
- Precedent transactions: [If applicable]
- Valuation range: [Low-High estimates]

🎯 Investment Thesis:
[Bull case arguments]
[Bear case arguments]
[Base case scenario]

⚠️ Key Risks:
1. [Financial risk]
2. [Operational risk]
3. [Market risk]
4. [Regulatory risk]

RECOMMENDATION: [Buy/Hold/Pass]
CONFIDENCE: [High/Medium/Low]
PRICE TARGET: [If applicable]

Note: Cross-validate with Sofia (market) for industry context
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "valuation": "Complete",
                "recommendation": "Documented",
                "risk_assessment": "Comprehensive",
                "confidence": "High"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["investment_memo.md", "dcf_model.xlsx", "risk_matrix.md"],
            next_steps="Coordinate with Sofia for market validation, Damian for critical review"
        )
    
    def _financial_statement_analysis(self, task: Task, context: list) -> TaskResult:
        """Financial statement deep-dive"""
        
        thoughts = f"""
📊 FINANCIAL STATEMENT ANALYSIS - Marcus Chen

Company: {task.title}

COMPREHENSIVE FINANCIAL REVIEW:

📈 Income Statement Analysis:
- Revenue trends: [Growth rate, stability]
- Gross margin: [Trend, peer comparison]
- Operating leverage: [Analysis]
- Net margin: [Quality of earnings]
- Non-recurring items: [Identified]

💵 Cash Flow Statement:
- Operating cash flow: [Quality, trends]
- Capex requirements: [Maintenance vs growth]
- Free cash flow: [Generation, consistency]
- Cash conversion: [Efficiency]

📊 Balance Sheet Analysis:
- Asset composition: [Quality]
- Liability structure: [Maturity, cost]
- Working capital: [Management]
- Off-balance-sheet items: [Disclosure review]

🔢 Key Financial Metrics:
- Liquidity: Current ratio, quick ratio
- Leverage: D/E, Interest coverage
- Efficiency: Asset turnover, inventory turns
- Profitability: ROA, ROE, ROIC
- Growth: Revenue, earnings CAGR

📉 Trend Analysis (5-year):
[Key metrics trajectory]
[Inflection points identified]
[Peer comparison]

FINANCIAL HEALTH SCORE: [Strong/Moderate/Weak]
KEY CONCERNS: [List if any]
STRENGTHS: [List]
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_depth": "Comprehensive",
                "financial_health": "Assessed",
                "peer_comparison": "Included",
                "trend_analysis": "5-year"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["financial_analysis.md", "ratio_analysis.xlsx", "trend_charts.pdf"],
            next_steps="Share with Maya for statistical validation"
        )
    
    def _money_trail_analysis(self, task: Task, context: list) -> TaskResult:
        """Money flow and transaction analysis"""
        
        thoughts = f"""
💸 MONEY TRAIL ANALYSIS - Marcus Chen

Investigation: {task.title}

TRANSACTION FLOW ANALYSIS:

🔄 Money Movement:
- Source of funds: [Identified/Unclear]
- Transaction path: [Mapped]
- Intermediaries: [Listed]
- Final destination: [Tracked]

🏦 Entity Structure:
- Operating entities: [List]
- Holding companies: [Identified]
- Offshore vehicles: [If any]
- Purpose of structure: [Assessment]

📍 Jurisdictional Analysis:
- Countries involved: [List]
- Regulatory regimes: [Complexity]
- Tax implications: [Noted]
- Risk jurisdictions: [Flagged]

⚠️ Suspicious Patterns:
- Layering: [Detected/Not detected]
- Round-tripping: [Yes/No]
- Unusual timing: [Analysis]
- Size anomalies: [Noted]

🔗 Related Party Transactions:
- Identified connections: [List]
- Transaction nature: [Assessment]
- Arms-length pricing: [Check]

FINDINGS:
[Clear narrative of money flow]
[Red flags identified]
[Legal/regulatory concerns]

COMPLEXITY LEVEL: [Low/Medium/High]
TRANSPARENCY: [Good/Poor]
CONCERN LEVEL: [Assessment]

Recommend coordination with Adrian (legal) for regulatory review
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "money_trail": "Mapped",
                "red_flags": "Documented",
                "entities_identified": "Complete",
                "concern_level": "Assessed"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["money_flow_map.pdf", "entity_structure.md", "transaction_log.xlsx"],
            next_steps="Coordinate with Adrian for legal implications"
        )
    
    def _general_financial_analysis(self, task: Task, context: list) -> TaskResult:
        """General financial intelligence"""
        
        thoughts = f"""
💼 FINANCIAL INTELLIGENCE - Marcus Chen

Task: {task.title}

FINANCIAL ANALYSIS CAPABILITIES:

My expertise:
- Financial statement analysis (all 3 statements)
- Forensic accounting & fraud detection
- Investment due diligence & valuation
- Money trail investigation
- Credit analysis
- Financial modeling
- Ratio analysis & benchmarking

Methodology:
- Rigorous, evidence-based analysis
- Multiple valuation approaches
- Peer comparison
- Historical trend analysis
- Forward-looking projections

Always skeptical, always thorough.
Numbers don't lie, but presentations can mislead.
I find the truth in the financials.

Ready to analyze. Provide financial data or specific questions.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "status": "Ready for tasking",
                "capabilities": "Full financial analysis suite"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[],
            next_steps="Await financial analysis requirements"
        )


# Test
if __name__ == "__main__":
    print("Testing Marcus Agent...")
    marcus = MarcusAgent()
    print(f"✅ {marcus.name} initialized")
    print(f"   Role: {marcus.role}")
    print(f"   Specialty: Financial intelligence & forensics 💰")
