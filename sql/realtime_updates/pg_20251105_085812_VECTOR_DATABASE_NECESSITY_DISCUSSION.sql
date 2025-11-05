INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/VECTOR_DATABASE_NECESSITY_DISCUSSION.md',
    'general_documentation',
    '🔍 DYSKUSJA: CZY NAPRAWDĘ POTRZEBUJEMY QDRANT?',
    '# 🔍 DYSKUSJA: CZY NAPRAWDĘ POTRZEBUJEMY QDRANT?

**Data:** 2025-11-05  
**Prowadzący:** Aleksander Nowak  
**Temat:** Wektory, embeddingi i semantyczne wyszukiwanie

---

## ❓ PYTANIE KLUCZOWE

Czy po',
    481,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();