INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/analysis/ADRIAN_LEGAL_ANALYSIS.md',
    'analysis',
    '⚖️ LEGAL ANALYSIS: Robert Telus - CPK Land Transaction',
    '# ⚖️ LEGAL ANALYSIS: Robert Telus - CPK Land Transaction

**Prepared by:** Adrian Kowalski (Legal Analyst)  
**Date:** 2025-11-04  
**Investigation ID:** INV-2025-11-04-001  
**Based on:** Elena''s OSI',
    694,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();