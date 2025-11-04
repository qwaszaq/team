INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/capabilities/INTERNET_RESEARCH_CAPABILITY.md',
    'general_documentation',
    '🌐 INTERNET RESEARCH CAPABILITY',
    '# 🌐 INTERNET RESEARCH CAPABILITY
## Direct Web Access & Data Collection

**Date:** 2025-11-04  
**Status:** ✅ VERIFIED & OPERATIONAL  
**Discovered During:** Robert Telus - CPK Investigation (Real Dat',
    493,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();