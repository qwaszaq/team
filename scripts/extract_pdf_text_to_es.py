#!/usr/bin/env python3
"""
Extract text from downloaded PDFs and update Elasticsearch documents with content field.

Uses PyMuPDF (fitz) for fast extraction. Falls back to pdfminer if needed.
"""
import sys
import json
from pathlib import Path
from typing import Optional
import subprocess

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    from pdfminer.high_level import extract_text as pdfminer_extract
    HAS_PDFMINER = True
except ImportError:
    HAS_PDFMINER = False


def extract_text_fitz(pdf_path: Path) -> Optional[str]:
    """Extract text using PyMuPDF (fast)."""
    if not HAS_FITZ:
        return None
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"  ⚠️  fitz failed for {pdf_path.name}: {e}", file=sys.stderr)
        return None


def extract_text_pdfminer(pdf_path: Path) -> Optional[str]:
    """Extract text using pdfminer (fallback)."""
    if not HAS_PDFMINER:
        return None
    try:
        text = pdfminer_extract(str(pdf_path))
        return text.strip()
    except Exception as e:
        print(f"  ⚠️  pdfminer failed for {pdf_path.name}: {e}", file=sys.stderr)
        return None


def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using available methods."""
    text = extract_text_fitz(pdf_path)
    if text:
        return text
    text = extract_text_pdfminer(pdf_path)
    if text:
        return text
    return ""


def main():
    run_dir = Path("investigations/external/grupa_azoty_reports/run_20251104_205052")
    pdf_dir = run_dir / "pdfs"
    summary_file = run_dir / "summary.json"
    
    if not summary_file.exists():
        print(f"❌ Summary file not found: {summary_file}")
        sys.exit(1)
    
    summary = json.loads(summary_file.read_text())
    index_name = summary.get("index_name", "osint_reports_pdf")
    
    # Get list of indexed docs from ES
    cmd = [
        "curl", "-s", "-u", "elastic:changeme123",
        f"http://localhost:9200/{index_name}/_search?size=1000"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to query ES: {result.stderr}")
        sys.exit(1)
    
    response = json.loads(result.stdout)
    docs = response.get("hits", {}).get("hits", [])
    
    print(f"📄 Processing {len(docs)} documents...")
    print()
    
    bulk_updates = []
    success_count = 0
    error_count = 0
    
    for i, doc in enumerate(docs, 1):
        doc_id = doc["_id"]
        source = doc["_source"]
        local_path = Path(source["local_path"])
        
        if not local_path.exists():
            print(f"  ⚠️  [{i}/{len(docs)}] File not found: {local_path.name}")
            error_count += 1
            continue
        
        # Extract text
        text = extract_text(local_path)
        
        if not text:
            print(f"  ⚠️  [{i}/{len(docs)}] No text extracted: {local_path.name}")
            error_count += 1
            continue
        
        # Truncate to reasonable size for ES (1MB text ~= 250k tokens)
        text_preview = text[:500000] if len(text) > 500000 else text
        
        # Prepare update
        action = {"update": {"_index": index_name, "_id": doc_id}}
        update_doc = {"doc": {"content": text_preview, "content_length": len(text)}}
        
        bulk_updates.append(json.dumps(action))
        bulk_updates.append(json.dumps(update_doc))
        
        success_count += 1
        if i % 50 == 0:
            print(f"  ✅ Processed {i}/{len(docs)}...")
    
    # Bulk update ES
    if bulk_updates:
        bulk_ndjson = "\n".join(bulk_updates) + "\n"
        bulk_file = run_dir / "elasticsearch_text_updates.ndjson"
        bulk_file.write_text(bulk_ndjson, encoding="utf-8")
        
        print()
        print(f"📤 Updating Elasticsearch...")
        
        cmd = [
            "curl", "-s", "-u", "elastic:changeme123",
            "-H", "Content-Type: application/x-ndjson",
            "--data-binary", f"@{bulk_file}",
            f"http://localhost:9200/{index_name}/_bulk"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            has_errors = response.get("errors", False)
            took_ms = response.get("took", 0)
            print(f"  ✅ Bulk update completed: {took_ms}ms, errors={has_errors}")
        else:
            print(f"  ❌ Bulk update failed: {result.stderr}")
    
    print()
    print("="*80)
    print(f"✅ Text extraction completed")
    print(f"   Success: {success_count}/{len(docs)}")
    print(f"   Errors: {error_count}/{len(docs)}")
    print(f"   Index: {index_name}")
    print("="*80)


if __name__ == "__main__":
    if not HAS_FITZ and not HAS_PDFMINER:
        print("❌ No PDF extraction library available!")
        print("   Install: pip install PyMuPDF  (or: pip install pdfminer.six)")
        sys.exit(1)
    main()
