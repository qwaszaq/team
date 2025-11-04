INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/guides/QUICK_START.md',
    'protocol',
    '⚡ Quick Start Guide - Get Running in 5 Minutes!',
    '# ⚡ Quick Start Guide - Get Running in 5 Minutes!

**Helena Auto-Execution System - Fastest Path to Success**

---

## 🎯 Goal

Get Helena automatically propagating your documents to all 4 databases in',
    420,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();