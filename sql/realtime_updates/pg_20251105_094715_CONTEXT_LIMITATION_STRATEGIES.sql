INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/architecture/CONTEXT_LIMITATION_STRATEGIES.md',
    'architecture',
    '⚠️ CONTEXT LIMITATION - STRATEGIE I ROZWIĄZANIA',
    '# ⚠️ CONTEXT LIMITATION - STRATEGIE I ROZWIĄZANIA

**Problem:** Local Agent (44k) vs Claude (200k)  
**Data:** 2025-11-05  
**Autorzy:** Katarzyna Wiśniewska (Architect) + Aleksander Nowak

---

## 📊 ',
    392,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();