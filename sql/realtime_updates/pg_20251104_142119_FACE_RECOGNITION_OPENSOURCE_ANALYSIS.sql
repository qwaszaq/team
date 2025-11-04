INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/research/FACE_RECOGNITION_OPENSOURCE_ANALYSIS.md',
    'analysis',
    '🎯 Open Source Face Recognition Software - Deep Dive Analysis',
    '# 🎯 Open Source Face Recognition Software - Deep Dive Analysis

**Task ID:** RESEARCH-FACE-REC-001  
**Date:** 2025-11-04  
**Team:** Analytical Team  
**Lead:** Viktor Kovalenko  
**Status:** ✅ Compl',
    696,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();