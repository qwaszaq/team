INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/HYBRID_DEPLOYMENT_STRATEGY_SESSION.md',
    'protocol',
    '🎯 STRATEGIA WDROŻENIA SYSTEMU HYBRYDOWEGO - SESJA ZESPOŁU',
    '# 🎯 STRATEGIA WDROŻENIA SYSTEMU HYBRYDOWEGO - SESJA ZESPOŁU

**Data:** 2025-11-05  
**Prowadzący:** Aleksander Nowak (Orchestrator)  
**Uczestnicy:** Cały zespół Destiny Team (10 agentów)  
**Cel:** W',
    797,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();