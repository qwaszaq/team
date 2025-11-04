INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/SEJM_API_ANALYSIS_CONCEPT.md',
    'analysis',
    '🏛️ Sejm API Analysis System - Complete Concept',
    '# 🏛️ Sejm API Analysis System - Complete Concept

**Project:** Parliamentary Committee Work Analysis  
**API:** https://api.sejm.gov.pl/committees.html  
**Date:** 2025-11-04  
**Teams:** Analytical T',
    692,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();