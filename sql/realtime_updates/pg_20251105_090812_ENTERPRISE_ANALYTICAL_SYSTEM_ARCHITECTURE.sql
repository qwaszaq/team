INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/ENTERPRISE_ANALYTICAL_SYSTEM_ARCHITECTURE.md',
    'architecture',
    '🎯 ARCHITEKTURA DLA ENTERPRISE ANALYTICAL SYSTEM - WYCOFANIE KRYTYKI',
    '# 🎯 ARCHITEKTURA DLA ENTERPRISE ANALYTICAL SYSTEM - WYCOFANIE KRYTYKI

**Data:** 2025-11-05  
**Prowadzący:** Aleksander Nowak (Orchestrator)  
**Status:** KOREKTA STRATEGII

---

## ⚠️ ALEKSANDER NOW',
    604,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();