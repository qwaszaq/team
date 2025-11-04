"""
Sejm API Client
===============

Client for Polish Parliament (Sejm) API
Enables analysis of committee work, sittings, and legislative activity

API Documentation: https://api.sejm.gov.pl/committees.html

Author: Elena Volkov (OSINT) + Tomasz Kamiński (Developer)
Date: 2025-11-04
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import time

class SejmAPIClient:
    """
    Client for Sejm API
    
    Usage:
        client = SejmAPIClient()
        committees = client.get_committees(term=9)
        sittings = client.get_committee_sittings("ASW", term=9)
    """
    
    BASE_URL = "https://api.sejm.gov.pl/sejm"
    
    def __init__(self, rate_limit_delay: float = 0.1):
        """
        Initialize client
        
        Args:
            rate_limit_delay: Delay between requests in seconds (default 0.1s = 10 req/s)
        """
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "SejmAnalysisTool/1.0"
        })
    
    def _make_request(self, endpoint: str) -> Dict:
        """Make API request with rate limiting"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
    
    def get_committees(self, term: int) -> List[Dict]:
        """
        Get list of all committees for a term
        
        Args:
            term: Parliament term number (e.g., 9 for 2019-2023)
        
        Returns:
            List of committees with code and name
        """
        endpoint = f"term{term}/committees"
        return self._make_request(endpoint) or []
    
    def get_committee(self, code: str, term: int) -> Dict:
        """Get details of a specific committee"""
        endpoint = f"term{term}/committees/{code}"
        return self._make_request(endpoint) or {}
    
    def get_committee_sittings(self, code: str, term: int) -> List[Dict]:
        """
        Get list of all sittings for a committee
        
        Args:
            code: Committee code (e.g., "ASW")
            term: Parliament term number
        
        Returns:
            List of sittings with basic info
        """
        endpoint = f"term{term}/committees/{code}/sittings"
        return self._make_request(endpoint) or []
    
    def get_sitting_details(self, code: str, sitting_num: int, term: int) -> Dict:
        """
        Get detailed information about a specific sitting
        
        Args:
            code: Committee code
            sitting_num: Sitting number
            term: Parliament term
        
        Returns:
            Detailed sitting data including agenda, attendees, documents
        """
        endpoint = f"term{term}/committees/{code}/sittings/{sitting_num}"
        return self._make_request(endpoint) or {}


class CommitteeAnalyzer:
    """
    Analyzer for committee work
    
    Provides analysis of:
    - Meeting frequency
    - Agenda topics
    - Attendance patterns
    - Legislative activity
    """
    
    def __init__(self, client: SejmAPIClient):
        self.client = client
    
    def analyze_committee_term(
        self, 
        code: str, 
        term: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Complete analysis of committee work for a term
        
        Args:
            code: Committee code (e.g., "ASW")
            term: Parliament term
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
        
        Returns:
            Comprehensive analysis report
        """
        print(f"📊 Analyzing committee {code}, term {term}...")
        
        # Get basic committee info
        committee = self.client.get_committee(code, term)
        print(f"   Committee: {committee.get('name', code)}")
        
        # Get all sittings
        sittings = self.client.get_committee_sittings(code, term)
        print(f"   Total sittings: {len(sittings)}")
        
        # Filter by date if specified
        if start_date or end_date:
            sittings = self._filter_by_date(sittings, start_date, end_date)
            print(f"   Filtered sittings: {len(sittings)}")
        
        # Analyze
        analysis = {
            "committee": committee,
            "term": term,
            "total_sittings": len(sittings),
            "date_range": self._get_date_range(sittings),
            "frequency": self._analyze_frequency(sittings),
            "sitting_numbers": [s.get("num") for s in sittings if s.get("num")],
        }
        
        # Get detailed analysis for sample of sittings
        print(f"   Fetching detailed data...")
        detailed_sample = self._get_detailed_sample(code, term, sittings, sample_size=20)
        
        if detailed_sample:
            analysis["detailed_analysis"] = {
                "sample_size": len(detailed_sample),
                "agenda_items": self._analyze_agenda(detailed_sample),
                "attendance": self._analyze_attendance(detailed_sample),
                "documents": self._analyze_documents(detailed_sample)
            }
        
        return analysis
    
    def _filter_by_date(self, sittings: List[Dict], start: str, end: str) -> List[Dict]:
        """Filter sittings by date range"""
        filtered = []
        for sitting in sittings:
            date = sitting.get("date") or sitting.get("from", "")
            if date:
                if start and date < start:
                    continue
                if end and date > end:
                    continue
                filtered.append(sitting)
        return filtered
    
    def _get_date_range(self, sittings: List[Dict]) -> Dict:
        """Get date range of sittings"""
        if not sittings:
            return {"start": None, "end": None}
        
        dates = []
        for s in sittings:
            date = s.get("date") or s.get("from", "")
            if date:
                dates.append(date[:10] if len(date) > 10 else date)
        
        if dates:
            return {"start": min(dates), "end": max(dates)}
        return {"start": None, "end": None}
    
    def _analyze_frequency(self, sittings: List[Dict]) -> Dict:
        """Analyze meeting frequency"""
        if not sittings:
            return {}
        
        # Count by year
        by_year = {}
        by_month = {}
        
        for sitting in sittings:
            date = sitting.get("date") or sitting.get("from", "")
            if date and len(date) >= 7:
                year = date[:4]
                month = date[:7]
                
                by_year[year] = by_year.get(year, 0) + 1
                by_month[month] = by_month.get(month, 0) + 1
        
        return {
            "by_year": by_year,
            "by_month": by_month,
            "busiest_year": max(by_year.items(), key=lambda x: x[1])[0] if by_year else None,
            "busiest_month": max(by_month.items(), key=lambda x: x[1])[0] if by_month else None
        }
    
    def _get_detailed_sample(
        self, 
        code: str, 
        term: int, 
        sittings: List[Dict],
        sample_size: int = 20
    ) -> List[Dict]:
        """Get detailed data for a sample of sittings"""
        # Sample evenly across the term
        if len(sittings) <= sample_size:
            sample_indices = range(len(sittings))
        else:
            step = len(sittings) // sample_size
            sample_indices = range(0, len(sittings), step)[:sample_size]
        
        detailed = []
        for i in sample_indices:
            sitting_num = sittings[i].get("num")
            if sitting_num:
                details = self.client.get_sitting_details(code, sitting_num, term)
                if details:
                    detailed.append(details)
        
        return detailed
    
    def _analyze_agenda(self, detailed_sittings: List[Dict]) -> Dict:
        """Analyze agenda items"""
        total_items = 0
        topics = []
        
        for sitting in detailed_sittings:
            points = sitting.get("points", [])
            total_items += len(points)
            
            for point in points:
                title = point.get("title", "")
                if title:
                    topics.append(title)
        
        return {
            "total_agenda_items": total_items,
            "avg_items_per_sitting": total_items / len(detailed_sittings) if detailed_sittings else 0,
            "sample_topics": topics[:10]  # First 10 topics as sample
        }
    
    def _analyze_attendance(self, detailed_sittings: List[Dict]) -> Dict:
        """Analyze attendance patterns"""
        attendances = []
        
        for sitting in detailed_sittings:
            attendees = sitting.get("attendees", [])
            if attendees:
                attendances.append(len(attendees))
        
        if not attendances:
            return {}
        
        return {
            "avg_attendance": sum(attendances) / len(attendances),
            "min_attendance": min(attendances),
            "max_attendance": max(attendances)
        }
    
    def _analyze_documents(self, detailed_sittings: List[Dict]) -> Dict:
        """Analyze documents"""
        total_docs = 0
        
        for sitting in detailed_sittings:
            # Count different document types
            points = sitting.get("points", [])
            for point in points:
                # Documents might be in various fields
                if "prints" in point:
                    total_docs += len(point["prints"])
        
        return {
            "total_documents_in_sample": total_docs
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=" * 80)
        report.append(f"📊 ANALIZA PRACY KOMISJI SEJMOWEJ")
        report.append("=" * 80)
        report.append("")
        
        # Basic info
        committee = analysis.get("committee", {})
        report.append(f"Komisja: {committee.get('name', 'N/A')}")
        report.append(f"Kod: {committee.get('code', 'N/A')}")
        report.append(f"Kadencja: {analysis.get('term')}")
        report.append("")
        
        # Sittings summary
        report.append("─" * 80)
        report.append("POSIEDZENIA")
        report.append("─" * 80)
        report.append(f"Łączna liczba posiedzeń: {analysis.get('total_sittings')}")
        
        date_range = analysis.get("date_range", {})
        if date_range.get("start"):
            report.append(f"Zakres dat: {date_range['start']} - {date_range['end']}")
        report.append("")
        
        # Frequency
        freq = analysis.get("frequency", {})
        if freq:
            report.append("Częstotliwość posiedzeń:")
            by_year = freq.get("by_year", {})
            for year in sorted(by_year.keys()):
                report.append(f"  {year}: {by_year[year]} posiedzeń")
            
            if freq.get("busiest_year"):
                report.append(f"  Najbardziej aktywny rok: {freq['busiest_year']}")
            report.append("")
        
        # Detailed analysis
        detailed = analysis.get("detailed_analysis", {})
        if detailed:
            report.append("─" * 80)
            report.append(f"SZCZEGÓŁOWA ANALIZA (próbka {detailed.get('sample_size')} posiedzeń)")
            report.append("─" * 80)
            
            agenda = detailed.get("agenda_items", {})
            if agenda:
                report.append(f"Łączna liczba punktów porządku: {agenda.get('total_agenda_items')}")
                report.append(f"Średnio punktów na posiedzenie: {agenda.get('avg_items_per_sitting', 0):.1f}")
                
                topics = agenda.get("sample_topics", [])
                if topics:
                    report.append("")
                    report.append("Przykładowe tematy:")
                    for i, topic in enumerate(topics[:5], 1):
                        report.append(f"  {i}. {topic[:80]}...")
                report.append("")
            
            attendance = detailed.get("attendance", {})
            if attendance:
                report.append(f"Średnia frekwencja: {attendance.get('avg_attendance', 0):.1f} osób")
                report.append(f"Zakres: {attendance.get('min_attendance', 0)} - {attendance.get('max_attendance', 0)} osób")
                report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Demo usage
    print("🏛️  Sejm API Client - Demo")
    print()
    
    # Initialize
    client = SejmAPIClient()
    analyzer = CommitteeAnalyzer(client)
    
    # Analyze Komisja Administracji i Spraw Wewnętrznych (2019-2023)
    analysis = analyzer.analyze_committee_term(
        code="ASW",
        term=9,
        start_date="2019-11-12",  # Start of term 9
        end_date="2023-11-12"     # End of term 9
    )
    
    # Generate report
    report = analyzer.generate_report(analysis)
    print()
    print(report)
    
    # Save results
    with open("sejm_asw_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print()
    print("✅ Analysis complete!")
    print("   Results saved to: sejm_asw_analysis.json")
