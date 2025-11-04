INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/protocols/AUTO_PROPAGATION_PROTOCOL.md',
    'protocol',
    'Protokół Automatycznej Propagacji Wiedzy',
    '# Protokół Automatycznej Propagacji Wiedzy

**Data utworzenia:** Tue Nov  4 09:29:22 CET 2025  
**Autor:** System Automatyzacji  
**Status:** Produkcyjny dokument

---

## 1. Wprowadzenie

Ten protokó',
    68,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();