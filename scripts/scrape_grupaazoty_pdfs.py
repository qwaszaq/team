#!/usr/bin/env python3
"""
Scrape PDF periodic reports from Grupa Azoty Tarnów IR and prepare Elasticsearch bulk.

- Crawls starting from a base URL, follows internal links containing 'raport'/'raporty'
- Collects absolute links to .pdf files
- Downloads PDFs to an output directory
- Writes:
  - summary.json with counts and file metadata
  - elasticsearch_bulk.ndjson with index actions (no auth)

No external dependencies (stdlib only).
"""
import sys
import os
import re
import json
import time
import hashlib
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (compatible; DestinyBot/1.0; +https://example.local)"

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        href = None
        for k, v in attrs:
            if k.lower() == 'href':
                href = v
                break
        if href:
            self.links.append(href)


def http_get(url: str, timeout: int = 20) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_links(url: str) -> list[str]:
    try:
        html = http_get(url).decode('utf-8', errors='ignore')
    except Exception as e:
        return []
    parser = LinkExtractor()
    parser.feed(html)
    return parser.links


def is_same_host(url: str, base_netloc: str) -> bool:
    try:
        return urlparse(url).netloc in ("", base_netloc)
    except Exception:
        return False


def normalize_url(href: str, base_url: str) -> str:
    try:
        return urljoin(base_url, href)
    except Exception:
        return href


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    base_url = "https://tarnow.grupaazoty.com/relacje-inwestorskie/raporty-okresowe"
    out_root = Path("investigations/external/grupa_azoty_reports")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"run_{timestamp}"
    pdf_dir = out_dir / "pdfs"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    base_netloc = urlparse(base_url).netloc

    to_visit = [base_url]
    visited = set()
    pdf_urls: set[str] = set()

    # Simple crawl within domain, limited breadth
    max_pages = 50
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            links = fetch_links(url)
        except Exception:
            continue
        for href in links:
            abs_url = normalize_url(href, url)
            if not is_same_host(abs_url, base_netloc):
                continue
            # Collect PDFs
            if abs_url.lower().endswith('.pdf'):
                pdf_urls.add(abs_url)
                continue
            # Heuristic: follow IR subpages with raport keywords
            path = urlparse(abs_url).path.lower()
            if any(k in path for k in ["raport", "raporty", "sprawozd", "okresow"]):
                if abs_url not in visited and abs_url not in to_visit:
                    to_visit.append(abs_url)
        # Be polite
        time.sleep(0.3)

    # Download PDFs
    records = []
    for i, pdf_url in enumerate(sorted(pdf_urls)):
        try:
            content = http_get(pdf_url, timeout=40)
        except Exception:
            continue
        fname = pdf_url.split('/')[-1] or f"report_{i}.pdf"
        safe_fname = re.sub(r"[^A-Za-z0-9_.-]", "_", fname)
        fpath = pdf_dir / safe_fname
        fpath.write_bytes(content)
        size = fpath.stat().st_size
        file_hash = sha256_file(fpath)
        rec = {
            "issuer": "Grupa Azoty (Tarnów)",
            "source_base_url": base_url,
            "report_url": pdf_url,
            "filename": safe_fname,
            "file_size": size,
            "sha256": file_hash,
            "downloaded_at": datetime.utcnow().isoformat() + 'Z',
            "local_path": str(fpath),
            "report_type": "periodic_report",  # heuristic
        }
        records.append(rec)
        # Be polite
        time.sleep(0.2)

    # Write summary
    summary = {
        "base_url": base_url,
        "visited_pages": len(visited),
        "pdf_found": len(pdf_urls),
        "pdf_downloaded": len(records),
        "out_dir": str(out_dir),
        "index_name": "osint_reports_pdf",
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Prepare Elasticsearch bulk NDJSON
    index_name = summary["index_name"]
    bulk_lines = []
    for rec in records:
        action = {"index": {"_index": index_name}}
        bulk_lines.append(json.dumps(action))
        bulk_lines.append(json.dumps(rec, ensure_ascii=False))
    (out_dir / "elasticsearch_bulk.ndjson").write_text("\n".join(bulk_lines) + "\n", encoding="utf-8")

    # Print brief report
    print("PDF crawl completed")
    print(json.dumps(summary, indent=2))
    print(f"Artifacts: {out_dir}")
    print("To index into Elasticsearch (with Basic auth):")
    bulk_path = out_dir / 'elasticsearch_bulk.ndjson'
    print(f"  curl -u 'elastic:YOUR_PASSWORD' -s -H 'Content-Type: application/x-ndjson' --data-binary @{bulk_path} http://localhost:9200/{index_name}/_bulk")
    print("If index missing, create minimal mapping:")
    mapping = {"mappings": {"properties": {"downloaded_at": {"type": "date"}, "file_size": {"type": "long"}}}}
    mapping_json = json.dumps(mapping)
    print(f"  curl -u 'elastic:YOUR_PASSWORD' -s -XPUT http://localhost:9200/{index_name} -H 'Content-Type: application/json' -d '{mapping_json}'")

if __name__ == "__main__":
    main()
