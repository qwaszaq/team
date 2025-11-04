INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/SEARCH_ORCHESTRATOR.md',
    'architecture',
    'SearchOrchestrator - Unified Search Interface',
    '# SearchOrchestrator - Unified Search Interface

## Overview

SearchOrchestrator provides a unified API for querying across all Destiny framework data layers:
- **Elasticsearch**: Full-text search, ag',
    421,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();