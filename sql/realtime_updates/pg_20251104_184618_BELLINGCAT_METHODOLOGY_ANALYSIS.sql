INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md',
    'analysis',
    '🔍 Bellingcat Methodology Analysis - Quality Standards & Investigative Excellence',
    '# 🔍 Bellingcat Methodology Analysis - Quality Standards & Investigative Excellence

**Research By:** Elena Volkov (OSINT Lead) + Maya Patel (Analysis)  
**Orchestrated By:** Aleksander Nowak  
**Date:',
    1539,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();