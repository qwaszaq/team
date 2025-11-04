INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/architecture/DATA_SEPARATION_ARCHITECTURE.md',
    'architecture',
    '🏗️ DATA SEPARATION ARCHITECTURE',
    '# 🏗️ DATA SEPARATION ARCHITECTURE
## Separacja Danych Projektowych od Danych Investigacyjnych

**Date:** 2025-11-04  
**Critical Requirement:** Dane projektowe NIE MOGĄ mieszać się z danymi roboczymi ',
    732,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();