INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/USAGE_GUIDE.md',
    'guide',
    '🚀 Destiny System - Przewodnik Użycia',
    '# 🚀 Destiny System - Przewodnik Użycia

**Data utworzenia:** 2025-11-04  
**Status systemu:** ✅ Operational  
**Wersja:** 1.0

---

## 📋 Spis Treści

1. [Szybki Start](#szybki-start)
2. [Podstawowe Uż',
    505,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();