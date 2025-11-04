INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/protocols/AUTOMATIC_DATABASE_EXECUTION_PROTOCOL.md',
    'protocol',
    '🔄 Automatic Database Execution Protocol',
    '# 🔄 Automatic Database Execution Protocol

**Data:** 2025-11-04  
**Status:** OBOWIĄZKOWY - MANDATORY  
**Autor:** System + Helena

---

## ⚠️ WYMÓG KRYTYCZNY

**Helena MUSI automatycznie wykonywać za',
    367,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();