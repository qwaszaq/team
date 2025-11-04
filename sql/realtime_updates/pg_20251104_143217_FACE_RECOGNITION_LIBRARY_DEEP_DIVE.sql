INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/research/FACE_RECOGNITION_LIBRARY_DEEP_DIVE.md',
    'architecture',
    '🔍 face_recognition Library - Complete Deep Dive',
    '# 🔍 face_recognition Library - Complete Deep Dive

**Library:** `ageitgey/face_recognition`  
**Research Date:** 2025-11-04  
**Team:** Analytical Team  
**Lead:** Viktor Kovalenko  
**Focus:** Techni',
    835,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();