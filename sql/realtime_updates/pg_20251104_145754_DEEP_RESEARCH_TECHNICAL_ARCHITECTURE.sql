INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.md',
    'architecture',
    '🏗️ Deep Research System - Technical Architecture',
    '# 🏗️ Deep Research System - Technical Architecture

**Document Type:** Technical Implementation Specification  
**Date:** 2025-11-04  
**Lead:** Maria Wiśniewska (Software Architect)  
**Contributors:',
    907,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();