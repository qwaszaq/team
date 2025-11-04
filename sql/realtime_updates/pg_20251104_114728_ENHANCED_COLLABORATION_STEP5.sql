INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/ENHANCED_COLLABORATION_STEP5.md',
    'general_documentation',
    'Enhanced Collaboration System - Step 5: Collaboration Pattern Recognizer',
    '# Enhanced Collaboration System - Step 5: Collaboration Pattern Recognizer

**Date:** 2025-11-04  
**Component:** CollaborationPatternRecognizer  
**Status:** ✅ Implemented  
**Branch:** feature/enhan',
    415,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();