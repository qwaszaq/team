INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/SYSTEM_CAPABILITIES_UPDATE_2025_11_04.md',
    'team_documentation',
    '🚀 SYSTEM CAPABILITIES UPDATE - November 4, 2025',
    '# 🚀 SYSTEM CAPABILITIES UPDATE - November 4, 2025

**TO:** All Destiny Team Agents (Technical + Analytical)  
**FROM:** Aleksander Nowak (Orchestrator)  
**CC:** Helena Kowalczyk (Knowledge Manager)  ',
    556,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();