INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/FINAL_PERSPECTIVE_HYBRID_ANALYTICAL_SYSTEM.md',
    'team_documentation',
    '🎭 SPOJRZENIE Z DYSTANSU - HYBRID ANALYTICAL SYSTEM',
    '# 🎭 SPOJRZENIE Z DYSTANSU - HYBRID ANALYTICAL SYSTEM

**Data:** 2025-11-05  
**Autor:** Aleksander Nowak (Orchestrator)  
**Perspektywa:** 10,000 feet view

---

## 🌅 WIZJA - Co Właściwie Budujemy?

`',
    295,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();