INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/strategy/REVISED_MULTIAGENT_FEASIBILITY_DISCUSSION.md',
    'team_documentation',
    '🔄 PONOWNA DYSKUSJA - WYKONALNOŚĆ SYSTEMU MULTIAGENTOWEGO',
    '# 🔄 PONOWNA DYSKUSJA - WYKONALNOŚĆ SYSTEMU MULTIAGENTOWEGO

**Data:** 2025-11-05  
**Prowadzący:** Aleksander Nowak (Orchestrator)  
**Fokus:** Realna wykonalność, uproszczenie architektury, przetwarz',
    586,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();