INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'BATCH_MIGRATION_PLAN.md',
    'architecture',
    'Batch Processing Migration Plan',
    '# Batch Processing Migration Plan

## Executive Summary
Replace real-time database processing with intelligent batch system to resolve PostgreSQL performance crisis.

## Current State (CRITICAL)
- **R',
    157,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();