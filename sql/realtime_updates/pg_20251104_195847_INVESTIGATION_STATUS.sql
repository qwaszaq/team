INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/active/telus_cpk_real_001/INVESTIGATION_STATUS.md',
    'status_report',
    '🔍 Investigation Status: Telus-CPK Real Data',
    '# 🔍 Investigation Status: Telus-CPK Real Data

**Investigation ID:** telus_cpk_real_001  
**Date Started:** 2025-11-04  
**Status:** Phase 1 Complete (OSINT Collection)  
**Next:** Full Multi-Agent An',
    79,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();