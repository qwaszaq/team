#!/usr/bin/env python3
"""
Universal Agent Knowledge Search System
=======================================
Allows ALL agents to search the knowledge base before starting work
Saves tokens and prevents duplicate efforts
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AgentKnowledgeSearch')


class AgentSearchInterface(ABC):
    """Base interface for agent-specific search implementations"""
    
    def __init__(self, agent_name: str, es_url: str = "http://localhost:9200"):
        self.agent_name = agent_name
        self.es_url = es_url
        self.es_auth = ("elastic", "changeme123")
        self.search_history = []
        
    def search_knowledge(self, 
                        query: str, 
                        indices: List[str] = None,
                        filters: Dict = None,
                        size: int = 10) -> List[Dict]:
        """
        Universal search method for all agents
        """
        
        # Default indices if not specified
        if not indices:
            indices = ["project_knowledge", "universal_documents", "osint_reports_pdf"]
            
        # Log search
        self.search_history.append({
            'agent': self.agent_name,
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'indices': indices
        })
        
        logger.info(f"🔍 {self.agent_name} searching: '{query}'")
        
        # Build ES query
        es_query = self._build_query(query, filters)
        
        all_results = []
        
        # Search each index
        for index in indices:
            try:
                response = requests.post(
                    f"{self.es_url}/{index}/_search",
                    json={**es_query, "size": size},
                    auth=self.es_auth
                )
                
                if response.status_code == 200:
                    data = response.json()
                    hits = data.get('hits', {}).get('hits', [])
                    
                    for hit in hits:
                        result = {
                            'score': hit['_score'],
                            'index': index,
                            'id': hit['_id'],
                            'source': hit['_source'],
                            'highlights': hit.get('highlight', {})
                        }
                        all_results.append(result)
                        
            except Exception as e:
                logger.error(f"Error searching {index}: {e}")
                
        # Sort by score
        all_results.sort(key=lambda x: x['score'], reverse=True)
        
        return all_results[:size]
        
    def _build_query(self, query: str, filters: Dict = None) -> Dict:
        """Build Elasticsearch query"""
        
        es_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["content^2", "title", "filename", "description"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "filter": []
                }
            },
            "highlight": {
                "fields": {
                    "content": {"fragment_size": 200, "number_of_fragments": 2}
                }
            }
        }
        
        # Add filters if provided
        if filters:
            for field, value in filters.items():
                es_query["query"]["bool"]["filter"].append({
                    "term": {f"{field}.keyword": value}
                })
                
        return es_query
        
    @abstractmethod
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Each agent implements their own pre-work search logic"""
        pass


class HelenaSearch(AgentSearchInterface):
    """Helena's search implementation"""
    
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Helena checks for duplicate tasks and existing documentation"""
        
        results = self.search_knowledge(
            task_description,
            indices=["project_knowledge", "helena_tasks"]
        )
        
        if results and results[0]['score'] > 5.0:
            report = f"""
# 🔍 Helena: Found Existing Work

**Query:** {task_description}

## 📚 Existing Resources:
"""
            for i, result in enumerate(results[:3], 1):
                source = result['source']
                report += f"""
### {i}. {source.get('filename', 'Unknown')}
- **Score:** {result['score']:.2f}
- **Type:** {source.get('doc_type', 'Unknown')}
- **Date:** {source.get('indexed_at', 'Unknown')}
"""
                if result.get('highlights'):
                    report += "- **Relevant excerpt:**\n"
                    for _, highlights in result['highlights'].items():
                        for highlight in highlights[:1]:
                            report += f"  > {highlight}\n"
                            
            report += """
## 💡 Recommendation:
Review existing work before proceeding. This will save time and tokens.
"""
            return True, report
        else:
            return False, "No significant existing work found. Proceed with task."


class AleksanderSearch(AgentSearchInterface):
    """Aleksander's search implementation"""
    
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Aleksander searches for orchestration patterns and system architecture"""
        
        # Search for architectural patterns
        results = self.search_knowledge(
            f"orchestration architecture {task_description}",
            indices=["project_knowledge"],
            filters={"doc_type": "markdown_document"}
        )
        
        if results:
            report = f"""
# 🎯 Aleksander: Orchestration Context

**Task:** {task_description}

## 📐 Relevant Architecture & Patterns:
"""
            for result in results[:3]:
                source = result['source']
                report += f"\n- **{source.get('filename')}**: "
                if result.get('highlights'):
                    highlight = list(result['highlights'].values())[0][0]
                    report += f"{highlight[:150]}..."
                    
            return True, report
        
        return False, "No relevant orchestration patterns found."


class MarcusSearch(AgentSearchInterface):
    """Marcus's search implementation for financial analysis"""
    
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Marcus searches for financial data and reports"""
        
        # Extract company name if present
        company_keywords = ["Grupa Azoty", "KGHM", "Orlen", "PGNiG"]
        company = None
        for kw in company_keywords:
            if kw.lower() in task_description.lower():
                company = kw
                break
                
        # Search for financial reports
        query = f"financial report analysis {task_description}"
        filters = {"tags": "financial"} if not company else None
        
        results = self.search_knowledge(
            query,
            indices=["osint_reports_pdf", "project_knowledge", "universal_documents"],
            filters=filters
        )
        
        if results:
            report = f"""
# 💰 Marcus: Financial Analysis Resources

**Analysis Request:** {task_description}
{'**Company:** ' + company if company else ''}

## 📊 Available Financial Data:
"""
            
            # Group by year if possible
            by_year = {}
            for result in results[:10]:
                source = result['source']
                year = source.get('report_year', 'Unknown')
                if year not in by_year:
                    by_year[year] = []
                by_year[year].append(source)
                
            for year in sorted(by_year.keys(), reverse=True):
                if by_year[year]:
                    report += f"\n### Year: {year}\n"
                    for doc in by_year[year][:3]:
                        report += f"- {doc.get('filename', 'Unknown')} ({doc.get('report_period', 'N/A')})\n"
                        
            report += """
## 💡 Analysis Approach:
1. Review existing reports for baseline data
2. Identify trends across periods
3. Focus on new insights not previously documented
"""
            return True, report
            
        return False, "No existing financial data found. Will need to gather from scratch."


class ElenaSearch(AgentSearchInterface):
    """Elena's OSINT search implementation"""
    
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Elena searches for existing OSINT investigations"""
        
        # Search for investigations
        results = self.search_knowledge(
            f"investigation OSINT {task_description}",
            indices=["project_knowledge", "osint_reports_pdf"],
            size=20
        )
        
        # Filter for investigation-related docs
        investigation_results = [
            r for r in results 
            if 'investigation' in str(r['source'].get('tags', [])).lower() or
               'osint' in str(r['source'].get('tags', [])).lower() or
               r['source'].get('doc_type', '').lower() in ['investigation', 'report']
        ]
        
        if investigation_results:
            report = f"""
# 🕵️ Elena: OSINT Investigation Resources

**Investigation:** {task_description}

## 🔍 Previous Investigations:
"""
            for result in investigation_results[:5]:
                source = result['source']
                report += f"""
### {source.get('filename', 'Unknown')}
- **Type:** {source.get('doc_type', 'Investigation')}
- **Date:** {source.get('indexed_at', 'Unknown')}
- **Tags:** {', '.join(source.get('tags', []))}
"""
                if result.get('highlights'):
                    report += "- **Key findings:**\n"
                    for _, highlights in result['highlights'].items():
                        report += f"  > {highlights[0][:200]}...\n"
                        
            report += """
## 🎯 Investigation Strategy:
1. Build on existing findings
2. Verify if data is still current
3. Expand scope to new sources
4. Cross-reference with recent developments
"""
            return True, report
            
        return False, "No prior investigations found. Starting fresh OSINT collection."


class UniversalAgentSearch:
    """Factory for agent-specific search implementations"""
    
    def __init__(self):
        self.agents = {
            'Helena': HelenaSearch,
            'Aleksander': AleksanderSearch,
            'Marcus': MarcusSearch,
            'Elena': ElenaSearch,
            # Add more agents as needed
        }
        
    def get_agent_search(self, agent_name: str) -> AgentSearchInterface:
        """Get search interface for specific agent"""
        
        SearchClass = self.agents.get(agent_name)
        if SearchClass:
            return SearchClass(agent_name)
        else:
            # Return base implementation for other agents
            return GenericAgentSearch(agent_name)
            

class GenericAgentSearch(AgentSearchInterface):
    """Generic search for agents without specific implementation"""
    
    def search_before_work(self, task_description: str) -> Tuple[bool, str]:
        """Generic pre-work search"""
        
        results = self.search_knowledge(task_description)
        
        if results:
            report = f"""
# 🔍 {self.agent_name}: Knowledge Search Results

**Task:** {task_description}

## 📚 Found {len(results)} relevant documents:
"""
            for i, result in enumerate(results[:5], 1):
                source = result['source']
                report += f"\n{i}. **{source.get('filename', 'Unknown')}** (score: {result['score']:.2f})\n"
                
            return True, report
            
        return False, "No relevant documents found."


def demonstrate_agent_searches():
    """Demonstrate how different agents search before starting work"""
    
    print("🤖 AGENT KNOWLEDGE SEARCH DEMONSTRATION")
    print("=" * 80)
    print("Showing how agents can search BEFORE wasting tokens on duplicate work")
    print()
    
    # Test scenarios
    test_cases = [
        {
            'agent': 'Helena',
            'task': 'Create documentation for batch processing system'
        },
        {
            'agent': 'Marcus',
            'task': 'Analyze Grupa Azoty financial performance for 2023'
        },
        {
            'agent': 'Elena',
            'task': 'Investigate Robert Telus and CPK land transactions'
        },
        {
            'agent': 'Aleksander',
            'task': 'Design orchestration pattern for multi-agent collaboration'
        }
    ]
    
    factory = UniversalAgentSearch()
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"AGENT: {test['agent']}")
        print(f"TASK: {test['task']}")
        print("=" * 80)
        
        # Get agent-specific search
        agent_search = factory.get_agent_search(test['agent'])
        
        # Search before work
        found_existing, report = agent_search.search_before_work(test['task'])
        
        print(report)
        
        if found_existing:
            print(f"\n✅ {test['agent']} found existing work - saving tokens!")
        else:
            print(f"\n📝 {test['agent']} will proceed with new work")
            
        print("\nPress Enter to continue...")
        input()


# Integration with agent base classes
class SearchEnabledAgent:
    """Mixin for agents to add search capability"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.search = UniversalAgentSearch().get_agent_search(agent_name)
        
    def check_existing_work(self, task: str) -> Dict:
        """Check for existing work before starting"""
        
        found, report = self.search.search_before_work(task)
        
        return {
            'found_existing': found,
            'report': report,
            'should_proceed': not found or input(f"\n{self.agent_name}: Found existing work. Proceed anyway? (y/n): ").lower() == 'y'
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Knowledge Search System")
    parser.add_argument('--agent', required=True, help='Agent name')
    parser.add_argument('--search', required=True, help='Search query')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    
    args = parser.parse_args()
    
    if args.demo:
        demonstrate_agent_searches()
    else:
        # Single agent search
        factory = UniversalAgentSearch()
        agent_search = factory.get_agent_search(args.agent)
        
        print(f"\n🔍 {args.agent} searching for: {args.search}")
        print("=" * 80)
        
        results = agent_search.search_knowledge(args.search)
        
        if results:
            print(f"\nFound {len(results)} results:\n")
            for i, result in enumerate(results[:5], 1):
                source = result['source']
                print(f"{i}. {source.get('filename', 'Unknown')} (score: {result['score']:.2f})")
                print(f"   Type: {source.get('doc_type', 'Unknown')}")
                print(f"   Index: {result['index']}")
                if result.get('highlights'):
                    print("   Preview:")
                    for _, highlights in result['highlights'].items():
                        print(f"   > {highlights[0][:150]}...")
                print()
        else:
            print("No results found.")