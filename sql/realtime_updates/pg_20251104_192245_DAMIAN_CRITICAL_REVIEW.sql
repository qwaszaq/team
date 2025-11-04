INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/telus_cpk_land_investigation/analysis/DAMIAN_CRITICAL_REVIEW.md',
    'team_documentation',
    '🎭 CRITICAL REVIEW: Robert Telus Investigation - Devil''s Advocate Analysis',
    '# 🎭 CRITICAL REVIEW: Robert Telus Investigation - Devil''s Advocate Analysis

**Prepared by:** Damian Rousseau (Critical Thinking Agent)  
**Experience Level:** Intermediate (150 XP)  
**Date:** 2025-1',
    800,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();