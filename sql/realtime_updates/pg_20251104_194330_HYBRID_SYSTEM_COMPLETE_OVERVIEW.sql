INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/guides/HYBRID_SYSTEM_COMPLETE_OVERVIEW.md',
    'team_documentation',
    '🔍 HYBRID ON-PREM INTELLIGENCE SYSTEM',
    '# 🔍 HYBRID ON-PREM INTELLIGENCE SYSTEM
## Kompletny Przegląd Systemu: Local LLM + Cloud Supervisor + Data Hygiene

**Date:** 2025-11-04  
**Author:** Aleksander Nowak (Technical Orchestrator)  
**Stat',
    1188,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();