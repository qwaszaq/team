#!/usr/bin/env python3
"""
Ingest OSINT investigation sources into all data layers with hygienic separation.

- Uses a dedicated project_id namespace per investigation, e.g.:
  project_id = "investigation-telus_cpk_real_001"
- Adds metadata to mark scope: data_scope=investigation, usage_scope=task_only, etc.
- Stores rich context and tags in PostgreSQL messages table
- Uses per-project Qdrant collection and Redis key via HelenaCore(project_id=...)

Usage:
  python scripts/ingest_investigation_osint.py --investigation-id telus_cpk_real_001 \
      --made-by Elena --importance 0.9
"""
import argparse
import os
from pathlib import Path
from typing import Dict, List

from helena_core import HelenaCore


def chunk_text(text: str, max_chars: int = 4000) -> List[str]:
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunks.append(text[start:end])
        start = end
    return chunks


def build_metadata(investigation_id: str, source_path: Path) -> Dict:
    filename = source_path.name
    return {
        "message_type": "OSINT_SOURCE",
        "recipient": "Investigations",
        "data_scope": "investigation",
        "investigation_id": investigation_id,
        "usage_scope": "task_only",
        "visibility": "investigation_only",
        "retention": "ephemeral-90d",
        "source_path": str(source_path),
        "source_type": "web_html",
        "tags": [
            "osint",
            "investigation",
            "telus",
            "cpk",
            "real-data",
            f"investigation:{investigation_id}",
            f"file:{filename}",
            "phase:osint",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--investigation-id", required=True, help="e.g. telus_cpk_real_001")
    parser.add_argument("--source-root", default="investigations/active", help="Root folder for investigations/active")
    parser.add_argument("--made-by", default="Elena", help="Agent name for attribution")
    parser.add_argument("--importance", type=float, default=0.9, help="Importance score 0..1 (>=0.75 embeds to Qdrant)")
    args = parser.parse_args()

    investigation_id = args.investigation_id
    project_id = f"investigation-{investigation_id}"

    root = Path(args.source_root) / investigation_id / "sources" / "web"
    if not root.exists():
        raise SystemExit(f"Sources folder not found: {root}")

    helena = HelenaCore(project_id=project_id)

    html_files = sorted(root.glob("*.html"))
    if not html_files:
        raise SystemExit(f"No HTML sources found in {root}")

    total_points = 0
    for fp in html_files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        meta = build_metadata(investigation_id, fp)

        # Soft-chunk to avoid huge embeddings and to improve recall
        chunks = chunk_text(text, max_chars=4000)
        for idx, chunk in enumerate(chunks, start=1):
            content = f"[OSINT {fp.name} | chunk {idx}/{len(chunks)}]\n\n{chunk}"
            helena.save_to_all_layers(
                event_type="message",
                content=content,
                importance=args.importance,
                made_by=args.made_by,
                additional_data=meta,
            )
            total_points += 1

    print("\n================================================================================")
    print(f"OSINT ingestion completed for {investigation_id}")
    print(f"Project namespace: {project_id}")
    print(f"Files processed: {len(html_files)} | Chunks stored: {total_points}")
    print("- Data scope: investigation (task_only, investigation_only)")
    print("- Propagated to: PostgreSQL, Qdrant (if importance>=0.75), Redis")
    print("================================================================================\n")


if __name__ == "__main__":
    main()
