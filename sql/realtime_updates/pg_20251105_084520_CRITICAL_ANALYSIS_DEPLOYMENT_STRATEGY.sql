INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/CRITICAL_ANALYSIS_DEPLOYMENT_STRATEGY.md',
    'analysis',
    '🔍 KRYTYCZNA ANALIZA STRATEGII WDROŻENIA - MYŚLENIE KRYTYCZNE',
    '# 🔍 KRYTYCZNA ANALIZA STRATEGII WDROŻENIA - MYŚLENIE KRYTYCZNE

**Analiza:** Aleksander Nowak (Orchestrator)  
**Data:** 2025-11-05  
**Dokument analizowany:** HYBRID_DEPLOYMENT_STRATEGY_SESSION.md

-',
    293,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();