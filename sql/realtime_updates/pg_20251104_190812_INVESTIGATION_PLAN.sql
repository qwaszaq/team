INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/INVESTIGATION_PLAN.md',
    'general_documentation',
    '🔍 INVESTIGATION PLAN: Robert Telus - CPK Land Transaction',
    '# 🔍 INVESTIGATION PLAN: Robert Telus - CPK Land Transaction

**Investigation ID:** INV-2025-11-04-001  
**Case Name:** Robert Telus - CPK Railway Land Sale Analysis  
**Status:** ACTIVE  
**Priority:*',
    238,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();