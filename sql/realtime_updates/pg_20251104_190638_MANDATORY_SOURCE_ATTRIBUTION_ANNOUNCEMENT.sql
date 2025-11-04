INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.md',
    'team_documentation',
    '🔴 MANDATORY PROTOCOL: SOURCE ATTRIBUTION',
    '# 🔴 MANDATORY PROTOCOL: SOURCE ATTRIBUTION

**TO:** ALL Investigative & Research Agents  
**FROM:** Aleksander Nowak (Orchestrator)  
**DATE:** 2025-11-04  
**PRIORITY:** 🔴 CRITICAL - IMMEDIATE COMPLI',
    422,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();