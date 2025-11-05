#!/usr/bin/env python3
"""
Universal Batch Processor for All File Types
============================================
Processes any supported file type to Elasticsearch in batches
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add project root
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from elasticsearch_batch_processor import ElasticsearchBatchProcessor, SearchOrchestrator
from universal_file_extractor import UniversalFileExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('UniversalBatchProcessor')

class UniversalBatchProcessor:
    """Process any file type in batch mode to Elasticsearch"""
    
    def __init__(self, batch_size: int = 50):
        self.extractor = UniversalFileExtractor()
        self.es_processor = ElasticsearchBatchProcessor(batch_size=batch_size)
        self.search_orchestrator = SearchOrchestrator(self.es_processor)
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'by_type': {}
        }
        
    def process_directory(self, 
                         directory: Path, 
                         pattern: str = "*",
                         recursive: bool = True,
                         investigation_id: Optional[str] = None,
                         index_name: str = "universal_documents"):
        """Process all matching files in directory"""
        
        logger.info("=" * 80)
        logger.info(f"📁 Processing Directory: {directory}")
        logger.info(f"   Pattern: {pattern}")
        logger.info(f"   Recursive: {recursive}")
        logger.info(f"   Index: {index_name}")
        logger.info("=" * 80)
        
        # Find files
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))
            
        # Filter out directories and hidden files
        files = [f for f in files if f.is_file() and not f.name.startswith('.')]
        
        self.stats['total_files'] = len(files)
        logger.info(f"Found {len(files)} files to process")
        
        # Group by extension for reporting
        extensions = {}
        for f in files:
            ext = f.suffix.lower()
            extensions[ext] = extensions.get(ext, 0) + 1
            
        logger.info("File types found:")
        for ext, count in sorted(extensions.items()):
            logger.info(f"   {ext}: {count} files")
            
        # Process files
        start_time = time.time()
        
        for i, file_path in enumerate(files, 1):
            try:
                self._process_file(
                    file_path=file_path,
                    index_name=index_name,
                    investigation_id=investigation_id,
                    file_number=i,
                    total_files=len(files)
                )
                
                # Progress update
                if i % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed
                    eta = (len(files) - i) / rate
                    logger.info(f"⏱️  Progress: {i}/{len(files)} ({rate:.1f} files/sec, ETA: {eta:.0f}s)")
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                self.stats['errors'] += 1
                
        # Final flush
        self.es_processor.flush()
        
        # Summary
        elapsed = time.time() - start_time
        self._print_summary(elapsed)
        
    def _process_file(self, 
                     file_path: Path, 
                     index_name: str,
                     investigation_id: Optional[str],
                     file_number: int,
                     total_files: int):
        """Process a single file"""
        
        logger.info(f"\n[{file_number}/{total_files}] Processing: {file_path.name}")
        
        # Extract text and metadata
        text, metadata = self.extractor.extract(file_path)
        
        # Skip if extraction failed completely
        if metadata.get('error') and not text:
            logger.warning(f"   ⚠️  Skipping due to extraction error: {metadata['error']}")
            self.stats['skipped'] += 1
            return
            
        # Prepare ES metadata
        es_metadata = {
            'index': index_name,
            'investigation_id': investigation_id or 'general',
            'doc_type': self._determine_doc_type(file_path, metadata),
            'issuer': self._extract_issuer(file_path, text),
            'tags': self._generate_tags(file_path, text, metadata),
            **metadata  # Include all extractor metadata
        }
        
        # Special handling for different file types
        file_ext = file_path.suffix.lower()
        
        if file_ext in ['.xls', '.xlsx', '.csv']:
            es_metadata['doc_type'] = 'spreadsheet'
            es_metadata['tags'].append('tabular-data')
            
        elif file_ext in ['.doc', '.docx', '.odt', '.rtf']:
            es_metadata['doc_type'] = 'document'
            es_metadata['tags'].append('text-document')
            
        elif file_ext in ['.html', '.htm', '.xml']:
            es_metadata['doc_type'] = 'markup'
            es_metadata['tags'].append('structured-text')
            
        elif file_ext == '.json':
            es_metadata['doc_type'] = 'data'
            es_metadata['tags'].append('structured-data')
            
        # Add to batch
        self.es_processor.add_document(
            file_path=file_path,
            content=text,
            metadata=es_metadata
        )
        
        self.stats['processed'] += 1
        ext = file_path.suffix.lower()
        self.stats['by_type'][ext] = self.stats['by_type'].get(ext, 0) + 1
        
        logger.info(f"   ✅ Processed: {len(text)} chars, {len(metadata)} metadata fields")
        
    def _determine_doc_type(self, file_path: Path, metadata: Dict) -> str:
        """Determine document type from file and metadata"""
        
        ext = file_path.suffix.lower()
        name_lower = file_path.name.lower()
        
        # Financial documents
        if any(term in name_lower for term in ['financial', 'finansow', 'report', 'raport', 'statement']):
            return 'financial_report'
            
        # Legal documents
        elif any(term in name_lower for term in ['legal', 'prawny', 'contract', 'umowa', 'agreement']):
            return 'legal_document'
            
        # Technical documents
        elif any(term in name_lower for term in ['technical', 'techniczny', 'spec', 'documentation']):
            return 'technical_document'
            
        # Logs
        elif ext in ['.log', '.txt'] and 'log' in name_lower:
            return 'log_file'
            
        # Data files
        elif ext in ['.json', '.xml', '.csv']:
            return 'data_file'
            
        # Default by extension
        elif ext in ['.pdf']:
            return 'pdf_document'
        elif ext in ['.doc', '.docx', '.odt', '.rtf']:
            return 'word_document'
        elif ext in ['.xls', '.xlsx', '.ods']:
            return 'spreadsheet'
        elif ext in ['.html', '.htm']:
            return 'web_page'
        elif ext in ['.md']:
            return 'markdown_document'
        else:
            return 'document'
            
    def _extract_issuer(self, file_path: Path, text: str) -> str:
        """Extract document issuer/author"""
        
        # From filename
        if 'grupa' in file_path.name.lower() and 'azoty' in file_path.name.lower():
            return 'Grupa Azoty S.A.'
            
        # From content (first 1000 chars)
        text_start = text[:1000].lower()
        
        issuers = {
            'grupa azoty': 'Grupa Azoty S.A.',
            'kghm': 'KGHM Polska Miedź S.A.',
            'orlen': 'PKN Orlen S.A.',
            'pgnig': 'PGNiG S.A.',
            'cpk': 'Centralny Port Komunikacyjny',
        }
        
        for key, issuer in issuers.items():
            if key in text_start:
                return issuer
                
        return 'Unknown'
        
    def _generate_tags(self, file_path: Path, text: str, metadata: Dict) -> List[str]:
        """Generate relevant tags for the document"""
        
        tags = []
        
        # File type tag
        ext = file_path.suffix.lower()
        if ext:
            tags.append(ext[1:])  # Remove dot
            
        # Content-based tags
        text_lower = text[:5000].lower()  # Check first 5000 chars
        
        tag_keywords = {
            'financial': ['revenue', 'przychody', 'ebitda', 'profit', 'zysk'],
            'legal': ['agreement', 'umowa', 'contract', 'kontrakt'],
            'technical': ['specification', 'specyfikacja', 'architecture'],
            'environmental': ['sustainability', 'environment', 'środowisko'],
            'quarterly': ['quarter', 'kwartał', 'q1', 'q2', 'q3', 'q4'],
            'annual': ['annual', 'roczny', 'yearly'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
                
        # Size-based tags
        file_size = metadata.get('file_size', 0)
        if file_size > 10 * 1024 * 1024:  # > 10MB
            tags.append('large-file')
        elif file_size < 10 * 1024:  # < 10KB
            tags.append('small-file')
            
        # Quality tags
        if metadata.get('has_text') is False:
            tags.append('ocr-needed')
        if metadata.get('error'):
            tags.append('extraction-error')
            
        return list(set(tags))  # Remove duplicates
        
    def _print_summary(self, elapsed_time: float):
        """Print processing summary"""
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ BATCH PROCESSING COMPLETE")
        logger.info("=" * 80)
        
        logger.info(f"\n📊 Overall Statistics:")
        logger.info(f"   Total files: {self.stats['total_files']}")
        logger.info(f"   Processed: {self.stats['processed']}")
        logger.info(f"   Skipped: {self.stats['skipped']}")
        logger.info(f"   Errors: {self.stats['errors']}")
        logger.info(f"   Time: {elapsed_time:.2f} seconds")
        logger.info(f"   Rate: {self.stats['processed']/elapsed_time:.1f} files/second")
        
        logger.info(f"\n📁 By File Type:")
        for ext, count in sorted(self.stats['by_type'].items()):
            logger.info(f"   {ext}: {count} files")
            
        logger.info(f"\n🔍 Extraction Statistics:")
        extractor_stats = self.extractor.get_stats()
        logger.info(f"   Successful: {extractor_stats['successful']}")
        logger.info(f"   Failed: {extractor_stats['failed']}")
        
        logger.info(f"\n📊 Elasticsearch Statistics:")
        es_stats = self.es_processor.get_stats()
        for key, value in es_stats.items():
            logger.info(f"   {key}: {value}")
            
    def search_documents(self, query: str, index: str = "universal_documents"):
        """Search indexed documents"""
        
        logger.info(f"\n🔍 Searching for: '{query}' in index: {index}")
        
        results = self.search_orchestrator.full_text_search(query, index)
        
        logger.info(f"Found {len(results)} results:")
        
        for i, result in enumerate(results[:10], 1):
            source = result['source']
            logger.info(f"\n{i}. {source.get('filename', 'Unknown')}")
            logger.info(f"   Type: {source.get('doc_type', 'Unknown')}")
            logger.info(f"   Score: {result['score']:.2f}")
            logger.info(f"   File type: {source.get('file_type', 'Unknown')}")
            logger.info(f"   Tags: {', '.join(source.get('tags', []))}")
            
            if result.get('highlights'):
                logger.info("   Highlights:")
                for field, highlights in result['highlights'].items():
                    for highlight in highlights[:2]:
                        logger.info(f"   - ...{highlight.strip()}...")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Batch Processor")
    parser.add_argument('directory', nargs='?', help='Directory to process')
    parser.add_argument('--pattern', default='*', help='File pattern (default: *)')
    parser.add_argument('--recursive', action='store_true', help='Process subdirectories')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size')
    parser.add_argument('--index', default='universal_documents', help='ES index name')
    parser.add_argument('--investigation', help='Investigation ID')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--test', action='store_true', help='Test mode')
    
    args = parser.parse_args()
    
    processor = UniversalBatchProcessor(batch_size=args.batch_size)
    
    if args.test:
        # Test with project files
        logger.info("🧪 TEST MODE - Processing sample files")
        
        test_dir = Path(".")
        test_patterns = ['*.md', '*.json', '*.txt', '*.py']
        
        for pattern in test_patterns[:2]:  # Just MD and JSON for test
            logger.info(f"\nTesting pattern: {pattern}")
            processor.process_directory(
                directory=test_dir,
                pattern=pattern,
                recursive=False,
                index_name="test_universal",
                investigation_id="test"
            )
            
        # Test search
        processor.search_documents("agent", "test_universal")
        
    elif args.search:
        processor.search_documents(args.search, args.index)
        
    elif args.directory:
        directory = Path(args.directory)
        if not directory.exists():
            logger.error(f"Directory not found: {directory}")
            return
            
        processor.process_directory(
            directory=directory,
            pattern=args.pattern,
            recursive=args.recursive,
            index_name=args.index,
            investigation_id=args.investigation
        )
        
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # Process all PDFs in directory")
        print("  python universal_batch_processor.py /path/to/docs --pattern '*.pdf'")
        print()
        print("  # Process all Office documents recursively")
        print("  python universal_batch_processor.py /path/to/docs --pattern '*.doc*' --recursive")
        print()
        print("  # Process everything in investigation")
        print("  python universal_batch_processor.py investigations/active --recursive --investigation case001")
        print()
        print("  # Search indexed documents")
        print("  python universal_batch_processor.py --search 'financial statement 2023'")


if __name__ == "__main__":
    main()