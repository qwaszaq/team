INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/status/QDRANT_INDEXING_COMPLETE.md',
    'general_documentation',
    '✅ Qdrant Indexing Complete - Automatyzacja 100%',
    '# ✅ Qdrant Indexing Complete - Automatyzacja 100%

**Data:** 2025-11-04 09:40  
**Status:** Wszystkie dokumenty zaindexowane

---

## 🎉 Problem Rozwiązany!

Helena teraz **faktycznie propaguje do Qdra',
    159,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();