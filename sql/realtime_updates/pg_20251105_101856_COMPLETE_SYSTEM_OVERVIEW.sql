INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'COMPLETE_SYSTEM_OVERVIEW.md',
    'team_documentation',
    '🚀 COMPLETE SYSTEM OVERVIEW - Destiny Analytical System',
    '# 🚀 COMPLETE SYSTEM OVERVIEW - Destiny Analytical System

**Date:** 2025-11-05  
**Status:** ✅ FULLY OPERATIONAL - ALL COMPONENTS BUILT  
**Progress:** 60% (Week 1 ahead of schedule)

---

## 🎯 WHAT W',
    539,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();