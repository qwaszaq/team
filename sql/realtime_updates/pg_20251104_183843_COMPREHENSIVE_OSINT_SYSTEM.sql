INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/COMPREHENSIVE_OSINT_SYSTEM.md',
    'team_documentation',
    '🕵️ Comprehensive OSINT System - Enterprise Architecture',
    '# 🕵️ Comprehensive OSINT System - Enterprise Architecture

**Prepared by:** Aleksander Nowak (Orchestrator) + Elena Volkov (OSINT Lead)  
**Date:** 2025-11-04  
**Status:** 🔨 DESIGN PHASE  
**Classifi',
    851,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();