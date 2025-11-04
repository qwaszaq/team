INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/status/HELENA_PROCESSING_REPORT_20251104.md',
    'protocol',
    '📊 Helena Processing Report - Dzisiejsze Zmiany',
    '# 📊 Helena Processing Report - Dzisiejsze Zmiany

**Data:** 2025-11-04 09:22  
**Wykonane przez:** Helena Kowalczyk (Data Infrastructure Specialist)  
**Tryb:** Batch Catchup Processing  
**Status:** ',
    351,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();