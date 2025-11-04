INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/protocols/HELENA_VECTOR_1024_REQUIREMENT.md',
    'architecture',
    '🎯 OBOWIĄZEK: Helena - Vectors 1024 Dimensions',
    '# 🎯 OBOWIĄZEK: Helena - Vectors 1024 Dimensions

**Data:** 2025-11-04  
**Status:** OBOWIĄZKOWY - MANDATORY  
**Priority:** CRITICAL  
**Autor:** System Architecture

---

## ⚠️ WYMÓG KRYTYCZNY

**Hel',
    358,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();