INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/ADAPTIVE_LEARNING_SYSTEM.md',
    'general_documentation',
    '🧠 Adaptive Learning System - Intelligence That Grows',
    '# 🧠 Adaptive Learning System - Intelligence That Grows

**Date:** 2025-11-04  
**Status:** ✅ ACTIVE  
**Version:** 1.0  

---

## 🎯 Vision

**System inteligencji, który się UCZY.**

Nie tylko wykonuje',
    428,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();