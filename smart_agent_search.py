#!/usr/bin/env python3
"""
Smart Agent Search System - Token Efficient
===========================================
Minimalizuje użycie tokenów poprzez cache i inteligentne zapytania
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import requests

class SmartAgentSearch:
    """
    Inteligentny system wyszukiwania dla agentów
    - Cache wyników
    - Rate limiting
    - Tylko gdy naprawdę potrzebne
    """
    
    def __init__(self):
        self.cache_dir = Path("search_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Konfiguracja
        self.cache_ttl_hours = 24  # Cache ważny 24h
        self.max_searches_per_hour = 100  # Max 100 zapytań na godzinę
        self.es_url = "http://localhost:9200"
        self.es_auth = ("elastic", "changeme123")
        
        # Rate limiting
        self.search_history_file = self.cache_dir / "search_history.json"
        self.load_search_history()
        
    def load_search_history(self):
        """Wczytaj historię zapytań"""
        if self.search_history_file.exists():
            with open(self.search_history_file, 'r') as f:
                self.search_history = json.load(f)
        else:
            self.search_history = []
            
    def save_search_history(self):
        """Zapisz historię zapytań"""
        with open(self.search_history_file, 'w') as f:
            json.dump(self.search_history, f)
            
    def can_search(self) -> Tuple[bool, str]:
        """Sprawdź czy można wykonać zapytanie (rate limiting)"""
        
        # Usuń stare wpisy (starsze niż godzina)
        now = datetime.now()
        cutoff = (now - timedelta(hours=1)).isoformat()
        self.search_history = [s for s in self.search_history if s['timestamp'] > cutoff]
        
        # Sprawdź limit
        if len(self.search_history) >= self.max_searches_per_hour:
            return False, f"Rate limit exceeded ({self.max_searches_per_hour}/hour). Try again later."
            
        return True, "OK"
        
    def search_if_needed(self, 
                        agent_name: str, 
                        query: str,
                        confidence_threshold: float = 0.7) -> Optional[Dict]:
        """
        Szukaj TYLKO jeśli:
        1. Nie ma w cache
        2. Agent naprawdę tego potrzebuje (confidence_threshold)
        3. Nie przekroczono limitu
        """
        
        # Sprawdź cache
        cached_result = self.get_from_cache(query)
        if cached_result:
            print(f"✅ {agent_name}: Using cached result (saving tokens!)")
            return cached_result
            
        # Sprawdź rate limit
        can_search, reason = self.can_search()
        if not can_search:
            print(f"⚠️  {agent_name}: {reason}")
            return None
            
        # Zdecyduj czy naprawdę szukać
        if not self.should_search(agent_name, query, confidence_threshold):
            print(f"💭 {agent_name}: Query too vague, skipping search to save tokens")
            return None
            
        # Wykonaj wyszukiwanie
        print(f"🔍 {agent_name}: Performing new search...")
        result = self.perform_search(agent_name, query)
        
        # Cache wynik
        if result:
            self.save_to_cache(query, result)
            
        # Zapisz w historii
        self.search_history.append({
            'agent': agent_name,
            'query': query,
            'timestamp': datetime.now().isoformat()
        })
        self.save_search_history()
        
        return result
        
    def should_search(self, agent_name: str, query: str, threshold: float) -> bool:
        """
        Inteligentnie zdecyduj czy wyszukiwać
        """
        
        # Zbyt krótkie zapytania - nie szukaj
        if len(query.split()) < 3:
            return False
            
        # Zbyt ogólne zapytania - nie szukaj
        generic_terms = ['check', 'find', 'search', 'look', 'get', 'analyze']
        query_words = query.lower().split()
        if len([w for w in query_words if w in generic_terms]) > len(query_words) / 2:
            return False
            
        # Agent-specific rules
        if agent_name == "Helena":
            # Helena szuka tylko przy konkretnych zadaniach
            return any(term in query.lower() for term in ['duplicate', 'existing', 'similar', 'previous'])
            
        elif agent_name == "Marcus":
            # Marcus szuka tylko przy konkretnych firmach/okresach
            return any(term in query.lower() for term in ['2023', '2024', 'q1', 'q2', 'q3', 'q4', 'annual', 'quarterly'])
            
        elif agent_name == "Elena":
            # Elena szuka przy konkretnych nazwiskach/firmach
            return len([w for w in query_words if w[0].isupper()]) >= 1  # Przynajmniej 1 nazwa własna
            
        # Domyślnie - szukaj jeśli confidence > threshold
        return True
        
    def get_cache_key(self, query: str) -> str:
        """Generuj klucz cache"""
        return hashlib.md5(query.lower().encode()).hexdigest()
        
    def get_from_cache(self, query: str) -> Optional[Dict]:
        """Pobierz z cache jeśli istnieje i jest ważny"""
        
        cache_key = self.get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cached = json.load(f)
                
            # Sprawdź czy cache jest nadal ważny
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time < timedelta(hours=self.cache_ttl_hours):
                return cached['result']
                
        return None
        
    def save_to_cache(self, query: str, result: Dict):
        """Zapisz wynik do cache"""
        
        cache_key = self.get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump({
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'result': result
            }, f)
            
    def perform_search(self, agent_name: str, query: str) -> Dict:
        """Wykonaj faktyczne wyszukiwanie"""
        
        # Prosty search w project_knowledge
        es_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["content", "filename", "title"],
                    "type": "best_fields"
                }
            },
            "size": 5,
            "_source": ["filename", "doc_type", "indexed_at"]
        }
        
        try:
            response = requests.post(
                f"{self.es_url}/project_knowledge/_search",
                json=es_query,
                auth=self.es_auth
            )
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', {}).get('hits', [])
                
                return {
                    'total': data['hits']['total']['value'],
                    'results': [
                        {
                            'filename': hit['_source'].get('filename', 'Unknown'),
                            'score': hit['_score'],
                            'type': hit['_source'].get('doc_type', 'Unknown')
                        }
                        for hit in hits
                    ]
                }
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            
        return {'total': 0, 'results': []}


# Prosty interfejs dla agentów
class AgentSearchHelper:
    """Prosty helper dla agentów - minimalizuje złożoność"""
    
    def __init__(self):
        self.search_engine = SmartAgentSearch()
        
    def quick_check(self, agent_name: str, topic: str) -> str:
        """
        Szybkie sprawdzenie - zwraca prosty string
        """
        
        # Buduj zapytanie inteligentnie
        if agent_name == "Marcus" and "financial" not in topic.lower():
            query = f"financial report {topic}"
        elif agent_name == "Elena" and "investigation" not in topic.lower():
            query = f"investigation OSINT {topic}"
        else:
            query = topic
            
        # Szukaj
        result = self.search_engine.search_if_needed(agent_name, query)
        
        if not result:
            return f"{agent_name}: No search performed (rate limit or vague query)"
            
        if result['total'] == 0:
            return f"{agent_name}: No existing work found on '{topic}'"
            
        # Prosty raport
        report = f"{agent_name}: Found {result['total']} related documents:\n"
        for i, doc in enumerate(result['results'][:3], 1):
            report += f"  {i}. {doc['filename']} (relevance: {doc['score']:.1f})\n"
            
        return report
        

# Przykład użycia w agencie
def agent_example():
    """Pokazuje jak agent powinien używać systemu"""
    
    helper = AgentSearchHelper()
    
    # Agent pyta TYLKO gdy ma konkretne zadanie
    print("PRZYKŁAD 1: Helena sprawdza czy zadanie już istnieje")
    print(helper.quick_check("Helena", "batch processing PostgreSQL implementation"))
    print()
    
    print("PRZYKŁAD 2: Marcus szuka danych finansowych")
    print(helper.quick_check("Marcus", "Grupa Azoty 2023"))
    print()
    
    print("PRZYKŁAD 3: Zbyt ogólne zapytanie - system odmówi")
    print(helper.quick_check("Aleksander", "check something"))
    print()
    
    print("PRZYKŁAD 4: Powtórne zapytanie - użyje cache")
    print(helper.quick_check("Helena", "batch processing PostgreSQL implementation"))
    

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--stats', action='store_true', help='Show search statistics')
    parser.add_argument('--clear-cache', action='store_true', help='Clear search cache')
    
    args = parser.parse_args()
    
    if args.demo:
        agent_example()
        
    elif args.stats:
        search = SmartAgentSearch()
        print(f"📊 Search Statistics:")
        print(f"   Searches in last hour: {len(search.search_history)}")
        print(f"   Rate limit: {search.max_searches_per_hour}/hour")
        print(f"   Cache TTL: {search.cache_ttl_hours} hours")
        
        cache_files = list(search.cache_dir.glob("*.json"))
        cache_files = [f for f in cache_files if f.name != "search_history.json"]
        print(f"   Cached results: {len(cache_files)}")
        
    elif args.clear_cache:
        search = SmartAgentSearch()
        for f in search.cache_dir.glob("*.json"):
            if f.name != "search_history.json":
                f.unlink()
        print("✅ Cache cleared")
        
    else:
        parser.print_help()
        print("\nUsage in agent code:")
        print("```python")
        print("helper = AgentSearchHelper()")
        print("result = helper.quick_check('AgentName', 'specific topic')")
        print("print(result)")
        print("```")