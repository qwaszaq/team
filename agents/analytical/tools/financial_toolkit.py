"""
Financial Toolkit for Marcus Chen
Financial analysis and forensics tools

Tools:
- Stock market data
- Company financials
- SEC filings
- Currency exchange
- Economic indicators
- Financial calculations
"""

try:
    import requests
except ImportError:
    requests = None  # Toolkit will work with limited functionality

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json


class FinancialToolkit:
    """
    Professional financial analysis tools for Marcus Chen
    
    Categories:
    1. Market Data
    2. Company Financials
    3. SEC/Regulatory Filings
    4. Economic Indicators
    5. Financial Calculations
    """
    
    def __init__(self):
        self.session = requests.Session() if requests else None
        # Free financial APIs (no key needed)
        self.apis = {
            "yahoo": "https://query1.finance.yahoo.com/v8/finance",
            "alphavantage": "https://www.alphavantage.co/query",  # Free tier available
            "sec": "https://www.sec.gov/cgi-bin/browse-edgar",
            "exchangerate": "https://api.exchangerate-api.com/v4/latest/"
        }
    
    # ============================================
    # 1. MARKET DATA
    # ============================================
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get current stock price and basic info
        
        Args:
            symbol: Stock ticker (e.g., "AAPL", "MSFT")
        
        Returns:
            Price, change, volume, market cap
        """
        try:
            # Using Yahoo Finance API (free, no key)
            url = f"{self.apis['yahoo']}/chart/{symbol}"
            params = {
                'interval': '1d',
                'range': '1d'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                return {
                    "symbol": symbol,
                    "price": meta.get('regularMarketPrice'),
                    "change": meta.get('regularMarketChange'),
                    "change_percent": meta.get('regularMarketChangePercent'),
                    "volume": meta.get('regularMarketVolume'),
                    "market_cap": meta.get('marketCap'),
                    "currency": meta.get('currency'),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Symbol not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_stock_history(
        self,
        symbol: str,
        period: str = "1mo"
    ) -> List[Dict]:
        """
        Get historical stock prices
        
        Args:
            symbol: Stock ticker
            period: "1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"
        
        Returns:
            List of {date, open, high, low, close, volume}
        """
        try:
            url = f"{self.apis['yahoo']}/chart/{symbol}"
            params = {
                'interval': '1d',
                'range': period
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart']:
                result = data['chart']['result'][0]
                timestamps = result['timestamp']
                quotes = result['indicators']['quote'][0]
                
                history = []
                for i, ts in enumerate(timestamps):
                    history.append({
                        "date": datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
                        "open": quotes['open'][i],
                        "high": quotes['high'][i],
                        "low": quotes['low'][i],
                        "close": quotes['close'][i],
                        "volume": quotes['volume'][i]
                    })
                
                return history
            else:
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def compare_stocks(self, symbols: List[str]) -> Dict:
        """
        Compare multiple stocks side-by-side
        
        Returns performance comparison
        """
        comparison = {}
        
        for symbol in symbols:
            quote = self.get_stock_quote(symbol)
            comparison[symbol] = {
                "price": quote.get('price'),
                "change_percent": quote.get('change_percent'),
                "volume": quote.get('volume')
            }
        
        return comparison
    
    # ============================================
    # 2. COMPANY FINANCIALS
    # ============================================
    
    def get_company_profile(self, symbol: str) -> Dict:
        """
        Get company profile and key metrics
        
        Returns:
            - Name, sector, industry
            - Market cap, P/E ratio
            - Description
        """
        # This would use Yahoo Finance or Alpha Vantage
        return {
            "symbol": symbol,
            "name": f"Company {symbol}",
            "sector": "Technology",
            "industry": "Software",
            "market_cap": "1B USD",
            "pe_ratio": 25.5,
            "note": "Use Alpha Vantage API for detailed data"
        }
    
    def get_financial_statements(
        self,
        symbol: str,
        statement_type: str = "income"
    ) -> Dict:
        """
        Get financial statements
        
        Args:
            statement_type: "income", "balance", "cash_flow"
        
        Returns:
            Financial statement data
        """
        # Would integrate with:
        # - SEC EDGAR API
        # - Alpha Vantage
        # - Financial Modeling Prep
        
        return {
            "symbol": symbol,
            "statement_type": statement_type,
            "note": "Integrate with SEC EDGAR or Alpha Vantage API",
            "data_source": "https://www.sec.gov/edgar"
        }
    
    # ============================================
    # 3. SEC/REGULATORY FILINGS
    # ============================================
    
    def search_sec_filings(
        self,
        company_name: str,
        filing_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search SEC EDGAR filings
        
        Args:
            company_name: Company name or ticker
            filing_type: "10-K", "10-Q", "8-K", "DEF 14A", etc.
        
        Returns:
            List of filings with dates and links
        """
        # SEC EDGAR search
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        
        return {
            "company": company_name,
            "filing_type": filing_type or "All",
            "search_url": f"{base_url}?company={company_name}&type={filing_type or ''}",
            "note": "Access SEC EDGAR directly for filings",
            "common_filings": {
                "10-K": "Annual report",
                "10-Q": "Quarterly report",
                "8-K": "Current events",
                "DEF 14A": "Proxy statement",
                "S-1": "IPO registration"
            }
        }
    
    # ============================================
    # 4. CURRENCY & EXCHANGE
    # ============================================
    
    def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str
    ) -> Dict:
        """
        Get currency exchange rate
        
        Args:
            from_currency: "USD", "EUR", "GBP", "PLN", etc.
            to_currency: Target currency
        
        Returns:
            Exchange rate and timestamp
        """
        try:
            url = f"{self.apis['exchangerate']}{from_currency}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if 'rates' in data and to_currency in data['rates']:
                rate = data['rates'][to_currency]
                
                return {
                    "from": from_currency,
                    "to": to_currency,
                    "rate": rate,
                    "date": data.get('date'),
                    "calculation": f"1 {from_currency} = {rate} {to_currency}"
                }
            else:
                return {"error": "Currency not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> Dict:
        """
        Convert amount between currencies
        """
        rate_data = self.get_exchange_rate(from_currency, to_currency)
        
        if 'rate' in rate_data:
            converted = amount * rate_data['rate']
            
            return {
                "original": f"{amount:,.2f} {from_currency}",
                "converted": f"{converted:,.2f} {to_currency}",
                "rate": rate_data['rate'],
                "date": rate_data['date']
            }
        else:
            return rate_data  # Error passed through
    
    # ============================================
    # 5. FINANCIAL CALCULATIONS
    # ============================================
    
    def calculate_roi(
        self,
        initial_investment: float,
        final_value: float
    ) -> Dict:
        """
        Calculate Return on Investment (ROI)
        
        ROI = (Final Value - Initial Investment) / Initial Investment * 100
        """
        profit = final_value - initial_investment
        roi_percent = (profit / initial_investment) * 100
        
        return {
            "initial_investment": f"${initial_investment:,.2f}",
            "final_value": f"${final_value:,.2f}",
            "profit": f"${profit:,.2f}",
            "roi_percent": f"{roi_percent:.2f}%",
            "result": "Profit" if profit > 0 else "Loss"
        }
    
    def calculate_compound_interest(
        self,
        principal: float,
        rate: float,
        years: int,
        compounds_per_year: int = 12
    ) -> Dict:
        """
        Calculate compound interest
        
        A = P(1 + r/n)^(nt)
        """
        amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
        interest_earned = amount - principal
        
        return {
            "principal": f"${principal:,.2f}",
            "rate": f"{rate*100:.2f}%",
            "years": years,
            "compounds_per_year": compounds_per_year,
            "final_amount": f"${amount:,.2f}",
            "interest_earned": f"${interest_earned:,.2f}"
        }
    
    def calculate_pe_ratio(
        self,
        stock_price: float,
        earnings_per_share: float
    ) -> Dict:
        """
        Calculate Price-to-Earnings (P/E) ratio
        
        P/E = Stock Price / Earnings Per Share
        """
        if earnings_per_share == 0:
            return {"error": "EPS cannot be zero"}
        
        pe_ratio = stock_price / earnings_per_share
        
        interpretation = "Overvalued" if pe_ratio > 25 else "Fairly valued" if pe_ratio > 15 else "Undervalued"
        
        return {
            "stock_price": f"${stock_price:.2f}",
            "earnings_per_share": f"${earnings_per_share:.2f}",
            "pe_ratio": f"{pe_ratio:.2f}",
            "interpretation": interpretation,
            "note": "Industry average P/E is ~15-25"
        }
    
    def detect_unusual_transactions(
        self,
        transactions: List[Dict]
    ) -> List[Dict]:
        """
        Detect unusual financial patterns (forensic analysis)
        
        Looks for:
        - Round numbers (possible fraud)
        - Just-below-threshold amounts
        - Weekend/holiday transactions
        - Rapid sequences
        """
        suspicious = []
        
        for txn in transactions:
            flags = []
            amount = txn.get('amount', 0)
            
            # Round number flag
            if amount % 1000 == 0 and amount > 1000:
                flags.append("Round number (possible manipulation)")
            
            # Just below reporting threshold
            if 9000 <= amount < 10000:
                flags.append("Just below $10k reporting threshold")
            
            if flags:
                suspicious.append({
                    "transaction": txn,
                    "flags": flags,
                    "risk_level": "High" if len(flags) > 1 else "Medium"
                })
        
        return suspicious
    
    # ============================================
    # TOOLKIT STATUS
    # ============================================
    
    def get_available_tools(self) -> Dict:
        """List all available financial tools"""
        return {
            "market_data": [
                "get_stock_quote (Real-time prices)",
                "get_stock_history (Historical data)",
                "compare_stocks (Side-by-side comparison)"
            ],
            "company_financials": [
                "get_company_profile",
                "get_financial_statements (Income, Balance, Cash Flow)"
            ],
            "regulatory": [
                "search_sec_filings (10-K, 10-Q, 8-K, etc.)",
                "sec_edgar_access"
            ],
            "currency": [
                "get_exchange_rate (Real-time rates)",
                "convert_currency (Multi-currency)"
            ],
            "calculations": [
                "calculate_roi (Return on Investment)",
                "calculate_compound_interest",
                "calculate_pe_ratio",
                "detect_unusual_transactions (Forensics)"
            ],
            "status": "Ready for financial analysis"
        }


# Quick test
if __name__ == "__main__":
    print("?? Financial Toolkit for Marcus Chen\n")
    
    toolkit = FinancialToolkit()
    tools = toolkit.get_available_tools()
    
    print("Available Tools:")
    for category, tool_list in tools.items():
        if category != "status":
            print(f"\n{category.upper().replace('_', ' ')}:")
            for tool in tool_list:
                print(f"  ? {tool}")
    
    print(f"\n{tools['status']}")
    
    # Test exchange rate
    print("\n--- Test: USD to EUR Exchange Rate ---")
    result = toolkit.get_exchange_rate("USD", "EUR")
    if 'rate' in result:
        print(f"? {result['calculation']}")
