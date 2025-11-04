INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/DESTINY_CHAT_UI_HYBRID_INTEGRATION.md',
    'general_documentation',
    '💬 DESTINY CHAT UI - Hybrid System Integration',
    '# 💬 DESTINY CHAT UI - Hybrid System Integration
## Browser Interface dla On-Prem Intelligence System

**Date:** 2025-11-04  
**Status:** Concept (To Be Implemented Later)  
**Priority:** High (User Re',
    537,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();