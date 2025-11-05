#!/usr/bin/env python3
"""
Helena Enhanced Task Processor
==============================
Adds duplicate detection to Helena's task processing workflow
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import subprocess

# Add project root
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from helena_duplicate_detector import HelenaTaskValidator, DuplicateTaskDetector

class HelenaEnhancedProcessor:
    """Enhanced task processor with duplicate detection"""
    
    def __init__(self):
        self.validator = HelenaTaskValidator()
        self.detector = DuplicateTaskDetector()
        
    def process_new_task(self, task_description: str, task_type: str = "general") -> Dict:
        """
        Process a new task with duplicate detection
        """
        
        print("=" * 80)
        print("🤖 Helena Enhanced Task Processing")
        print("=" * 80)
        print(f"Task: {task_description[:100]}...")
        print(f"Type: {task_type}")
        print()
        
        # Step 1: Check for duplicates
        print("Step 1: Checking for duplicates...")
        validation_result = self.validator.validate_new_task({
            'description': task_description,
            'type': task_type,
            'timestamp': datetime.now().isoformat()
        })
        
        # Step 2: Display results
        if validation_result['is_duplicate']:
            print(f"\n⚠️  DUPLICATE DETECTED!")
            print(f"Similarity: {validation_result['similarity_score']*100:.1f}%")
            print(f"Most similar task: {validation_result['similar_tasks'][0]['filename']}")
            print(f"\nDuplicate report saved: {validation_result['report_path']}")
            
            # Show report content
            with open(validation_result['report_path'], 'r') as f:
                print("\n" + "-" * 40)
                print(f.read())
                print("-" * 40)
                
            # Ask user what to do
            if validation_result['similarity_score'] > 0.9:
                print("\n🤔 This task is VERY similar to existing work.")
                print("Options:")
                print("1. View existing results")
                print("2. Proceed anyway (update/refresh)")
                print("3. Cancel")
                
                response = input("\nYour choice (1/2/3): ").strip()
                
                if response == "1":
                    # Show existing results
                    self._show_existing_results(validation_result['similar_tasks'][0])
                    return {'status': 'viewing_existing', 'result': validation_result}
                elif response == "3":
                    print("\n❌ Task cancelled.")
                    return {'status': 'cancelled', 'result': validation_result}
                else:
                    print("\n✅ Proceeding with task (updating existing work)...")
                    
        else:
            print("\n✅ No duplicates found! This is new work.")
            
        # Step 3: Process the task
        print("\nStep 2: Processing task...")
        
        # Create Helena task file
        task_filename = f"helena_task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_enhanced.md"
        task_path = Path("helena_tasks") / task_filename
        task_path.parent.mkdir(exist_ok=True)
        
        # Add duplicate warning if needed
        if validation_result['is_duplicate']:
            task_content = f"""# ⚠️  Task Update/Refresh

**Note:** This task has {validation_result['similarity_score']*100:.1f}% similarity to existing work.
Most similar: {validation_result['similar_tasks'][0]['filename']}

---

{task_description}
"""
        else:
            task_content = task_description
            
        # Save task
        with open(task_path, 'w') as f:
            f.write(task_content)
            
        print(f"✅ Task saved: {task_path}")
        
        # Trigger Helena processing (if realtime watcher is running)
        print("\nStep 3: Task queued for Helena processing...")
        print("(The realtime watcher will detect and process it automatically)")
        
        return {
            'status': 'processed',
            'task_file': str(task_path),
            'is_duplicate': validation_result['is_duplicate'],
            'validation_result': validation_result
        }
        
    def _show_existing_results(self, similar_task: Dict):
        """Show existing results for a similar task"""
        
        print(f"\n📄 Existing Results: {similar_task['filename']}")
        print("=" * 60)
        
        # Try to retrieve the document
        try:
            # Search for the document content
            query = {
                "query": {
                    "term": {
                        "_id": similar_task['id']
                    }
                },
                "_source": ["content", "filename", "indexed_at"]
            }
            
            import requests
            response = requests.post(
                f"http://localhost:9200/{similar_task['index']}/_search",
                json=query,
                auth=("elastic", "changeme123")
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['hits']['hits']:
                    doc = data['hits']['hits'][0]['_source']
                    content = doc.get('content', 'Content not available')
                    
                    # Show first 2000 chars
                    if len(content) > 2000:
                        print(content[:2000] + "\n\n... [truncated] ...")
                    else:
                        print(content)
                        
        except Exception as e:
            print(f"Error retrieving document: {e}")
            
        print("\n" + "=" * 60)
        
    def check_investigation_duplicate(self, company: str, topic: str):
        """
        Specialized check for investigation duplicates
        """
        
        print("=" * 80)
        print("🔍 Helena: Investigation Duplicate Check")
        print("=" * 80)
        print(f"Company: {company}")
        print(f"Topic: {topic}")
        print()
        
        query = f"{topic} {company}"
        is_duplicate, report = self.detector.check_investigation(query, company)
        
        print(report)
        
        if is_duplicate:
            response = input("\nHow would you like to proceed? (1-4): ").strip()
            return {'is_duplicate': True, 'user_choice': response}
        else:
            return {'is_duplicate': False}


def main():
    """Test the enhanced processor"""
    
    processor = HelenaEnhancedProcessor()
    
    # Test cases
    test_tasks = [
        {
            'description': "Create a comprehensive batch processing system for PostgreSQL to handle high-volume data ingestion",
            'type': 'technical_implementation'
        },
        {
            'description': "Analyze financial reports for Grupa Azoty from 2023 with focus on sustainability metrics",
            'type': 'financial_analysis'
        },
        {
            'description': "Build a real-time monitoring dashboard for system health metrics",
            'type': 'new_feature'
        }
    ]
    
    print("🧪 Testing Helena Enhanced Processor")
    print("=" * 80)
    
    for i, task in enumerate(test_tasks, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST CASE {i}")
        print('='*80)
        
        result = processor.process_new_task(
            task['description'],
            task['type']
        )
        
        print(f"\nResult: {result['status']}")
        
        input("\nPress Enter for next test...")
        
    # Test investigation duplicate check
    print("\n\n" + "="*80)
    print("INVESTIGATION DUPLICATE CHECK TEST")
    print("="*80)
    
    processor.check_investigation_duplicate("Grupa Azoty", "financial performance analysis")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Helena Enhanced Task Processor")
    parser.add_argument('--task', help='Task description')
    parser.add_argument('--type', default='general', help='Task type')
    parser.add_argument('--check-investigation', nargs=2, metavar=('COMPANY', 'TOPIC'),
                       help='Check for investigation duplicates')
    parser.add_argument('--test', action='store_true', help='Run test cases')
    
    args = parser.parse_args()
    
    processor = HelenaEnhancedProcessor()
    
    if args.task:
        # Process single task
        result = processor.process_new_task(args.task, args.type)
        print(f"\n✅ Task processing complete: {result['status']}")
        
    elif args.check_investigation:
        # Check investigation
        company, topic = args.check_investigation
        processor.check_investigation_duplicate(company, topic)
        
    elif args.test:
        # Run tests
        main()
        
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # Process a new task")
        print("  python helena_enhanced_processor.py --task 'Analyze Q4 2024 financial results'")
        print()
        print("  # Check investigation duplicate")  
        print("  python helena_enhanced_processor.py --check-investigation 'Grupa Azoty' 'debt analysis'")
        print()
        print("  # Run test cases")
        print("  python helena_enhanced_processor.py --test")