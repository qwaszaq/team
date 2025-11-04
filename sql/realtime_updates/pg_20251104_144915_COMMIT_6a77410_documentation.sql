INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_6a77410_documentation.md',
    'general_documentation',
    'Add dashboard demo and interactive tutorial',
    '# Add dashboard demo and interactive tutorial

**Auto-Generated Documentation**

**Date:** 2025-11-04 14:49:14
**Commit:** `6a77410`
**Type:** Documentation
**Author:** artur

---

## 📝 Commit Message',
    71,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();