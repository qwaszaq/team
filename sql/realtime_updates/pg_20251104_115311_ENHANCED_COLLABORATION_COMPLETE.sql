INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/ENHANCED_COLLABORATION_COMPLETE.md',
    'architecture',
    '🎉 Enhanced Cross-Team Collaboration System - COMPLETE!',
    '# 🎉 Enhanced Cross-Team Collaboration System - COMPLETE!

**Date:** 2025-11-04  
**Status:** ✅ 100% COMPLETE  
**Branch:** feature/enhanced-cross-team-collaboration  
**Version:** 1.0.0

---

## 🏆 SYS',
    427,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();