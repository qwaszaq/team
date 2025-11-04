INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/orchestration/TRANSPARENCY_SYSTEM.md',
    'general_documentation',
    '🎯 Transparency + Cross-Team Orchestration System',
    '# 🎯 Transparency + Cross-Team Orchestration System

**Date:** 2025-11-04  
**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Sprint:** B+C Implementation

---

## 🎯 Purpose

This system provides',
    428,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();