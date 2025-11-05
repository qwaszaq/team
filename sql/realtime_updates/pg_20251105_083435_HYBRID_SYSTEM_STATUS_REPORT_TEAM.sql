INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/status/HYBRID_SYSTEM_STATUS_REPORT_TEAM.md',
    'team_documentation',
    '🚀 RAPORT STATUS SYSTEMU HYBRYDOWEGO - ZESPÓŁ DESTINY TEAM',
    '# 🚀 RAPORT STATUS SYSTEMU HYBRYDOWEGO - ZESPÓŁ DESTINY TEAM

**Data:** 2025-11-05  
**Temat:** Hybrid On-Prem Intelligence System  
**Status:** Production-Ready Design + Partial Implementation  
**Zes',
    986,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();