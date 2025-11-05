#!/usr/bin/env python3
"""
Index Project Knowledge to Elasticsearch
=========================================
Indexes all project documentation (MD files) for searchable knowledge base
"""

import sys
from pathlib import Path
from datetime import datetime
import logging

# Add project root
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from universal_batch_processor import UniversalBatchProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ProjectKnowledgeIndexer')

class ProjectKnowledgeIndexer:
    """Index project documentation to Elasticsearch"""
    
    def __init__(self):
        self.processor = UniversalBatchProcessor(batch_size=50)
        self.project_root = Path("/Users/artur/coursor-agents-destiny-folder")
        
        # Categories based on directory structure
        self.categories = {
            'docs/status': 'status_updates',
            'docs/team': 'team_protocols',
            'docs/protocols': 'system_protocols',
            'docs/guides': 'implementation_guides',
            'docs/analysis': 'technical_analysis',
            'docs/architecture': 'system_architecture',
            'docs/research': 'research_findings',
            'docs/concepts': 'conceptual_designs',
            'docs/tasks': 'task_definitions',
            'docs/capabilities': 'capability_specs',
            'docs/technical': 'technical_docs',
            'docs/auto-generated': 'auto_generated',
            'helena_tasks': 'helena_tasks',
            'agents': 'agent_documentation',
        }
        
    def index_all_documentation(self):
        """Index all project documentation"""
        
        logger.info("=" * 80)
        logger.info("🚀 PROJECT KNOWLEDGE INDEXING")
        logger.info("=" * 80)
        logger.info(f"Project root: {self.project_root}")
        logger.info(f"Target index: project_knowledge")
        logger.info("")
        
        total_processed = 0
        
        # Process each category
        for path_pattern, category in self.categories.items():
            category_path = self.project_root / path_pattern
            
            if category_path.exists():
                logger.info(f"\n📁 Processing category: {category}")
                logger.info(f"   Path: {category_path}")
                
                # Count files first
                md_files = list(category_path.rglob("*.md"))
                logger.info(f"   Found {len(md_files)} MD files")
                
                if md_files:
                    # Process with category-specific metadata
                    self._process_category(
                        category_path=category_path,
                        category=category,
                        investigation_id=f"project_{category}"
                    )
                    
                    total_processed += len(md_files)
                    
        # Also process root-level MD files
        root_md_files = list(self.project_root.glob("*.md"))
        if root_md_files:
            logger.info(f"\n📁 Processing root-level files")
            logger.info(f"   Found {len(root_md_files)} MD files")
            
            for md_file in root_md_files:
                self.processor.process_directory(
                    directory=md_file.parent,
                    pattern=md_file.name,
                    recursive=False,
                    index_name="project_knowledge",
                    investigation_id="project_root"
                )
                
            total_processed += len(root_md_files)
            
        logger.info("\n" + "=" * 80)
        logger.info(f"✅ INDEXING COMPLETE")
        logger.info(f"   Total files processed: {total_processed}")
        logger.info("=" * 80)
        
        # Show sample searches
        self._demonstrate_search()
        
    def _process_category(self, category_path: Path, category: str, investigation_id: str):
        """Process a specific category of documents"""
        
        # Custom metadata enrichment based on category
        if category == 'status_updates':
            # Status updates are time-sensitive
            self.processor.process_directory(
                directory=category_path,
                pattern="*.md",
                recursive=True,
                index_name="project_knowledge",
                investigation_id=investigation_id
            )
            
        elif category == 'team_protocols':
            # Team protocols are important references
            self.processor.process_directory(
                directory=category_path,
                pattern="*.md",
                recursive=True,
                index_name="project_knowledge",
                investigation_id=investigation_id
            )
            
        else:
            # Default processing
            self.processor.process_directory(
                directory=category_path,
                pattern="*.md",
                recursive=True,
                index_name="project_knowledge",
                investigation_id=investigation_id
            )
            
    def _demonstrate_search(self):
        """Show example searches on indexed knowledge"""
        
        logger.info("\n" + "=" * 80)
        logger.info("🔍 KNOWLEDGE SEARCH EXAMPLES")
        logger.info("=" * 80)
        
        example_queries = [
            # Architecture queries
            ("architecture postgres", "Find PostgreSQL architecture docs"),
            ("batch processing", "Find batch processing documentation"),
            ("elasticsearch integration", "Find ES integration docs"),
            
            # Agent queries
            ("helena agent tasks", "Find Helena's task documentation"),
            ("aleksander orchestration", "Find orchestration protocols"),
            
            # Protocol queries
            ("source attribution protocol", "Find source attribution rules"),
            ("verification protocol", "Find verification procedures"),
            
            # Status queries
            ("morning brief", "Find daily status updates"),
            ("system health", "Find health check documentation"),
            
            # Technical queries
            ("OSINT system", "Find OSINT system documentation"),
            ("knowledge graph neo4j", "Find graph database docs"),
        ]
        
        for query, description in example_queries[:5]:  # Just show 5 examples
            logger.info(f"\n💡 {description}")
            logger.info(f"   Query: '{query}'")
            self.processor.search_documents(query, "project_knowledge")
            
    def create_knowledge_dashboard(self):
        """Create a knowledge dashboard view"""
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "index": "project_knowledge",
            "categories": {},
            "search_tips": [
                "Use agent names (Helena, Aleksander, etc.) to find agent-specific docs",
                "Use 'protocol' to find system protocols and procedures",
                "Use 'architecture' to find technical architecture documents",
                "Use 'analysis' to find technical analysis and evaluations",
                "Use date ranges to find time-specific documentation"
            ],
            "key_documents": [
                "README.md - Project overview",
                "MORNING_BRIEF_*.md - Daily status updates",
                "COMPREHENSIVE_OSINT_SYSTEM.md - OSINT architecture",
                "BATCH_MIGRATION_PLAN.md - Batch processing design",
                "SOURCE_ATTRIBUTION_PROTOCOL.md - Attribution rules"
            ]
        }
        
        # Save dashboard
        dashboard_path = self.project_root / "PROJECT_KNOWLEDGE_DASHBOARD.json"
        import json
        with open(dashboard_path, 'w') as f:
            json.dump(dashboard, f, indent=2)
            
        logger.info(f"\n📊 Dashboard created: {dashboard_path}")
        
    def search_project_knowledge(self, query: str):
        """Search project knowledge base"""
        
        logger.info(f"\n🔍 Searching project knowledge for: '{query}'")
        
        results = self.processor.search_orchestrator.full_text_search(query, "project_knowledge")
        
        if results:
            logger.info(f"\nFound {len(results)} results:")
            
            for i, result in enumerate(results[:10], 1):
                source = result['source']
                score = result['score']
                
                # Extract key info
                filename = source.get('filename', 'Unknown')
                file_path = source.get('file_name', '')
                category = source.get('investigation_id', '').replace('project_', '')
                
                logger.info(f"\n{i}. {filename} (score: {score:.2f})")
                logger.info(f"   Category: {category}")
                logger.info(f"   Path: {file_path}")
                
                # Show highlights
                if result.get('highlights'):
                    logger.info("   Relevant excerpts:")
                    for field, highlights in result['highlights'].items():
                        for highlight in highlights[:2]:
                            # Clean up highlight
                            clean_highlight = highlight.strip().replace('\n', ' ')
                            if len(clean_highlight) > 150:
                                clean_highlight = clean_highlight[:150] + "..."
                            logger.info(f"   - ...{clean_highlight}")
        else:
            logger.info("No results found.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Index Project Knowledge")
    parser.add_argument('--search', help='Search indexed knowledge')
    parser.add_argument('--index', action='store_true', help='Index all documentation')
    parser.add_argument('--dashboard', action='store_true', help='Create knowledge dashboard')
    parser.add_argument('--quick', action='store_true', help='Quick index (just key directories)')
    
    args = parser.parse_args()
    
    indexer = ProjectKnowledgeIndexer()
    
    if args.search:
        # Just search
        indexer.search_project_knowledge(args.search)
        
    elif args.dashboard:
        # Create dashboard
        indexer.create_knowledge_dashboard()
        
    elif args.index or args.quick:
        # Index documentation
        if args.quick:
            # Quick mode - just key directories
            logger.info("🚀 QUICK MODE - Indexing key directories only")
            indexer.categories = {
                'docs/architecture': 'system_architecture',
                'docs/protocols': 'system_protocols',
                'docs/guides': 'implementation_guides',
            }
            
        indexer.index_all_documentation()
        
        # Create dashboard after indexing
        indexer.create_knowledge_dashboard()
        
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # Index all project documentation")
        print("  python index_project_knowledge.py --index")
        print()
        print("  # Quick index (key docs only)")
        print("  python index_project_knowledge.py --quick")
        print()
        print("  # Search indexed knowledge")
        print("  python index_project_knowledge.py --search 'batch processing'")
        print()
        print("  # Create knowledge dashboard")
        print("  python index_project_knowledge.py --dashboard")


if __name__ == "__main__":
    main()