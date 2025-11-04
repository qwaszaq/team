INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/technical/AGENT_TOOLKITS_COMPLETE.md',
    'team_documentation',
    '🛠️ Agent Toolkits - Complete Technical Specification',
    '# 🛠️ Agent Toolkits - Complete Technical Specification

**Prepared by:** Alex Morgan (Technical Liaison) + Elena Volkov (OSINT)  
**Date:** 2025-11-04  
**Status:** 🔨 IMPLEMENTATION READY  
**Focus:**',
    1328,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();