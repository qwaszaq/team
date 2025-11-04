INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_550ceab_bugfix.md',
    'general_documentation',
    'Resolve false-positive warnings in database connectivity checks',
    '# Resolve false-positive warnings in database connectivity checks

**Auto-Generated Documentation**

**Date:** 2025-11-04 12:38:37
**Commit:** `550ceab`
**Type:** Bugfix
**Author:** artur

---

## 📝 C',
    91,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();