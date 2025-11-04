"""
Analytical Team Toolkits

Professional tools for each analytical agent:
- Elena: OSINT Toolkit (web search, domain lookup, social media)
- Marcus: Financial Toolkit (market data, SEC filings, calculations)
- Sofia: Market Research Toolkit (trends, competitors, surveys)
- Adrian: Legal Toolkit (case law, regulations, compliance)
- Maya: Data Analysis Toolkit (pandas, visualization, statistics)
- Lucas: Report Toolkit (PDF generation, charts, presentations)
- Alex: Elasticsearch + Qdrant (Document search and processing)
"""

from .osint_toolkit import OSINTToolkit
from .financial_toolkit import FinancialToolkit
from .market_research_toolkit import MarketResearchToolkit
from .legal_toolkit import LegalToolkit
from .data_analysis_toolkit import DataAnalysisToolkit
from .report_toolkit import ReportToolkit
from .scraping_toolkit import ScrapingToolkit
from .mathematical_toolkit import MathematicalToolkit

__all__ = [
    'OSINTToolkit',
    'FinancialToolkit',
    'MarketResearchToolkit',
    'LegalToolkit',
    'DataAnalysisToolkit',
    'ReportToolkit',
    'ScrapingToolkit',
    'MathematicalToolkit',
]
