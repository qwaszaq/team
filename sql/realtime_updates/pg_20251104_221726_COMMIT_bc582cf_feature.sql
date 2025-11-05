INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_bc582cf_feature.md',
    'architecture',
    'Implement batch processing system to resolve PostgreSQL performance crisis',
    '# Implement batch processing system to resolve PostgreSQL performance crisis

**Auto-Generated Documentation**

**Date:** 2025-11-04 22:14:36
**Commit:** `bc582cf`
**Type:** Feature
**Author:** artur
',
    1186,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();