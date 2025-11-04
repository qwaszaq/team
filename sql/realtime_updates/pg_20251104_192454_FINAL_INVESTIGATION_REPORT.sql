INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/FINAL_INVESTIGATION_REPORT.md',
    'analysis',
    '🔍 INVESTIGATIVE METHODOLOGY DEMONSTRATION',
    '# 🔍 INVESTIGATIVE METHODOLOGY DEMONSTRATION
## Professional Intelligence System - Capability Showcase

**Investigation Case Study:** Robert Telus - CPK Land Transaction Analysis Framework  
**Investig',
    853,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();