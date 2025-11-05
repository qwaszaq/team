#!/usr/bin/env python3
"""
Process PDFs to Elasticsearch - Batch Mode
==========================================
Extract text from PDFs and index to Elasticsearch using batch processing
"""

import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import fitz  # PyMuPDF
import hashlib
from datetime import datetime
import subprocess

# Add project root
sys.path.insert(0, "/Users/artur/coursor-agents-destiny-folder")

from elasticsearch_batch_processor import ElasticsearchBatchProcessor, SearchOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PDFProcessor')

class PDFTextExtractor:
    """Extract text from PDFs with OCR fallback"""
    
    def __init__(self):
        self.stats = {
            'processed': 0,
            'text_extracted': 0,
            'ocr_needed': 0,
            'failed': 0
        }
        
    def extract_text(self, pdf_path: Path) -> Tuple[str, Dict]:
        """Extract text from PDF, return (text, metadata)"""
        
        try:
            # Open PDF
            doc = fitz.open(str(pdf_path))
            
            # Extract metadata
            metadata = {
                'page_count': len(doc),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', ''),
                'creation_date': doc.metadata.get('creationDate', ''),
                'modification_date': doc.metadata.get('modDate', ''),
            }
            
            # Extract text from all pages
            text_parts = []
            has_text = False
            
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text.strip():
                    has_text = True
                    text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
                    
            doc.close()
            
            if has_text:
                full_text = '\n\n'.join(text_parts)
                self.stats['text_extracted'] += 1
                metadata['extraction_method'] = 'native'
                metadata['confidence_score'] = 1.0
            else:
                # OCR needed (would implement here)
                logger.warning(f"⚠️  No text in {pdf_path.name} - OCR needed")
                full_text = f"[No extractable text - OCR required for {pdf_path.name}]"
                self.stats['ocr_needed'] += 1
                metadata['extraction_method'] = 'ocr_required'
                metadata['confidence_score'] = 0.0
                
            self.stats['processed'] += 1
            return full_text, metadata
            
        except Exception as e:
            logger.error(f"❌ Failed to extract from {pdf_path.name}: {e}")
            self.stats['failed'] += 1
            return f"[Error extracting text: {str(e)}]", {'error': str(e)}
            
    def extract_financial_metrics(self, text: str) -> Dict:
        """Extract financial metrics from text (simple pattern matching)"""
        import re
        
        metrics = {}
        
        # Revenue patterns (Polish)
        revenue_patterns = [
            r'Przychody.*?(\d+[\s,]\d+(?:[\s,]\d+)*)',
            r'przychody ze sprzedaży.*?(\d+[\s,]\d+(?:[\s,]\d+)*)',
            r'Revenues?.*?(\d+[\s,]\d+(?:[\s,]\d+)*)',
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(' ', '').replace(',', '')
                try:
                    metrics['revenue'] = float(value)
                    break
                except:
                    pass
                    
        # EBITDA patterns
        ebitda_patterns = [
            r'EBITDA.*?(\d+[\s,]\d+(?:[\s,]\d+)*)',
            r'Zysk operacyjny.*?(\d+[\s,]\d+(?:[\s,]\d+)*)',
        ]
        
        for pattern in ebitda_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(' ', '').replace(',', '')
                try:
                    metrics['ebitda'] = float(value)
                    break
                except:
                    pass
                    
        return metrics

class PDFBatchProcessor:
    """Process PDFs in batch mode"""
    
    def __init__(self, batch_size: int = 50):
        self.text_extractor = PDFTextExtractor()
        self.es_processor = ElasticsearchBatchProcessor(batch_size=batch_size)
        self.search_orchestrator = SearchOrchestrator(self.es_processor)
        
    def process_pdf_directory(self, directory: Path, investigation_id: str = "grupa_azoty_financial"):
        """Process all PDFs in directory"""
        
        logger.info("=" * 80)
        logger.info(f"📁 Processing PDF Directory: {directory}")
        logger.info("=" * 80)
        
        pdf_files = list(directory.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        start_time = time.time()
        
        for i, pdf_path in enumerate(pdf_files, 1):
            logger.info(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
            
            # Extract text
            text, pdf_metadata = self.text_extractor.extract_text(pdf_path)
            
            # Extract financial metrics
            if pdf_metadata.get('extraction_method') == 'native':
                financial_metrics = self.text_extractor.extract_financial_metrics(text)
            else:
                financial_metrics = {}
                
            # Prepare metadata for ES
            es_metadata = {
                'index': 'osint_reports_pdf',
                'issuer': self._extract_issuer(pdf_path),
                'investigation_id': investigation_id,
                'doc_type': 'financial_report',
                'report_year': self._extract_year(pdf_path),
                'report_period': self._extract_period(pdf_path),
                'report_url': f"https://grupaazoty.com/reports/{pdf_path.name}",
                'tags': ['financial', 'pdf', 'grupa-azoty'],
                'financial_metrics': financial_metrics,
                'pdf_metadata': pdf_metadata,
                'confidence_score': pdf_metadata.get('confidence_score', 1.0)
            }
            
            # Add to batch
            self.es_processor.add_document(
                file_path=pdf_path,
                content=text,
                metadata=es_metadata
            )
            
            # Progress update
            if i % 10 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                logger.info(f"⏱️  Progress: {i}/{len(pdf_files)} ({rate:.1f} files/sec)")
                
        # Final flush
        self.es_processor.flush()
        
        elapsed = time.time() - start_time
        
        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("✅ PROCESSING COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total time: {elapsed:.2f} seconds")
        logger.info(f"Processing rate: {len(pdf_files)/elapsed:.1f} files/second")
        logger.info("\n📊 Extraction Statistics:")
        for key, value in self.text_extractor.stats.items():
            logger.info(f"   {key}: {value}")
        logger.info("\n📊 Indexing Statistics:")
        for key, value in self.es_processor.get_stats().items():
            logger.info(f"   {key}: {value}")
            
    def _extract_issuer(self, pdf_path: Path) -> str:
        """Extract issuer from filename"""
        if 'azoty' in pdf_path.name.lower():
            return 'Grupa Azoty S.A.'
        return 'Unknown'
        
    def _extract_year(self, pdf_path: Path) -> Optional[int]:
        """Extract year from filename"""
        import re
        year_match = re.search(r'20\d{2}', pdf_path.name)
        if year_match:
            return int(year_match.group())
        return None
        
    def _extract_period(self, pdf_path: Path) -> Optional[str]:
        """Extract reporting period from filename"""
        filename_lower = pdf_path.name.lower()
        
        if any(q in filename_lower for q in ['q1', '1q', 'ikwartal']):
            return 'Q1'
        elif any(q in filename_lower for q in ['q2', '2q', 'iikwartal']):
            return 'Q2'
        elif any(q in filename_lower for q in ['q3', '3q', 'iiikwartal']):
            return 'Q3'
        elif any(q in filename_lower for q in ['q4', '4q', 'ivkwartal']):
            return 'Q4'
        elif any(a in filename_lower for a in ['annual', 'roczn', 'yearly']):
            return 'Annual'
        elif any(h in filename_lower for h in ['polrocze', 'h1', '1h', 'half']):
            return 'H1'
        return None
        
    def search_financial_data(self, query: str):
        """Search for financial data"""
        logger.info(f"\n🔍 Searching for: {query}")
        
        results = self.search_orchestrator.full_text_search(query)
        
        logger.info(f"Found {len(results)} results:")
        for i, result in enumerate(results[:5], 1):
            source = result['source']
            logger.info(f"\n{i}. {source.get('filename', 'Unknown')}")
            logger.info(f"   Score: {result['score']:.2f}")
            logger.info(f"   Year: {source.get('report_year', 'N/A')}")
            logger.info(f"   Period: {source.get('report_period', 'N/A')}")
            
            if result.get('highlights'):
                logger.info("   Highlights:")
                for field, highlights in result['highlights'].items():
                    for highlight in highlights[:2]:
                        logger.info(f"   - {highlight[:200]}...")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process PDFs to Elasticsearch")
    parser.add_argument('--directory', type=str, 
                       default="/Users/artur/coursor-agents-destiny-folder/investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs",
                       help='PDF directory to process')
    parser.add_argument('--batch-size', type=int, default=50,
                       help='Batch size for processing')
    parser.add_argument('--search', type=str,
                       help='Search query to test after processing')
    parser.add_argument('--skip-processing', action='store_true',
                       help='Skip processing, just search')
    
    args = parser.parse_args()
    
    processor = PDFBatchProcessor(batch_size=args.batch_size)
    
    if not args.skip_processing:
        pdf_dir = Path(args.directory)
        if pdf_dir.exists():
            processor.process_pdf_directory(pdf_dir)
        else:
            logger.error(f"Directory not found: {pdf_dir}")
            return
            
    if args.search:
        processor.search_financial_data(args.search)
        
    # Example searches
    if not args.search and not args.skip_processing:
        logger.info("\n" + "=" * 80)
        logger.info("📊 EXAMPLE SEARCHES")
        logger.info("=" * 80)
        
        example_queries = [
            "przychody 2023",
            "EBITDA quarterly",
            "sustainability report",
            "debt restructuring"
        ]
        
        for query in example_queries:
            processor.search_financial_data(query)
            time.sleep(1)

if __name__ == "__main__":
    # Check PyMuPDF installation
    try:
        import fitz
    except ImportError:
        logger.error("PyMuPDF not installed. Please run: pip install pymupdf")
        sys.exit(1)
        
    main()