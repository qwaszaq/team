INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/capabilities/DUCKDUCKGO_SEARCH_METHOD.md',
    'general_documentation',
    '🔍 DUCKDUCKGO SEARCH METHOD',
    '# 🔍 DUCKDUCKGO SEARCH METHOD
## Reliable Web Search Without Consent Walls

**Date:** 2025-11-04  
**Status:** ✅ VERIFIED WORKING  
**Advantage:** Better than Google for automated research!  

---

## ',
    398,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();