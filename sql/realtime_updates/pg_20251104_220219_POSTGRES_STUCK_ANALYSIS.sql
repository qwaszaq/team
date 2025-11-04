INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'POSTGRES_STUCK_ANALYSIS.md',
    'analysis',
    'PostgreSQL Stuck Analysis - November 4, 2025',
    '# PostgreSQL Stuck Analysis - November 4, 2025

## Summary of Issue
The PostgreSQL command `\d es_document_references` was stuck for 431+ seconds. This appears to be caused by multiple concurrent data',
    82,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();