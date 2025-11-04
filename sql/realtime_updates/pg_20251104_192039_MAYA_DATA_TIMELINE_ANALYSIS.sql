INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/analysis/MAYA_DATA_TIMELINE_ANALYSIS.md',
    'analysis',
    '📈 DATA ANALYSIS & TIMELINE: Robert Telus - CPK Land Transaction',
    '# 📈 DATA ANALYSIS & TIMELINE: Robert Telus - CPK Land Transaction

**Prepared by:** Maya Patel (Data Analyst)  
**Date:** 2025-11-04  
**Investigation ID:** INV-2025-11-04-001  
**Based on:** Elena (O',
    664,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();