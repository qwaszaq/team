INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/ENHANCED_COLLABORATION_STEP6.md',
    'architecture',
    'Enhanced Collaboration System - Step 6: Integrated System',
    '# Enhanced Collaboration System - Step 6: Integrated System

**Date:** 2025-11-04  
**Component:** EnhancedCrossTeamCollaboration  
**Status:** ✅ Implemented  
**Branch:** feature/enhanced-cross-team-',
    803,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();