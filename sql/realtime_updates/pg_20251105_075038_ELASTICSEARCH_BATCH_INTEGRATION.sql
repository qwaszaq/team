INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/ELASTICSEARCH_BATCH_INTEGRATION.md',
    'architecture',
    '🔍 Elasticsearch Batch Integration',
    '# 🔍 Elasticsearch Batch Integration

**Status:** ✅ COMPLETE  
**Created:** 2025-11-04  
**Type:** Technical Documentation  

## Overview

Complete batch-friendly Elasticsearch integration replacing pr',
    212,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();