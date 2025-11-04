INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/analysis/ELENA_OSINT_REPORT.md',
    'analysis',
    '🔍 OSINT REPORT: Robert Telus - CPK Land Transaction',
    '# 🔍 OSINT REPORT: Robert Telus - CPK Land Transaction

**Prepared by:** Elena Volkov (OSINT Specialist)  
**Date:** 2025-11-04  
**Investigation ID:** INV-2025-11-04-001  
**Classification:** Public I',
    431,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();