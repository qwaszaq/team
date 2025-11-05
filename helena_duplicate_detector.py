#!/usr/bin/env python3
"""
Helena's Duplicate Task Detector
=================================
Prevents duplicate work by checking if similar tasks were already completed
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HelenaDuplicateDetector')

class DuplicateTaskDetector:
    """Helena's intelligence to detect duplicate or similar tasks"""
    
    def __init__(self, 
                 es_url: str = "http://localhost:9200",
                 es_user: str = "elastic",
                 es_password: str = "changeme123"):
        self.es_url = es_url
        self.es_auth = (es_user, es_password)
        self.similarity_threshold = 0.7  # 70% similarity to consider duplicate
        
    def check_for_duplicates(self, 
                           new_task: str, 
                           task_type: str = None,
                           investigation_id: str = None) -> Tuple[bool, List[Dict]]:
        """
        Check if a similar task was already completed
        Returns: (is_duplicate, similar_tasks)
        """
        
        logger.info(f"🔍 Helena checking for duplicate tasks...")
        logger.info(f"   New task: {new_task[:100]}...")
        
        # Search in multiple indices
        indices_to_search = [
            "project_knowledge",      # Project documentation
            "helena_tasks",           # Helena's task history
            "osint_reports_pdf",      # OSINT investigations
            "universal_documents"     # General documents
        ]
        
        all_similar_tasks = []
        
        for index in indices_to_search:
            similar = self._search_similar_in_index(
                new_task, 
                index, 
                task_type,
                investigation_id
            )
            all_similar_tasks.extend(similar)
            
        # Sort by similarity score
        all_similar_tasks.sort(key=lambda x: x['score'], reverse=True)
        
        # Check if any are above threshold
        is_duplicate = False
        if all_similar_tasks and all_similar_tasks[0]['score'] > self.similarity_threshold:
            is_duplicate = True
            
        return is_duplicate, all_similar_tasks[:5]  # Return top 5 matches
        
    def _search_similar_in_index(self, 
                                task: str, 
                                index: str,
                                task_type: str = None,
                                investigation_id: str = None) -> List[Dict]:
        """Search for similar tasks in a specific index"""
        
        # Build query
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": task,
                                "fields": [
                                    "content^2",      # Content is most important
                                    "filename",
                                    "title",
                                    "investigation_objective",
                                    "task_description"
                                ],
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
                    "content": {"fragment_size": 200},
                    "investigation_objective": {},
                    "task_description": {}
                }
            },
            "_source": ["filename", "investigation_id", "doc_type", "indexed_at", "tags"],
            "size": 10
        }
        
        # Add filters if provided
        if task_type:
            query["query"]["bool"]["filter"].append({
                "term": {"doc_type": task_type}
            })
            
        if investigation_id:
            query["query"]["bool"]["filter"].append({
                "term": {"investigation_id.keyword": investigation_id}
            })
            
        try:
            # Check if index exists
            exists_response = requests.head(
                f"{self.es_url}/{index}",
                auth=self.es_auth
            )
            
            if exists_response.status_code != 200:
                return []
                
            # Execute search
            response = requests.post(
                f"{self.es_url}/{index}/_search",
                json=query,
                auth=self.es_auth
            )
            
            if response.status_code != 200:
                logger.warning(f"Search failed for index {index}: {response.text}")
                return []
                
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])
            
            similar_tasks = []
            for hit in hits:
                source = hit['_source']
                
                # Calculate normalized score (0-1)
                max_score = data['hits']['max_score'] or 1
                normalized_score = hit['_score'] / max_score
                
                similar_task = {
                    'score': normalized_score,
                    'index': index,
                    'id': hit['_id'],
                    'filename': source.get('filename', 'Unknown'),
                    'doc_type': source.get('doc_type', 'Unknown'),
                    'investigation_id': source.get('investigation_id', 'Unknown'),
                    'indexed_at': source.get('indexed_at', 'Unknown'),
                    'tags': source.get('tags', []),
                    'highlights': hit.get('highlight', {})
                }
                
                similar_tasks.append(similar_task)
                
            return similar_tasks
            
        except Exception as e:
            logger.error(f"Error searching index {index}: {e}")
            return []
            
    def generate_duplicate_report(self, 
                                 new_task: str, 
                                 similar_tasks: List[Dict]) -> str:
        """Generate a report about duplicate/similar tasks"""
        
        report = f"""
# 🔍 Helena's Duplicate Detection Report

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** {'⚠️  DUPLICATE DETECTED' if similar_tasks else '✅ NO DUPLICATES FOUND'}

## 📋 New Task Request:
```
{new_task}
```

## 🔎 Similar Tasks Found:
"""
        
        if not similar_tasks:
            report += "\nNo similar tasks found in the system.\n"
        else:
            for i, task in enumerate(similar_tasks, 1):
                similarity_percent = task['score'] * 100
                status_emoji = "🔴" if similarity_percent > 80 else "🟡" if similarity_percent > 60 else "🟢"
                
                report += f"""
### {i}. {task['filename']} {status_emoji}
- **Similarity:** {similarity_percent:.1f}%
- **Type:** {task['doc_type']}
- **Investigation:** {task['investigation_id']}
- **Index:** {task['index']}
- **Date:** {task['indexed_at']}
- **Tags:** {', '.join(task['tags']) if task['tags'] else 'None'}
"""
                
                # Add highlights if available
                if task['highlights']:
                    report += "- **Relevant excerpts:**\n"
                    for field, highlights in task['highlights'].items():
                        for highlight in highlights[:2]:
                            clean_highlight = highlight.replace('<em>', '**').replace('</em>', '**')
                            report += f"  - ...{clean_highlight}...\n"
                            
        # Add recommendations
        report += "\n## 💡 Helena's Recommendations:\n"
        
        if similar_tasks and similar_tasks[0]['score'] > 0.8:
            report += """
**⚠️  HIGH SIMILARITY DETECTED!**

This task appears to be a duplicate or very similar to existing work. 
I recommend:
1. Review the existing results first
2. If this is intentional, clarify what's different about this request
3. Consider building upon existing work rather than starting fresh
"""
        elif similar_tasks and similar_tasks[0]['score'] > 0.6:
            report += """
**🟡 MODERATE SIMILARITY DETECTED**

Related work exists that might be relevant. Consider:
1. Reviewing existing materials for context
2. Identifying specific gaps to focus on
3. Referencing previous work to avoid redundancy
"""
        else:
            report += """
**✅ APPEARS TO BE A NEW TASK**

No significant duplicates found. This seems to be new work.
Proceeding with task execution is recommended.
"""
            
        return report
        
    def check_investigation(self, 
                          investigation_query: str,
                          company: str = None) -> Tuple[bool, str]:
        """
        Specialized check for investigation duplicates
        """
        
        # Enhance query with company name if provided
        if company:
            enhanced_query = f"{investigation_query} {company}"
        else:
            enhanced_query = investigation_query
            
        is_duplicate, similar_tasks = self.check_for_duplicates(
            enhanced_query,
            task_type="investigation"
        )
        
        # Generate specialized investigation report
        if is_duplicate:
            report = f"""
# ⚠️  Helena: Similar Investigation Detected!

I found existing investigations that match your request:
"""
            for task in similar_tasks[:3]:
                report += f"""
## 📁 {task['filename']} (Similarity: {task['score']*100:.1f}%)
- Investigation: {task['investigation_id']}
- Date: {task['indexed_at']}
"""
                if task['highlights']:
                    report += "- Key findings:\n"
                    for field, highlights in task['highlights'].items():
                        for highlight in highlights[:1]:
                            report += f"  - {highlight[:200]}...\n"
                            
            report += """
            
## 🤔 What would you like to do?
1. **View existing results** - I can retrieve the full investigation
2. **Update investigation** - Add new information to existing work  
3. **New investigation** - If you need a fresh perspective
4. **Compare timeframes** - If you want to see changes over time
"""
        else:
            report = "✅ No similar investigations found. This appears to be new work."
            
        return is_duplicate, report


class HelenaTaskValidator:
    """Integrate duplicate detection into Helena's workflow"""
    
    def __init__(self):
        self.duplicate_detector = DuplicateTaskDetector()
        
    def validate_new_task(self, task: Dict) -> Dict:
        """
        Validate a new task before processing
        """
        
        task_description = task.get('description', '')
        task_type = task.get('type', 'general')
        
        # Check for duplicates
        is_duplicate, similar_tasks = self.duplicate_detector.check_for_duplicates(
            task_description,
            task_type
        )
        
        # Generate report
        report = self.duplicate_detector.generate_duplicate_report(
            task_description,
            similar_tasks
        )
        
        # Save report
        report_path = Path(f"helena_tasks/duplicate_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
            
        # Return validation result
        validation_result = {
            'task': task,
            'is_duplicate': is_duplicate,
            'similarity_score': similar_tasks[0]['score'] if similar_tasks else 0,
            'similar_tasks': similar_tasks,
            'report_path': str(report_path),
            'recommendation': 'SKIP' if is_duplicate and similar_tasks[0]['score'] > 0.9 else 'PROCEED'
        }
        
        # Log result
        if is_duplicate:
            logger.warning(f"⚠️  DUPLICATE DETECTED: {task_description[:50]}...")
            logger.warning(f"   Most similar: {similar_tasks[0]['filename']} ({similar_tasks[0]['score']*100:.1f}%)")
        else:
            logger.info(f"✅ New task validated: {task_description[:50]}...")
            
        return validation_result


# Example usage
if __name__ == "__main__":
    # Test duplicate detection
    detector = DuplicateTaskDetector()
    
    test_cases = [
        "Analyze Grupa Azoty financial reports for 2023",
        "Investigate Robert Telus CPK land transaction", 
        "Create batch processing system for PostgreSQL",
        "Implement OSINT system with Bellingcat methodology"
    ]
    
    print("🔍 Helena's Duplicate Detection Test")
    print("=" * 60)
    
    for test_task in test_cases:
        print(f"\n📋 Checking: {test_task}")
        is_duplicate, similar_tasks = detector.check_for_duplicates(test_task)
        
        if is_duplicate:
            print(f"   ⚠️  DUPLICATE! Most similar: {similar_tasks[0]['filename']}")
            print(f"   Similarity: {similar_tasks[0]['score']*100:.1f}%")
        else:
            print("   ✅ No duplicates found")
            
    # Test investigation check
    print("\n" + "=" * 60)
    print("🔍 Investigation Duplicate Check")
    
    is_dup, report = detector.check_investigation(
        "financial analysis chemical industry",
        company="Grupa Azoty"
    )
    
    print(report)